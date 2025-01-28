#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 4h
# RESULT [Puzzle 2023/19]: PART1 [367602] - PART2 [125317461667458] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use Storable 'dclone';
use AOC qw(DEBUG INFO TRACE);
$AOC::NAME = "Aplenty: not just a state machine";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 240;
$AOC::LEARNED = "Ranges, again";
#########################
# Init	
my $year = "2023";
my $puzzle = "19";

my @Tests;
push @Tests, { NAME => 'Parts-3', RESULT1 => 19114, RESULT2 => 167409079868000, INPUT  => << 'EOEX',
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
EOEX
};
##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	my %Instructions;
	my @Parts;

	##### Parse input
	# Instructions
	while (<$inputFilehandle>) {
		chomp;
		last if (/^$/);
		/^(\w+)\{(.*)\}/;
		&addInstr(\%Instructions, $1, $2);
	}

	# Parts
	while (<$inputFilehandle>) {
		chomp;
		last if (/^$/);
		/\{(.*)\}/;
		&addPart(\@Parts, $1);
	}

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		foreach my $part (@Parts) {
			$p1_result += &sorter(\%Instructions, $part);
		}
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";

		# Recursively split ranges
		my $rStartRange = {
			'x' => { START => 1, END => 4000},
			'm' => { START => 1, END => 4000},
			'a' => { START => 1, END => 4000},
			's' => { START => 1, END => 4000},
		};

		$p2_result = &splitRange(\%Instructions, $rStartRange, "in");
		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 367602 125317461667458
	return ($p1_result, $p2_result);
}

### Part 2

# Filter a range through the instructions, split ranges according to the rules in the instruction and travel both paths of the conditional
sub splitRange {
	my $rInstructions = shift;
	my $rRange = shift;
	my $instrName = shift;

	# Reached an end
	if ($instrName eq 'R') {
		TRACE "splitRange: [%3s] Discarding range %s", $instrName, rangeStr($rRange);
		return 0;
	}
	elsif ($instrName eq 'A') {
		TRACE "splitRange: [%3s] Summing range %s", $instrName, rangeStr($rRange);
		return sumUp($rRange);
	}
	TRACE "splitRange: [%3s] range %s", $instrName, rangeStr($rRange);

	my $sum;

	# Apply all rules to the ranges
	foreach my $rRule (@{$rInstructions->{$instrName}}) {
		DEBUG "splitRange: [%3s] rule '%s (%3s)' range %s", $instrName, $rRule->{ATTR}, $rRule->{TARGET}, rangeStr($rRange);

		if ($rRule->{ATTR} eq 'Z') {
			# For the ranges that no rule before applied: the last rule is the default rule (always)
			TRACE "splitRange: [%3s] DEFAULT rule '%s (%s)' range %s", $instrName, $rRule->{ATTR}, $rRule->{TARGET}, rangeStr($rRange);
			return $sum + splitRange($rInstructions, $rRange, $rRule->{TARGET});
		}

		# Apply the next rule, get back a range that did not match it, and the split-of range which matched.
		my ($rNoMatch, $rMatch) = splitRangeByRule($rRule, $rRange);
		if ($rMatch) {
			# Split off the matched range, run it through the target rule
			TRACE "splitRange: [%3s] MATCH   rule '%s (%s)' range %s", $instrName, $rRule->{ATTR}, $rRule->{TARGET}, rangeStr($rRange);
			$sum += splitRange($rInstructions, $rMatch, $rRule->{TARGET});
		}
		last unless $rNoMatch; # if all ranges matched the last rule
		$rRange = $rNoMatch;
	}
}

# Check the range against the rule, split the range into MATCHED and NOT MATCHED range
sub splitRangeByRule {
	my $rRule = shift;
	my $rRange = shift;

	my $attr = $rRule->{ATTR};
	my $split = $rRule->{COUNT};
	my $start = $rRange->{$attr}{START};
	my $end = $rRange->{$attr}{END};

	# Less than rule
	if ($rRule->{GTLT} eq '<') {
		if ($start < $split && $end >= $split) {
			my $r1 = dclone $rRange;
			my $r2 = dclone $rRange;

			$r1->{$attr}{START} = $start;
			$r1->{$attr}{END} = $split - 1;
			$r2->{$attr}{START} = $split;
			$r2->{$attr}{END} = $end;
			TRACE "splitRangeByRule: split into two";
			return ($r2, $r1);
		}
		else { 
			if ($start >= $split) {
				TRACE "splitRangeByRule: NO MATCH";
				return ($rRange, undef);
			}
			else {
				TRACE "splitRangeByRule: ALL MATCH";
				return (undef, $rRange);
			}
		}
	}
	# Greater than rule
	elsif ($rRule->{GTLT} eq '>') {
		if ($start <= $split && $end > $split) {
			my $r1 = dclone $rRange;
			my $r2 = dclone $rRange;
			$r1->{$attr}{START} = $start;
			$r1->{$attr}{END} = $split;
			$r2->{$attr}{START} = $split + 1;
			$r2->{$attr}{END} = $end;
			TRACE "splitRangeByRule: split into two";
			return ($r1, $r2);
		}
		else {
			if ($start > $split) {
				TRACE "splitRangeByRule: ALL MATCH";
				return (undef, $rRange);
			}
			else {
				TRACE "splitRangeByRule: NO MATCH";
				return ($rRange, undef);
			}
		}
	}
	else {
		die "splitRangeByRule: illegal instruction -> " . $rRule->{GTLT};
	}
}

sub rangeStr {
	my $rRange = shift;
	return sprintf "x%04d-%04d m%04d-%04d a%04d-%04d s%04d-%04d", 
		$rRange->{x}{START}, $rRange->{x}{END}, 
		$rRange->{m}{START}, $rRange->{m}{END},
		$rRange->{a}{START}, $rRange->{a}{END},
		$rRange->{s}{START}, $rRange->{s}{END};
}

# Nr of possible combinations for these XMAS ranges
sub sumUp {
	my $rRange = shift;
	my $sum = ($rRange->{x}{END} - $rRange->{x}{START} +1)
		* ($rRange->{m}{END} - $rRange->{m}{START} +1)
		* ($rRange->{a}{END} - $rRange->{a}{START} +1)
		* ($rRange->{s}{END} - $rRange->{s}{START} +1);
	;
	TRACE "sumUp: %s -> %d", &rangeStr($rRange), $sum;
	return $sum;
}


### PART 1

# Sort engine: run part through instructions
sub sorter {
	my $rInstructions = shift;
	my $rPart = shift;

	my $instrName = "in";
	
	while (1) {
		TRACE "Sorter: %s -> [%s]", &partStr($rPart), $instrName;
		foreach my $rRule (@{$rInstructions->{$instrName}}) {
			$instrName = checkRule($rRule, $rPart);
			return 0 if ($instrName eq 'R');
			return &partVal($rPart) if ($instrName eq 'A');
			last if ($instrName);
		}
	}
}

sub checkRule {
	my $rRule = shift;
	my $rPart = shift;

	if ($rRule->{ATTR} eq 'Z') {
		return $rRule->{TARGET};
	}

	if ($rRule->{GTLT} eq '<') {
		return $rRule->{TARGET} if ($rPart->{$rRule->{ATTR}} < $rRule->{COUNT});
	}
	elsif ($rRule->{GTLT} eq '>') {
		return $rRule->{TARGET} if ($rPart->{$rRule->{ATTR}} > $rRule->{COUNT});
	}
	else {
		die "checkRule: illegal instruction -> " . $rRule->{GTLT};
	}

	return "";
}

sub partVal {
	my $rPart = shift;
	return $rPart->{x} + $rPart->{m} + $rPart->{a} + $rPart->{s};
}
sub partStr {
	my $rPart = shift;
	return sprintf "%4d-%4d-%4d-%4d", $rPart->{x}, $rPart->{m}, $rPart->{a}, $rPart->{s};
}

# {  x=787,m=2655,a=1222,s=2876  }
sub addPart{
	my $rParts = shift;
	my $str = shift;
	my %part;
	foreach my $partStr (split ',', $str) {
		if ($partStr =~ /(\w)=(\d+)/) {
			$part{$1} = $2;
		}
		else {
			die "addParts: bad part: $str";
		}
	}
	TRACE "addParts: xmas = %s", &partStr(\%part);
	push @$rParts, \%part;
}


# px{  a<2006:qkq,m>2090:A,rfg  }
sub addInstr{
	my $rRule = shift;
	my $name = shift;
	my $instrStr = shift;
	my @chain;
	foreach my $str (split ',', $instrStr) {
		my %instr;
		if ($str =~ /(\w)(.)(\d+):(\w+)/) {
			$instr{ATTR} = $1;
			$instr{GTLT} = $2;
			$instr{COUNT} = $3;
			$instr{TARGET} = $4;
			TRACE "addInstr: [$name] $1 $2 $3 -> $4";
		}
		elsif ($str =~ /^(\w+)$/) {
			$instr{ATTR} = 'Z';
			$instr{TARGET} = $1;
			TRACE "addInstr: [$name] default -> $1";
		}
		else {
			die "addInstr: bad instruction $name -> $str";
		}
		push @chain, \%instr;
	}
	$rRule->{$name} = \@chain;
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 19: Aplenty ---

The Elves of Gear Island are thankful for your help and send you on your way. They even have a hang glider that someone stole from Desert Island; since you're already going that direction, it would help them a lot if you would use it to get down there and return it to them.

As you reach the bottom of the relentless avalanche of machine parts, you discover that they're already forming a formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny
Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true. The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex were considering a specific part, it would perform the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).
If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns. If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for all of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?

Your puzzle answer was 367602.

--- Part Two ---

Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. How many distinct combinations of ratings will be accepted by the Elves' workflows?

Your puzzle answer was 125317461667458.

#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 5h?
# RESULT [Puzzle 2023/12]: PART1 [7792] - PART2 [13012052341533]
# Part 2 -> [13012052341533] (587994 vs 84652760618705675 cached calls, factor 143968749033) 85E15
# Part 2 -> [13012052341533] (587994 vs 84652760618705675 cached calls, factor 143968749033)
# Part 2 -> [13012052341533] (509331 vs 62381346322055952 cached calls, factor 122477026378)
# After some optimization, a magnitute less calls, but not really faster -> 40s
# Part 2 -> [13012052341533] (358418 vs   218905549618562 cached calls, factor    610754900) 218E12
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE PROGRESS);
use Memoize;
$AOC::NAME = "Hot Springs: some springs don't scale";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 300;
$AOC::LEARNED = "Memoization, Dynamic Programming cache";
#########################
# Init	
my $year = "2023";
my $puzzle = "12";

my @Tests;
push @Tests, { NAME => 'Springs-21', RESULT1 => 21, RESULT2 => 525152, INPUT  => << 'EOEX',
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
EOEX
# ?###???????? 3,2,1#.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1
};
##################################

my $GOOD = '.';
my $BAD  = '#';
my $UNKN = '?';
my $actualCalls;

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);
	my $allCalls;

	$actualCalls = 0;

	INFO "*** Setup & Input ***";
	##### Parse input
	my @lines = <$inputFilehandle>; #chomp @notes;
	my $linenr = 1;
	foreach (@lines) {
		chomp;
		next if (/^$/);
		PROGRESS $linenr++, scalar @lines;
		# Part 1
		/(.*) (.*)/;
		# Brute force all possible permutation for ? = . or #
		$p1_result += &unscramble($1, $2);

		# Part 2
		my $p2Format1 = sprintf "%s?%s?%s?%s?%s", $1, $1, $1, $1, $1;
		my $p2Format2 = sprintf "%s,%s,%s,%s,%s", $2, $2, $2, $2, $2;
		my $calls;
		my ($calls, $sum) = &solveR($p2Format1, split(',', $p2Format2));
		$p2_result += $sum;
		$allCalls += $calls;
		INFO "PART2: [%s] [%s] (%d calls)", $_, $sum, $calls;
	}

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		#INFO "*** Part 1 running ***";
		#$p1_result = 0;
		INFO "*** Part 1 -> [%d]", $p1_result;
	}
	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		#INFO "*** Part 2 running ***";
		#$p2_result = 0;
		INFO "*** Part 2 -> [%d] (%d vs %d cached calls, factor %d)", $p2_result, $actualCalls, $allCalls-$actualCalls, $allCalls/$actualCalls;
	}

	##### RESULTS #####
	# 7792, 13012052341533
	return ($p1_result, $p2_result);	
}

# Cache all these function calls: 
# dynamic-programming / Memoization used as a boost, trading memory against performance
memoize('solveR'); 

sub solveR {
	$actualCalls++;
	my $springs = shift;
	my @damageGroups = @_;

	$springs =~ s/^\.*//; # Leading . are of no interest

	DEBUG "solveR: [%s] [%s]", $springs, join('-',  @damageGroups);
	if (length $springs == 0) {
		# End of spring list: Solution found ... or not.
		TRACE "solveR: ------------------------------- end of input: %d", scalar @damageGroups == 0 ? 1 : 0;
		return (1, scalar @damageGroups == 0 ? 1 : 0); # ok if no more groups needed
	}

	my $spring = substr($springs, 0, 1);

  if ($spring eq '#' ) {
		# We have a damaged spring

		# Min springs needed to satisfy remaining groups (optimisation):
		my $minSpringsNeeded=-1;
		foreach my $group (@damageGroups) {
			$minSpringsNeeded += $group + 1;
		}
		if ($minSpringsNeeded > length($springs)) {
				TRACE "solveR: Not enough springs left for the remaining groups: 0";
				return (1,  0);
		}

		if (scalar(@damageGroups) == 0  || length($springs) < $damageGroups[0]) {
				TRACE "solveR: Either we don't have a group for this, or not enough springs left for this group: 0";
				return (1,  0);
		}

		if (substr($springs, $damageGroups[0], 1) eq '#') {
				TRACE "solveR: To many damaged coming up for this group: 0";
				return (1,  0);
		}
		if (index(substr($springs, 0, $damageGroups[0]), '.') != -1) {
				TRACE "solveR: Not enough damaged coming up for this group: 0";
				return (1,  0);
		}

		if (length($springs) > $damageGroups[0]) {
				if (substr($springs, $damageGroups[0], 1) eq '?') {
						# If next spring after group is '?' -> it must be '.' 
						# Advance springs to end of group + 1
						TRACE "solveR: Remove this group and next char (? must mean .)";
						my ($calls, $sum) =  &solveR(substr($springs, $damageGroups[0]+1), (@damageGroups[1..$#damageGroups]));
						return ($calls+1, $sum);
				}
		}

		TRACE "solveR: Group found. Remove group and #{n} from spring and check the rest";
		my ($calls, $sum) =   &solveR( substr($springs, $damageGroups[0]), (@damageGroups[1..$#damageGroups]));
		return ($calls+1, $sum);

	}
	elsif ($spring eq '?' ) {
		# Here it splits: Try both paths: ? -> . or #
		TRACE "solveR: Return aggregate of both paths";
		my ($calls1, $sum1) = &solveR('#' . substr($springs, 1), (@damageGroups));
		my ($calls2, $sum2) = &solveR('.' . substr($springs, 1), (@damageGroups));
		return ($calls1 + $calls2 + 1, $sum1 + $sum2);
	}

	INFO "solveR: SHOULD NOT GET HERE!";
}

# Brute force: replace all ? with . or # and check whether they fit the second format
sub unscramble {
	my $format1 = shift;
	my $format2 = shift;

	my $nrOfUnknown = $format1 =~ tr/\?//;
	return 1 if ($nrOfUnknown == 0);

	my $nrOfMatches = 0;
	for (my $i = 0; $i < 2**$nrOfUnknown; $i++) {
		my $teststring = &replaceWithBits($format1, $nrOfUnknown, $i);
		
		#DEBUG "unscramble: [%s] has %d: %d (%0${nrOfUnknown}b-> [%s]", $format1, $nrOfUnknown, $i, $i, $teststring;
		$nrOfMatches++ if (&matchFormats($teststring, $format2));
	}

	DEBUG "unscramble: [%s] [%s] has %d", $format1, $format2, $nrOfMatches;
	return $nrOfMatches;
}

sub matchFormats {
	my $format1 = shift;
	my $format2 = shift;

	my $match = ($format2 eq getFormat2($format1));
	#DEBUG "matchFormats [%s (%s)] [%s] match: %s", $format1, getFormat2($format1), $format2, $match ? "YES" : "NO";
	return $match;
}

sub getFormat2 {
	my $format1 = shift;
	my $result;

	my $curDamaged;
	for (my $i = 0; $i < length $format1; $i++) {
		my $c = substr($format1, $i, 1);
		#DEBUG "getFormat2: C [%s]", $c;
		if ($c eq '#') {
			$curDamaged++;
		}
		elsif ($c eq '.' && $curDamaged) {
			$result .= ',' if ($result ne "");
			$result .= $curDamaged;
			$curDamaged = 0;
		}
	}
	$result .= ',' if ($curDamaged && $result ne "");
	$result .= $curDamaged if ($curDamaged);
	#DEBUG "getFormat2: [$format1], [$result]";
	return $result;
}


sub replaceWithBits {
	my ($str, $nr, $bits) = @_;
	my $result;
	my $n = 0;
	for (my $i = 0; $i < length $str; $i++) {
		my $c = substr($str, $i, 1);
		#DEBUG "C: [$c]";
		if ($c eq '?') {
			$c = ($bits >> $n) & 0x01  ? '#' : '.';#vec($bits, $n, 1) ? '#' : '.';
			#DEBUG "BITS: C: [$c]: %d (%0${nr}b) -> %d", $bits, $bits, ($bits >> $n) & 0x01; #($bitsvec($bits, $n, 1);
			$n++;
		}
		$result .= $c;
	}
	return $result;
}
############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 12: Hot Springs ---

You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary, ornate building.

As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot springs, weren't you?" You indicate that this definitely looks like hot springs to you.

"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

You look in the direction the researcher is pointing and suddenly notice the massive metal helixes towering overhead. "This way!"

It only takes you a few more steps to reach the main gate of the massive fenced-off area containing the springs. You go through the gate and into a small administrative building.

"Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.

"Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not until we get more lava to heat our forges. And our springs. The springs aren't very springy unless they're hot!"

"Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal operation, but we should be able to find one springy enough to launch you up there!"

There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#
In this example, the number of possible arrangements for each row is:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 4 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 1 arrangement
????.######..#####. 1,6,5 - 4 arrangements
?###???????? 3,2,1 - 10 arrangements
Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?

Your puzzle answer was 7792.

--- Part Two ---

As you look out at the field of springs, you feel like there are way more springs than the condition records list. When you examine the records, you discover that they were actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with five copies of itself (separated by ?) and replace the list of contiguous groups of damaged springs with five copies of itself (separated by ,).

So, this row:

.# 1
Would become:

.#?.#?.#?.#?.# 1,1,1,1,1
The first line of the above example would become:

???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
In the above example, after unfolding, the number of possible arrangements for some rows is now much larger:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 16384 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 16 arrangements
????.######..#####. 1,6,5 - 2500 arrangements
?###???????? 3,2,1 - 506250 arrangements
After unfolding, adding all of the possible arrangement counts together produces 525152.

Unfold your condition records; what is the new sum of possible arrangement counts?

Your puzzle answer was 13012052341533.

Both parts of this puzzle are complete! They provide two gold stars: **

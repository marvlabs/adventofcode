#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/08.pl
# Solved in: 1h50
# RESULT [Puzzle 08]: PART1 [13301] - PART2 [7309459565207] 
###
use strict;
use threads;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE PROGRESS);
$AOC::NAME = "Haunted Wasteland: Ghost navigation";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 110;
$AOC::LEARNED = "Find cycles and LCM them";
#########################
# Init
my $year = "2023";
my $puzzle = "08";

my @Tests;
push @Tests, { NAME => 'Camel Map 2', RESULT1 => 2, INPUT  => << 'EOEX1',
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
EOEX1
};

push @Tests, { NAME => 'Camel Map 6', RESULT1 => 6, INPUT  => << 'EOEX2',
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
EOEX2
};
push @Tests, { NAME => 'Ghost Map 6', RESULT2 => 6, INPUT  => << 'EOEX3',
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
EOEX3
};
##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result);

	INFO "*** Setup & Input ***";
	##### Parse input
	my $directions = <$inputFilehandle>;
	chomp $directions;
	my @NextDir = split(//, $directions);

	my %Map;
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		/(\w+) = .(\w+), (...)/;
		$Map{$1}{L} = $2;
		$Map{$1}{R} = $3;
		#DEBUG "PARSE: Map [%s]: [%s] <=> [%s]", $1, $Map{$1}{L}, $Map{$1}{R};
	}

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		$p1_result = &navigateMapTo(\%Map, \@NextDir, 'AAA', 'ZZZ');
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		# Ghost-navigate: Do it for every start pos with ..A:
		my %Ghosts;
		my %Endpos;
		foreach my $pos (keys %Map) {
			if ($pos =~ /..A/) {;
				$Ghosts{$pos}{POSITION} = $pos;
				DEBUG "Found Ghost at start [%s]", $pos;
			} 
			elsif ($pos =~ /..Z/) {;
				$Endpos{$pos}{POSITION} = $pos;
				DEBUG "Found a possible end position at [%s]", $pos;
			} 
		}

		# Find out how many steps each ghost needs to hit all end positions, and then again from there, to assess cyclicality
		# (Bit overblown, turns out: we could just check that the ghosts hits any ..Z end position, but... why not. Like this we can check uniqueness)
		my $nr = 1;
		foreach my $target (keys %Endpos) {
			PROGRESS $nr++, scalar keys %Endpos;
			foreach my $ghost (keys %Ghosts) {
				
				# Let thread workers do the navigation
				$Ghosts{$ghost}{WORKER} = threads->create( 
					sub {
						#DEBUG "Ghost/Target solution for [%s] -> [%s]", $ghost, $target;
						my $steps = &navigateMapTo(\%Map, \@NextDir, $ghost, $target);
						DEBUG "Ghost/Target solution for [%s] -> [%s] -> [%d] : %s", $ghost, $target, $steps, $steps == -1 ? "UNREACHABLE" : "ok";
						return $steps;
					}
				);
			}

			foreach my $ghost (keys %Ghosts) {
				# Collect the result
				my $steps = $Ghosts{$ghost}{WORKER}->join();

				# Phew, turns out: every ghost has only one reachable endpos, and it's cyclic!
				if ($steps > 0) {
					# Check that this ghost doesn't already have a possible target
					if ($Ghosts{$ghost}{ENDPOS}) {
						# Not good, we would have to compute multiple possible LCM's if we get here.
						DEBUG "Ghost/Target solution for [%s] -> [%s] -> [%d] : %s NOT UNIQUE", $ghost, $target, $steps;
						die "Amend code: non-unique ghost-target solutioin found for [$ghost]";
					}
					$Ghosts{$ghost}{ENDPOS} = $target;
					$Ghosts{$ghost}{STEPS}  = $steps;
					# Verify cyclicity:
					my $cycle = &navigateMapTo(\%Map, \@NextDir, $target, $target);
					DEBUG "Ghost/Target solution for [%s] -> [%s] -> [%d] : %s", $ghost, $target, $steps, $steps == $cycle ? "CYCLIC" : "NOT good";
				}
			}
		}

		my $lcm = 1;
		foreach my $ghost (keys %Ghosts) {
			my $newlcm = &lcm($lcm, $Ghosts{$ghost}{STEPS});
			DEBUG "LCM of [%s - %d] and [%d] is [%d]", $ghost, $Ghosts{$ghost}{STEPS}, $lcm, $newlcm;
			$lcm = $newlcm;
		}
		$p2_result = $lcm;
		INFO "*** Part 2 -> [%d]", $p2_result;


		# Brute force??? Shiiiite, doesn't compute AT ALL...
		# # Now navigate every ghost
		# my $nrOfSteps = 0;
		# while (my $step = shift @NextDir) {
		# 	$nrOfSteps++;
		# 	DEBUG "Ghost steps [%d]: all ghosts take a [%s]", $nrOfSteps, $step if ($nrOfSteps % 1000000 == 0);

		# 	my $allGhostsReachedZPosition = 1;
		# 	foreach my $ghost (keys %Ghosts) {
		# 		my $position = $Ghosts{$ghost}{POSITION};
		# 		#DEBUG "      Ghost [%s] from [%s] take [%s] to [%s]", $ghost, $position, $step, $Map{$position}{$step};
		# 		$Ghosts{$ghost}{POSITION} = $Map{$position}{$step};
		# 		$allGhostsReachedZPosition = 0 if (substr ($Ghosts{$ghost}{POSITION}, 2, 1) ne 'Z');
		# 	}
		# 	push(@NextDir, $step);
		# 	last if ($allGhostsReachedZPosition);
		# }
	}

	##### RESULTS #####
	#printf "Results - Part 1: sum is %d\n", $p1_result;
	#printf "Results - Part 2: sum is %d\n", $p2_result;
	# 13301 7309459565207
	return ($p1_result, $p2_result);
}

# Step through map from start, match against desired target.
# Arbitrarly declare "IMPOSSIBLE!" after n steps without reaching the target :)
sub navigateMapTo {
	my $rMap = shift;
	my $rInstructions = shift;
	my $position = shift;
	my $targetRegex = shift;

	my $nrOfSteps = 0;
	my @nextDir = (@$rInstructions);
	while (my $step = shift @nextDir) {
	 	$nrOfSteps++;
	 	#DEBUG "navigateMapTo: from [%s] take [%s] to [%s]", $position, $step, $rMap->{$position}{$step};
	 	$position = $rMap->{$position}{$step};
	 	push(@nextDir, $step);
	 	last if ($position =~ $targetRegex);
		return -1 if ($nrOfSteps > 100000);
	}
	return $nrOfSteps;
}

###
# Pilfered math from https://programming-idioms.org/idiom/75/compute-lcm/3074/perl (CC-BY-SA)
# Greatest common divider
sub gcd {
	my ($x, $y) = @_;
	while ($x) { ($x, $y) = ($y % $x, $x) }
	$y
}
# Lowest common multiple
sub lcm {
	my ($x, $y) = @_;
	($x && $y) and $x / gcd($x, $y) * $y or 0
}
###

############################# 
# MAIN
# Run tests first
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 8: Haunted Wasteland ---

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

Your puzzle answer was 13301.

--- Part Two ---

The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

Your puzzle answer was 7309459565207.

Both parts of this puzzle are complete! They provide two gold stars: **

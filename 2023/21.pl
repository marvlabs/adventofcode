#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 5h
# RESULT [Puzzle 2023/21]: PART1 [3651] - PART2 [607334325965751] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE);
use XY::Board;
use XY::XY qw(XY);
use Data::Dumper;
$AOC::NAME = "Step Counter: looong walks";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 300;
$AOC::LEARNED = "Simulation, Math solving in algebra and sequences applied";
#########################
# Init	
my $year = "2023";
my $puzzle = "21";

my @Tests;
push @Tests, { NAME => 'Garden 6', RESULT1 => 16, ATTRIBUTE1 => 6, INPUT  => << 'EOEX',
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
EOEX
};
# Hmmm, doesn't work for test input -> must check periodicity...
# push @Tests, { NAME => 'Garden ININITE', RESULT2 => 1594, ATTRIBUTE2 => 50, INPUT  => << 'EOEX',
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# EOEX
# };
##################################
my $START = ord 'S';
my $PLOT = ord '.';
my $ROCK = ord '#';
my $REACHED = ord 'O';
my $EMPTY = ord 'x';

# A lot of walking for the Elf
my $NrOfStepsPart1 =       64;
my $NrOfStepsPart2 = 26501365;

# Short-circuit the lengthy simulation with pre-computed values for debugging if 1
my $USE_PRECOMPUTED_VALUES = 0;

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my $testAttribute1 = shift;
	my $testAttribute2 = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	##### Parse input
	my $boardstr;
	my $boardY;
	my $boardX;

	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		$boardstr .= $_;
		$boardX = length $boardstr unless($boardX);
		$boardY++;
	}

	# Set up field
	my $board = XY::Board->new($boardX, $boardY);
	$board->setTiles($boardstr);

	binmode(STDOUT, ":encoding(UTF-8)");
	#DEBUG "Parse: Board [%d/%d]\n%s", $boardX, $boardY, $board->toString();

	my $startPos = &findStart($board);

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		my $nrOfSteps = $NrOfStepsPart1;
		$nrOfSteps = $testAttribute1 if ($testAttribute1);

		my $part1Board = $board->duplicate();
		my $pos = $startPos;
		TRACE "Part 1: start pos is %s", $pos->toString();
		my $pResults = &elfStep($part1Board, $pos, $REACHED, $nrOfSteps);
		$p1_result = $pResults->{$nrOfSteps};#&countReached($part1Board);
		DEBUG "Part1: FilledBoard %s\n%s", $pos->toString(), $part1Board->toString();
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		$NrOfStepsPart2 = $testAttribute2 if ($testAttribute2);

		# Finding out properties about the indefinite farm
		my $fieldX = $board->getSizeX();
		my $fieldY = $board->getSizeY();
		# $startPos is actually in the middle of a square board
		die "Start position is not in the middle of the board" if ($startPos->x() != int($fieldX / 2) || $startPos->y() != int($fieldY / 2));
		die "Board is not square " if ($fieldX  != $fieldY);

		my $nrOfSteps=$NrOfStepsPart2;

		my $stepsUntilBorder = int($fieldX / 2);
		my $boardsSeenX = int (($nrOfSteps-$stepsUntilBorder-1) / $fieldX + 1);
		my $stepsIntoLastBoard = ($nrOfSteps-$stepsUntilBorder-1) % $fieldX;

		INFO "Part2: some info: Square board: %d/%d, Start %s: until border: %d.\n  With %d steps:\n  - Boards seen on X+ %d.\n  - Steps left on last board %d.",
			$fieldX, $fieldY, $startPos->toString(),
			$stepsUntilBorder, $nrOfSteps, $boardsSeenX, $stepsIntoLastBoard;

		# Nr of boards seen in one direction with 26501365 steps: 202300
		# (ending up at far edge of board)
		# For sequence detection, we step 0, 1, 2, ... times to the edge of the next board
		# Some simulation results. They form a quadratic sequence!
		#$nrOfSteps = 65 + 131*0; #  65 =>   3751
		#$nrOfSteps = 65 + 131*1; # 196 =>  33531
		#$nrOfSteps = 65 + 131*2; # 327 =>  92991
		#$nrOfSteps = 65 + 131*3; # 458 => 182131
		#$nrOfSteps = 65 + 131*4; # 589 => 300951
		my $steps0 = $stepsUntilBorder + 0 * $fieldX;
		my $steps1 = $stepsUntilBorder + 1 * $fieldX;
		my $steps2 = $stepsUntilBorder + 2 * $fieldX;

		INFO "Part2: Cycle because of straight X0-Y0 line: \n  We expand onto %d boards (in all directions)\n  Lets find the quadratic sequence by simulating 0, 1, 2 board crossings (+offset walk to border %d)\n  => %d, %d, %d steps",
			$boardsSeenX, $stepsUntilBorder,
			$steps0, $steps1, $steps2;

		my ($res0, $res1, $res2);
		#$USE_PRECOMPUTED_VALUES = 1;
	 	if (!$USE_PRECOMPUTED_VALUES) {
			INFO "Part2: Simulating %d steps...", $steps2;

			# Setting up board large enough to traverse 0,1,2 horizontal
			my $factor = 5;
			my $boardN = XY::Board->new($fieldX * $factor, $fieldY * $factor, $EMPTY);
			for (my $x = 0; $x < $factor; $x++) {
				for (my $y = 0; $y < $factor; $y++) {
					$boardN->placeBoard($board, XY($x*$fieldX, $y*$fieldY));
				}
			}
			my $startPosN = XY(int($fieldX*$factor / 2), int($fieldY*$factor/2));

			my $pResults = &elfStep($boardN, $startPosN, $REACHED, $steps2);
			DEBUG "Part2 : 5 x board \n%s", $boardN->toString();

			$res0 = $pResults->{$steps0}; # 3751;
			$res1 = $pResults->{$steps1}; # 33531;
			$res2 = $pResults->{$steps2}; # 92991;
		}
		else {
			my $ODD = 0;
			INFO "!!! ATTENTION !!! USE_PRECOMPUTED_VALUES is set: the sequence has NOT been simulated";
			if (!$ODD) {
				INFO "Part2: Short-circuit simulation, using pre-computed values odd & even nr of steps";
				($res0, $res1, $res2) = (3751, 33531, 92991); # PRE-COMPUTED! Just for debugging
			}
			else {
				# Version with ODD nr of moves only
				INFO "Part2: Short-circuit simulation, using pre-computed values odd nr of steps only";
				($res0, $res1, $res2) = (3751, 92991, 300951);
				$boardsSeenX = $boardsSeenX / 2;
			}
		}

		DEBUG "Part2: Simulation result: sequence (0,1,2) = (%d, %d, %d)", $res0, $res1, $res2;

		# Quadratic factors for sequence x (0,1,2)
		my $a = ($res0 - 2*$res1 + $res2) / 2;
		my $b = (-3*$res0 + 4*$res1 - $res2) / 2;
		my $c = $res0;
		INFO "Part 2: Quadratic equation for sequence (%d,%d,%d) is :\n  %d * x^2 + %d * x + %d . Calculating for %d", $res0, $res1, $res2, $a, $b, $c, $boardsSeenX;

		my $x = $boardsSeenX;
		$p2_result = $a * $x**2 + $b * $x + $c;

		#####
		# Alternative: with sequence expansion from day 09
		INFO "Part 2: Alternative: with sequence expansion from day 09 (%d,%d,%d) for %d", $res0, $res1, $res2, $boardsSeenX;
		my $p2_alternative = (&expandSequence( [$res0, $res1, $res2], $boardsSeenX+1))[-1];
		die "Part2: Sequence expansion did not give same result as quad function: $p2_result != $p2_alternative" if ($p2_result != $p2_alternative);
		#####

		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 3651 607334325965751
	return ($p1_result, $p2_result);
}
######

# Step through the board, (like flood fill without filling)
# Note the number of positions we're at after every step (-> the result hash)
# Fill the board with the positions on the last step (for console output)
sub elfStep {
	my $board = shift;
	my $pos = shift;
	my $fill = shift;
	my $maxSteps = shift;

	my %resultPerStep;
	
	my %fillNext;
	$fillNext{$pos->toString()} = $pos;

	my $steps = 0;
	while ($steps < $maxSteps) {
		$steps++;

		my @toFill;
		push @toFill, (values %fillNext);
		%fillNext = ();

		#print "FIELDS: " . Dumper(\@toFill);
		while (my $field = pop(@toFill)) {
			#TRACE "elfStep: %s (%s)", $field->toString(), chr($board->getAt($field));
			my $rNeighbours = $field->directNeighbours();
			foreach my $neighDir (keys %$rNeighbours) {
				my $neigh = $rNeighbours->{$neighDir};
				next unless ($board->valid($neigh));
				next if ($board->is($neigh, $ROCK));
				
				if ($steps == $maxSteps) {
					#TRACE "elfStep: setting %s (%s) to reached", $neigh->toString(), chr($board->getAt($neigh));
					$board->setAt($neigh, $REACHED);
				}
				else {
					#TRACE "elfStep: step [%d] is at %s", $steps+1, $neigh->toString();
				}
				$fillNext{$neigh->toString()} = $neigh;
			}
		}
		$resultPerStep{$steps} = scalar keys %fillNext;
		DEBUG "elfStep: Step %d has %d positions", $steps, $resultPerStep{$steps};
	}
	return \%resultPerStep;
}


sub findStart { 
	my $board = shift;
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			return XY($x, $y) if $board->is(XY($x, $y), $START);
		}
	}
}

# Reworked from day 09:
# - Iterative, not recursive anymore
# - Returns the expanded sequence with n (= desired - existing) elements added
sub expandSequence {
	my $rSequence = shift;
	my $nrOfElems = shift;

	my %lastValues;
	$lastValues{0} = @$rSequence[-1];

	# Get difference of sequence, then difference of diff-sequence and so on until a 0-sequence is found
	my $diffDepth = 0;
	my $isZero = 0;
	my $rCurrentSequence = $rSequence;
	while (!$isZero) {
		$diffDepth++;
		$isZero = 1;

		my @diffSeq;
		for (my $x = 0; $x < scalar(@$rCurrentSequence) - 1; $x++) {
			my $diff = @$rCurrentSequence[$x+1] - @$rCurrentSequence[$x];
			$isZero = 0 if ($isZero && $diff !=0 );
			push(@diffSeq, $diff);
		}
		$lastValues{$diffDepth} = $diffSeq[-1];
		$rCurrentSequence = \@diffSeq;
	}

	# Generate n next values by adding the last element of the lower-down sequence
	my @result = (@$rSequence);
	for (my $i = 0; $i < $nrOfElems - scalar @$rSequence; $i++) {
		my $lastVal = 0;
		for (my $depth = $diffDepth-1; $depth >= 0; $depth--) {
			$lastValues{$depth} += $lastValues{$depth+1};
		}
		push @result, $lastValues{0};
	}

	return ( (@result));
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 21: Step Counter ---

You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#). For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?

Your puzzle answer was 3651.

--- Part Two ---

The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats infinitely in every direction.

So, if you were to look one additional map-width or map-height out from the edge of the example map above, you would find that it keeps repeating:

.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked S, though - every other repeated S is replaced with a normal garden plot (.).

Here are the number of reachable garden plots in this new infinite version of the example map for different numbers of steps:

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.
However, the step count the Elf needs is much larger! Starting from the garden plot marked S on your infinite map, how many garden plots could the Elf reach in exactly 26501365 steps?

Your puzzle answer was 607334325965751.

Both parts of this puzzle are complete! They provide two gold stars: **


###############
# Additional info and alternatives

#my @sequence = (3751, 33531,  92991);#, 182131,);#300951# -> sequence says:449451, 627631, 835491, 1073031
#my @sequence = (3751, 92991, 300951);#,       ,);#300951# -> sequence says:        627631,         1073031,        1637151

# For x 1,2,3
my $seq1 = 33531;
my $seq2 = 92991;
my $seq3 = 182131;
my $diff1 = $seq2 - $seq1; # (u2-u1) -> 3a + b
my $diff2 = $seq3 - 2*$seq2 +$seq1; # (u3 - * u2 + u1) -> 2a
my $a = $diff2 / 2;
my $b = $diff1 - 3*$a;
my $c = $seq1 - $b - $a;
INFO "Part 2 Quad is : %d * x^2 + %d * x + %d", $a, $b, $c;

# For x 0,1,2
my $seq0 = 3751;
my $seq1 = 33531;
my $seq2 = 92991;
my $a = ($seq1 - 2*$seq2 + $seq3) / 2;
my $b = (-3*$seq1 + 4*$seq2 - $seq3) / 2;
my $c = $seq1;
# 14840 n^2 + 14940 n + 3751, with n = 202300
# INFO: Part 2 Quad is : 14840 * x^2 + 14940 * x + 3751

#14840 * x^2 + -14740 * x + 3651
# for odd sequence : 59360 * x^2 + -88840 * x + 33231

# https://www.wolframalpha.com/input?i=quadratic+fit+calculator&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3x%22%7D+-%3E%22%7B+0%2C+1%2C+2%7D%22&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3y%22%7D+-%3E%22%7B+3751%2C+33531%2C+92991%7D%22
# Wolfram with {0, 1, 2} = {3751, 33531, 92991}
# -> 14840x^2 + 14940x + 3751
# Wolfram with {0, 1, 2} = {3751, 92991, 300951}
# -> 59360^2 + 29880 + 3751
###############

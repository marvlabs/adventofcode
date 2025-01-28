#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 2h25
# RESULT [Puzzle 2023/14]: PART1 [106186] - PART2 [106390] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::Board;
use XY::XY qw(XY);
use AOC qw(DEBUG TRACE INFO PROGRESS BOARD BOARD_PAUSE);
use Memoize;
use Digest::SHA qw(sha1_hex);
$AOC::NAME = "Parabolic Reflector Dish: shuffle stones";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 145;
$AOC::LEARNED = "Memoization cache optimaziton, cycle detection";
#########################
# Init	
my $year = "2023";
my $puzzle = "14";

my @Tests;
push @Tests, { NAME => 'NorthRocks 136', RESULT1 => 136, RESULT2 => 64, INPUT  => << 'EOEX',
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
EOEX
};
##################################
# Alternative solutions:
my $USE_PERIOD_DETECTION = 1; # Be smart and skip unnecessary cycles (40s)
my $USE_MY_MEMOIZATION = 1;   # If un-smart: use bespoke caching (~200s for the real solution). Otherwise use general memoization (slower, ~900s)
###

my $ROUND = ord 'O';
my $CUBE  = ord '#';
my $SPACE = ord '.';
my $CYCLES = 1000000000;


sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
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
	$AOC::BOARD_LAG=0;
	BOARD $board;
	$AOC::BOARD_LAG=0;
	# binmode(STDOUT, ":encoding(UTF-8)");
	# DEBUG "Parse: Input Field [%d/%d]\n%s", $boardX, $boardY, $board->toString();

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		&moveAllONorth($board);
		DEBUG "Part1: after tilt North\n%s", $board->toString();
		$p1_result = &evaluate($board);
		INFO "*** Part 1 -> [%d]", $p1_result;
		BOARD_PAUSE 1;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";

		if ($USE_PERIOD_DETECTION) {
			# Use my own cache with hash of board string. 
			# Detect period, skip unnecessary cycles
			# -> runs 42s
			my %BoardsCache;
			my $period = 0;
			for (my $i = 1; $i <= $CYCLES; $i++) {
				PROGRESS $i;
				my $key = &oneCycle($board);
				DEBUG "Part2: [%d] cycles key [%s] weight [%d]", $i, $key, evaluate($board);

				if (exists $BoardsCache{$key} && $period == 0) {
					$period = $i - $BoardsCache{$key};
					# Skip the next n rounds which would not contribute
					my $next = $i + int(($CYCLES - $i )/ $period) * $period;
					INFO "Part2: repetition found after [%d] cycles: same as [%d] -> period [%d] continuing at [%d]", $i, $BoardsCache{$key}, $period, $next;
					$i = $next;
				} 
				else {
					$BoardsCache{$key} = $i;
				}
			}
			$p2_result =  &evaluate($board);
		}
		else {
			###########################
			### Alternative solutions:
			### Version with full loop, use memoization: call with board ref and key, get back resulting key

			if ($USE_MY_MEMOIZATION) {
				# Use my specific cache implementation: 
				# Not bad! runs in 6:33, 5 times faster than the general memoization below (including test input, which takes about the same time)
				my %cycleCache;
				my $key = sha1_hex($board->toString());
				my ($weight, $nextKey);
				for (my $i = 1; $i <= $CYCLES; $i++) {
					$nextKey = $cycleCache{$key}{KEY};
					$weight  = $cycleCache{$key}{WEIGHT};
					#DEBUG "Part2 MYCACHE: [%d] cache hit with [%s]", $i, $key;
					if (!defined $nextKey) {
						($nextKey, $weight) = &oneCycleMemoized($board, $key);
						$cycleCache{$key}{KEY} = $nextKey;
						$cycleCache{$key}{WEIGHT} = $weight;
						#DEBUG "Part2 MYCACHE: [%d] cache miss with [%s]", $i, $key;
					}
					$key = $nextKey;
					#DEBUG  "Part2 MYCACHE: [%d] cycles key is [%s], weight [%d]", $i, $key, $weight;
					#DEBUG ("Part2 MYCACHE: [%d] cycles", $i) if ($i % 10000000 == 0);
				}
				$p2_result = $weight;
			}
			else {
				# Use module memoize:
				# -> really slow: 1E9 is still a lot of loops to look up in cache
				# Runs 28:09 (including test input, which takes about the same time)
				memoize('oneCycleMemoized');
				my $key = sha1_hex($board->toString());
				my $weight;
				for (my $i = 1; $i <= $CYCLES; $i++) {
					($key, $weight) = &oneCycleMemoized($board, $key);
					#DEBUG  "Part2 MEMOIZED: [%d] cycles key is [%s], weight [%d]", $i, $key, $weight;
					DEBUG ("Part2 MEMOIZED: [%d] cycles", $i) if ($i % 10000000 == 0);
				}
				$p2_result = $weight;
			}
		}
		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 106186 106390
	return ($p1_result, $p2_result);
}

###########
# Part 2 functions, a bit generalized

sub oneCycle { 
	my $board = shift;
	&moveAllStones($board, 'N');
	&moveAllStones($board, 'W');
	&moveAllStones($board, 'S');
	&moveAllStones($board, 'E');

	# return a hash which can be compared -> we're going to hit a repetition soon!
	return sha1_hex($board->toString());
}

sub moveAllStones { 
	my $board = shift;
	my $dir = shift;
	if ($dir eq 'N') {
		# Start NW
			for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
				if ($board->is(XY($x, $y), $ROUND)) {
					&moveOneStone($board, XY($x, $y), $dir);
				}
			}
		}
	}
	elsif ($dir eq 'W') {
		# Start NW
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			for (my $y = 0; $y < $board->getSizeY(); $y++) {
				if ($board->is(XY($x, $y), $ROUND)) {
					&moveOneStone($board, XY($x, $y), $dir);
				}
			}
		}
	}
	elsif ($dir eq 'S') {
		# Start SE
		for (my $y = $board->getSizeY()-1; $y >=0 ; $y--) {
			for (my $x = $board->getSizeX()-1; $x >=0 ; $x--) {
				if ($board->is(XY($x, $y), $ROUND)) {
					&moveOneStone($board, XY($x, $y), $dir);
				}
			}
		}
	}
	else {
		# Start SE
		for (my $x = $board->getSizeX()-1; $x >=0 ; $x--) {
			for (my $y = $board->getSizeY()-1; $y >=0 ; $y--) {
				if ($board->is(XY($x, $y), $ROUND)) {
					&moveOneStone($board, XY($x, $y), $dir);
				}
			}
		}
	}
}

sub moveOneStone { 
	my $board = shift;
	my $field = shift;
	my $dir = shift;

	my $targetField = $field;
	my $nextField = $targetField->add(XY::XY::aim($dir));
	while ($board->is($nextField, $SPACE)) {
		$targetField = $nextField;
		$nextField = $targetField->add(XY::XY::aim($dir));
	}
	#TRACE "moveOneStone: %s can move $dir to ", $field->toString(), $targetField->toString() unless ($field->equal($targetField));
	$board->moveTo($field, $targetField, $SPACE) unless ($field->equal($targetField));
}

# Alternative: a bit slower
sub moveOneStoneRecursive { 
	my $board = shift;
	my $field = shift;
	my $dir = shift;

	my $targetField = $field->add(XY::XY::aim($dir));
	if ($targetField && $board->is($targetField, $SPACE)) {
		#TRACE "moveOneStone: %s can move %s", $field->toString(), $dir;
		$board->moveTo($field, $targetField, $SPACE);
		&moveOneStone($board, $targetField, $dir)
	}
}

# Alternative solutions: test with memoization cache
sub oneCycleMemoized { 
	my $board = shift;
	my $key = shift;
	&moveAllStones($board, 'N');
	&moveAllStones($board, 'W');
	&moveAllStones($board, 'S');
	&moveAllStones($board, 'E');

	# return a hash which can be used to memoize this call
	return sha1_hex($board->toString()), &evaluate($board);
}

###########
# Part one functions
sub evaluate { my $board = shift;
	my $sum;
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			if ($board->is(XY($x, $y), $ROUND)) {
				$sum += $board->getSizeY() - $y;
			}
		}
	}
	return $sum;
}

sub moveAllONorth { my $board = shift;
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			if ($board->is(XY($x, $y), $ROUND)) {
				&moveOneONorth($board, XY($x, $y));
			}
		}
	}
}

sub moveOneONorth { 
	my $board = shift;
	my $field = shift;

	my $northField = $field->add(XY::XY::aim('N'));
	if ($northField && $board->is($northField, $SPACE)) {
		TRACE "moveOneONorth: %s can move N", $field->toString();
		$board->moveTo($field, $northField, $SPACE);
		&moveOneONorth($board, $northField)
	}
}
############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

Your puzzle answer was 106186.

--- Part Two ---

The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

Your puzzle answer was 106390.

Both parts of this puzzle are complete! They provide two gold stars: **

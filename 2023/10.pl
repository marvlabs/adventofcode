#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 3h50'
# RESULT [Puzzle 10]: PART1 [6613] - PART2 [511] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::Board;
use XY::XY qw(XY);
use AOC qw(DEBUG TRACE INFO PROGRESS BOARD BOARD_PAUSE);
$AOC::NAME = "Pipe Maze: XY shennaningans";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 230;
$AOC::LEARNED = "Inside/Outside edge counting";
#########################
# Init	
my $year = "2023";
my $puzzle = "10";

my @Tests;

push @Tests, { NAME => 'Loop-4 easy', RESULT1 => 4, INPUT  => << 'EOEX',
.....
.S-7.
.|.|.
.L-J.
.....
EOEX
};

push @Tests, { NAME => 'Loop-4 hidden', RESULT1 => 4, INPUT  => << 'EOEX',
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
EOEX
};

push @Tests, { NAME => 'Loop-8 easy', RESULT1 => 8, , INPUT  => << 'EOEX',
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
EOEX
};

push @Tests, { NAME => 'Loop-8 hidden', RESULT1 => 8, INPUT  => << 'EOEX',
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
EOEX
};

push @Tests, { NAME => 'Include-4', RESULT1 => 23, RESULT2 => 4, INPUT  => << 'EOEX',
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
EOEX
};

push @Tests, { NAME => 'Include-4 squeeze', RESULT1 => 22, RESULT2 => 4, INPUT  => << 'EOEX',
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
EOEX
};

push @Tests, { NAME => 'Include-8', RESULT1 => 70, RESULT2 => 8, INPUT  => << 'EOEX',
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
EOEX
};
# ...results in :
# .╭────╮╭╮╭╮╭╮╭─╮....
# .│╭──╮││││││││╭╯....
# .││.╭╯││││││││╰╮....
# ╭╯╰╮╰╮╰╯╰╯││╰╯●╰─╮..
# ╰──╯.╰╮●●●╰╯↓╮╭─╮╰╮.
# ....╭─╯●●╭╮╭╯│╰╮╰╮╰╮
# ....╰╮●╭╮││╰╮│●╰╮╰╮│
# .....│╭╯╰╯│╭╯│╭╮│.╰╯
# ....╭╯╰─╮.││.││││...
# ....╰───╯.╰╯.╰╯╰╯...

push @Tests, { NAME => 'Include-10 hidden', 	RESULT1 => 80, RESULT2 => 10, INPUT  => << 'EOEX',
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
EOEX
};

##################################
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
my $START = ord 'S';
my $GROUND = ord '.';

# Pipe: we go 'DIR' and encounter symbol 'pipe' -> next direction, eg we step east E and find J : 'EJ' leads us => N
my %PipeDirectsTo = (
	"S|" => 'S',
	"N|" => 'N',
	"W-" => 'W',
	"E-" => 'E',
	"SL" => 'E',
	"WL" => 'N',
	"EJ" => 'N',
	"SJ" => 'W',
	"E7" => 'S',
	"N7" => 'W',
	"NF" => 'E',
	"WF" => 'S',
);

my %PipeDisplayChar = ( #https://www.w3schools.com/charsets/ref_utf_box.asp
	"|" => 0x2502, # │ / 9475, # ┃
	"-" => 0x2500, # ─ / 9473, # ━
	"L" => 0x2570, # ╰ / 9495, # ┗
	"J" => 0x256f, # ╭ / 9499, # ┛
	"7" => 0x256e, # ╮ / 9491, # ┓
	"F" => 0x256d, # ╭ / 9487, # ┏
	"W" => 8592, # ←
	"N" => 8593, # ↑
	"E" => 8594, # →
	"S" => 8595, # ↓
	"I" => 9679, # ● / 9618, # ▒
);


sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";
	##### Parse input
	# Parse input
	my $labstr;
	my $labY;
	my $labX;
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		$labstr .= $_;
		$labX = length $labstr unless($labX);
		$labY++;
	}
	DEBUG "Read field init $labX/$labY\n";
	# Set up field
	my $board = XY::Board->new($labX, $labY);
	$board->setTiles($labstr);


	my $StartPos = &findStartS($board);
	$AOC::BOARD_LAG=0;
	BOARD $board;
	$AOC::BOARD_LAG=300;
	# binmode(STDOUT, ":encoding(UTF-8)");
	# DEBUG "Parse: Input Field [%d/%d]\n%s", $labX, $labY, $board->toString();

	# Find one of the two possible first steps away from start: We have exactly two pipes connected to the start field
	my $firstStep;
	my $rPossibleFields = $StartPos->directNeighbours();
	foreach my $dir (keys %$rPossibleFields) {
		my $pipe = chr($board->getAt($rPossibleFields->{$dir}));
		my $pipeIndex = $dir . $pipe;
		#DEBUG "PossibleStart: Checking from %s go %s: [%s] with [%s] ...", $StartPos->toString(), $dir, $pipe, $pipeIndex;

		if (exists $PipeDirectsTo{$pipeIndex}) {
			INFO "START: from %s go %s: [%s] (with %s) directs %s", $StartPos->toString(), $dir, $pipe, $pipeIndex, $PipeDirectsTo{$pipeIndex};
			$firstStep = $dir;
			last;
		}
	}
	


	##### Part 1 #####

	# Record all the parts of the pipe along the way
	my %PipeParts;

	# We need part one for part two, so don't skip -> configure a part-1 testresult also for the part two test inputs
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";

		my $steps = 0;
		my $pos = $StartPos;
		my $nextStep = $firstStep;
		my $StartFieldPipe;

		while (1) {
			my $dir = XY::XY::aim($nextStep);
			#DEBUG "STEP AT %s wanting to go %s (%s)", $pos->toString(), $nextStep, $dir->toString();
			my $nextPos = $pos->add($dir);

			my $pipe = chr($board->getAt($nextPos));
			if ($pipe eq chr($START)) {
				# We are getting back to start

				# Record last tile
				#DEBUG "PipeParts: %s adding last part (%s)", $pos->toString(), $PipeParts{$pos->toString()};
				$PipeParts{$pos->toString()} = chr($board->getAt($pos));
				$board->setAt($pos, $PipeDisplayChar{$PipeParts{$pos->toString()}});

				# Record Start field
				$StartFieldPipe = &computeStartFieldPipe ($firstStep, $nextStep);
				$PipeParts{$StartPos->toString()} = $StartFieldPipe;
				$board->setAt($StartPos, $PipeDisplayChar{$firstStep});
				INFO "STARTFIELDPIPE at %s is [%s]", $nextPos->toString(), $StartFieldPipe;

				last;
			};

			my $pipeIndex = $nextStep . $pipe;
			if (not exists $PipeDirectsTo{$pipeIndex}) {
				DEBUG "STEP PROBLEM: can't go on from %s -> %s: [%s] with [%s] directs nowhere", $pos->toString(), $nextStep, $pipe, $pipeIndex;
				die "No more steps possible"
			}
			#DEBUG "STEPS: (%4d) from %s go %s: [%s] with [%s] directs %s", $steps, $pos->toString(), $nextStep, $pipe, $pipeIndex, $PipeDirectsTo{$pipeIndex};
			$nextStep = $PipeDirectsTo{$pipeIndex};
			
			# For part two: record that part of the pipe, and replace with nicer character for drawing :)
			$PipeParts{$pos->toString()} = chr($board->getAt($pos));
			$board->setAt($pos, $PipeDisplayChar{$PipeParts{$pos->toString()}}) unless $pos->equal($StartPos);

			$pos = $nextPos;
			$steps++;
		};

		$p1_result = ($steps+1)/2;
		DEBUG "Part 1: Solved Pipe \n%s", $board->toString();
		INFO "*** Part 1 -> [%d]", $p1_result;
		BOARD_PAUSE 1;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		$AOC::BOARD_LAG=2000;

		# Go through each row, toggle out/in on every lower-vertical and vertical pipe boundaries ( | J L ) as we cross them.
		# (Also works with the upper vertical ( | F 7 ))
		# Count the non-pipe fields which are IN
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $out = 1;
			for (my $x = 0; $x < $board->getSizeX(); $x++) {
				my $field = XY($x, $y);
				#DEBUG "IN/OUT: checking %s", $field->toString();
				if ($PipeParts{$field->toString()}) {
					#DEBUG "IN/OUT: %s is part of pipe", $field->toString();
					my $part = $PipeParts{$field->toString()};
					if ("|JL" =~ /$part/) {
						$out = !$out;
						#DEBUG "IN/OUT: switching to %s at %s", $out ? 'OUT' : ' IN', $field->toString();
					}
				}
				elsif (!$out && chr($board->getAt($field) eq '.')) {
					#DEBUG "IN/OUT: found IN '.' %s", $field->toString();
					$board->setAt($field, $PipeDisplayChar{'I'});
					$p2_result++;
				}
			}
		}
		DEBUG "Part2: Enclosed by Pipe \n%s", $board->toString();
		INFO "*** Part 2 -> [%d]", $p2_result;
		BOARD_PAUSE 1;
	}

	##### RESULTS #####
	# 6613 511
	return ($p1_result, $p2_result);
}

#### Pipe helpers

# Go through fields and return the one with 'S'
sub findStartS { my $board = shift;
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
			if ($board->is($field, $START)) {
				return $field;
			}
		}
	}
}

# What is the start tile? It must redirect from the last step taken to our start step
sub computeStartFieldPipe { my ($firstStep, $lastStep) = @_;
	# $pipeIndex = $nextStep . ? => $firstStep
	foreach my $index (keys %PipeDirectsTo) {
		if (substr($index, 0, 1) eq $lastStep && $firstStep eq $PipeDirectsTo{$index}) {
			return substr($index, 1, 1);
		}
	}
}
############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

Your puzzle answer was 6613.

--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

Your puzzle answer was 511.

Both parts of this puzzle are complete! They provide two gold stars: **

#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 1h30
# RESULT [Puzzle 2023/16]: PART1 [6994] - PART2 [7488]
# THREAD version: 3s instead of 9s when parceling out the ray traces
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG TRACE INFO PROGRESS BOARD BOARD_PAUSE);
use XY::Board;
use XY::XY qw(XY);
use threads;
$AOC::NAME = "The Floor Will Be Lava: shine a light";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 90;
$AOC::LEARNED = "Perl threads";
#########################
# Init	
my $year = "2023";
my $puzzle = "16";

my @Tests;
push @Tests, { NAME => 'Test 1', RESULT1 => 46, RESULT2 => 51, INPUT  => << 'EOEX',
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
EOEX
};
##################################

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

	#binmode(STDOUT, ":encoding(UTF-8)");
	# DEBUG "Parse: Mirror Board [%d/%d]\n%s", $boardX, $boardY, $board->toString();

	##### Part 1 #####
	my $boardP1 = $board->duplicate();
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		$AOC::BOARD_LAG = 0;
		BOARD $boardP1;
		$AOC::BOARD_LAG = 300;
		my %energized;
		my %seen; # store beam pos and dir already seen!
		&traceOneRay($boardP1, \%seen, \%energized, XY(-1,0), 'E', 1);
		$p1_result = scalar keys %energized;

		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";

		# Threaded: shine lights from all four edges and find max energized
		my @workers;

		INFO "Part2: Shine Top down";
		my $nr = 1;
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			$boardP1->setAt(XY($x,0), ord('v')); # GUI visualization on P1 board only
			push @workers, threads->create( 
				sub { return &rayTrace($board, XY($x,-1), 'S'); } 
			);
		}
		while (my $worker = pop @workers) {
			PROGRESS $nr++;
			my $nrOfEnergized = $worker->join();
			DEBUG ("Part2: new max = %d", $nrOfEnergized) if ($nrOfEnergized > $p2_result);
			$p2_result = $nrOfEnergized if ($nrOfEnergized > $p2_result);
		}

		INFO "Part2: Shine Bottom up";
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			$boardP1->setAt(XY($x,$board->getSizeX()-1), ord('^')); # GUI visualization on P1 board only
			push @workers, threads->create( 
				sub { return &rayTrace($board, XY($x, $board->getSizeY()), 'N'); }
			);
		}
		while (my $worker = pop @workers) {
			PROGRESS $nr++;
			my $nrOfEnergized = $worker->join();
			DEBUG ("Part2: new max = %d", $nrOfEnergized) if ($nrOfEnergized > $p2_result);
			$p2_result = $nrOfEnergized if ($nrOfEnergized > $p2_result);
		}

		INFO "Part2: Shine Left to right";
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			$boardP1->setAt(XY(0,$y), ord('>')); # GUI visualization on P1 board only
			push @workers, threads->create( 
				sub { return &rayTrace($board, XY(-1,$y), 'E'); }
			);
		}
		while (my $worker = pop @workers) {
			PROGRESS $nr++;
			my $nrOfEnergized = $worker->join();
			DEBUG ("Part2: new max = %d", $nrOfEnergized) if ($nrOfEnergized > $p2_result);
			$p2_result = $nrOfEnergized if ($nrOfEnergized > $p2_result);
		}

		INFO "Part2: Shine Right to left";
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			$boardP1->setAt(XY($board->getSizeX()-1, $y), ord('<')); # GUI visualization on P1 board only
			push @workers, threads->create( 
				sub { return &rayTrace($board, XY($board->getSizeX(), $y), 'W'); }
			);
		}
		while (my $worker = pop @workers) {
			PROGRESS $nr++;
			my $nrOfEnergized = $worker->join();
			DEBUG ("Part2: new max = %d", $nrOfEnergized) if ($nrOfEnergized > $p2_result);
			$p2_result = $nrOfEnergized if ($nrOfEnergized > $p2_result);
		}

		INFO "*** Part 2 -> [%d]", $p2_result;
		BOARD_PAUSE 1;
	}

	##### RESULTS #####
	# 6994 7488
	return ($p1_result, $p2_result);
}

#######

# Possible tiles
my $TILE   = ord '.';
my $ETILE  = ord 'o';
my $SPLITV = ord '|';
my $SPLITH = ord '-';
my $MIRUP  = ord '/';
my $MIRDOWN = ord '\\';

# If direction is d and hitting item i: di -> resulting direction
my %dirChange = (
	"E\\" => 'S',
	"N\\" => 'W',
	"W\\" => 'N',
	"S\\" => 'E',
	"E/" => 'N',
	"N/" => 'E',
	"W/" => 'S',
	"S/" => 'W',
);


# Do one run, return the nr of energized fields
sub rayTrace {
	my $board = shift;
	my $start = shift;
	my $dir = shift;

	my %tileEnergized;
	my %beamSeen; # store beam pos and dir already seen!
	TRACE "Part2: Trying %s", $start->toString();
	&traceOneRay($board, \%beamSeen, \%tileEnergized, $start, $dir, 0);
	return scalar keys %tileEnergized;
}

# Shine a beam of light from one edge in, trace it around the board
# Use BeamSeen and TileEnergized to store the state (board inmutable, necessary for the threaded version)
# A split ray will cause a recursive call and will need these states.
# Finished when the ray either leaves the board or would enter a loop (same tile, same direction)
sub traceOneRay {
	my $board = shift;
	my $rBeamSeen = shift;
	my $rTileEnergized = shift;
	my $field = shift;
	my $dir = shift;
	my $markEnergizedFields = shift;

	#DEBUG "traceOneRay: START %s -> %s", $field->toString(), $dir;

	# Go to first tile (first input is from outside the board with a direction, split rays come from the splitter tile with a direction)
	$field = $field->add(XY::XY::aim($dir));

	while (my $c = $board->getAt($field)) {
		#DEBUG "traceOneRay: STEP %s (%s) -> %s", $field->toString(), chr $c, $dir;

		# Store all fields we passed through as 'energized'
		my $key = $field->toString();
		$rTileEnergized->{$key}++;

		# Cache all fields we passed through with the direction: 
		# We don't want to be caught in a ray-loop
		$key .= $dir;
		last if ($rBeamSeen->{$key});
		$rBeamSeen->{$key}++;

		######
		# Check the tile we're on:
		if ($c == $TILE) {
			# Energize and pass through
			$board->setAt($field, $ETILE) if $markEnergizedFields; # That was for part one -> visualize the outcome board by replacing all energized . with #
			$field = $field->add(XY::XY::aim($dir));
		}
		elsif ($c == $ETILE) {
		 	# Already energized, go on
		 	$field = $field->add(XY::XY::aim($dir));
		}
		elsif ($c == $MIRUP || $c == $MIRDOWN) {
			$dir = $dirChange{$dir . chr $c};
			#DEBUG "traceOneRay: DIRCHANGE %s (%s) -> %s", $field->toString(), chr $c, $dir;
			$field = $field->add(XY::XY::aim($dir));
		}
		elsif ($c == $SPLITV) {
			if ($dir eq 'N' || $dir eq 'S') {
				# '|' irrelevant when traveling vertically
				$field = $field->add(XY::XY::aim($dir));
			}
			else {
				# Split into two beams when traveling E or W -> N and S
				#DEBUG "traceOneRay: SPLITV EW %s (%s) -> %s", $field->toString(), chr $c, $dir;
				# First: ray trace the north beam...
				&traceOneRay($board, $rBeamSeen, $rTileEnergized, $field, 'N', $markEnergizedFields);
				# ... then carry on with the south beam
				$dir = 'S';
				#DEBUG "traceOneRay: SPLITV EW %s (%s) -> continuing this beam %s", $field->toString(), chr $c, $dir;
				$field = $field->add(XY::XY::aim($dir));
			}
		}
		elsif ($c == $SPLITH) {
			if ($dir eq 'E' || $dir eq 'W') {
				# '|' irrelevant when traveling horizontally
				$field = $field->add(XY::XY::aim($dir));
			}
			else {
				# Split into two beams when traveling N or S -> E and W
				#DEBUG "traceOneRay: SPLITV NS %s (%s) -> %s", $field->toString(), chr $c, $dir;
				# First: ray trace the east beam...
				&traceOneRay($board, $rBeamSeen, $rTileEnergized, $field, 'E', $markEnergizedFields);
				# ... then carry on with the west beam
				$dir = 'W';
				#DEBUG "traceOneRay: SPLITV NS %s (%s) -> continuing this beam %s", $field->toString(), chr $c, $dir;
				$field = $field->add(XY::XY::aim($dir));
			}
		}
		
	}
	#DEBUG "traceOneRay: Beam finished at %s -> %s", $field->toString(), $dir;
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 16: The Floor Will Be Lava ---

With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

Your puzzle answer was 6994.

--- Part Two ---

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?

Your puzzle answer was 7488.

Both parts of this puzzle are complete! They provide two gold stars: **

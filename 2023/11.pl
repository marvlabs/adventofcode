#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 1h50'
# RESULT [Puzzle 2023/11]: PART1 [9974721] - PART2 [702770569197] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::Board;
use XY::XY qw(XY);
use AOC qw(DEBUG INFO);
$AOC::NAME = "Cosmic Expansion: Galaxy shift";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 110;
$AOC::LEARNED = "XY board can complicate things - just use the coords of the objects";
#########################
# Init	
my $year = "2023";
my $puzzle = "11";

my @Tests;
push @Tests, { NAME => 'Galaxy 1', RESULT1 => 374, RESULT2 => 1030, INPUT  => << 'EOEX',
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
EOEX
};
my $SPACE = '.';
my $GALAXY = '#';

my $EXPANSION_TEST = 9;
my $EXPANSION_REAL = 999999;
my $EXPANSION = $EXPANSION_TEST;
##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";
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

	binmode(STDOUT, ":encoding(UTF-8)");
	DEBUG "Parse: Input Field [%d/%d]\n%s", $labX, $labY, $board->toString();


	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";

		# Expand our universe: create new board
		my $expandedboard = &expandVertical(&expandHorizontal($board));
		DEBUG "Parse: Horizontal expanded [%d/%d]\n%s", $expandedboard->getSizeX(), $expandedboard->getSizeY(), $expandedboard->toString();
		my $rGalaxiesPart1 = &findGalaxies($expandedboard);
		###
		# Alternatively it would also work with Part-2 solution instead of actual universe expansion :)
		# my $rGalaxiesPart1 = &findGalaxies($board);
		# &shiftGalaxiesVertical($board, 1, $rGalaxiesPart1);
		# &shiftGalaxiesHorizontal($board, 1, $rGalaxiesPart1);
		###
		$p1_result = &sumAllDistancesBetweenGalaxies([values %$rGalaxiesPart1]);
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";

		# Universe expansion by 1E6 would blow the machine? Just shift the Galaxy coordinates further away
		my $rGalaxiesPart2 = &findGalaxies($board);
		&shiftGalaxiesVertical($board, $EXPANSION, $rGalaxiesPart2);
		&shiftGalaxiesHorizontal($board, $EXPANSION, $rGalaxiesPart2);
		$p2_result = &sumAllDistancesBetweenGalaxies([values %$rGalaxiesPart2]);
		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 9974721 702770569197
	return ($p1_result, $p2_result);
}

# Check each galaxy for distance to the remaining galaxies, sum up
sub sumAllDistancesBetweenGalaxies {
	my $rGalaxies = shift;
	my $sum;

	while (my $galaxyField = shift @$rGalaxies) {
		#DEBUG "sumAllDistancesBetweenGalaxies: Checking Galaxy at [%s]", $galaxyField->toString();
		foreach my $targetField (@$rGalaxies) {
			my $dist = abs($galaxyField->x() - $targetField->x()) +  abs($galaxyField->y() - $targetField->y());
			#DEBUG "sumAllDistancesBetweenGalaxies: [%s] to [%s] -> [%d]", $galaxyField->toString(), $targetField->toString(), $dist;
			$sum += $dist;
		}
	}
	return $sum;
}

# Get coords of all galaxy on the board
sub findGalaxies {
	my $board = shift;
	my %Galaxies;

	my $nrOfGalaxies;
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				$nrOfGalaxies++;
				$Galaxies{$field->toString()} = $field;
				#DEBUG "findGalaxies: found Galaxy at [%s]", $field->toString();
			}
		}
	}
	DEBUG "findGalaxies: found [%d]", $nrOfGalaxies;
	return \%Galaxies;
}


### Shift galaxy coordinates if an empty row/col is detected
sub shiftGalaxiesHorizontal {
	my $board = shift;
	my $expansion = shift;
	my $rGalaxies = shift;

	for (my $x = $board->getSizeX()-1; $x >= 0; $x--) {
		my $isEmpty = 1;
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				 $isEmpty = 0;
				 last;
			}
		}
		if ($isEmpty) {
			DEBUG "shiftGalaxiesHorizontal: Need to horizontal shift all Galaxies beyond [%d] by %d", $x, $expansion;
			foreach my $galaxy (keys %$rGalaxies) {
				my $field = $rGalaxies->{$galaxy};
				if ($field->x() > $x) {
					my $newField = XY($field->x()+$expansion, $field->y());
					#DEBUG "shiftGalaxiesHorizontal: Galaxy (was: %s) %s -> %s", $galaxy, $field->toString(), $newField->toString();
					$rGalaxies->{$galaxy} = $newField;
				}
			}
		}
	}
}

sub shiftGalaxiesVertical {
	my $board = shift;
	my $expansion = shift;
	my $rGalaxies = shift;

	for (my $y = $board->getSizeY()-1; $y >= 0; $y--) {
		my $isEmpty = 1;
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				 $isEmpty = 0;
				 last;
			}
		}
		if ($isEmpty) {
			DEBUG "shiftGalaxiesVertical: Need to vertical shift all Galaxies beyond [%d] by %d", $y, $expansion;
			foreach my $galaxy (keys %$rGalaxies) {
				my $field = $rGalaxies->{$galaxy};
				if ($field->y() > $y) {
					my $newField = XY($field->x(), $field->y()+$expansion);
					#DEBUG "shiftGalaxiesVertical: Galaxy (was: %s) %s -> %s", $galaxy, $field->toString(), $newField->toString();
					$rGalaxies->{$galaxy} = $newField;
				}
			}
		}
	}
}


### Expand our galaxy board by the number of empty row/col detected and copy any Galaxies beyond these rows a bit farther away
### (insert empty row/col)
sub expandHorizontal {
	my $board = shift;
	my $newColcount = $board->getSizeX() + &nrOfEmptyCols($board);
	DEBUG "expandHorizontal: from [%d] to [%d] cols", $board->getSizeX(), $newColcount;

	my $expandedBoard = XY::Board->new($newColcount, $board->getSizeY());

	my $expandedX = -1;
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		$expandedX++;

		my $isEmpty = 1;
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				 $isEmpty = 0;
			}
			$expandedBoard->setAt(XY($expandedX, $y), $board->getAt($field));
		}

		if ($isEmpty) {
			$expandedX++;
			for (my $y = 0; $y < $expandedBoard->getSizeY(); $y++) {
				my $field = XY($expandedX, $y);
				$expandedBoard->setAt($field, ord $SPACE);
			}
		}
	}
	return $expandedBoard;
}

sub nrOfEmptyCols {
	my $board = shift;
	my $nrOfEmptyCols;

	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		my $isEmpty = 1;
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				 $isEmpty = 0;
				 last;
			}
		}
		$nrOfEmptyCols++ if $isEmpty;
	}
	return $nrOfEmptyCols;
}

sub expandVertical {
	my $board = shift;
	my $newRowcount = $board->getSizeY() + &nrOfEmptyRows($board);
	DEBUG "expandVertical: from [%d] to [%d] rows", $board->getSizeY(), $newRowcount;

	my $expandedBoard = XY::Board->new($board->getSizeX(), $newRowcount);

	my $expandedY = -1;
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		$expandedY++;

		my $isEmpty = 1;
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				 $isEmpty = 0;
			}
			$expandedBoard->setAt(XY($x, $expandedY), $board->getAt($field));
		}

		if ($isEmpty) {
			$expandedY++;
			for (my $x = 0; $x < $expandedBoard->getSizeX(); $x++) {
				my $field = XY($x, $expandedY);
				$expandedBoard->setAt($field, ord $SPACE);
			}
		}
	}
	return $expandedBoard;
}

sub nrOfEmptyRows {
	my $board = shift;
	my $nrOfEmptyRows;

	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		my $isEmpty = 1;
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
			if ($board->is($field, ord $GALAXY)) {
				 $isEmpty = 0;
				 last;
			}
		}
		$nrOfEmptyRows++ if $isEmpty;
	}
	return $nrOfEmptyRows;
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
$EXPANSION = $EXPANSION_REAL;
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 11: Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 9974721.

--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 702770569197.

Both parts of this puzzle are complete! They provide two gold stars: **

#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 2h
# RESULT [Puzzle 2023/13]: PART1 [35232] - PART2 [37982] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::Board;
use XY::XY qw(XY);
use AOC qw(DEBUG INFO TRACE PROGRESS);
$AOC::NAME = "Point of Incidence: Mirror Mirrage";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 120;
$AOC::LEARNED = "Allow for innacuracy";
#########################
# Init	
my $year = "2023";
my $puzzle = "13";

my @Tests;
push @Tests, {  NAME => 'Mirror-hor 5', RESULT1 => 5, RESULT2 => 300, INPUT  => << 'EOEX',
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
EOEX
};

push @Tests, {NAME => 'Mirror-vert 4', RESULT1 => 400, RESULT2 => 100, INPUT  => << 'EOEX',
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
EOEX
};

push @Tests, {  NAME => 'Mirror-both', RESULT1 => 405, RESULT2 => 400, INPUT  => << 'EOEX',
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
EOEX
};


##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";
	##### Parse input

	local $/ = ''; # Paragraph mode
	my @notes = <$inputFilehandle>; #chomp @notes;

	my $nr = 1;
	foreach my $note (@notes) {
		PROGRESS $nr++;#, scalar @notes;
		my $boardstr;
		my $boardY;
		my $boardX;
		foreach my $line (split('\n', $note)) {
			$boardstr .= $line;
			$boardX = length $boardstr unless($boardX);
			$boardY++;
		}
		# We got one note, solve it
		my ($mirror, $smudgedMirror) = &findMirror($boardstr, $boardX, $boardY);
		$p1_result += $mirror;
		$p2_result += $smudgedMirror;
	}

	INFO "*** Part 1 -> [%d]", $p1_result;
	INFO "*** Part 2 -> [%d]", $p2_result;
	##### RESULTS #####
	# 35232, 37982
	return ($p1_result, $p2_result);
}

# Part1 and Part2:
# - get a board input string
# - build a XY board
# - check for horizontal and vertical mirrorness
# 		- without and with allowing for one flawed input
sub findMirror { my ($labstr, $labX, $labY) = @_;
	# Set up field
	my $board = XY::Board->new($labX, $labY);
	$board->setTiles($labstr);
	$board->setOutputMapping (());
	# Instead of having different evaluation functions for horizontal and vertical, rotate the board for the second check
	my $board90 = $board->rotate90();

	DEBUG "findMirror: [%d/%d]\n%s", $labX, $labY, $board->toString();

	my $vert = &findVert($board);
	my $hor  = &findVert($board90);

	my $smudgedVert = &findSmudgedVert($board);
	my $smudgedHor  = &findSmudgedVert($board90);
	
	return ($vert*100 + $hor, $smudgedVert * 100 + $smudgedHor)
}

# Part2: find vertical mirror line, but allowing for exactly one smudged value
sub findSmudgedVert {
	my $board = shift;

	for (my $y = 0; $y < $board->getSizeY()-1; $y++) {
		# First: we need two identical lines

		# Check possible smudged line for flawed equality
		if (oneCharDiff(&getHorLineStr($board, $y), &getHorLineStr($board, $y+1))) {
			DEBUG "findSmudgedVert: found smudge twin at [%d,%d]\n   [%s]\n   [%s]", $y, $y+1, &getHorLineStr($board, $y),  &getHorLineStr($board, $y+1);
			# Go up and down, see if all other lines match perfectly
			my $isMirror = 1;
			for (my ($up, $down) = ($y-1, $y+2); $down < $board->getSizeY() && $up >= 0; $up--, $down++) {
				$isMirror = 0 if (&getHorLineStr($board, $up) ne &getHorLineStr($board, $down));
				last unless $isMirror;
			}
			DEBUG ("findSmudgedVert: found smudged line at [%d]", $y) if ($isMirror);
			DEBUG ("findSmudgedVert: is smudged vertical mirror at [%d]", $y+1) if ($isMirror);
			return $y+1 if ($isMirror);
		}

		# Or we have a clean twin match
		elsif (&getHorLineStr($board, $y) eq &getHorLineStr($board, $y+1)) {
			DEBUG "findSmudgedVert: found twin at [%d,%d]\n   [%s]\n   [%s]", $y, $y+1, &getHorLineStr($board, $y),  &getHorLineStr($board, $y+1);
			# Go up and down, see if all lines match if we allow for one smudge somewhere
			my $isMirror = 1;
			my $hasSmudge = 0;
			for (my ($up, $down) = ($y-1, $y+2); $down < $board->getSizeY() && $up >= 0; $up--, $down++) {
				if (&getHorLineStr($board, $up) ne &getHorLineStr($board, $down)) {
					# Can we still allow for a smudge?
					if ($hasSmudge) {
						$isMirror = 0;
						last;
					}
					if (oneCharDiff(&getHorLineStr($board, $up), &getHorLineStr($board, $down))) {
						# Found a smudged match. The rest must be clean matches
						$hasSmudge = 1;
						DEBUG "findSmudgedVert: found smudged line at [%d]", $up;
					}
				}
				last unless $isMirror;
			}
			DEBUG ("findSmudgedVert: is smudged vertical mirror at [%d]", $y+1) if ($isMirror && $hasSmudge);
			return $y+1 if ($isMirror && $hasSmudge);
		}

	}
	return 0;
}

# True if the strings differ exactly at one position
sub oneCharDiff { my ($str1, $str2) = @_;
	my $diff = 0;
	for (my $i = 0; $i < length($str1); $i++) {
		$diff++ if (substr($str1, $i, 1) ne substr($str2, $i, 1));
		return 0 if ($diff > 1);
	}
	return $diff;
}

# Part 1: find vertical mirrored lines
sub findVert {
	my $board = shift;

	for (my $y = 0; $y < $board->getSizeY()-1; $y++) {
		# First: we need two identical lines
		if (&getHorLineStr($board, $y) eq &getHorLineStr($board, $y+1)) {
			DEBUG "findVert: found twin at [%d,%d] [%s]", $y, $y+1, &getHorLineStr($board, $y);
			# Go up and down, see if all lines match
			my $isMirror = 1;
			for (my ($up, $down) = ($y-1, $y+2); $down < $board->getSizeY() && $up >= 0; $up--, $down++) {
				$isMirror = 0 if (&getHorLineStr($board, $up) ne &getHorLineStr($board, $down));
				last unless $isMirror;
			}
			DEBUG ("findVert: is vertical mirror at [%d]", $y+1) if ($isMirror);
			return $y+1 if ($isMirror);
		}
	}
	return 0;
}

sub getHorLineStr { my ($board, $y) = @_;
	my $str2 = join('', map (chr, $board->getRowValues($y)));
}


############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 13: Point of Incidence ---

With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

Your puzzle answer was 35232.

--- Part Two ---

You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the new reflection line in each pattern in your notes?

Your puzzle answer was 37982.

Both parts of this puzzle are complete! They provide two gold stars: **
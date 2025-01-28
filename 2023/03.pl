#!perl
###
# https://adventofcode.com/2023/day/3
# run: 2023/03.pl
# Solved in: 75'
# RESULT [Puzzle 03]: PART1 [540025] - PART2 [84584891]
###
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::Board;
use XY::XY qw(XY);
use strict;
use AOC qw(DEBUG INFO TRACE);
$AOC::NAME = "Gear Ratios: first XY board";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 75;
$AOC::LEARNED = "XY board usage";
#########################
# Init
my $year = "2023";
my $puzzle = "03";

my @Tests;
push @Tests, { NAME => 'Partsmap', RESULT1 => 4361, RESULT2 => 467835, INPUT  => << 'EOEX1',
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
EOEX1
};
##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my ($p1_result, $p2_result);

	my $CEMPTY = ord('.');

	my %PartNumbers;
	my $idxStart = 256;#383;
	my $idxOfPartNumbers=$idxStart;

	# Parse input
	my $labstr;
	my $labY;
	my $labX;
	while (<$inputFilehandle>) {	chomp;
		next if (/^$/);
		$labX = length $_ unless($labX);
		$labY++;

		while ($_ =~ /([0-9]+)/g) {
			my $number = $1; # substr($_, ($pos) - length($1), length($1));
			my $endpos = pos($_);
			my $startpos = $endpos - length($number);
			my $line = $.;
			$idxOfPartNumbers++;
			#printf "[%3d] found [%5d] pos [%3d - %3d] -> [%5d]\n", $line, $number, $startpos, $endpos;
			$PartNumbers{$idxOfPartNumbers} = $number;
			for (my $x=$startpos; $x < $endpos; $x++) {
				substr($_, $x, 1, chr($idxOfPartNumbers));
			}
		}
		$labstr .= $_;

	}
	DEBUG "Read field init $labX/$labY";

	#####
	# Set up field
	my $board = XY::Board->new($labX, $labY);
	$board->setTiles($labstr);

	binmode(STDOUT, ":encoding(UTF-8)");
	DEBUG "Board: %d x %d :\n%s", $board->getSizeX(), $board->getSizeY(), $board->toString();


	# Part 1 : find all symbols and adjacent part numbers
	my %partNrsWhichAreAroundField;
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
			my $cField = $board->getAt($field);
			if ($cField != $CEMPTY && $cField < $idxStart) {
				#printf "Symbol [%s] at [%s]\n", chr($cField), $field->toString();

				my $rNeighbours = $board->neighbours($field);
				foreach my $fieldValue (%$rNeighbours) {
					if ($fieldValue > $idxStart) {
						$partNrsWhichAreAroundField{$fieldValue} ++;
						#printf "Valid Part %s [%d]\n", $field->toString(), $fieldValue;
					}
				}
			}
		}
	}

	foreach my $idx (keys %partNrsWhichAreAroundField) {
		TRACE "Part [%5d] is valid", $PartNumbers{$idx};
		$p1_result += $PartNumbers{$idx};
	}

	# Part 2 : find all gears '*' which have two part numbers adjacent and multiply
	my %partNrsWhichAreAroundField;
	my $CGEAR = ord('*');
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
			my $cField = $board->getAt($field);
			if ($cField == $CGEAR) {

				my $rNeighbours = $board->neighbours($field);

				my %partNrAround;
				foreach my $fieldValue (%$rNeighbours) {
					if ($fieldValue > $idxStart) {
						$partNrAround{$fieldValue} ++;
						#printf "Valid Part %s [%d]\n", $field->toString(), $fieldValue;
					}
				}
				if (scalar keys %partNrAround == 2) {
					my ($idx1, $idx2) = (keys %partNrAround);
					my $ratio = $PartNumbers{$idx1} * $PartNumbers{$idx2};
					TRACE "Valid Gear %s has ratio [%6d]", $field->toString(), $ratio;
					$p2_result += $ratio;
				}
			}
		}
	}


	# 540025
	INFO "Results - Part 1: sum is %d", $p1_result;
	# 84584891
	INFO "Results - Part 2: sum is %d", $p2_result;
	return ($p1_result, $p2_result);
}

############################# 
# MAIN
# Run tests first
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Your puzzle answer was 540025.

--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

Your puzzle answer was 84584891.

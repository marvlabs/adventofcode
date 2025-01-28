#!perl
###
# https://adventofcode.com/2023/day/1
# run: 2023/01.pl
# Solved in: 15'
# RESULT [Puzzle 01]: PART1 [52974] - PART2 [53340]
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE PROGRESS);
$AOC::NAME = "Trebuchet: parse numbers";
$AOC::DIFFICULTY = 1;
$AOC::TIMEUSED = 15;
$AOC::LEARNED = "";
#########################
# Init
my $year = "2023";
my $puzzle = "01";

my @Tests;
push @Tests, { NAME => 'WordsNumeric', RESULT1 => 142, INPUT  => << 'EOEX1',
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
EOEX1
};
push @Tests, { NAME => 'WordsAlphaNum', RESULT2 => 281, INPUT  => << 'EOEX2',
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
EOEX2
};
##################################
sub solvePuzzle {
	my $inputFilehandle = shift;
	my ($p1_result, $p2_result);

	my %values = (1=>1, 2=>2, 3=>3, 4=>4, 5=>5, 6=>6, 7=>7, 8=>8, 9=>9,one=>1, two=>2, three=>3, four=>4, five=>5, six=>6, seven=>7, eight=>8, nine=>9 );
	my $regex1 = "[0-9]";
	my $regex2 = "[0-9]|one|two|three|four|five|six|seven|eight|nine";

	# Parse input
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		PROGRESS $.;

		# Part 1
		/($regex1)/;
		my $p1_digit10=$1;
		/.*($regex1)/;
		my $p1_digit1=$1;
		my $p1_nr = 10*$values{$p1_digit10} + $values{$p1_digit1};
		$p1_result += $p1_nr;

		# Part 2
		/($regex2)/;
		my $p2_digit10=$1;
		/.*($regex2)/;
		my $p2_digit1=$1;
		my $p2_nr = 10*$values{$p2_digit10} + $values{$p2_digit1};
		$p2_result += $p2_nr;

		DEBUG "%2d | %6s %6s %2d: Sum %6d | %6d  [$_]", $p1_nr, $p2_digit10, $p2_digit1, $p2_nr, $p1_result, $p2_result;
	}

	# 52974
	INFO "Results - Part 1: sum is %d", $p1_result;
	# 53340
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
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

Your puzzle answer was 52974.

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

Your puzzle answer was 53340.

Both parts of this puzzle are complete! They provide two gold stars: **

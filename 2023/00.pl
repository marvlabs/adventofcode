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
$AOC::NAME = "TESTS";
$AOC::DIFFICULTY = 1;
$AOC::TIMEUSED = 15;
$AOC::LEARNED = "";
#########################
# Init
my $year = "2015";
my $puzzle = "30";

my @Tests;
push @Tests, { NAME => 'WordsNumeric', RESULT1 => 142, INPUT  => << 'EOEX1',
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
EOEX1
};
##################################
sub solvePuzzle {
	my $inputFilehandle = shift;
	my ($p1_result, $p2_result);

	# Parse input
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		PROGRESS $.;
	}
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

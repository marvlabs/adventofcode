#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/09.pl
# Solved in: 
# RESULT [Puzzle 09]: PART1 [1757008019] - PART2 [995]
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE PROGRESS);
$AOC::NAME = "Mirage Maintenance: sequences";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 70;
$AOC::LEARNED = "Use reverse...";
#########################
# Init
my $year = "2023";
my $puzzle = "09";

my @Tests;
push @Tests, { NAME => 'Sequences', RESULT1 => 114, RESULT2 => 2, INPUT  => << 'EOEX1',
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
EOEX1
};
##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result);

	INFO "*** Setup & Input ***";
	##### Parse input
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		# Part 1 & 2
		PROGRESS $.;
		my @sequence = split (' ');
		DEBUG "P1&2 Extrapolate: [%s]", join (' ', @sequence);
		$p1_result += &extrapolateSequence(\@sequence);
		$p2_result += &extrapolateSequence([reverse (@sequence)]);
	}

	##### Part 1 #####
	# 1757008019 995
	return ($p1_result, $p2_result);
}


sub extrapolateSequence {
	my $rSequence = shift;
	#DEBUG "extrapolateSequence: [%s]", join ("-", @$rSequence);

	my $lastVal = @$rSequence[scalar(@$rSequence)-1];
	my $isZero = 1;
	my @diffSeq;
	for (my $x = 0; $x < scalar(@$rSequence) - 1; $x++) {
		my $diff = @$rSequence[$x+1] - @$rSequence[$x];
		$isZero = 0 if ($isZero && $diff !=0 );
		push(@diffSeq, $diff);
	}
	return $lastVal if ($isZero);

	my $result = $lastVal + &extrapolateSequence(\@diffSeq);
	DEBUG "extrapolateSequence: Result of [%s] with last value [%d] -> [%d]", join (" ", @$rSequence), $lastVal,  $result;
	return $result;
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 9: Mirage Maintenance ---

You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. The sandstorm subsequently subsides, somehow seeing you standing at an oasis!

The camel goes to get some water and you stretch your neck. As you look up, you discover what must be yet another giant floating island, this one made of metal! That must be where the parts to fix the sand machines come from.

There's even a hang glider partially buried in the sand here; once the sun rises and heats up the sand, you might be able to use the glider and the hot air to get all the way up to the metal island!

While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. It must have a delicate ecosystem; you might as well take some ecological readings while you wait. Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.

You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a single value. For example:

0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.

In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:

0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:

0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0
You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:

0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0
Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:

0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0
So, the next value of the first history is 18.

Finding all-zero differences for the second history requires an additional sequence:

1   3   6  10  15  21
  2   3   4   5   6
    1   1   1   1
      0   0   0
Then, following the same process as before, work out the next value in each sequence from the bottom up:

1   3   6  10  15  21  28
  2   3   4   5   6   7
    1   1   1   1   1
      0   0   0   0
So, the next value of the second history is 28.

The third history requires even more sequences, but its next value can be found the same way:

10  13  16  21  30  45  68
   3   3   5   9  15  23
     0   2   4   6   8
       2   2   2   2
         0   0   0
So, the next value of the third history is 68.

If you find the next value for each history in this example and add them together, you get 114.

Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?

Your puzzle answer was 1757008019.

--- Part Two ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0
Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?

Your puzzle answer was 995.

Both parts of this puzzle are complete! They provide two gold stars: **

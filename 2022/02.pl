#!/usr/bin/perl
###
# https://adventofcode.com/2022/day/2
###
use strict;

# Part 1:
# Oponent Rock A
# Oponent Paper B
# Oponent Scissors C
# Value Rock X = 1
# Value Paper Y = 2
# Value Scissors Z = 3
# Value Loose = 0
# Value Draw = 3
# Value Win = 6
my %rpsLookupPart1 = (
	"A X" => 1+3,
	"A Y" => 2+6,
	"A Z" => 3+0,
	"B X" => 1+0,
	"B Y" => 2+3,
	"B Z" => 3+6,
	"C X" => 1+6,
	"C Y" => 2+0,
	"C Z" => 3+3,
);


# Part 2:
# Oponent Rock A
# Oponent Paper B
# Oponent Scissors C
# X Loose = 0 
# Y Draw = 3
# Z Win = 6
my %rpsLookupPart2 = (
	"A X" => 3+0,
	"A Y" => 1+3,
	"A Z" => 2+6,
	"B X" => 1+0,
	"B Y" => 2+3,
	"B Z" => 3+6,
	"C X" => 2+0,
	"C Y" => 3+3,
	"C Z" => 1+6,
);

my $totalPart1 = 0;
my $totalPart2 = 0;
while (<>) {
	chomp;
	$totalPart1 += $rpsLookupPart1{$_};
	$totalPart2 += $rpsLookupPart2{$_};
	print "Part1 $_ -> $rpsLookupPart1{$_} : $totalPart1  || Part2 $_ -> $rpsLookupPart2{$_} : $totalPart2\n"
}





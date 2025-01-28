#!/usr/bin/perl
###
# https://adventofcode.com/2022/day/1
###
use strict;

my $elf1 = 0;
my $elf2 = 0;
my $elf3 = 0;

sub closeElf {
	my $cal = shift;

	if ($cal > $elf1) { 
		$elf3 = $elf2;
		$elf2 = $elf1;
		$elf1 = $cal;
	}
	elsif ($cal > $elf2) { 
		$elf3 = $elf2;
		$elf2 = $cal;
	}
	elsif ($cal > $elf2) { 
		$elf3 = $cal;
	}
	else {
		return;
	}
	print "New leaderbord: $elf1 - $elf2 - $elf3 : " . ($elf1+$elf2+$elf3) . "\n";
}

my $caloriesMax = 0;
my $caloriesCurrent = 0;



while (<>) {
	if (/^$/) {
		&closeElf($caloriesCurrent);
		$caloriesCurrent = 0;
	}
	else {
		$caloriesCurrent += $_;
	}
}
&closeElf($caloriesCurrent)





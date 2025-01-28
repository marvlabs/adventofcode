#!perl
###
use strict;
use Data::Dumper;
use Storable qw(store retrieve);

my $statfile = "2023.stat";
my $rStat = retrieve $statfile if (-r $statfile);

#print "STATISTICS: ", Dumper($Statistics);

my $runtime;
my $worktime;
printf "Advent of Code 2023                               Tests [nr, run time]    Puzzle [Difficulty, work time, run time]      lessons learned\n";
printf "---------------------------------------------------------------------------------------------------------------------------------------\n";
foreach my $day (sort keys %$rStat) {
	$runtime += $rStat->{$day}{SOLVETIME};
	$worktime += $rStat->{$day}{TIMEUSED};
	my $t = $rStat->{$day}{TIMEUSED};
	my $timestr = (($t >= 60) ? sprintf("%dh", $t/60) : "  ") . sprintf("%02dm", $t%60);
	printf "2023-$day %-50s %d %3.3fs       D%d  %s  %8.3fs   %s\n", 
		$rStat->{$day}{NAME},
		$rStat->{$day}{NROFTESTS}, $rStat->{$day}{TESTTIME}, 
		$rStat->{$day}{DIFFICULTY}, $timestr, $rStat->{$day}{SOLVETIME}, 
		$rStat->{$day}{LEARNED};
}
printf "---------------------------------------------------------------------------------------------------------------------------------------\n";
printf "Advent of Code 2023 Total:   work %dh%dm,   runtime %d seconds\n", $worktime/60, $worktime%60, $runtime;
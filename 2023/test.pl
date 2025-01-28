#!perl
use strict;
use Memoize;
use Time::HiRes qw(time);
use List::Util qw(min);
use feature 'say';
use Data::Dumper;

# use Graph::Undirected;
# use Graph::Easy;
use IPC::Open2;
use IPC::Run qw( run timeout );
use Curses;


##############
# main

#&testMemoization;
#&shoelaceTest;
#&sequenceTest;
#&runTest;
&cursesTest;

##############
# tests
sub cursesTest {
	initscr;

	my $w1 = newwin(
    1,       # height (y)
    COLS(),  # width  (x)
    0,       # start y
    1        # start x
    );

	$w1->addstr( 
    0,       # relative y to window
    0,       # relative x to window
    "Hello" 
    );

	my $w2 = newwin( 1, COLS(), 2 ,0 );
	$w2->addstr(0, 10, "World"  );

	$w1->refresh();
	$w2->refresh();

	sleep 10;
	endwin;
}

# my $val = 1;
# undef $val;
# my $sum = $val + 42;
# printf "%d\n", $sum;
# printf "Min is : %d\n", min($val, $sum, 45);

sub runTest {
	my @cmd = qw (python3 2023/24_z3.py);
	my ($in, $out, $err);
	$in = <<EOIN ;
386183914429810 203234597957945 537104238090859 6 106 -164
191853805235172 96933297552275 142797538377781 205 517 229
447902097938436 262258252263185 255543483328939 -136 38 89
EOIN
	#run \@cmd, \undef, \my $output;
	run \@cmd, \$in, \$out, \$err, timeout( 10 ) or die "cat: $?";

}


sub sequenceTest {
	my @seq = ( 6, 11, 18, 27,);# 38, 51);
	printf "Expanded sequence of [%s] is [%s] \n", join ('-', @seq), join ('-', &expandSequence(\@seq, 7));
	@seq = (3751,33531,92991);# 182131, 300951, 449451, 627631, 835491, 1073031 ##( 6, 11, 18, 27,);# 38, 51);
	my $idx = 202300;
	printf "Val idx %d of [%s] is [%d] \n", $idx, join ('-', @seq), (&expandSequence(\@seq, $idx+1))[-1];
}
sub expandSequence {
	my $rSequence = shift;
	my $nrOfElems = shift;

	my %lastValues;
	$lastValues{0} = @$rSequence[-1];

	# Get difference of sequence, then difference of diff-sequence and so on until a 0-sequence is found
	my $diffDepth = 0;
	my $isZero = 0;
	my $rCurrentSequence = $rSequence;
	while (!$isZero) {
		$diffDepth++;
		$isZero = 1;

		my @diffSeq;
		for (my $x = 0; $x < scalar(@$rCurrentSequence) - 1; $x++) {
			my $diff = @$rCurrentSequence[$x+1] - @$rCurrentSequence[$x];
			$isZero = 0 if ($isZero && $diff !=0 );
			push(@diffSeq, $diff);
		}
		$lastValues{$diffDepth} = $diffSeq[-1];
		$rCurrentSequence = \@diffSeq;
	}

	# Generate n next values by adding the last element of the lower-down sequence
	my @result = (@$rSequence);
	for (my $i = 0; $i < $nrOfElems - scalar @$rSequence; $i++) {
		my $lastVal = 0;
		for (my $depth = $diffDepth-1; $depth >= 0; $depth--) {
			$lastValues{$depth} += $lastValues{$depth+1};
		}
		push @result, $lastValues{0};
	}

	return ( (@result));
}



sub shoelaceTest {
	my @poly = ( [3,4], [5,11], [12,8], [9,5], [5,6], [3,4], [5,11],);

	say area_by_shoelace(   [3,4], [5,11], [12,8], [9,5], [5,6]   );
	say area_by_shoelace( [ [3,4], [5,11], [12,8], [9,5], [5,6] ] );
	say area_by_shoelace(  @poly );
	say area_by_shoelace( \@poly );
	
	say area_by_shoelace(   [0,0], [2,0], [2,2], [0,2],  );

}

sub area_by_shoelace {
    my $area;
    our @p;
    $#_ > 0 ? @p = @_ : (local *p = shift);
    $area += $p[$_][0] * $p[($_+1)%@p][1] for 0 .. @p-1;
    $area -= $p[$_][1] * $p[($_+1)%@p][0] for 0 .. @p-1;
    return abs $area/2;
}

###############
my %memo; # for my cache implemenation

sub testMemoization {
	my $SCALE = 10000000;
	my $DISTINCT = 109;
	my ($start, $end, $res);

	if ($SCALE < 1000001) {
		$res = 0;
		$start = time();
		for (my $x = 0; $x < $SCALE; $x++) {
			# Call function with few variations many times over
			$res += &someExpensiveFunction($x % 109);
		}
		$end = time();
		printf "Normal   [%d]: %0.2f\n", $res, $end - $start;
	}

	$res = 0;
	$start = time();
	my $key="none";
	my $val;
	for (my $x = 0; $x < $SCALE; $x++) {
		# Call function with few variations many times over
		$res += someExpensiveFunction_myCache($x % 109);
	}
	$end = time();
	printf "My cache [%d]: %0.2f\n", $res, $end - $start;
	printf "   cache size: %d items\n", scalar keys %memo;

	memoize('someExpensiveFunction');
	$res = 0;
	$start = time();
	for (my $x = 0; $x < $SCALE; $x++) {
		# Call function with few variations many times over
		$res += &someExpensiveFunction($x % 109);
	}
	$end = time();
	printf "Memoized [%d]: %0.2f\n", $res, $end - $start;
}

sub someExpensiveFunction_myCache {
	my $key = shift;
	my $val = $memo{$key};
	if (!defined $val) {
		$val = &someExpensiveFunction($key);
		$memo{$key} = $val;
	}
	return $val;
}

sub someExpensiveFunction {
	my $input = shift;
	my $res;
	for (my $i = 0; $i < $input * 3; $i++) {
		$res = $input * $input;
	}
	# do something slighlty time consuming
	return $res;
}

##############
sub testSubstr {
	my $str = "012345";
	my $s1 = substr($str, 6, 1);
	print "s1: [$s1]\n";
}

##############
sub testMap {
	my @numlist = (65, 66, 67);
	my $str1 = join ('', @numlist);
	my $str2 = join ('', map(chr, (@numlist)));
	print "[$str1] [$str2]\n";
}
##############

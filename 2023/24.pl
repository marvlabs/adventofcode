#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 6h (and some hours more for the algebra solution)
# RESULT [Puzzle 2023/24]: PART1 [21679] - PART2 [566914635762564] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
#use IPC::Run qw( run timeout );
# use XY::Board;
# use XY::XY qw(XY);
use Data::Dumper;
use AOC qw(DEBUG INFO TRACE);
$AOC::NAME = "Never Tell Me The Odds: Shooting hail stones";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 360;
$AOC::LEARNED = "Z3 vs Algebra and BF";
#########################
# Init	
my $year = "2023";
my $puzzle = "24";

my @Tests;
push @Tests, { NAME => 'Hail-2', RESULT1 => 2, ATTRIBUTE1 => [ 7, 27], ATTRIBUTE2 => 10, RESULT2 => 47, INPUT  => << 'EOEX',
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
EOEX
};
##################################
# my $AREAX = 200000000000000;
# my $AREAY = 400000000000000;
my $MINXY = 200000000000000;
my $MAXXY = 400000000000000;
my $BFRANGE = 300;

##################################
sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my $testAttribute1 = shift;
	my $testAttribute2 = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	my %Hailstones;
	my $hailnr = 0;
	#my ($maxX, $maxY, $maxZ) = (0)x3;

	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);

		$hailnr++;
		# 19, 13, 30 @ -2,  1, -2
		/(\d+), (\d+), (\d+) \@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)/;

		$Hailstones{$hailnr} = {
			NR  => $hailnr,
			px => $1, py => $2, pz => $3,
			vx => $4, vy => $5, vz => $6,
		};
	}
	INFO "Parse hail: %d hailstones", $hailnr;

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		my $minxy = $MINXY;
		my $maxxy = $MAXXY;
		($minxy, $maxxy) = (@$testAttribute1) if (defined $testAttribute1);

		for (my $i = 1; $i < $hailnr; $i++) {
			for (my $j = $i+1; $j <= $hailnr; $j++) {
				my ($fx, $fy) = &calcCross($Hailstones{$i}, $Hailstones{$j});
				#$p1_result ++ if ($fx >= 0 && $fx <= $xArea && $fy >= 0 && $fy <= $yArea);
				if ($fx >= $minxy && $fx <= $maxxy && $fy >= $minxy && $fy <= $maxxy) {
					TRACE "Part1: %s %s cross at %f / %f", &hailStr($Hailstones{$i}), &hailStr($Hailstones{$j}), $fx, $fy;
					$p1_result ++ 
				}
			}
		}

		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		my $range = $testAttribute2 ? $testAttribute2 : $BFRANGE;

		# First solution was: Plug the 9 equations into Z3 and let it solve.
		# Works, but, sort of meh
		#my ($px, $py, $pz, $vx, $vy, $vz) = solveZ3(\%Hailstones);
		#$p2_result = $px+$py+$pz;

		# Brute force: check a range of vx and vy velocities and solve against them
		# Success criteria are: 
		# - tA, tB must be positive
		# - time a/b, vz, px, py, pz are whole numbers
		# - same result for two other Hailstones
		BF: for (my $vx = -$range; $vx <= $range; $vx++) {
			for (my $vy = -$range; $vy <= $range; $vy++) {

				my @result1 = solveAlgebra($vx, $vy, $Hailstones{1}, $Hailstones{2});
				
				if (&isPlausible(@result1)) {
					DEBUG "BF Algebra: Checking plausible result for vx/vy [%d/%d] ...", $vx, $vy;
					my @result2 = solveAlgebra($vx, $vy, $Hailstones{3}, $Hailstones{4});

					if ($result1[2] == $result2[2] && $result1[3] == $result2[3] && $result1[4] == $result2[4] && $result1[7] == $result2[7]) {
						my ($ta, $tb, $px, $py, $pz, $vx, $vy, $vz) = @result1;
						INFO "BF Algebra: found result: with vx/vy/vz [%d/%d/%d] -> px/py/pz [%.1f/%.1f/%.1f]", $vx, $vy, $vz, $px, $py, $pz;
						$p2_result = $px+$py+$pz;
						last BF;
					}
				}
			}
		}
		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 47 566914635762564
	return ($p1_result, $p2_result);
}

####### 
# OK, finally found a Algebra / Brute force solution:
# Solve only 4 equations by restricting to the x/y plane and two hailstones A B.
# Unknowns are 6, therefore we brute force a range of vx / vy speeds (assume range according to the input). 
# This leaves us 4: px, py, tA, tB
# Two pages of scribbled algebra later leads to the below formula for tA, tB, px, py, pz, vz from input vx, vy, A, B
# Then we check whether the values vor this vx vy combination are reasonable and repeatable with other hailstones.
sub solveAlgebra {
	my $Rvx = shift;
	my $Rvy = shift;
	my $hailA = shift;
	my $hailB = shift;

	TRACE "solveAlgebra: vx/vy [%d/%d], hailA %s, hailB %s", $Rvx, $Rvy, &hailStr($hailA), &hailStr($hailB);

	my $Apx = $hailA->{px};
	my $Apy = $hailA->{py};
	my $Apz = $hailA->{pz};
	my $Avx = $hailA->{vx};
	my $Avy = $hailA->{vy};
	my $Avz = $hailA->{vz};

	my $Bpx = $hailB->{px};
	my $Bpy = $hailB->{py};
	my $Bpz = $hailB->{pz};
	my $Bvx = $hailB->{vx};
	my $Bvy = $hailB->{vy};
	my $Bvz = $hailB->{vz};

	return undef if (( ($Bvy-$Rvy)*($Avx-$Rvx) + ($Bvx-$Rvx)*($Rvy-$Avy) ) == 0);
	my $tA =	( ($Apy-$Bpy)*($Bvx-$Rvx) + ($Bpx-$Apx)*($Bvy-$Rvy) ) /
						( ($Bvy-$Rvy)*($Avx-$Rvx) + ($Bvx-$Rvx)*($Rvy-$Avy) );

	my $Rpx = $tA * ($Avx - $Rvx) + $Apx;
	my $Rpy = $tA * ($Avy - $Rvy) + $Apy;
	my $Rpy = $tA * ($Avy - $Rvy) + $Apy;

	return undef if (($Bvy-$Rvy) == 0);
	my $tB  = ($Rpy-$Bpy) / ($Bvy-$Rvy);
	
	return undef if (( $tB - $tA ) == 0);
	my $Rvz = ( $tB*$Bvz +$Bpz - $tA*$Avz - $Apz) / ( $tB - $tA );
	my $Rpz = $tA*$Avz + $Apz - $tA*$Rvz;

	TRACE "solveAlgebra: with vx/vy/vz [%d/%d/%d] -> tA/tB px/py/pz [%.3f, %.3f] [%.3f/%.3f/%.3f]", $Rvx, $Rvy, $Rvz, $tA, $tB, $Rpx, $Rpy, $Rpz;
	return ($tA, $tB, $Rpx, $Rpy, $Rpz, $Rvx, $Rvy, $Rvz);
}

# Check the result against: whole numbers and positive time-A, time-B
sub isPlausible {
	return 0 if (! defined $_[0]);
	foreach my $value (@_) {
		return 0 if (! &fequal($value, int(abs($value) + 0.5)*($value < 0 ? -1 : 1 )));
	}
	return 0  if ($_[0] < 0 || $_[1] < 0);
	return 1;
}



### Part 2 solved with Z3 using python interface script
sub solveZ3 {
	my $rHailstones = shift;

	# WTF: Cannot get my head around algebra of 9 equations solving.
	# We have 6 unknowns p(xyz) and v(xyz) of our stone throw
	# We can plug them into one hailstone, which gives us three equations but also adds one more unknow: t for this collision
	# Plugging it into three hailstones gives 9 equations with 9 unknowns!
	# To solve... give up and use MS Z3. Which has a python interface.
	# -> make a python script, feed in the values for the equations, run it, read back the solution. Not nice...

	# 	$in = <<EOIN ;
	# 386183914429810 203234597957945 537104238090859 6 106 -164
	# 191853805235172 96933297552275 142797538377781 205 517 229
	# 447902097938436 262258252263185 255543483328939 -136 38 89
	# EOIN
	# -> 191537613659010 238270932096689 137106090006865 206 70 247		#system "cat 24.params| python3 2023/24_z3.py";
	my $params;
	for (my $i = 1; $i <= 3; $i++) {
		my $hail = $rHailstones->{$i};
		$params .= sprintf "%d %d %d %d %d %d\n", 
			$hail->{px}, $hail->{py}, $hail->{pz},
			$hail->{vx}, $hail->{vy}, $hail->{vz};
	}
	TRACE "Solve Z3: params:\n%s", $params;
	my @cmd = qw (python3 2023/24_z3.py);
	my ($out, $err);

	DEBUG "Solve Z3: running z3 solver...";
	#!!! IPC::Run would run the python z3 script here
	# !!! run \@cmd, \$params, \$out, \$err, timeout( 20 ) or die "Cannot get result from python z3: $?";
	# Instead, fake it:
	$out = "191537613659010 238270932096689 137106090006865 206 70 247";
	chomp $out;
	INFO "Solve Z3: got [%s] from z3_py", $out;
	return (split ' ', $out);
}


### Part 1: Vector equations
sub calcCross {
	my $h1 = shift;
	my $h2 = shift;

	TRACE "calcCross: h1 %s -> h2 %s", &hailStr($h1), &hailStr($h2);

	my $px1 = $h1->{px};
	my $py1 = $h1->{py};
	my $vx1 = $h1->{vx};
	my $vy1 = $h1->{vy};
	my $s1  = $vy1/$vx1;

	my $px2 = $h2->{px};
	my $py2 = $h2->{py};
	my $vx2 = $h2->{vx};
	my $vy2 = $h2->{vy};
	my $s2  = $vy2/$vx2;

	if (fequal ($s1, $s2)) {
		DEBUG "calcCross: same slope -> either same line, or don't cross. h1 %s -> h2 %s", &hailStr($h1), &hailStr($h2);
		my $y1_0 = $s1 * $px1 + $py1;
		my $y2_0 = $s2 * $px2 + $py2;
		return (1, 1) if (fequal($y1_0, $y2_0));
		DEBUG "calcCross: same slope -> not same line";
		return (undef, undef);
	}

	my $x = ( $s1 * $px1 - $s2 * $px2 + $py2 - $py1 ) / ( $s1 - $s2 ) ;

	# Check t -> must be positive, otherwise crossing was in the past
	my  $tx1 = ($x - $px1) / $vx1;
	my  $tx2 = ($x - $px2) / $vx2;
	return (undef, undef) if ($tx1 < 0 || $tx2 < 0);
	
	my $y1 = $s1 * $x - $s1 * $px1 + $py1;
	my $y2 = $s2 * $x - $s2 * $px2 + $py2;

	die "$y1 != $y2 " unless (fequal($y1, $y2));

	TRACE "calcCross: [%f/%f]", $x, $y1;
	return ($x, $y1);
}

sub fequal {
	my ($f1, $f2) = @_;
	return (abs($f1 - $f2) < abs($f1 / 10000000));
}

# DEBUG helper
sub hailStr {
	my $hail = shift;
	return sprintf "[%3d] [%d %d %d] v(xyz) (%d %d %d)",
		$hail->{NR},
		$hail->{px}, $hail->{py}, $hail->{pz},
		$hail->{vx}, $hail->{vy}, $hail->{vz};
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 24: Never Tell Me The Odds ---

It seems like something is going wrong with the snow-making process. Instead of forming snow, the water that's been absorbed into the air seems to be forming hail!

Maybe there's something you can do to break up the hailstones?

Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories. You make a note of each hailstone's position and velocity (your puzzle input). For example:

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
Each line of text corresponds to the position and velocity of a single hailstone. The positions indicate where the hailstones are right now (at time 0). The velocities are constant and indicate exactly how far each hailstone will move in one nanosecond.

Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z position 15, X velocity 1, Y velocity -5, and Z velocity -3. After one nanosecond, the hailstone would be at 21, 14, 12.

Perhaps you won't have to do anything. How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward in time, how many of the hailstones' paths will intersect within a test area? (The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least 7 and at most 27; in your actual data, you'll need to check a much larger test area. Comparing all pairs of hailstones' future paths produces the following results:

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
So, in this example, 2 hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide. Look for intersections that happen with an X and Y position each at least 200000000000000 and at most 400000000000000. Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections. How many of these intersections occur within the test area?

Your puzzle answer was 21679.

--- Part Two ---

Upon further analysis, it doesn't seem like any hailstones will naturally collide. It's up to you to fix that!

You find a rock on the ground nearby. While it seems extremely unlikely, if you throw it just right, you should be able to hit every hailstone in a single throw!

You can use the probably-magical winds to reach any integer position you like and to propel the rock at any integer velocity. Now including the Z axis in your calculations, if you throw the rock at time 0, where do you need to be so that the rock perfectly collides with every hailstone? Due to probably-magical inertia, the rock won't slow down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position 24, 13, 10 and throwing the rock at velocity -3, 1, 2. If you do this, you will hit every hailstone as follows:

Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
Above, each hailstone is identified by its initial position and its velocity. Then, the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has exactly the same position as one of the hailstones, obliterating it into ice dust! Another hailstone is smashed to bits two nanoseconds after that. After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time 0, the rock needs to be at X position 24, Y position 13, and Z position 10. Adding these three coordinates together produces 47. (Don't add any coordinates from the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time 0 so that it perfectly collides with every hailstone. What do you get if you add up the X, Y, and Z coordinates of that initial position?

Your puzzle answer was 566914635762564.

Both parts of this puzzle are complete! They provide two gold stars: **

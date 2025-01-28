#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 4h
# RESULT [Puzzle 2023/22]: PART1 [424] - PART2 [55483]
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use List::Util qw (min max);
use List::PriorityQueue;
use AOC qw(DEBUG INFO TRACE);
#use XY::XY qw(XY);
use XY::XYZ qw(XYZ);
use Data::Dumper;
$AOC::NAME = "Sand Slabs: Jenga Tetris";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 240;
$AOC::LEARNED = "handle xyz cubes";
#########################
# Init	
my $year = "2023";
my $puzzle = "22";

my @Tests;
push @Tests, { NAME => 'Tetris-5', RESULT1 => 5, RESULT2 => 7, INPUT  => << 'EOEX',
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
EOEX
};
##################################
my $SPACE = ord '.';
my $BRICK = ord '#';

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";
	##### Parse input
	my %Bricks;
	my $bricknr = 0;
	my ($maxX, $maxY, $maxZ) = (0)x3;

	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);

		$bricknr++;
		/(\d),(\d),(\d+).(\d),(\d),(\d+)/;

		$Bricks{$bricknr} = {
			NR  => $bricknr,
			C1x => $1, C1y => $2, C1z => $3,
			C2x => $4, C2y => $5, C2z => $6,
			SUPPORTS => {}, ISSUPPORTEDBY => {},
		};
	}
	INFO "Parse brick: %d bricks", $bricknr;

	# All occupied cubes in the initial column of falling bricks. Key [x-y-z]
	my %Air;
	foreach my $brick (values %Bricks) {
		placeBrickInAir(\%Air, $brick);
	}
	INFO "Setup: Mapped all %d bricks to their 3-d space in the air, occupying %d cubes", $bricknr, scalar (keys %Air);
	foreach my $aircube (keys %Air) {
		TRACE "Setup: Air %s has brick %4d", $aircube, $Air{$aircube};
	}

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";

		my $moves = &bricksFall(\%Bricks, \%Air);
		INFO "Part 1: all bricks have fallen in %d moves", $moves;

		&bricksSupporting(\%Bricks, \%Air);
		INFO "Part 1: bricks have been related to each other";

		INFO "Part 1: checking save disintegration";
		foreach my $brick (values %Bricks) {
			$p1_result += &canDisintegrate(\%Bricks, $brick);
		}

		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		
		INFO "Part 2: Disintegrate each rock in turn to see what happens";
		foreach my $bricknr (keys %Bricks) {
			my %fallingBricks;
			&wouldFall(\%Bricks, $bricknr, \%fallingBricks);
			my $wouldFall = scalar (keys %fallingBricks) - 1; # NOT counting the disintegrated brick
			$p2_result += $wouldFall;
			TRACE "Part 2: brick %4d causes %d others to fall", $bricknr, $wouldFall;
		}
		INFO "*** Part 2 -> [%d]", $p2_result;
	}
	##### RESULTS #####
	# 424 55483
	return ($p1_result, $p2_result);
}

########
# Part 2

# Breath first: find all bricks which would fall when disintegrating this one.
sub wouldFall {
	my $rBricks = shift;
	my $brickNr = shift;
	my $rFallingBricks = shift;

	TRACE "wouldFall: checking %d", $brickNr;

	$rFallingBricks->{$brickNr}++;
	my $wouldFall = 0;

	my %startToFall; # Breath first: direct fallers before recursion

	foreach my $supported (keys %{$rBricks->{$brickNr}{SUPPORTS}}) {
		TRACE "wouldFall: supported by %d: %d", $brickNr, $supported;

		my $supportedBrickWouldFall = 1;
		foreach my $isSupportedBy (keys %{$rBricks->{$supported}{ISSUPPORTEDBY}}) {
			if (! exists $rFallingBricks->{$isSupportedBy}) {
				TRACE "wouldFall: supported brick %4d is supported by another, non falling: %d",  $supported, $isSupportedBy;
				$supportedBrickWouldFall = 0;
				last;
			}
		}

		if ($supportedBrickWouldFall) {
			TRACE "wouldFall: brick starting to fall %d", $supported;
			$startToFall{$supported}++;
		}
	}

	# Add the newly falling bricks to the already falling ones
	foreach my $newlyFalling (keys %startToFall) {
		$rFallingBricks->{$newlyFalling} ++;
	}
	# Recusively process the newly falling ones
	foreach my $newlyFalling (keys %startToFall) {
		&wouldFall($rBricks, $newlyFalling, $rFallingBricks);
	}
}

########
# Part 1

sub canDisintegrate {
	my $rBricks = shift;
	my $brick = shift;

	# Brick can savely be disintegrated if it doesn't support any other bricks...
	if (scalar keys %{$brick->{SUPPORTS}} == 0) {
		TRACE "canDisintegrate: %d ok, supports nothing", $brick->{NR};
		return 1;
	}

	# ...or if the ones it supports have more than one supporters
	foreach my $supported (keys %{$brick->{SUPPORTS}}) {
		if (scalar keys %{$rBricks->{$supported}{ISSUPPORTEDBY}} == 1) {
			# Current brick is the only support for it, cannot disintegrate
			TRACE "canDisintegrate: %d nok, is single support for %d", $brick->{NR}, $rBricks->{$supported}{NR};
			return 0;
		}
	}
	TRACE "canDisintegrate: %d ok, supports nothing which isn't supported elsewhere", $brick->{NR};
	return 1;
}

sub bricksSupporting {
	my $rBricks = shift;
	my $rAir = shift;

	DEBUG "bricksSupporting: wire bricks together: brick is supporting / supported by";
	my %otherBricksUnderneath;
	my %otherBricksAbove;

	foreach my $brick (values %$rBricks) {
		TRACE "bricksSupporting: checking %d", $brick->{NR};

		foreach my $cube (@{$brick->{CUBES}}) {
			if ($cube->z() > 1) {
				my $cubeUnderneath = $cube->add(XY::XYZ::down());
				if (exists $rAir->{$cubeUnderneath->toString()} && $rAir->{$cubeUnderneath->toString()} != $brick->{NR}) {
					$brick->{ISSUPPORTEDBY}{$rAir->{$cubeUnderneath->toString()}} ++;
				}
			}

			my $cubeAbove = $cube->add(XY::XYZ::up());
			if (exists $rAir->{$cubeAbove->toString()} && $rAir->{$cubeAbove->toString()} != $brick->{NR}) {
				$brick->{SUPPORTS}{$rAir->{$cubeAbove->toString()}} ++;
			}
		}
		#print "DEBUG ISSUPPORTEDBY: ", Dumper ($brick->{ISSUPPORTEDBY});
		#print "DEBUG SUPPORTS: ", Dumper ($brick->{SUPPORTS});
	}
	return 0;
}

sub bricksFall {
	#my $rTower = shift;
	my $rBricks = shift;
	my $rAir = shift;

	DEBUG "bricksFall: Move free floating bricks down until everything is settled";
	my $nrOfMoves = 0;

	# All bricks: move it one down if no aircube underneath is occupied (except by itself :-)
	# Stop when no more bricks are moving
	my $bricksMoved = 1;
	while ($bricksMoved) {
		$bricksMoved = 0;

		# Put the bricks in a priority queue: move lowest bricks first (instead of just going through them randomly)
		# This brings the 'moves until settled' down to 1276 (from 80318 with single step moves, then 38466 with optimized move-as-far-as-possible)
		my $bricksList = new List::PriorityQueue;
		map { $bricksList->update($_, $_->{C1z})} values %$rBricks;

		while (my $brick = $bricksList->pop()) {
			TRACE "bricksFall: try to move %d %s", $brick->{NR}, brickStr($brick);
			my $brickCanMoveN = 999999;
			
			# Check out every cube of the brick individually
			foreach my $cube (@{$brick->{CUBES}}) {
				if ($cube->z() == 1) {
					# This brick has one cube at ground level
					$brickCanMoveN = 0;
					last;
				}
				
				my $cubeUnderneath = $cube->add(XY::XYZ::down());
				my $cubeCanMoveN = 0;
				while (!(exists $rAir->{$cubeUnderneath->toString()} && $rAir->{$cubeUnderneath->toString()} != $brick->{NR})) {
					#TRACE "bricksFall: brick %4d %s has cube %s. Underneath is %s", $brick->{NR}, brickStr($brick), $cube->toString(), $cubeUnderneath->toString();
					$cubeCanMoveN++;
					last if ($cubeCanMoveN >= $brickCanMoveN);
					$cubeUnderneath = $cubeUnderneath->add(XY::XYZ::down());
					last if ($cubeUnderneath->z() == 0)
				}
				#TRACE "bricksFall: brick %4d %s has cube %s. It can move %d down", $brick->{NR}, brickStr($brick), $cubeUnderneath->toString(), $cubeCanMoveN;
				$brickCanMoveN = min($brickCanMoveN, $cubeCanMoveN);
				last if ($brickCanMoveN == 0);
			}

			next unless ($brickCanMoveN > 0);

			# We can move this brick down N levels: create a new list of cubes for this brick after the move
			my @newCubes;
			foreach my $cube (@{$brick->{CUBES}}) {
				delete $rAir->{$cube->toString()}; # remove the old cube from space
				push @newCubes, $cube->add(XY::XYZ::down()->mult($brickCanMoveN));
			}
			$brick->{CUBES} = \@newCubes;
			foreach my $cube (@{$brick->{CUBES}}) {
				$rAir->{$cube->toString()} = $brick->{NR}; # add new cube to space
			}
			$brick->{C1z} -= $brickCanMoveN;
			$brick->{C2z} -= $brickCanMoveN;
			TRACE "bricksFall: brick %4d has moved down %d -> %s", $brick->{NR}, $brickCanMoveN, brickStr($brick);

			$bricksMoved = 1;
			$nrOfMoves ++;
		}
	}
	return $nrOfMoves;
}

sub placeBrickInAir {
	my $rAir = shift;
	my $brick = shift;
	TRACE "placeBrickInAir %d: %s", $brick->{NR}, &brickStr($brick);

	my @cubes = ();

	for (my $z = $brick->{C1z}; $z <= $brick->{C2z}; $z++) {
		for (my $x = $brick->{C1x}; $x <= $brick->{C2x}; $x++) {
			for (my $y = $brick->{C1y}; $y <= $brick->{C2y}; $y++) {
				my $cube = XYZ($x, $y, $z);
				push @cubes, XYZ($x, $y, $z);
				die "Air volume for brick " . $brick->{NR} . " already occupied by another brick" if (exists $rAir->{$cube->toString()} );
				$rAir->{$cube->toString()} = $brick->{NR};
			}
		}
	}
	$brick->{CUBES} = \@cubes;
	#die "Brick volume != nr of cubes in brick" unless (scalar @cubes == ($brick->{C2x}-$brick->{C1x} + 1) * ($brick->{C2y}-$brick->{C1y} + 1) * ($brick->{C2z}-$brick->{C1z} + 1));
}

# DEBUG helper
sub brickStr {
	my $brick = shift;
	return sprintf "[%d-%d-%d/%d-%d-%d] d(xyz) (%d-%d-%d) V %d",
		$brick->{C1x}, $brick->{C1y}, $brick->{C1z},
		$brick->{C2x}, $brick->{C2y}, $brick->{C2z},
		$brick->{C2x}-$brick->{C1x} + 1,
		$brick->{C2y}-$brick->{C1y} + 1,
		$brick->{C2z}-$brick->{C1z} + 1,
		($brick->{C2x}-$brick->{C1x} + 1) * ($brick->{C2y}-$brick->{C1y} + 1) * ($brick->{C2z}-$brick->{C1z} + 1);
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 22: Sand Slabs ---

Enough sand has fallen; it can finally filter water for Snow Island.

Well, almost.

The sand has been falling as large compacted bricks of sand, piling up to form an impressive stack here near the edge of Island Island. In order to make use of the sand to filter water, some of the bricks will need to be broken apart - nay, disintegrated - back into freely flowing sand.

The stack is tall enough that you'll have to be careful about choosing which bricks to disintegrate; if you disintegrate the wrong brick, large portions of the stack could topple, which sounds pretty dangerous.

The Elves responsible for water filtering operations took a snapshot of the bricks while they were still falling (your puzzle input) which should let you work out which bricks are safe to disintegrate. For example:

1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
Each line of text in the snapshot represents the position of a single brick at the time the snapshot was taken. The position is given as two x,y,z coordinates - one for each end of the brick - separated by a tilde (~). Each brick is made up of a single straight line of cubes, and the Elves were even careful to choose a time for the snapshot that had all of the free-falling bricks at integer positions above the ground, so the whole snapshot is aligned to a three-dimensional cube grid.

A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate - in other words, that the brick is a single cube.

Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in volume, both oriented horizontally. The first brick extends in the x direction, while the second brick extends in the y direction.

A line like 0,0,1~0,0,10 represents a ten-cube brick which is oriented vertically. One end of the brick is the cube located at 0,0,1, while the other end of the brick is located directly above it at 0,0,10.

The ground is at z=0 and is perfectly flat; the lowest z value a brick can have is therefore 1. So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are both resting on the ground, but 3,3,2~3,3,3 was above the ground at the time of the snapshot.

Because the snapshot was taken while the bricks were still falling, some bricks will still be in the air; you'll need to start by figuring out where they will end up. Bricks are magically stabilized, so they never rotate, even in weird situations like where a long horizontal brick is only supported on one end. Two bricks cannot occupy the same position, so a falling brick will come to rest upon the first other brick it encounters.

Here is the same example again, this time with each brick given a letter so it can be marked in diagrams:

1,0,1~1,2,1   <- A
0,0,2~2,0,2   <- B
0,2,3~2,2,3   <- C
0,0,4~0,2,4   <- D
2,0,5~2,2,5   <- E
0,1,6~2,1,6   <- F
1,1,8~1,1,9   <- G
At the time of the snapshot, from the side so the x axis goes left to right, these bricks are arranged like this:

 x
012
.G. 9
.G. 8
... 7
FFF 6
..E 5 z
D.. 4
CCC 3
BBB 2
.A. 1
--- 0
Rotating the perspective 90 degrees so the y axis now goes left to right, the same bricks are arranged like this:

 y
012
.G. 9
.G. 8
... 7
.F. 6
EEE 5 z
DDD 4
..C 3
B.. 2
AAA 1
--- 0
Once all of the bricks fall downward as far as they can go, the stack looks like this, where ? means bricks are hidden behind other bricks at that location:

 x
012
.G. 6
.G. 5
FFF 4
D.E 3 z
??? 2
.A. 1
--- 0
Again from the side:

 y
012
.G. 6
.G. 5
.F. 4
??? 3 z
B.C 2
AAA 1
--- 0
Now that all of the bricks have settled, it becomes easier to tell which bricks are supporting which other bricks:

Brick A is the only brick supporting bricks B and C.
Brick B is one of two bricks supporting brick D and brick E.
Brick C is the other brick supporting brick D and brick E.
Brick D supports brick F.
Brick E also supports brick F.
Brick F supports brick G.
Brick G isn't supporting any bricks.
Your first task is to figure out which bricks are safe to disintegrate. A brick can be safely disintegrated if, after removing it, no other bricks would fall further directly downward. Don't actually disintegrate any bricks - just determine what would happen if, for each brick, only that brick were disintegrated. Bricks can be disintegrated even if they're completely surrounded by other bricks; you can squeeze between bricks if you need to.

In this example, the bricks can be disintegrated as follows:

Brick A cannot be disintegrated safely; if it were disintegrated, bricks B and C would both fall.
Brick B can be disintegrated; the bricks above it (D and E) would still be supported by brick C.
Brick C can be disintegrated; the bricks above it (D and E) would still be supported by brick B.
Brick D can be disintegrated; the brick above it (F) would still be supported by brick E.
Brick E can be disintegrated; the brick above it (F) would still be supported by brick D.
Brick F cannot be disintegrated; the brick above it (G) would fall.
Brick G can be disintegrated; it does not support any other bricks.
So, in this example, 5 bricks can be safely disintegrated.

Figure how the blocks will settle based on the snapshot. Once they've settled, consider disintegrating a single brick; how many bricks could be safely chosen as the one to get disintegrated?

Your puzzle answer was 424.

--- Part Two ---

Disintegrating bricks one at a time isn't going to be fast enough. While it might sound dangerous, what you really need is a chain reaction.

You'll need to figure out the best brick to disintegrate. For each brick, determine how many other bricks would fall if that brick were disintegrated.

Using the same example as above:

Disintegrating brick A would cause all 6 other bricks to fall.
Disintegrating brick F would cause only 1 other brick, G, to fall.
Disintegrating any other brick would cause no other bricks to fall. So, in this example, the sum of the number of other bricks that would fall as a result of disintegrating each brick is 7.

For each brick, determine how many other bricks would fall if that brick were disintegrated. What is the sum of the number of other bricks that would fall?

Your puzzle answer was 55483.

Both parts of this puzzle are complete! They provide two gold stars: **

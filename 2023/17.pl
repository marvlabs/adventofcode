#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 7h ?
# RESULT [Puzzle 2023/17]: PART1 [1244] - PART2 [1367] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use List::PriorityQueue;
use AOC qw(DEBUG TRACE INFO PROGRESS BOARD BOARD_PAUSE);
use XY::Board;
use XY::XY qw(XY);
$AOC::NAME = "Clumsy Crucible: Path optmize";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 500;
$AOC::LEARNED = "Graph, Dijkstra";
#########################
# Init	
my $year = "2023";
my $puzzle = "17";

my @Tests;
push @Tests, { NAME => 'Crucible-102', RESULT1 => 102, RESULT2 => 94, INPUT  => << 'EOEX',
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
EOEX
};

push @Tests, { NAME => 'Ultracrucible-94', RESULT1 => 59, RESULT2 => 71, INPUT  => << 'EOEX',
111111111111
999999999991
999999999991
999999999991
999999999991
EOEX
};

##################################
my $MaxStep = 3;
my $MinStepUltra = 4;
my $MaxStepUltra = 10;
my $MaxVal = 9999;
my $BaseLine;
my $Target;

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	##### Parse input
	my $boardstr;
	my $boardY;
	my $boardX;
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		$boardstr .= $_;
		$boardX = length $boardstr unless($boardX);
		$boardY++;
	}

	# Set up field
	my $board = XY::Board->new($boardX, $boardY);
	$board->setTiles($boardstr);

	#binmode(STDOUT, ":encoding(UTF-8)");
	#DEBUG "Parse: Board [%d/%d]\n%s", $boardX, $boardY, $board->toString();

		##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		# My depth first recursion probably still runs on one core...
		# Not even close, and certainly no cigar :-(
		#$BaseLine = &getSimpleBaseline($board);
		#$Target = XY($board->getSizeX()-1, $board->getSizeY()-1);
		#my $start = XY(0,0);
		#my %seen;
		#my $movesE = &optimizePath($board, $start, 'E', 0, $MaxStep, \%seen, 0);
		#my $movesS = &optimizePath($board, $start, 'S', 0, $MaxStep, \%seen, 0);
		#$p1_result = min ($movesE, $movesS);

		my $guiBoard = $board->duplicate();
		$AOC::BOARD_LAG = 0;
		BOARD $guiBoard;
		$AOC::BOARD_LAG = 0;
		#&dijkstraOptimize($board, $MinStepUltra, $MaxStepUltra); # use the more general ULTRA optimizer, works also for part 1
		$p1_result = &dijkstraOptimizeUltra($board, 1, $MaxStep, $guiBoard);
		INFO "*** Part 1 -> [%d]", $p1_result;
		BOARD_PAUSE 1;
		#sleep 3;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		my $guiBoard = $board->duplicate();
		$AOC::BOARD_LAG = 0;
		BOARD $guiBoard;
		$AOC::BOARD_LAG = 0;
		$p2_result = &dijkstraOptimizeUltra($board, $MinStepUltra, $MaxStepUltra, $guiBoard);
		INFO "*** Part 2 -> [%d]", $p2_result;
		BOARD_PAUSE 1
	}

	##### RESULTS #####
	# 1244 1367
	return ($p1_result, $p2_result);
}


### Part 2

my %DirBack = (
	N => 'S',
	E => 'W',
	S => 'N',
	W => 'E',
);

# Implement a Dijkstra with the boundary conditions of the puzzle:
# Make nodes for every direction we can come land on a field
sub dijkstraOptimizeUltra {
	my $board = shift;
	my $minMoves = shift;
	my $maxMoves = shift;
	my $guiBoard = shift;

	# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
	my %nodes;	# Unvisited nodes
	my %path; 	# Visited nodes
	my $distances = new List::PriorityQueue;	# Easy way to keep track of the next minimal distanc of the unvisited nodes

	# Init values:
	# Generate all possible nodes: key is [x,y]D (direction)
	# The node holds the field, the direction we have when landing on it, the current min value and which field we came from
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $field = XY($x, $y);
			foreach my $dir (qw(N E S W)) {
				my $key = $field->toString() . $dir;
				my %node = (
					FIELD => $field,
					DIR   => $dir,
					VALUE => $MaxVal,
					FROM => "",
				);
				$nodes{$key} = \%node;
				#TRACE "dijkstraOptimize: Node %s value %d", $key, $nodes{$key}->{VALUE};
			}
		}
	}

	# Insert a special target node (without Direction Information - we don't care. We treat the target field as one node)
	my %targetNode = ( FIELD => XY($board->getSizeX()-1, $board->getSizeY()-1), VALUE => $MaxVal);
	my $targetNodeKey = $targetNode{FIELD}->toString();
	$nodes{$targetNodeKey} = \%targetNode;

	# Add a start node to get us going
	my %startNode = ( 
		FIELD => XY(0,0), 
		VALUE => 0,
		DIR   => '',
		FROM => XY(-1,-1),
	);
	my $key = "[0,0]";
	$nodes{$key} = \%startNode;
	
	while ($key) {
		my $node = $nodes{$key};
		DEBUG "dijkstraOptimizeUltra: Checking node %9s (value %d)", $key, $node->{VALUE};

		# Dijkstra: Add this node to the path
		$path{$key} = $node->{VALUE};

		# Dijkstra: Find all reachable nodes from this one
		DIRECTION: foreach my $dir (qw(N E S W)) {
			if ($dir eq $node->{DIR} || $dir eq $DirBack{$node->{DIR}}) {
				TRACE "dijkstraOptimizeUltra: %s Cannot go straight on or turn back '%s'", $key, $dir;
				next;
			}

			# Move in straight line to field before a reachable node: 
			# We need to go at least min and consider max-min nodes from there on
			# Calculate the cost on the way
			my $reachableField = $node->{FIELD};
			my $value = $node->{VALUE};
			for (my $steps = 1; $steps < $minMoves; $steps++) {
				$reachableField = $reachableField->add(XY::XY::aim($dir));
				if (!$board->valid($reachableField)) {
					# Overshoot -> break to next direction
					TRACE "dijkstraOptimizeUltra: %s Out of bounds %s", $key, $reachableField->toString();
					next DIRECTION;
				};
				$value += $board->getAt($reachableField) - ord('0');
			}
			# The next ones need to be checked and calculated if valid
			for (my $steps = $minMoves; $steps <= $maxMoves; $steps++) {
				$reachableField = $reachableField->add(XY::XY::aim($dir));
				if (!$board->valid($reachableField)) {
					TRACE "dijkstraOptimizeUltra: %s Out of bounds %s", $key, $reachableField->toString();
					next DIRECTION;
				};

				$value += $board->getAt($reachableField) - ord('0');

				my $reachableNodeKey;
				if ($reachableField->equal($targetNode{FIELD})) {
					# We reached the target here
					$reachableNodeKey = $targetNodeKey;
				}
				else {
					$reachableNodeKey = $reachableField->toString() . $dir;
				}

				TRACE "dijkstraOptimizeUltra: Node %s is reachable with value %d. Current value %d", $reachableNodeKey, $value, $nodes{$reachableNodeKey}->{VALUE};
				if ($value < $nodes{$reachableNodeKey}->{VALUE}) {
					# Dijkstra: Update this node: we found a cheaper route
					$nodes{$reachableNodeKey}->{VALUE} = $value;
					$nodes{$reachableNodeKey}->{FROM} = $node->{FIELD};

					# Dijkstra: Add / update in priority list (easiest way to determine the next node to visit)
					$distances->update($reachableNodeKey, $value);
					TRACE "dijkstraOptimizeUltra: Node %s value %d", $reachableNodeKey, $value;
				}
			}
		}
		
		# Dijkstra: The next node to visit is the one with the smallest value
		my $nextKey = $distances->pop();
		if ($nextKey eq $targetNodeKey) {
			INFO "dijkstraOptimizeUltra: target %s is the closest remaining node: Value %d", $nextKey, $nodes{$nextKey}->{VALUE};
			return $nodes{$nextKey}->{VALUE};
		}
		$key = $nextKey;
		$guiBoard->setAt($nodes{$key}->{FIELD}, ord('.'));
	}
}


### Part 1

# My first Dijkstra: This implementation for part 1 considered the field, direction and nr of steps as key for nodes
# The above Ultra implementation is more general and can replace this one.
# Left in for the history of it :)
sub dijkstraOptimize {
	my $board = shift;

	my %nodes;
	my %path;
	my $distances = new List::PriorityQueue;

	# Init values
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		for (my $y = 0; $y < $board->getSizeY(); $y++) {
			my $field = XY($x, $y);
			foreach my $dir (qw(N E S W)) {
				for (my $steps = 1; $steps <= $MaxStep; $steps++) {
					my $key = $field->toString() . $dir . $steps;
					my %node = (
						FIELD => $field,
						DIR   => $dir,
						STEP  => $steps,
						VALUE => $MaxVal,
						FROM => "",
					);
					$nodes{$key} = \%node;
					#TRACE "dijkstraOptimize: Node %s value %d", $key, $nodes{$key}->{VALUE};
				}
			}
		}
	}

	my %targetNode = ( FIELD => XY($board->getSizeX()-1, $board->getSizeY()-1), VALUE => $MaxVal);
	my $targetNodeKey = $targetNode{FIELD}->toString();
	$nodes{$targetNodeKey} = \%targetNode;

	my %startNode = ( 
		FIELD => XY(0,0), 
		VALUE => 0,
		DIR   => '',
		STEP  => 0,
		FROM => XY(-1,-1),
	);


	my $key = "[0,0]";
	$nodes{$key} = \%startNode;

	while ($key) {
		my $node = $nodes{$key};
		DEBUG "dijkstraOptimize: Checking node %s (field %s)", $key, $node->{FIELD}->toString();

		# Add this node to the path
		$path{$key} = $node->{VALUE};

		# Find all reachable nodes from this one
		foreach my $dir (qw(N E S W)) {
			my $step = $node->{STEP};
			if ($dir eq $node->{DIR}) {
				$step++;
				if ($step > $MaxStep) { 
					TRACE "dijkstraOptimize: %s Cannot go on '%s' any more, max step limit reached", $key, $dir;
					next;
				}
			}
			else {
				$step = 1;
			}
						
			my $reachableField = $node->{FIELD}->add(XY::XY::aim($dir));

			if (!$board->valid($reachableField)) {
				TRACE "dijkstraOptimize: %s Out of bounds %s", $key, $reachableField->toString();
				next;
			};

			if ($node->{FROM}->equal($reachableField)) {
				TRACE "dijkstraOptimize: %s Cannot turn around %s", $key, $reachableField->toString();
				next;
			}

			my $value = $node->{VALUE} + $board->getAt($reachableField) - ord('0');

			my $reachableNodeKey;
			if ($reachableField->equal($targetNode{FIELD})) {
				# We reached the target here
				$reachableNodeKey = $targetNodeKey;
			}
			else {
			 $reachableNodeKey = $reachableField->toString() . $dir . $step;
			}

			TRACE "dijkstraOptimize: Node %s is reachable with value %d. Current value %d", $reachableNodeKey, $value, $nodes{$reachableNodeKey}->{VALUE};
			if ($value < $nodes{$reachableNodeKey}->{VALUE}) {
				# Update this node: it's cheaper from here
				$nodes{$reachableNodeKey}->{VALUE} = $value;
				$nodes{$reachableNodeKey}->{FROM} = $node->{FIELD};

				# Add / update in priority list
				$distances->update($reachableNodeKey, $value);
				TRACE "dijkstraOptimize: Node %s value %d", $reachableNodeKey, $value;
			}
		}
		
		my $nextKey = $distances->pop();
		if ($nextKey eq $targetNodeKey) {
			INFO "dijkstraOptimize: target %s is the closest remaining node: Value %d", $nextKey, $nodes{$nextKey}->{VALUE};
			return $nodes{$nextKey}->{VALUE};
		}
		$key = $nextKey;
	}
}

######################
# Depth first recursion:
# Doesn't work -> toooooo slow
# Well, was worth a try
# my %LR = (
# 	ER => 'S',
# 	EL => 'N',
# 	SL => 'E',
# 	SR => 'W',
# 	WL => 'S',
# 	WR => 'N',
# 	NL => 'W',
# 	NR => 'E',
# );

# sub optimizePath {
# 	my $board = shift;
# 	my $field = shift;
# 	my $dir = shift;
# 	my $moves = shift;
# 	my $movesInDir = shift;
# 	my $rSeen = shift;
# 	my $sum = shift;

# 	DEBUG "optimizeBoard: %s %s (%d moves), sum [%d]", $field->toString(), $dir, $moves, $sum;

# 	$field = $field->add(XY::XY::aim($dir));
# 	return $MaxVal unless $board->valid($field);
# 	$moves++;

# 	$sum += $board->getAt($field) - ord('0');

# 	if ($field->equal($Target)) {
# 		INFO "optimizeBoard: Target reached at cost: %d", $sum;
# 		$BaseLine = $sum if ($sum < $BaseLine);
# 		return $sum;
# 	}


# 	if ($sum + 3 * $field->manhattanDist($Target) - 20 >= $BaseLine) {
# 		#DEBUG "optimizeBoard: %s Path & distance [%d] is over the base line", $field->toString(), $sum + $field->manhattanDist($Target);
# 		return $MaxVal
# 	}
# 	if ($sum >= $BaseLine) {
# 	 	#DEBUG "optimizeBoard: Path [%d] is over the base line", $sum;
# 	 	return $MaxVal
# 	 }


# 	if ($moves > 2* ($field->x()+$field->y())) {
# 		#DEBUG "optimizeBoard: %s took to many moves (%d)", $field->toString(), $moves;
# 		return $MaxVal
# 	}


# 	# Check that we haven't hit this field cheaper already, from the same side with the same nr of dirs left
# 	my $seenKey = $field->toString() . $dir . $movesInDir;
# 	#TRACE "optimizeBoard: %s %s, sum [%d] -> key [%s]", $field->toString(), $dir, $sum, $seenKey;
# 	if (exists $rSeen->{$seenKey}) {
# 		#TRACE "optimizeBoard: %s %s, sum [%d] -> key exists [%s]", $field->toString(), $dir, $sum, $seenKey;
# 		return $MaxVal if ($sum > $rSeen->{$seenKey}{SUM});
# 		$rSeen->{$seenKey}{SUM} = $sum;
# 		$rSeen->{$seenKey}{MOVES} = $movesInDir
# 	}
# 	else {
# 		$rSeen->{$seenKey}{SUM} = $sum;
# 		$rSeen->{$seenKey}{MOVES} = $movesInDir
# 	}

# 	# Three possibilities -> straight on, R, L
# 	my ($resultDir, $resultR, $resultL) = ($MaxVal) x 3;

# 	# Try to favor a direct path:
# 	if ($dir eq 'E') {
# 		$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 		if ($movesInDir < $MaxStep-1) {
# 			$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 		}
# 		$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 	}
# 	elsif ($dir eq 'S') {
# 		$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 		if ($movesInDir < $MaxStep-1) {
# 			$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 		}
# 		$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 	}
# 	elsif ($dir eq 'N') {
# 		$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 		$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 		if ($movesInDir < $MaxStep-1) {
# 			$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 		}
# 	}
# 	elsif ($dir eq 'W') {
# 		$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 		$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 		if ($movesInDir < $MaxStep-1) {
# 			$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 		}
# 	}

# 	# # Try to favor a left edge first path:
# 	# if ($dir eq 'E') {
# 	# 	$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 	# 	if ($movesInDir < $MaxStep-1) {
# 	# 		$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 	# 	}
# 	# 	$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 	# }
# 	# elsif ($dir eq 'S') {
# 	# 	if ($movesInDir < $MaxStep-1) {
# 	# 		$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 	# 	}
# 	# 	$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 	# 	$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 	# }
# 	# elsif ($dir eq 'N') {
# 	# 	$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 	# 	$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 	# 	if ($movesInDir < $MaxStep-1) {
# 	# 		$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 	# 	}
# 	# }
# 	# elsif ($dir eq 'W') {
# 	# 	$resultL = optimizePath($board, $field, $LR{$dir.'L'}, $moves, 0, $rSeen, $sum);
# 	# 	if ($movesInDir < $MaxStep-1) {
# 	# 		$resultDir = optimizePath($board, $field, $dir, $moves, $movesInDir+1, $rSeen, $sum);
# 	# 	}
# 	# 	$resultR = optimizePath($board, $field, $LR{$dir.'R'}, $moves, 0, $rSeen, $sum);
# 	# }


# 	return min($resultDir, $resultR, $resultL);
# }


# sub getSimpleBaseline {
# 	my $board = shift;
# 	my $field = XY(0,0);
# 	my $sum = 0;

# 	# # Go down and right till we reach goal
# 	# while (!$field->equal($Target)) {
# 	# 	$field = $field->add(XY::XY::aim('S'));
# 	# 	$sum += $board->getAt($field) - ord('0');
# 	# 	TRACE "getSimpleBaseline: S %s -> %d", $field->toString(), chr($board->getAt($field));

# 	# 	$field = $field->add(XY::XY::aim('E'));
# 	# 	$sum += $board->getAt($field) - ord('0');
# 	# 	TRACE "getSimpleBaseline: E %s -> %d", $field->toString(), chr($board->getAt($field));
# 	# }
	
# 	# Down, then right
# 	for (my $y = 0; $y < $board->getSizeY()-1; $y++) {
# 		$field = $field->add(XY::XY::aim('S'));
# 		$sum += $board->getAt($field) - ord('0');
# 	}
# 	for (my $x = 0; $x < $board->getSizeX()-1; $x++) {
# 		$field = $field->add(XY::XY::aim('E'));
# 		$sum += $board->getAt($field) - ord('0');
# 	}
# 	$sum = 1300; 
# 	INFO "getSimpleBaseline: TARGET %s -> %d", $field->toString(), $sum;
# 	return $sum+20;
# }

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 17: Clumsy Crucible ---

The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?

Your puzzle answer was 1244.

--- Part Two ---

The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example:

111111111111
999999999991
999999999991
999999999991
999999999991
Sadly, an ultra crucible would need to take an unfortunate path like this one:

1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what is the least heat loss it can incur?

Your puzzle answer was 1367.

Both parts of this puzzle are complete! They provide two gold stars: **

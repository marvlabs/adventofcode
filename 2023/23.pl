#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 5h
# RESULT [Puzzle 2023/23]: PART1 [94] - PART2 [6230]
 ###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use List::Util qw (min max);
use Storable 'dclone';
use XY::Board;
use XY::XY qw(XY);
use Data::Dumper;
use AOC qw(DEBUG INFO TRACE);
$AOC::NAME = "A Long Walk: Maxing out again";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 300;
$AOC::LEARNED = "Optimize by using Graph (Nodes, Edges)";
#########################
# Init	
my $year = "2023";
my $puzzle = "23";

my @Tests;
push @Tests, { NAME => 'Sloap Walk', RESULT1 => 94, RESULT2 => 154, INPUT  => << 'EOEX',
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
EOEX
};
##################################
my $EMPTY = ord '.';
my $ROCK  = ord '#';
my $SEEN  = ord 'O';
my $N = ord '^';
my $E = ord '>';
my $S = ord 'v';
my $W = ord '<';

my %Slope = (
	$S => 'S',
	$E => 'E',
	$N => 'N',
	$W => 'W',
);
my %SlopeOpposite = (
	N => $S,
	E => $W,
	S => $N,
	W => $E,
);
my %Opposite = (
	N => 'S',
	E => 'W',
	S => 'N',
	W => 'E',
);

# EVIL GLOBALS for output info
my $CURRENTLONGEST = 0;
my $SOLUTIONSFOUND = 0;

###################
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
	binmode(STDOUT, ":encoding(UTF-8)");
	DEBUG "Parse: Board [%d/%d]\n%s", $boardX, $boardY, $board->toString();

	# Start and end currentNode
	my $start = XY(1,0);
	my $end = XY($boardX-2, $boardY-1);

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		$CURRENTLONGEST = 0;
		$SOLUTIONSFOUND = 0;

		INFO "*** Part 1 running ***";
		$p1_result = &walkBoard($board, $start, $end, 0);
		INFO "Part 1: Checked %d possible routes. The longest takes %s steps", $SOLUTIONSFOUND, $p1_result;
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";
		$CURRENTLONGEST = 0;
		$SOLUTIONSFOUND = 0;

		# Remove slopes from input
		my $nonSteepBoard = $board->duplicate();
		for(my $x = 0; $x < $nonSteepBoard->getSizeX(); $x++) {
			for(my $y = 0; $y < $nonSteepBoard->getSizeY(); $y++) {
				next if ($nonSteepBoard->is(XY($x, $y), $EMPTY) || $nonSteepBoard->is(XY($x, $y), $ROCK));
				$nonSteepBoard->setAt(XY($x, $y), $EMPTY);
			}
		}

		# Build a node tree
		my %Nodes;
		&findNodesAndEdges ($nonSteepBoard, \%Nodes, $start, $end);
		TRACE "Part 2: Board after nodes scanning\n%s", $nonSteepBoard->toString();
		INFO "Part 2: Found %d nodes ,%d edges", scalar keys %Nodes, scalar map { keys %{$Nodes{$_}} } keys %Nodes;

		$p2_result = &walkNodes(\%Nodes, $start->toString(), $end->toString(), {}, 0);
		INFO "Part 2: Checked %d possible routes. The longest takes %s steps", $SOLUTIONSFOUND, $p2_result;
		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 1930 6230
	return ($p1_result, $p2_result);
}

# Part 2: Turn the walking problem into a graph. 
# - Every junction is a node
# - Edges are the number of steps from node to node if directly reachable
# - Find all possible paths from start to end, keep the longest

# Check out all paths from currentNode to target.
# Use a 'seen' hash to make sure we don't double back
# Return the max path till target for every recursion
sub walkNodes {
	my $rNodes = shift;
	my $currentNode = shift;
	my $target = shift;
	my $rSeen = shift;
	my $steps = shift;

	$rSeen->{$currentNode} = $steps; # Could be used to backtrack by ordering the values, if relevant

	my @exploreNext;
	foreach my $reachableNode (keys %{$rNodes->{$currentNode}}) {
		next if (exists $rSeen->{$reachableNode});
		TRACE "walkNodes %s can reach %s in %d", $currentNode, $reachableNode, $rNodes->{$currentNode}{$reachableNode};
		push @exploreNext, $reachableNode;
	}
	
	return 0 unless @exploreNext; # Hit a dead end, all reachable nodes already visited

	my @solutions;
	foreach my $nextNode (@exploreNext) {
		if ($nextNode eq $target) {
			TRACE "walkNodes %s has reached target %s in %d", $currentNode, $nextNode, $steps + $rNodes->{$currentNode}{$nextNode};
			push @solutions,  $steps + $rNodes->{$currentNode}{$nextNode};
			$SOLUTIONSFOUND++;
		}
		else {
			my $result = &walkNodes($rNodes, $nextNode, $target, dclone $rSeen, $steps + $rNodes->{$currentNode}{$nextNode});
			push @solutions, $result;
		}
	}

	if (max((@solutions)) > $CURRENTLONGEST) {
		$CURRENTLONGEST = max((@solutions));
		INFO "walkBoard: longest walk is now: %d", $CURRENTLONGEST;
	}
	return max((@solutions));
}

# Walk the board, record all junctions and the nr of steps in between (in both directions)
# (adapted from Part 1 walker below)
sub findNodesAndEdges {
	my $board = shift;
	my $rNodes = shift;
	my $startField = shift;
	my $targetField = shift;
	my $dir = shift;

	TRACE "findNodesAndEdges: New Edge from %s", $startField->toString();
	my $field = $startField;
	my $lastDir;
	my $steps = 0;

	if ($dir) {
		# Move away from node, if not first call
		my $nextPos = $field->add(XY::XY::aim($dir));
		$lastDir = $dir;
		$field = $nextPos;
		$steps++;
		return if ($board->is($field, $SEEN)); # Already explored from the other direction
	}

	while (1) {
		TRACE "findNodesAndEdges: Positon %s", $field->toString();
		$board->setAt($field, $SEEN);

		if ($field->equal($targetField)) {
			INFO "findNodesAndEdges: Target reached. %s -> %s %d steps", $startField->toString(), $field->toString(), $steps;
			$rNodes->{$field->toString()}{$startField->toString()} = $steps;
			$rNodes->{$startField->toString()}{$field->toString()} = $steps;
			return;
		}

		my $rNeighbours = $board->directNeighbours($field);
		delete $rNeighbours->{$Opposite{$lastDir}} if $lastDir; # Remove where we came from, don't need to check backwards

		my @possibleDirs;
		foreach my $dir (keys %$rNeighbours) {
			next if ($rNeighbours->{$dir} eq $ROCK);

			if ($rNeighbours->{$dir} eq $SEEN) {
				my $node = $field->add(XY::XY::aim($dir));
				DEBUG "findNodesAndEdges: Known node '%s'. %s -> %s %d steps", $dir, $startField->toString(), $node->toString(), $steps+1;
				$rNodes->{$node->toString()}{$startField->toString()} = $steps+1;
				$rNodes->{$startField->toString()}{$node->toString()} = $steps+1;
			}
			else {
				push @possibleDirs, $dir;
			}
		}

		if (scalar @possibleDirs > 1) {
			# Junction found: record the edge...
			DEBUG "findNodesAndEdges: New node found. %s -> %s %d steps", $startField->toString(), $field->toString(), $steps;
			$rNodes->{$field->toString()}{$startField->toString()} = $steps;
			$rNodes->{$startField->toString()}{$field->toString()} = $steps;

			# ... then split into n recursive calls
			map { &findNodesAndEdges($board, $rNodes, $field, , $targetField, $_)} @possibleDirs;
			TRACE "findNodesAndEdges: Return from (%d) split %s", scalar @possibleDirs, $field->toString();
			return;
		}

		# Move on to next field
		my $nextDir = pop @possibleDirs;
		if (! $nextDir) {
			TRACE "findNodesAndEdges: Cannot find next dir from %s", $field->toString();
			return -1;
		}
		my $nextPos = $field->add(XY::XY::aim($nextDir));
		$lastDir = $nextDir;
		TRACE "findNodesAndEdges: %s dir %s -> %s", $field->toString(), $nextDir, $nextPos->toString();
		$field = $nextPos;
		$steps++;
	}
}


########
# Part 1: really walk the board. Works because of the one-way slopes -> many unidirectional junctions, way less recursions
# (To slow for part 2 where all edges are bi-directional.)
# Walk: create copy of the board, walk to next junction,  add steps
# split off into two new walks on junction, return max of both
# return when end, return max steps
sub walkBoard() {
	my $inputBoard = shift;
	my $field = shift;
	my $end = shift;
	my $steps = shift;

	TRACE "walkBoard: New Path from %s", $field->toString();

	my $board = $inputBoard->duplicate();
	my $startField = $field;
	my $lastDir;
	
	while (!$field->equal($end)) {
		TRACE "walkBoard: Positon %s", $field->toString();

		my $nextDir;

		if (! $board->is($field, $EMPTY)) {
			$nextDir = $Slope{$board->getAt($field)};
			TRACE "walkBoard: standing on slope %s, dir is %s", $field->toString(), $nextDir;
			$board->setAt($field, $SEEN);
		}
		
		else {
			$board->setAt($field, $SEEN);

			my $rNeighbours = $board->directNeighbours($field);
			delete $rNeighbours->{$Opposite{$lastDir}} if $lastDir; # Remove where we came from

			my @possibleDirs;
			foreach my $dir (keys %$rNeighbours) {
				next if ($rNeighbours->{$dir} eq $ROCK);
				next if ($rNeighbours->{$dir} eq $SEEN);
				next if ($rNeighbours->{$dir} eq $SlopeOpposite{$dir});
				push @possibleDirs, $dir;
			}
			if (scalar @possibleDirs > 1) {
				my @walks = map { &walkBoard($board, $field->add(XY::XY::aim($_)), $end, $steps+1 )} @possibleDirs;
				TRACE "walkBoard: Return from (%d) split %s -> %s", scalar @possibleDirs, $field->toString(), join ('-' , @walks);
				if (max((@walks)) > $CURRENTLONGEST) {
					$CURRENTLONGEST = max((@walks));
					INFO "walkBoard: longest walk is now: %d", $CURRENTLONGEST;
				}
				return max((@walks));
			}
			$nextDir = pop @possibleDirs;
		}

		if (! $nextDir) {
			TRACE "walkBoard: Cannot find next dir from %s", $field->toString();
			return -1;
		}

		my $nextPos = $field->add(XY::XY::aim($nextDir));
		$lastDir = $nextDir;
		TRACE "walkBoard: %s dir %s -> %s", $field->toString(), $nextDir, $nextPos->toString();
		$field = $nextPos;
		$steps++;
	}

	if ($steps > $CURRENTLONGEST) {
		$CURRENTLONGEST = $steps;
		INFO "walkBoard: longest walk is now: %d", $CURRENTLONGEST;
	}
	$SOLUTIONSFOUND++;
	return $steps;
}

############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 23: A Long Walk ---

The Elves resume water filtering operations! Clean water starts flowing over the edge of Island Island.

They offer to help you go over the edge of Island Island, too! Just hold on tight to one end of this impossibly long rope and they'll lower you down a safe distance from the massive waterfall you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's being absorbed by the air itself. It looks like you'll finally have a little downtime while the moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow; why not take a walk?

There's a map of nearby hiking trails (your puzzle input) that indicates paths (.), forest (#), and steep slopes (^, >, v, and <).

For example:

#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
You're currently on the single path tile in the top row; your goal is to reach the single path tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite icy; if you step onto a slope tile, your next step must be downhill (in the direction the arrow is pointing). To make sure you have the most scenic hike possible, never step onto the same tile twice. What is the longest hike you can take?

In the example above, the longest hike you can take is marked with O, and your starting position is marked S:

#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#
This hike contains 94 steps. (The other possible hikes you could have taken were 90, 86, 82, 82, and 74 steps long.)

Find the longest hike you can take through the hiking trails listed on your map. How many steps long is the longest hike?

Your puzzle answer was 1930.

--- Part Two ---

As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll have no problem climbing up the steep slopes.

Now, treat all slopes as if they were normal paths (.). You still want to make sure you have the most scenic hike possible, so continue to ensure that you never step onto the same tile twice. What is the longest hike you can take?

In the example above, this increases the longest hike to 154 steps:

#S#####################
#OOOOOOO#########OOO###
#######O#########O#O###
###OOOOO#.>OOO###O#O###
###O#####.#O#O###O#O###
###O>...#.#O#OOOOO#OOO#
###O###.#.#O#########O#
###OOO#.#.#OOOOOOO#OOO#
#####O#.#.#######O#O###
#OOOOO#.#.#OOOOOOO#OOO#
#O#####.#.#O#########O#
#O#OOO#...#OOO###...>O#
#O#O#O#######O###.###O#
#OOO#O>.#...>O>.#.###O#
#####O#.#.###O#.#.###O#
#OOOOO#...#OOO#.#.#OOO#
#O#########O###.#.#O###
#OOO###OOO#OOO#...#O###
###O###O#O###O#####O###
#OOO#OOO#O#OOO>.#.>O###
#O###O###O#O###.#.#O###
#OOOOO###OOO###...#OOO#
#####################O#
Find the longest hike you can take through the surprisingly dry hiking trails listed on your map. How many steps long is the longest hike?

Your puzzle answer was 6230.

Both parts of this puzzle are complete! They provide two gold stars: **

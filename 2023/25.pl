#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 7h
# RESULT [Puzzle 2023/25]: PART1 [612945] - PART2 [0]
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE);
use List::Util 'shuffle';
use Data::Dumper;
$AOC::NAME = "Snowverload: wiring a lot of parts";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 420;
$AOC::LEARNED = "Graphs again: Karger min cut implementation";
#########################
# Init	
my $year = "2023";
my $puzzle = "25";

my @Tests;
push @Tests, { NAME => 'Test 1', RESULT1 => 54, INPUT  => << 'EOEX',
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
EOEX
};
##################################

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	my %Parts;
	my %Connections;

	##### Parse input
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);

		/(.*): (.*)/;
		foreach my $id (split / /, $2) {
			$Parts{$1}{$id} = 1;
			$Parts{$id}{$1} = 1;
		}
	}

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";

		# Karger min-cut is Monte-Carlo probabilistic: we need several runs to get the min cut with a high probability.
		# Because we know that it is '3' we can trigger on that to stop trying.
		my ($minCut, $n1, $n2) = 0;
		while ($minCut != 3) {
			($minCut, $n1, $n2) = &karger(\%Parts);
		}
		$p1_result = $n1 * $n2;
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "FINITO. It's finally snowing. No part two today :-)";
	}

	##### RESULTS #####
	# 612945 0
	return ($p1_result, $p2_result);
}


#####################################

# https://en.wikipedia.org/wiki/Karger%27s_algorithm
# Monte-Carlo find the min-cut of a graph:
# Contract nodes until only two left, return remaining edges between the two nodes left and the number of nodes on both sides of the min-cut location.
# High probability for min cut, but needs to run several times (until desired 3 found)
sub karger {
	my $rParts = shift;

	# Create Graph: for start every node has one machine part in it
	# As nodes get contracted, parts accumlate in less and less nodes
	# The node uses the part connections as it's inital edges to the other nodes
	my %Graph;
	foreach my $part (keys %$rParts) {
		$Graph{$part}{PARTS}{$part} = $rParts->{$part};
		foreach my $conn (keys %{$rParts->{$part}}) {
			push @{$Graph{$part}{EDGES}}, $conn;
			$Graph{$part}{NAME} = $part;
		}
	}

	# Randomly contract nodes until only two left
 	while (scalar %Graph > 2) {
 		my $nodeTarget   = (shuffle (keys %Graph))[0];
 		my $nodeAbsorbed = (shuffle (@{$Graph{$nodeTarget}{EDGES}}))[0];
	
 	 	TRACE "karger: merge Node %s into  %s", $nodeAbsorbed, $nodeTarget;

 	 	$Graph{$nodeTarget}{NAME} = $Graph{$nodeTarget}{NAME} . "+" . $Graph{$nodeAbsorbed}{NAME};

		# Copy all the parts to the target node
 		foreach my $part (keys %{$Graph{$nodeAbsorbed}{PARTS}}) {
			$Graph{$nodeTarget}{PARTS}{$part} = $Graph{$nodeAbsorbed}{PARTS}{$part};
		}
		# Remove edge to absorbed noded
		@{$Graph{$nodeTarget}{EDGES}} = grep {!/$nodeAbsorbed/} @{$Graph{$nodeTarget}{EDGES}};

		# Copy over the edges from the absorbed node, adjust the edge on the remote end to point to the target node instead the absorbed node
 		foreach my $edge (@{$Graph{$nodeAbsorbed}{EDGES}}) {
 			next if ($edge eq $nodeTarget); # no self loops: don't copy the edge to the target node
 			push @{$Graph{$nodeTarget}{EDGES}}, $edge; # Add connection from absorbed node to target node
			push @{$Graph{$edge}{EDGES}}, $nodeTarget; # Add target node to remote connected node
			@{$Graph{$edge}{EDGES}} = grep {!/$nodeAbsorbed/} @{$Graph{$edge}{EDGES}}; 	# Remove absorbed node from remote connected node
 		}
 		delete $Graph{$nodeAbsorbed};

		#print "karger GRAPH ", Dumper(\%Graph);
 		TRACE "karger: %d parts", scalar keys %Graph;
	}

	my ($node1, $node2) = keys %Graph;
	DEBUG "karger: Result: %3d remaining Edges, %4d / %4d parts", scalar @{$Graph{$node1}{EDGES}}, scalar keys %{$Graph{$node1}{PARTS}}, scalar keys %{$Graph{$node2}{PARTS}};
	return (scalar @{$Graph{$node1}{EDGES}}, scalar keys %{$Graph{$node1}{PARTS}}, scalar keys %{$Graph{$node2}{PARTS}});
}


############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 25: Snowverload ---

Still somehow without snow, you go to the last place you haven't checked: the center of Snow Island, directly below the waterfall.

Here, someone has clearly been trying to fix the problem. Scattered everywhere are hundreds of weather machines, almanacs, communication modules, hoof prints, machine parts, mirrors, lenses, and so on.

Somehow, everything has been wired together into a massive snow-producing apparatus, but nothing seems to be running. You check a tiny screen on one of the communication modules: Error 2023. It doesn't say what Error 2023 means, but it does have the phone number for a support line printed on it.

"Hi, you've reached Weather Machines And So On, Inc. How can I help you?" You explain the situation.

"Error 2023, you say? Why, that's a power overload error, of course! It means you have too many components plugged in. Try unplugging some components and--" You explain that there are hundreds of components here and you're in a bit of a hurry.

"Well, let's see how bad it is; do you see a big red reset button somewhere? It should be on its own module. If you push it, it probably won't fix anything, but it'll report how overloaded things are." After a minute or two, you find the reset button; it's so big that it takes two hands just to get enough leverage to push it. Its screen then displays:

SYSTEM OVERLOAD!

Connected components would require
power equal to at least 100 stars!
"Wait, how many components did you say are plugged in? With that much equipment, you could produce snow for an entire--" You disconnect the call.

You have nowhere near that many stars - you need to find a way to disconnect at least half of the equipment here, but it's already Christmas! You only have time to disconnect three wires.

Fortunately, someone left a wiring diagram (your puzzle input) that shows how the components are connected. For example:

jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
Each line shows the name of a component, a colon, and then a list of other components to which that component is connected. Connections aren't directional; abc: xyz and xyz: abc both represent the same configuration. Each connection between two components is represented only once, so some components might only ever appear on the left or right side of a colon.

In this example, if you disconnect the wire between hfx/pzl, the wire between bvb/cmg, and the wire between nvd/jqt, you will divide the components into two separate, disconnected groups:

9 components: cmg, frs, lhk, lsr, nvd, pzl, qnr, rsh, and rzs.
6 components: bvb, hfx, jqt, ntq, rhn, and xhk.
Multiplying the sizes of these groups together produces 54.

Find the three wires you need to disconnect in order to divide the components into two separate groups. What do you get if you multiply the sizes of these two groups together?

Your puzzle answer was 612945.

--- Part Two ---

You climb over weather machines, under giant springs, and narrowly avoid a pile of pipes as you find and disconnect the three wires.

A moment after you disconnect the last wire, the big red reset button module makes a small ding noise:

System overload resolved!
Power required is now 50 stars.
Out of the corner of your eye, you notice goggles and a loose-fitting hard hat peeking at you from behind an ultra crucible. You think you see a faint glow, but before you can investigate, you hear another small ding:

Power required is now 49 stars.

Please supply the necessary stars and
push the button to restart the system.
If you like, you can .

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, all that is left is for you to admire your Advent calendar.

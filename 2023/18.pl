#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 2h30
# RESULT [Puzzle 2023/18]: PART1 [42317] - PART2 [83605563360288] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::Board;
use XY::XY qw(XY);
use List::Util qw(min max);
use AOC qw(DEBUG INFO TRACE);
$AOC::NAME = "Lavaduct Lagoon: looong digs";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 150;
$AOC::LEARNED = "Flood fill, Shoelace";
#########################
# Init	
my $year = "2023";
my $puzzle = "18";

my @Tests;
push @Tests, { NAME => 'Trench-62', RESULT1 => 62, RESULT2 => 952408144115, INPUT  => << 'EOEX',
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
EOEX
};
##################################

# Part 1 stuff
my $GROUND = ord '.';
my $EMPTY   = ord ' ';
my $WALL   = ord '#';
my %DirPart1 = (
	D => 'S',
	L => 'W',
	U => 'N',
	R => 'E',
);

# Part 2 stuff
my %DirPart2 = (
	1 => 'S',
	2 => 'W',
	3 => 'N',
	0 => 'E',
);


sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	##### Parse input
	my @DigInstructions;
	my %Colors;

	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);

		# Dig instructions: "R 6 (#70c710)"" -> direction, distance colour
		/(\w) (\d+) ..(\w+)/;
		push @DigInstructions, { DIR => $1, DIST => $2, COLOR => hex($3) };
		$Colors{hex($3)} = chr ($WALL); # Just for output mapping on console
	}

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";

		# Set up field: Get dimensions, create board a bit larger to have an empty border around, set origin so that the dig is centred
		my ($edgeMin, $edgeMax) = &findDigBoundary(\@DigInstructions);
		my $board = XY::Board->new($edgeMax->x() - $edgeMin->x() + 3, $edgeMax->y() - $edgeMin->y() + 3, $GROUND);
		my $pos = XY(1,1)->subt($edgeMin);
		
		# Follow the dig instructions: put the trench on the board
		INFO "Part 1: Digging %d trenches...", scalar @DigInstructions;
		foreach my $dig (@DigInstructions) {
			$pos = &dig($board, $pos, $dig->{DIR}, $dig->{DIST}, $dig->{COLOR});
		}
		# Flood fill the outside of the trench to EMPTY
		INFO "Part 1: Flood filling outside...";
		&floodFill($board, XY(0,0), $EMPTY);

		$board->setOutputMapping(\%Colors); # We set the trench tiles to the color value -> map all to '#'
		binmode(STDOUT, ":encoding(UTF-8)");
		DEBUG "Part 1: Trench, outside flood filled to empty [%d/%d]\n%s", $board->getSizeX(), $board->getSizeY(), $board->toString();

		$p1_result = &countTrench($board); # Count everything which is not EMPTY: Trench and inside
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";

		# Part 2
		# Oh no, bloody Elves: R 6 (#70c710) now means dist is #70c71 and direction low nibble (0, 1, 2, 3) !
		# CANNOT do this with my board. Need to add yet another algorithm to my inventory: Shoelace to the rescue :)
		my @Nodes;
		my $rimTiles = 0; # to count the trench diggings
		my $currentNode = XY(0,0);

		foreach my $dig (@DigInstructions) {
			my $color = $dig->{COLOR};					# It's not a color anymore:
			my $dir = $DirPart2{$color & 0xf};	# Low nibble translates to direction
			my $dist = $color >> 4;							# The rest of the bits are the distance
			TRACE "Part 2: Instruction is dig %s for %d", $dir, $dist; 
			$currentNode = $currentNode->add(XY::XY::aim($dir)->mult($dist));
			$rimTiles += $dist;
			push @Nodes, $currentNode;
		}
		if ($currentNode->equal(XY(0,0))) {
			DEBUG "Part 2: Trench is closed, back at start";
			INFO "Part 2: Calculating Area for trench with %d nodes...", scalar @Nodes;
		}
		else {
			die "Part 2: We did not reach the start after all our digging -> %s", $currentNode->toString();
		}

		# Area calculation via shoelace:
		# Area is shoelace area (including half the rim!), plus half the rim, plus 1
		# (Why +1 ?: We have four outside edges more than inside edges (it's a loop). They in shoelace thy count as 1/4 for the area, but we need them whole!)
		$p2_result = &shoelace(\@Nodes) + $rimTiles / 2 + 1; 
		INFO "*** Part 2 -> [%d]", $p2_result;
	}
	##### RESULTS #####
	# 42317 83605563360288
	return ($p1_result, $p2_result);
}

###
# Part 2

# https://en.wikipedia.org/wiki/Shoelace_formula
# https://rosettacode.org/wiki/Shoelace_formula_for_polygonal_area#Perl
#  (Calculates the geometric inside area, including half the border! 
#   Example: [0/0 2/0 2/2 0/2] -> '4'. 
#            We might want '9' if including full border: 
#            add (border tiles / 2) + 1 (for the quarter corner tiles))
sub shoelace {
	my $rNodes = shift;
	my $area = 0;
	for (my $i = 0; $i < (scalar  @$rNodes) -1; $i++) {
		TRACE "shoelace: %s - %s", $rNodes->[$i]->toString(), $rNodes->[$i+1]->toString();
		my $n1 = $rNodes->[$i];
		my $n2 = $rNodes->[$i+1];
		$area += $n1->x() * $n2->y();
		$area -= $n1->y() * $n2->x();
	}
	return abs $area/2;
}


###
# Part 1

# Count every tile which is not outside (empty)
sub countTrench {
	my $board = shift;

	my $sum = 0;
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			$sum++ unless($board->is(XY($x, $y), $EMPTY));
		}
	}
	return $sum;
}

# Yeah, finally a flood fill: fun to code!
sub floodFill {
	my $board = shift;
	my $pos = shift;
	my $fill = shift;

	my @toFill;
	push @toFill, $pos;

	while (my $field = pop(@toFill)) {
		TRACE "floodFill: %s (%s)", $field->toString(), chr($board->getAt($field));
		my $rNeighbours = $field->directNeighbours();
		foreach my $neighDir (keys %$rNeighbours) {
			my $neigh = $rNeighbours->{$neighDir};
			next unless ($board->valid($neigh));
			if ($board->is($neigh, $GROUND)) {
				TRACE "floodFill: setting %s (%s) to o", $neigh->toString(), chr($board->getAt($neigh));
				$board->setAt($neigh, $fill);
				push(@toFill, $neigh);
			}
		}
	}
}

# Do one dig instruction on the board
sub dig {
	my $board = shift;
	my $pos = shift;
	my $dir = shift;
	my $dist = shift;
	my $color = shift;

	TRACE "dig: %s -> %d %s (%d)", $pos->toString(), $dist, $dir, $color;
	for (my $i = 0; $i < $dist; $i++) {
		$board->setAt($pos, $color);
		$pos = $pos->add(XY::XY::aim($DirPart1{$dir}));
	}
	return $pos;
}

# Follow all instructions and get the extent of the trench
# (to help set up a reasonable board)
sub findDigBoundary {
	my $rDigInstructions = shift;
	my $pos = XY(0,0);
	my ($minX, $minY, $maxX, $maxY) = (0,0,0,0);

	foreach my $dig (@$rDigInstructions) {
		$pos = $pos->add(XY::XY::aim($DirPart1{$dig->{DIR}})->mult($dig->{DIST}));

		$minX = min ($minX, $pos->x());
		$minY = min ($minY, $pos->y());
		$maxX = max ($maxX, $pos->x());
		$maxY = max ($maxY, $pos->y());
	}
	TRACE "findDigBoundary: %d/%d -> %d/%d", $minX, $minY, $maxX, $maxY;
	return (XY($minX, $minY), XY($maxX, $maxY));
}


############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 18: Lavaduct Lagoon ---

Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?

Your puzzle answer was 42317.

--- Part Two ---

The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

So, in the above example, the hexadecimal codes can be converted into the true instructions:

#70c710 = R 461937
#0dc571 = D 56407
#5713f0 = R 356671
#d2c081 = D 863240
#59c680 = R 367720
#411b91 = D 266681
#8ceee2 = L 577262
#caa173 = U 829975
#1b58a2 = L 112010
#caa171 = D 829975
#7807d2 = L 491645
#a77fa3 = U 686074
#015232 = L 5411
#7a21e3 = U 500254
Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?

Your puzzle answer was 83605563360288.

Both parts of this puzzle are complete! They provide two gold stars: **

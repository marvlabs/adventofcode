#!/usr/bin/perl
###
# https://adventofcode.com/2022/day/23
# run: ./23.pl 23.input
###
use lib "$ENV{HOME}/dev/div/adventofcode/aoclibs/lib";

use XY::Board;
use XY::XY qw(XY);

use strict;

my $CELVE = ord('#');
my $CGRND = ord('.');

# Parse input
my $labstr;
my $labY;
my $labX;
while (<>) {
	chomp;
	next if (/^$/);
	$labstr .= $_;
	$labX = length $labstr unless($labX);
	$labY++;
}
print "Read field init $labX/$labY\n";

#####
# Set up field
my $board = XY::Board->new($labX, $labY);
$board->setTiles($labstr);

# $board->setOutputMapping( {
# 	$CELVE =>  chr(128994),
# 	$CGRND =>  chr(129003),
# });
binmode(STDOUT, ":encoding(UTF-8)");
printf ("Board: %d x %d :\n%s", $board->getSizeX(), $board->getSizeY(), $board->toString());


### Checking rules:
# -> During the first half of each round, each Elf considers the eight positions adjacent to themself. If no other Elves are in one of those eight positions, the Elf does not do anything during this round. 
# -> Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:
# 1) If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
my %checkNorth = (
	'N'  => $XY::XY::north,
	'NE'  => $XY::XY::ne,
	'NW'  => $XY::XY::nw,
);
# 2) If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
my %checkSouth = (
	'S'  => $XY::XY::south,
	'SE'  => $XY::XY::se,
	'SW'  => $XY::XY::sw,
);
# 3) If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
my %checkWest = (
	'W'  => $XY::XY::west,
	'NW'  => $XY::XY::nw,
	'SW'  => $XY::XY::sw,
);
# 4) If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
my %checkEast = (
	'E'  => $XY::XY::east,
	'NE'  => $XY::XY::ne,
	'SE'  => $XY::XY::se,
);

my @allChecks = (
	{ ID=>'N', CHECK=>\%checkNorth},
	{ ID=>'S', CHECK=>\%checkSouth},
	{ ID=>'W', CHECK=>\%checkWest},
	{ ID=>'E', CHECK=>\%checkEast},
);

##################
# First part: do 10 rounds and see where we stand
my $nrOfRounds;
for ($nrOfRounds = 1; $nrOfRounds <= 10; $nrOfRounds++) {
	&boardResizeIfFull;
	my $elvesMoved = &oneRound;
	printf ("Curent board\n%s", $board->toString() );
	printf ("In round #%d we had %d elves moving\n%s",$nrOfRounds, $elvesMoved);
	last unless $elvesMoved;
}
# Result of first part:
my $round1Result = &getBoundary;

printf ("Curent board\n%s", $board->toString());
printf "Results - Part 1: there are %d empty fields within the elf rectangle after 10 rounds\n", $round1Result;

###
# Second part: do until all elves find their place
while (my $elvesMoved = &oneRound) {
	&boardResizeIfFull;
	$nrOfRounds++;
	printf ("Curent board\n%s", $board->toString() );
	printf ("In round #%d we had %d elves moving\n", $nrOfRounds, $elvesMoved);
}
my $round2Result = $nrOfRounds;

### RESULTS:
printf ("Curent board\n%s", $board->toString());

# 3815
printf "Results - Part 1: there are %d empty fields within the elf rectangle after 10 rounds\n", $round1Result;
# 893
printf "Results - Part 2: no more elves moved after %d rounds\n", $round2Result;

####################
sub boardResizeIfFull {
	# make sure board is large enough. If any elves are in a border row/col: enlarge board
	if ($board->rowIs(0, $CGRND) && $board->rowIs($board->getSizeY()-1, $CGRND) && 
		$board->colIs(0, $CGRND) && $board->colIs($board->getSizeX()-1, $CGRND))
	{
		# no border elves
	}
	else {
		$board = $board->resize($board->getSizeX()+10, $board->getSizeY()+10, XY(5, 5), ord '.');
	}
}

sub oneRound() {
	#### -> %Elves{#}
	# Find Elves
	my %Elves;
	my $nrOfElves;
	# all fields:
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY($x, $y);
				
			#printf("DEBUG Find Elves: field %s has %s\n", $field->toString(), $board->getAt($field));

			if ($board->getAt($field) == $CELVE) {
				$nrOfElves++;
				$Elves{$nrOfElves}{POS} = $field;
				#printf("Find Elves: %03d is at %s\n", $nrOfElves, $field->toString());
			}
		}
	}

	###
	# Do a half round: Find out what each elf wants

	# Check all elves, and note all desired targets:
	my %allTargets;
	while (my ($key, $elf) = each %Elves) {

		$elf->{WANTSMOVE} = 0;
		$elf->{WANTSDIR} = '';
		$elf->{WANTSTARGET} = '';
		# Check whether any other elves around:
		my $elfPos = $elf->{POS};
		my $rNeighbors = $board->neighbours($elfPos);
		foreach my $val (values %$rNeighbors) {
			if ($val == $CELVE) {
				$elf->{WANTSMOVE} = 1;
				last;
			}
		}

		if ($elf->{WANTSMOVE}) {
			# If the elf needs to move, check all directions
			$elf->{WANTSMOVE} = 0;
			foreach my $rCheck (@allChecks) {
				#printf("DEBUG all checks: %d -> %s\n", $nr, $allChecks{$nr}{ID});
				if (&fieldsAreFree($elfPos, $rCheck->{CHECK})) {
					$elf->{WANTSMOVE} = 1;
					$elf->{WANTSDIR} = $rCheck->{ID};
					$elf->{WANTSTARGET} = $elfPos->add(XY::XY::aim($elf->{WANTSDIR}));
					$allTargets{$elf->{WANTSTARGET}->toString()}++;
					last;
				}
			}
		}
			# printf("elf %0d at %s does %3s need to move: %s \n", $key, $elf->{POS}->toString(), 
			# 	$elf->{WANTSMOVE}?"": "not",
			# 	$elf->{WANTSDIR});
	}

	# Check on all targets: If more than one elf wants to go there, they don't get to move
	while (my ($key, $elf) = each %Elves) {
		next unless $elf->{WANTSMOVE};
		if ($allTargets{$elf->{WANTSTARGET}->toString()} > 1) {
			#printf("elf %0d at %s cannot move %s to %s, multiple target selection\n", $key, $elf->{POS}->toString(), $elf->{WANTSDIR}, $elf->{WANTSTARGET}->toString()); 
			$elf->{WANTSMOVE} = 0;
			$elf->{WANTSDIR} = '';
			$elf->{WANTSTARGET} = '';
		}
	}

	# Move the ones that can!
	my $elvesMoved = 0;
	while (my ($key, $elf) = each %Elves) {
		if ($elf->{WANTSMOVE}) {
			#printf("elf %0d at %s moves %s to %s,\n", $key, $elf->{POS}->toString(), $elf->{WANTSDIR}, $elf->{WANTSTARGET}->toString()); 
			$board->moveTo($elf->{POS}, $elf->{WANTSTARGET}, $CGRND);
			$elf->{POS} = $elf->{WANTSTARGET};
			$elvesMoved++;
		}
	}

	# ...and lastly: change the order of the direction check for the next round
	push @allChecks, shift @allChecks;

	#printf "Elves moved: %d\n", $elvesMoved;
	return $elvesMoved;
}

sub getBoundary {
	# Get boundary of exploration:
	# Check the first / last row / col with no elf
	my $minEmptyRow = -1;
	my $minEmptyCol = -1;
	my $maxEmptyRow = $board->getSizeX();
	my $maxEmptyCol = $board->getSizeY();

	# Rows
	my $foundNonEmptyRow = 0;
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		if (!$board->rowIs($y, $CGRND)) {
			if (!$foundNonEmptyRow) {
				$minEmptyRow = $y-1;
				$foundNonEmptyRow = 1;
			}
			$maxEmptyRow = $y+1;
		}
	}
	# Cols
	my $foundNonEmptyCol = 0;
	for (my $x = 0; $x < $board->getSizeX(); $x++) {
		if (!$board->colIs($x, $CGRND)) {
			if (!$foundNonEmptyCol) {
				$minEmptyCol = $x-1;
				$foundNonEmptyCol = 1;
			}
			$maxEmptyCol = $x+1;
		}
	}

	# Count empty fields within bounds
	my $emptyFields;
	for (my $y = $minEmptyRow+1; $y < $maxEmptyRow; $y++) {
		for (my $x = $minEmptyCol+1; $x < $maxEmptyCol; $x++) {
			my $field = XY($x, $y);
			$emptyFields++ if ($board->is($field, $CGRND));
		}
	}
	printf("Bounding rectangle is at %d/%d - %d/%d. Found %d empty fields within.\n", $minEmptyCol, $minEmptyRow, $maxEmptyCol, $maxEmptyRow, $emptyFields);
	return $emptyFields;
}



############################
sub fieldsAreFree {
	my $pos = shift;
	my $rCheckDirections = shift;

	my $rFields = $pos->addList($rCheckDirections);
	
	foreach my $field (values %$rFields) {
		if ($board->getAt($field) == $CELVE) {
			return 0;
		}
	}
	return 1;
}
############################
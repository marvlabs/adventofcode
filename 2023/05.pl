#!perl
###
# https://adventofcode.com/2023/day/5
# run: 2023/05.pl
# Solved in: 6h
# RESULT [Puzzle 05]: PART1 [107430936] - PART2 [23738616]
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE);
$AOC::NAME = "If You Give A Seed A Fertilizer: doesn't scale";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 360;
$AOC::LEARNED = "Range fitting is error prone";
#########################
# Init
my $year = "2023";
my $puzzle = "05";

my @Tests;
push @Tests, { NAME => 'Maps', RESULT1 => 35, RESULT2 => 46, INPUT  => << 'EOEX1',
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
EOEX1
};
##################################
my %Maps;
my $nrOfMaps;

sub solvePuzzle {
	my $inputFilehandle = shift;
	my ($p1_result, $p2_result);

	# Parse input
	my $seedline =  (<$inputFilehandle>);
	chomp;
	$seedline =~ /seeds: (.*)/;
	my @seeds = split (' ', $1);

	my @seedRanges = &createSeedRange($seedline); # Part2

	my $mapname;
	$nrOfMaps = 0;
	undef %Maps;
	while (<$inputFilehandle>) {
	 	chomp;
	 	if (/(.*):/) {
	 		$mapname = $1;
	 		$nrOfMaps++;
	 		DEBUG "maps: found new map [%s]", $mapname;
			$Maps{$nrOfMaps}{NAME} = $mapname;
			$Maps{$nrOfMaps}{MAPINSTRUCTIONS} = [()];
	 	}
	 	elsif (/(\d+) (\d+) (\d+)/) {
			&createRange($nrOfMaps, $mapname, $1, $2, $3);
	 	}
	 	elsif (/^$/) {
	 		$mapname = '';
	 	}
	}

	# PART 1
	# Take one seed and go through map chain
	my $nearestLocation = '';
	foreach my $seed (@seeds) {
		my $location = &mapChain($seed);
		$nearestLocation = $location if (!$nearestLocation || $location < $nearestLocation);
	}
	$p1_result = $nearestLocation;

	# 107430936
	INFO "Results - Part 1: nearest location is %d", $p1_result;

	# PART 2 - Brute Force, no dice. 
	# It actually also works -> takes about 12h to get through the 2'855'550'144 seeds
	# Take seedranges and go through map chain
	# my $nrOfMapchains = 0;
	# foreach my $rSeedRange (@seedRanges) {
	# 	$nrOfMapchains += $rSeedRange->{LENGTH};
	# }

	# PART 2 - Range list mapping approach
	# Map whole ranges and return maps
	my $rRangeList = \@seedRanges;
	for (my $i = 1; $i <= $nrOfMaps; $i++) {
		$rRangeList = &filterRangesThroughMapList($rRangeList, $Maps{$i});
	}

	$nearestLocation = '';
	foreach my $rLocationRange (@$rRangeList) {
		#printf "P2 Mapped Results : [%d - %d]\n", $rLocationRange->{START}, $rLocationRange->{END};
		$nearestLocation = $rLocationRange->{START} if (!$nearestLocation || $rLocationRange->{START} < $nearestLocation);
	}
	$p2_result = $nearestLocation;

	# 23738616
	INFO "Results - Part 2: nearest location is %d", $p2_result;
	return ($p1_result, $p2_result);
}

# For part 2
sub filterRangesThroughMapList {
	my $rRanges = shift;
	my $rMap = shift;
	DEBUG "Processing [%d] ranges through maplist %s", scalar @$rRanges, $rMap->{NAME};

	my @mapped;
	foreach my $rMapInstruction (@{$rMap->{MAPINSTRUCTIONS}}) { 
		my ($rMapped, $rNotMapped) = &filterRangesThroughMapInstruction($rRanges, $rMapInstruction);
		# printf "DEBUG filterRangesThroughMapList: after map instruction, we have:\n";
		# foreach my $r (@$rMapped) {
		# 	printf "MAPPED [%d - %d]\n", $r->{START}, $r->{END};
		# }
		# foreach my $r (@$rNotMapped) {
		# 	printf "NOT MAPPED [%d - %d]\n", $r->{START}, $r->{END};
		# }
		push @mapped, (@$rMapped);
		$rRanges = $rNotMapped;
	}

	push @mapped, (@$rRanges);
	return \@mapped;
}

sub filterRangesThroughMapInstruction {
	my $rRanges = shift;
	my $rMapInstruction = shift;

	my $mapSourceStart = $rMapInstruction->{SOURCESTART};
	my $mapSourceEnd   = $rMapInstruction->{SOURCEND};
	my $mapDisplace = $rMapInstruction->{DISPLACE};
	#printf "DEBUG filterRangesThroughMapInstruction: [%d - %d] (%d)\n", $mapSourceStart, $mapSourceEnd, $mapDisplace;

	my @listOfMapped;
	my @listOfNotMapped;

	foreach my $rRange ( @$rRanges) {
		my $inputStart = $rRange->{START};
		my $inputEnd   = $rRange->{END};

		my $inputStartInRange = $inputStart >= $mapSourceStart && $inputStart <= $mapSourceEnd;
		my $inputEndInRange   = $inputEnd   >= $mapSourceStart && $inputEnd   <= $mapSourceEnd;
		my $inputCoversMap    = $inputStart <  $mapSourceStart && $inputEnd   >  $mapSourceEnd;


		if ($inputCoversMap) {
			my %mappedRange;
			$mappedRange{START} = $mapSourceStart + $mapDisplace;
			$mappedRange{END}   = $mapSourceEnd   + $mapDisplace;

			my %remainder1;
			$remainder1{START} = $inputStart;
			$remainder1{END} = $mapSourceStart - 1;
			my %remainder2;
			$remainder2{START} = $mapSourceEnd + 1;
			$remainder2{END} = $inputEnd;

			#printf "DEBUG mapChainForRange: mapped chunk [%d - %d] to [%d - %d], remainder are [%d - %d] and [%d - %d]\n", 
				$mapSourceStart, $mapSourceEnd, $mappedRange{START}, $mappedRange{END}, $remainder1{START}, $remainder1{END}, $remainder2{START}, $remainder2{END};
			push(@listOfMapped, \%mappedRange);
			push(@listOfNotMapped, \%remainder1);
			push(@listOfNotMapped, \%remainder2);
		} 
		elsif ($inputStartInRange && $inputEndInRange) {
			my %mappedRange;
			$mappedRange{START} = $inputStart + $mapDisplace;
			$mappedRange{END}   = $inputEnd + $mapDisplace;
			#printf "DEBUG mapChainForRange: mapped complete range [%d - %d] to [%d - %d]\n", $inputStart, $inputEnd, $mappedRange{START}, $mappedRange{END};
			push(@listOfMapped, \%mappedRange);
		} 
		elsif ($inputStartInRange && !$inputEndInRange) {
			my %mappedRange;
			$mappedRange{START} = $inputStart + $mapDisplace;
			$mappedRange{END}   = $mapSourceEnd + $mapDisplace;

			my %remainder;
			$remainder{START} = $mapSourceEnd + 1;
			$remainder{END} = $inputEnd;

			#printf "DEBUG mapChainForRange: mapped part [%d - %d] to [%d - %d], remainder is [%d - %d]\n", $inputStart, $mapSourceEnd, $mappedRange{START}, $mappedRange{END}, $remainder{START}, $remainder{END};
			push(@listOfMapped, \%mappedRange);
			push(@listOfNotMapped, \%remainder);
		} 
		elsif (!$inputStartInRange && $inputEndInRange) {
			my %mappedRange;
			$mappedRange{START} = $mapSourceStart + $mapDisplace;
			$mappedRange{END}   = $inputEnd + $mapDisplace;

			my %remainder;
			$remainder{START} = $inputStart;
			$remainder{END} = $mapSourceStart - 1;

			#printf "DEBUG mapChainForRange: mapped part [%d - %d] to [%d - %d], remainder is [%d - %d]\n", $mapSourceStart, $inputEnd, $mappedRange{START}, $mappedRange{END}, $remainder{START}, $remainder{END};
			push(@listOfMapped, \%mappedRange);
			push(@listOfNotMapped, \%remainder);
		}
		else {
			my %remainder;
			$remainder{START} = $inputStart;
			$remainder{END} = $inputEnd;
			#printf "DEBUG mapChainForRange: nothing mapped remainder is [%d - %d]\n", $remainder{START}, $remainder{END};
			push(@listOfNotMapped, \%remainder);
		}
	}
	return (\@listOfMapped, \@listOfNotMapped);
}

### for Part 1
sub mapChain {
	my $input = shift;

	for (my $i = 1; $i <= $nrOfMaps; $i++) {
		#printf "DEBUG mapChain: [%d] -> %s \n", $input, $Maps{$i}{NAME};
		foreach my $rRange (@{$Maps{$i}{MAPINSTRUCTIONS}}) {
			if ($input >= $rRange->{SOURCESTART} && $input <= $rRange->{SOURCESTART} + $rRange->{LENGTH}) {
				my $mapped = $rRange->{TARGETSTART} - $rRange->{SOURCESTART} + $input;
				#printf "DEBUG mapChain: mapping [%d] -> [%d]\n", $input, $mapped;
				$input = $mapped;
				last;
			}
		}
	}
	return $input;

}

### For init
sub createSeedRange {
	my $seedline = shift;
	my @seedRanges;
	while ($seedline =~ /(\d+) (\d+)/g) {
		my %range;
		$range{START} = $1;
		$range{LENGTH} = $2;
		$range{END} = $1+$2-1;
		push (@seedRanges, \%range);
		DEBUG "DEBUG createSeedRange: [%d] -> [%d]", $1, $1+$2-1;
	}
	return @seedRanges;
}

sub createRange {
	my ($mapnr, $mapname, $destRangeStart, $sourceRangeStart, $rangeLength) = @_;
	#printf "DEBUG createRange: new [%10d] range for [%d-%s] [%d->%d]\n", $rangeLength, $mapnr, $mapname, $sourceRangeStart, $destRangeStart;
	my %Range;
	$Range{SOURCESTART} = $sourceRangeStart;
	$Range{SOURCEND}    = $sourceRangeStart + $rangeLength-1;
	$Range{TARGETSTART} = $destRangeStart;
	$Range{TARGETEND}   = $destRangeStart + $rangeLength-1;
	$Range{DISPLACE}    = $destRangeStart - $sourceRangeStart;
	$Range{LENGTH} = $rangeLength;
	push (@{$Maps{$mapnr}{MAPINSTRUCTIONS}}, \%Range);
}

############################# 
# MAIN
# Run tests first
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

Your puzzle answer was 107430936.

--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

Your puzzle answer was 23738616.


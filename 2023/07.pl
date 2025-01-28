#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/07.pl
# Solved in: 2h30
# RESULT [Puzzle 07]: PART1 [246163188] - PART2 [245794069]
###
# Note: fixed it up after the inital success.
# - Hand value can be calculated instead of cased. This gives back a comparable number for every hand.
# 		Value is the square of the count of every card group, eg. 'TT888' 2^2 + 3^2 = 13 -> FullHouse :
# 		(5 => 'HighCard', 7 => 'OnePair', 9 => 'TwoPair', 11 => 'ThreeKind', 13 => 'FullHouse', 17 => 'FourKind' =>, 25 => 'FiveKind');
# - Joker: instead of casing: Replace every joker with the card with the highes occurencies, then calculate as above.
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE PROGRESS);
$AOC::NAME = "Camel Cards: Poker hands rating";
$AOC::DIFFICULTY = 2;
$AOC::TIMEUSED = 150;
$AOC::LEARNED = "Think before code";
#########################
# Init
my $year = "2023";
my $puzzle = "07";

my @Tests;
push @Tests, { NAME => 'ElfPoker', RESULT1 => 6440, RESULT2 => 5905, INPUT  => << 'EOEX1',
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
EOEX1
};
##################################

my %CardRank          = (A => 14, K => 13, Q => 12, J => 11, T => 10, 9 => 9, 8 => 8, 7 => 7, 6 => 6, 5 => 5, 4 => 4, 3 => 3, 2 => 2 );
my %CardRankWithJoker = (A => 14, K => 13, Q => 12, J =>  1, T => 10, 9 => 9, 8 => 8, 7 => 7, 6 => 6, 5 => 5, 4 => 4, 3 => 3, 2 => 2 );
my %HandNames         = (5 => 'HighCard', 7 => 'OnePair', 9 => 'TwoPair', 11 => 'ThreeKind', 13 => 'FullHouse', 17 => 'FourKind' =>, 25 => 'FiveKind');
#my %HandRank          = (HighCard => 1, OnePair => 2, TwoPair => 3, ThreeKind => 4, FullHouse => 5, FourKind => 6, FiveKind => 7);
my %Hands;

sub solvePuzzle {
	my $inputFilehandle = shift;
	my ($p1_result, $p2_result);
	%Hands = ();

	# Parse input
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);
		PROGRESS $.;

		# Add hand to %Hands, calculate what it is
		# Assume no duplicate hands
		/(.*) (\d+)/;
		$Hands{$1}{BID} = $2;
		$Hands{$1}{HANDVALUE}	          = &smartHandIs($1);    #$HandRank{$Hands{$1}{IS}};
		$Hands{$1}{HANDVALUEWITHJOKER}	= &smartHandCanBe($1); #$HandRank{$Hands{$1}{ISWITHJOKER}};

		DEBUG "PARSE: [%s] bids [%3d]: is [%d %9s], with joker [%d %9s]", 
			$1, $Hands{$1}{BID}, 
			$Hands{$1}{HANDVALUE},          $HandNames{$Hands{$1}{HANDVALUE}},
			$Hands{$1}{HANDVALUEWITHJOKER}, $HandNames{$Hands{$1}{HANDVALUEWITHJOKER}};
	}

	INFO "*** Part 1 running ***";
	my $rank = 0;
	foreach my $hand (sort { sortHands ('HANDVALUE', \%CardRank) } (keys %Hands)) {
		$rank++;
		my $value = $rank * $Hands{$hand}{BID};
		$p1_result += $value;
		DEBUG "Rank-1: [%s] bids [%3d]: rank [%3d]: value [%6d] is [%d %s]", 
			$hand, $Hands{$hand}{BID}, $rank, 
			$value, $Hands{$hand}{HANDVALUE}, $HandNames{$Hands{$hand}{HANDVALUE}};
	}
	INFO "*** Part 1 -> [%d]", $p1_result;


	INFO "*** Part 2 running ***";
	my $rank = 0;
	foreach my $hand (sort { sortHands('HANDVALUEWITHJOKER', \%CardRankWithJoker) } (keys %Hands)) {
		$rank++;
		my $value = $rank * $Hands{$hand}{BID};
		$p2_result += $value;
		DEBUG "Rank-2: [%s] bids [%3d]: rank [%3d]: value [%6d] is [%d %s]", 
			$hand, $Hands{$hand}{BID}, $rank, 
			$value, $Hands{$hand}{HANDVALUEWITHJOKER}, $HandNames{$Hands{$hand}{HANDVALUEWITHJOKER}};
	}

	INFO "*** Part 2 -> [%d]", $p2_result;

	# 246163188
	INFO "Results - Part 1: sum is %d", $p1_result;
	# 245794069
	INFO "Results - Part 2: sum is %d", $p2_result;

	return ($p1_result, $p2_result);
}

sub sortHands {
	my $whichRank = shift; # Hand value found either at index HANDVALUE, or HANDVALUEWITHJOKER for part2
	my $rCardRank = shift; # Different card ranking, %CardRank for part 1, %CardRankWithJoker for part 2

	return $Hands{$a}{$whichRank} <=> $Hands{$b}{$whichRank} if ($Hands{$a}{$whichRank} != $Hands{$b}{$whichRank});

	# If equal hands, which first card is higher
	for (my $x = 0; $x < 5; $x++) {
		my $c1 = substr($a, $x, 1);
		my $c2 = substr($b, $x, 1);
		return $rCardRank->{$c1} <=> $rCardRank->{$c2} if ($c1 ne $c2);
	}
}

# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456
sub smartHandIs {
	my $hand = shift;

	# Count how many of each card faces we have in our five cards
	my %cardIndex;
	foreach my $card (split (//, $hand)) {
		$cardIndex{$card}++;
	}

	# Value is the square of the count of every card group, eg. 'TT888' 2^2 + 3^2 = 13 -> FullHouse :
	# (5 => 'HighCard', 7 => 'OnePair', 9 => 'TwoPair', 11 => 'ThreeKind', 13 => 'FullHouse', 17 => 'FourKind' =>, 25 => 'FiveKind');
	my $handValue;
	foreach my $face (keys %cardIndex) {
		$handValue += $cardIndex{$face} * $cardIndex{$face};
	}
	#return $HandNames{$handValue};
	return $handValue;
}

#### Part 2: J is a joker now...
sub smartHandCanBe {
	my $hand = shift;

	# Count how many of each card faces we have in our five cards
	my %cardIndex;
	foreach my $card (split (//, $hand)) {
		$cardIndex{$card}++;
	}

	my $nrOfJ = $cardIndex{'J'};
	if ($nrOfJ > 0 && $nrOfJ < 5) {
		undef $cardIndex{'J'};
		# Add the number of jokers to the highest counting other card, then valuate it as before
		my @sortedKeys = sort { $cardIndex{$b} <=> $cardIndex{$a} } (keys %cardIndex);
		my $topCard = $sortedKeys[0];
		my $handCanBe = $hand =~ s/J/$topCard/gr;
		DEBUG "smartHandCanBe: [%s] ->  [%s]", $hand, $handCanBe;
		$hand = $handCanBe;
	}
	return &smartHandIs($hand);
}

# Works, but not pretty :)
# sub handIs {
# 	my $hand = shift;

# 	# Count how many of each card faces we have in our five cards
# 	my %cardIndex;
# 	foreach my $card (split (//, $hand)) {
# 		$cardIndex{$card}++;
# 	}

# 	my ($haveTwo, $haveThree);
# 	foreach my $face (keys %cardIndex) {
# 		if ($cardIndex{$face} == 5) {
# 			return "FiveKind";
# 		}
# 		if ($cardIndex{$face} == 4) {
# 			return "FourKind";
# 		}

# 		if ($cardIndex{$face} == 3) {
# 			if ($haveTwo) {
# 				return "FullHouse"
# 			}
# 			$haveThree = 1;
# 		}
# 		elsif ($cardIndex{$face} == 2) {
# 			if ($haveThree) {
# 				return "FullHouse"
# 			}
# 			elsif ($haveTwo) {
# 				return "TwoPair"
# 			}
# 			$haveTwo = 1;
# 		}
# 	}

# 	return "ThreeKind" if ($haveThree);
# 	return "OnePair"   if ($haveTwo);
# 	return "HighCard";
# }

# #### Part 2: J is a joker now...
# sub handCanBe {
# 	my $hand = shift;

# 	# Count how many of each card faces we have in our five cards
# 	my %cardIndex;
# 	foreach my $card (split (//, $hand)) {
# 		$cardIndex{$card}++;
# 	}

# 	###
# 	# Cases for one to five jokers:

# 	## no joker, use normal hand routine
# 	if ($cardIndex{J} == 0) {
# 		return &smartHandIs($hand);
# 	}

# 	## 4 or 5 jokers, alwas FiveKind
# 	if ($cardIndex{J} >= 4) {
# 		return "FiveKind";
# 	}

# 	## Three jokers: FiveKind or FourKind
# 	if ($cardIndex{J} == 3) {
# 		foreach my $face (keys %cardIndex) {
# 			next if ($face eq 'J');
		
# 			if ($cardIndex{$face} == 2) {
# 					return "FiveKind"
# 			}
# 		}
# 		return "FourKind";
# 	}

# 	## Two jokers: FiveKind or FourKind or ThreeKind
# 	if ($cardIndex{J} == 2) {
# 		foreach my $face (keys %cardIndex) {
# 			next if ($face eq 'J');
		
# 			if ($cardIndex{$face} == 3) {
# 				return "FiveKind"
# 			}
# 			if ($cardIndex{$face} == 2) {
# 				return "FourKind";
# 			}			
# 		}
# 		return "ThreeKind";
# 	}

# 	## One Joker: at least one pair
# 	if ($cardIndex{J} == 1) {

# 		my ($haveTwo);
# 		foreach my $face (keys %cardIndex) {
# 			next if ($face eq 'J');

# 			if ($cardIndex{$face} == 4) {
# 				return "FiveKind";
# 			}

# 			if ($cardIndex{$face} == 3) {
# 					return "FourKind"
# 			}

# 			if ($cardIndex{$face} == 2) {
# 				if ($haveTwo) {
# 					return "FullHouse"
# 				}
# 				$haveTwo = 1;
# 			}
# 		}
# 		return "ThreeKind" if ($haveTwo);
# 		return "OnePair" ;
# 	}
# }

############################# 
# MAIN
# Run tests first
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?

Your puzzle answer was 246163188.

--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

Your puzzle answer was 245794069.

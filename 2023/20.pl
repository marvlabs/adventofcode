#!perl
###
# https://adventofcode.com/2023/day/6
# run: 2023/xx.pl
# Solved in: 3h
# RESULT [Puzzle 2023/20]: PART1 [763500168] - PART2 [207652583562007] 
###
use strict;
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use AOC qw(DEBUG INFO TRACE);
use Data::Dumper;
use Math::Utils;
$AOC::NAME = "Pulse Propagation: State machine";
$AOC::DIFFICULTY = 3;
$AOC::TIMEUSED = 180;
$AOC::LEARNED = "Cycle detection, again";
#########################
# Init	
my $year = "2023";
my $puzzle = "20";

my @Tests;
push @Tests, { NAME => 'Pulse-Simple', RESULT1 => 32000000, INPUT  => << 'EOEX',
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
EOEX
};
push @Tests, { NAME => 'Pulse-Complicated', RESULT1 => 11687500, INPUT  => << 'EOEX',
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
EOEX
};
##################################

my $FLIPFLOP = '%';
my $CONJUNCTION = '&';
my $BROADCASTER = 'broadcaster';
my $OUTPUT = 'output';
my $HIGH = 1;
my $LOW = 0;

# Part 2 input peaking for RX in my case
# &tr -> dh
# &xm -> dh
# &dr -> dh
# &nh -> dh
# &dh -> rx
# - find this conjunction (dh in my case) -> CONJUNCTIONFORFINAL
# - find all inputs connected to it -> NecessaryModules
# - then detect when these inputs themselves get a HIGH
# - to an LCM to propose a 'cycle' when all of them would deliver a high at the same time
my $FINALMACHINE = "rx";
my $CONJUNCTIONFORFINAL;
my %NecessaryModules;
# EVIL: global vars just to have them accessible for the part-2 hack
my $RX_GOT_LOW = 0;
my $NR_OF_BUTTON = 0;
###

sub solvePuzzle {
	my $inputFilehandle = shift;
	my $whichPart = shift;
	my ($p1_result, $p2_result) = (0,0);

	INFO "*** Setup & Input ***";

	# Reset globals after each run. Yes, the testcases got me off by 2000 first. Arghhhhhh!
	$RX_GOT_LOW = 0;
	$NR_OF_BUTTON = 0;
	$CONJUNCTIONFORFINAL = "";
	%NecessaryModules = ();

	# Store all the modules with their attributes: NAME, IS, STATE, list of INPUTS
	my %Modules;

	##### Parse input
	while (<$inputFilehandle>) {
		chomp;
		next if (/^$/);

		# Part 1
		/(.*) -> (.*)/;

		my %module;
		if (substr($1,0,1) eq $FLIPFLOP) {
			$module{IS} = $FLIPFLOP;
			$module{NAME} = substr($1,1);
			$module{STATE} = $LOW;
		}
		elsif (substr($1,0,1) eq $CONJUNCTION) {
			$module{IS} = $CONJUNCTION;
			$module{NAME} = substr($1,1);
		}
		else {
			$module{NAME} = $1;
			if ($1 eq $BROADCASTER) {
				$module{IS} = $BROADCASTER;
			}
			else {
				$module{IS} = $;
			}
		}
		$module{INPUTS} = {};

		my @targets;
		foreach my $target (split(/,/, $2)) {
			$target =~ s/^\s+//;
			push @targets, $target;
		}
		$module{TARGETS} = \@targets;
		$Modules{$module{NAME}} = \%module;
	}

	# Find all inputs for a module
	# Part 2 -> find the important module for the cycle detection
	&wireTargets(\%Modules, \%NecessaryModules);

	##### Part 1 #####
	if ($whichPart ne 'PART2ONLY') {
		INFO "*** Part 1 running ***";
		my ($nrOfLow, $nrOfHigh);
		for (my $i = 0; $i < 1000; $i ++) {
			$NR_OF_BUTTON++;
			my ($low, $high) = &pushButton(\%Modules);
			$nrOfLow += $low;
			$nrOfHigh += $high;
		}
		$p1_result = $nrOfHigh * $nrOfLow;
		INFO "*** Part 1 -> [%d]", $p1_result;
	}

	##### Part 2 #####
	if ($whichPart ne 'PART1ONLY') {
		INFO "*** Part 2 running ***";

		# Continue with pressing buttons until rx gets LOW
		while (!$RX_GOT_LOW) {
			$NR_OF_BUTTON++;
			&pushButton(\%Modules);

			# Shortcut: Check whether the necessary modules for an LCM cycle have been triggered
			my $allThere = 1;
			foreach my $key (keys %NecessaryModules) {
				if ($NecessaryModules{$key} == -1) {
					$allThere = 0;
					last;
				}
			}
			last if $allThere;
		}

		if ($RX_GOT_LOW) {
			# Not before the heat death of this machine...
			$p2_result = $NR_OF_BUTTON;
		}
		else {
			# Cycle detect: LCM of high input signal cycle for DH (which outputs low to RX)
			$p2_result = Math::Utils::lcm(values %NecessaryModules);
		}
		INFO "*** Part 2 -> [%d]", $p2_result;
	}

	##### RESULTS #####
	# 763500168 207652583562007
	return ($p1_result, $p2_result);
}

#####
## Modules simulation

# Put one LOW signal to the broadcaster in the signal queue for starting
# Work the signal queue until all no more signals to process: 
# - send the signal to the module
# - append all resulting signals to the queue
sub pushButton {
	my $rModules = shift;
	
	# Count the number of high and low pulses in the system
	my ($pulseH, $pulseL);
	
	my @signalqueue;
	push @signalqueue, { HL => $LOW, TARGET => $BROADCASTER, SOURCE => "BUTTON"};

	while (my $rSignal = shift @signalqueue) {
		TRACE "pushButton: %d -> %s", $rSignal->{HL}, $rSignal->{TARGET};
		$pulseH++ if ($rSignal->{HL} == $HIGH);
		$pulseL++ if ($rSignal->{HL} == $LOW);
		
		my @newSignals = &simulateModule($rModules->{$rSignal->{TARGET}}, $rSignal->{HL}, $rSignal->{SOURCE});
		push @signalqueue, (@newSignals);
	}

	return ($pulseH, $pulseL);
}


# Give an input pulse to a module, let it generate output pulses
sub simulateModule {
	my $rModule = shift;
	my $hl = shift;
	my $source = shift;

	### Part 2
	# Final module RX needs to get LOW...
	$RX_GOT_LOW = 1 if ($rModule->{NAME} eq $FINALMACHINE && $hl == 0);
	# ...or we check the input to the necessary modules and do an LCM once they come up
	if ($hl == 1 && $rModule->{NAME} eq $CONJUNCTIONFORFINAL && $NecessaryModules{$source} == -1 ) {
		$NecessaryModules{$source} = $NR_OF_BUTTON;
		DEBUG "simulateModule Part2: found necessary trigger from [%s] to [%s] at button %d", $rModule->{NAME}, $source, $NR_OF_BUTTON;
	}
	########

	TRACE "simulateModule: %s (%d from %s)", $rModule->{NAME}, $hl, $source;

	my @signalsGenerated;

	if ($rModule->{IS} eq $BROADCASTER) {
		# A broadcaster sends the incoming signal to all targets
		foreach my $targetName (@{$rModule->{TARGETS}}) {
			push @signalsGenerated, { HL => $hl, TARGET => $targetName, SOURCE => $rModule->{NAME} };
		}
	}

	elsif ($rModule->{IS} eq $FLIPFLOP) {
		# If a flip-flop gets a LOW signal, it inverts it state and propagates the new state
		return () if ($hl == $HIGH);
		$rModule->{STATE} ^= 1;
		foreach my $targetName (@{$rModule->{TARGETS}}) {
			push @signalsGenerated, { HL => $rModule->{STATE}, TARGET => $targetName, SOURCE => $rModule->{NAME} };
		}
	}

	elsif ($rModule->{IS} eq $CONJUNCTION) {
		# The conjunction remembers the last incoming signal from all sources.
		# It sends out LOW if all the sources sent a HIGH last. If not, it sends HIGH.
		$rModule->{INPUTS}{$source} = $hl;

		my $out = $LOW;
		foreach my $inputName (keys %{$rModule->{INPUTS}}) {
			if ($rModule->{INPUTS}{$inputName} == $LOW) {
				$out = $HIGH;
				last;
			}
		}
		foreach my $targetName (@{$rModule->{TARGETS}}) {
			push @signalsGenerated, { HL => $out, TARGET => $targetName, SOURCE => $rModule->{NAME} };
		}
	}

	foreach my $send (@signalsGenerated) {
		TRACE "simulateModule: %s (%d) generates %d to %s", $rModule->{NAME}, $hl, $send->{HL}, $send->{TARGET}; 
	}
	return @signalsGenerated;
}


# Connect all module outputs to their target as inputs
sub wireTargets {
	my $rModules = shift;
	my $rNecessaryModules = shift;

	foreach my $moduleName (keys %$rModules) {
		# All targets of this module
		foreach my $targetName (@{$rModules->{$moduleName}{TARGETS}}) {
			TRACE "wireTargets: module [%s] has target [%s]", $moduleName, $targetName;
			$rModules->{$targetName}{INPUTS}{$moduleName} = $LOW;
		}
	}

	### Part 2
	# Find the important modules
	foreach my $moduleName (keys %$rModules) {
		if (${$rModules->{$moduleName}{TARGETS}}[0] eq $FINALMACHINE) {
			$CONJUNCTIONFORFINAL = $moduleName;
			DEBUG "wireTargets: found final conjuction %s", $moduleName;
			last;
		} 
	}
	INFO "wireTargets: Part 2 hack doesn't work, final conjunction for $FINALMACHINE not found" unless $CONJUNCTIONFORFINAL;

	foreach my $moduleName (keys %$rModules) {
		if (${$rModules->{$moduleName}{TARGETS}}[0] eq $CONJUNCTIONFORFINAL) {
			$rNecessaryModules->{$moduleName} = -1;
			DEBUG "wireTargets: found input to final conjuction %s", $moduleName;
		} 
	}
	#########
}


############################# 
# MAIN
&AOC::Init($year, $puzzle, @ARGV);
&AOC::Test(\&solvePuzzle, \@Tests);
&AOC::Solve(\&solvePuzzle);
############################
__END__
--- Day 20: Pulse Propagation ---

With your help, the Elves manage to find the right parts and fix all of the machines. Now, they just need to send the command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. The cables don't connect to the machines directly, but rather to communication modules attached to the machines that perform various initialization tasks and also act as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module sends a pulse, it sends that type of pulse to each module in its list of destination modules.

There are several different types of modules:

Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button, a single low pulse is sent directly to the broadcaster module.

After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again. Never push the button if modules are still processing pulses.

Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b, and c, and then module a processes its pulse and sends more pulses, the pulses sent to modules b and c would have to be handled first.

The module configuration (your puzzle input) lists each module. The name of the module is preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a list of its destination modules. For example:

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
In this module configuration, the broadcaster has three destination modules named a, b, and c. Each of these modules is a flip-flop module (as indicated by the % prefix). a outputs to b which outputs to c which outputs to another module named inv. inv is a conjunction module (as indicated by the & prefix) which, because it has only one input, acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to a.

By pushing the button once, the following pulses are sent:

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a
After this sequence, the flip-flop modules all end up off, so pushing the button again repeats the same sequence.

Here's a more interesting example:

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
This module configuration includes the broadcaster, two flip-flops (named a and b), a single-input conjunction module (inv), a multi-input conjunction module (con), and an untyped module named output (for testing purposes). The multi-input conjunction module con watches the two flip-flop modules and, if they're both on, sends a low pulse to the output module.

Here's what happens if you push the button once:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output
Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are on and con remembers a high pulse from each of its two inputs, pushing the button a second time does something different:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.

Push the button a third time:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output
This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off, the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that, flip-flop b turns off, which causes con to update its state and send a high pulse to output.

Finally, with a on and b off, push the button a fourth time:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their original states.

To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got sent as a result (including the pulses sent by the button itself)?

In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4 high pulses are sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high pulses are sent. Multiplying these together gives 32000000.

In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses are sent. Multiplying these together gives 11687500.

Consult your module configuration; determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times, waiting for all pulses to be fully handled after each push of the button. What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?

Your puzzle answer was 763500168.

--- Part Two ---

The final machine responsible for moving the sand down to Island Island has a module attached named rx. The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press, what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

Your puzzle answer was 207652583562007.

Both parts of this puzzle are complete! They provide two gold stars: **

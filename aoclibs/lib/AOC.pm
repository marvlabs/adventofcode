package AOC;
use strict;
use warnings;
use HTTP::Tiny;
use Time::Local;
use Time::HiRes;
use Storable qw(store retrieve);
use XY::Board;
use XY::XY qw(XY);
my $CURSES = eval {
  require Curses;
  Curses->import(qw (initscr stdscr newwin addstring refresh endwin getch clrtoeol erase));#
  1;
};

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw();
our @EXPORT_OK = qw(DEBUG INFO TRACE PROGRESS BOARD BOARD_PAUSE);
our $DEBUG = 1; # 0 none, 1 debug, 2 trace
our $NAME = "(no name yet)";
our $DIFFICULTY;
our $TIMEUSED;
our $LEARNED;
our $BOARD_LAG;

my ($GUI, $BOARD, $winTitle, $winMain, $winStatus, $winProgress, $winDebug);
my ($Year, $Day, $InputFile);
my $Statistics = {};

BEGIN {
	if (! $ENV{AOC_SESSION}) {
		my $AOC_KEY_FILE = "aoc-session-key.secret";
		if (-r $AOC_KEY_FILE) {
			open KEY, "<", $AOC_KEY_FILE or die "Cannot read [$AOC_KEY_FILE], $!";
			my $key = <KEY>;
			chomp $key;
			$ENV{AOC_SESSION} = $key;
			#print "sessionkeyfile available : $ENV{AOC_SESSION}\n";
		}
	}
}
END {
	 if ($GUI) {
	 	#print "Need to destroy GUI\n";
		getch($winStatus);
		endwin();
	 }
}
###########
# Constants
my $AocUrl = "https://adventofcode.com/%4d/day/%d/input";

###########
# Helpers
sub TRACE {
	return unless $DEBUG > 1;
	my $msg = "TRACE: " . shift;
	if ($GUI) {
		addstring($winDebug, sprintf("$msg\n", @_));
		refresh($winDebug);
	}
	else {
		printf "$msg\n", @_;
	}
}
sub DEBUG {
	return unless $DEBUG;
	my $msg = "DEBUG: " . shift;
	if ($GUI) {
		addstring($winDebug, sprintf("$msg\n", @_));
		refresh($winDebug);
	}
	else {
		printf "$msg\n", @_;
	}
}
sub INFO {
	my $msg = shift;
	if ($GUI) {
		addstring($winMain, sprintf("$msg\n", @_));
		refresh($winMain);
	}
	else {
		printf "INFO: $msg\n", @_;
	}
}

sub STATUS {
	my $msg = shift;
	if ($GUI) {
		addstring($winStatus, sprintf("$msg\n", @_));
		refresh($winStatus);
	}
	else {
		printf "STATUS: $msg\n", @_;
	}
}

sub TITLE {
	my $msg = shift;
	if ($GUI) {
		addstring($winTitle, 0, 0, sprintf("$msg", @_));
		clrtoeol($winTitle);
		refresh($winTitle);
	}
	else {
		printf "AdventOfCode: $msg\n", @_;
	}
}

sub  PROGRESS {
	my ($count, $total) = @_;
	if ($GUI) {
		if (defined $total) {
			addstring($winProgress, 0, 0, sprintf("%3d%%", $count * 100 / $total ));
		}
		else {
			addstring($winProgress, 0, 0, sprintf("%10d", $count));
		}
		clrtoeol($winProgress);
		refresh($winProgress);
	}
}

sub drawTile {
	my ($xy, $char, $noRefresh) = @_;
	addstring($winDebug, $xy->y, $xy->x, $char);
	$winDebug->move(0,0);
	refresh($winDebug) unless ($noRefresh);
	Time::HiRes::usleep($BOARD_LAG);
}
sub BOARD {
	$BOARD = shift;
	if ($GUI) {
		$DEBUG=0;
		erase($winDebug);
		$winDebug->leaveok(0);
		for (my $y = 0; $y < $BOARD->getSizeY(); $y++) {
			for (my $x = 0; $x < $BOARD->getSizeX(); $x++) {
				my $pos = XY($x, $y);
				&drawTile($pos, chr($BOARD->getAt($pos)), 1);
			}
		}
		refresh($winDebug);
		$BOARD->setDrawFunction(\&drawTile);
	}
	else {
		binmode(STDOUT, ":encoding(UTF-8)");
		DEBUG "%s", $BOARD->toString();
	}
	#sleep 2;
}
sub BOARD_PAUSE {
	my $sleep = shift;
	sleep $sleep if ($GUI);
}

my $WTITLEY	=	 1;
my $WSTATY	=	 8;
my $WMAINY	= 10;
my $WPROGX	= 20;

sub Init {
	$Year = shift;
	$Day = shift;
	my @args = @_;

	STATUS "************ AOC %4d-%2d : %s ***", $Year, $Day, $NAME;

	$DEBUG = 0 if ($args[0] && $args[0] eq 'NODEBUG');
	$DEBUG = 1 if ($args[0] && $args[0] eq 'DEBUG');
	$DEBUG = 2 if ($args[0] && $args[0] eq 'TRACE');

	# Get input file (if not already available)
	$InputFile = "$Year/input/$Day.input";
	AOC::getMyInput($Year, $Day, $InputFile);
	my $statfile = "$Year.stat";
	$Statistics = retrieve $statfile if (-r $statfile);

	$GUI = 1 if ($CURSES && (($args[0] && $args[0] eq 'GUI') || ($args[1] && $args[1] eq 'GUI')));

	if($GUI) {
		initscr();
		$winTitle   = newwin($WTITLEY, $Curses::COLS - $WPROGX - 1, 0, 0);
		$winProgress = newwin($WTITLEY, $WPROGX, 0, $Curses::COLS - $WPROGX);
		$winStatus   = newwin($WSTATY, $Curses::COLS, $WTITLEY + 1, 0);
		$winMain     = newwin($WMAINY, $Curses::COLS, $WSTATY+$WTITLEY+2, 0); # stdscr() 
		$winDebug    = newwin($Curses::LINES-$WTITLEY-$WSTATY-$WMAINY-3, $Curses::COLS, $WTITLEY + $WSTATY + $WMAINY + 2, 0);
		$winStatus->scrollok(1);
		$winMain->scrollok(1);
		$winDebug->scrollok(1);
		#addstring($winStatus, "STATUS");
		#addstring($winMain, "MAIN\n");
		#addstring($winDebug, "DEBUG\n");
		#refresh($winStatus);
		#refresh($winMain);
		#refresh($winDebug);
		TITLE "************ AOC %4d-%2d : %s ***", $Year, $Day, $NAME;
		$BOARD_LAG=0;
	}
}



sub Test {
	my ($rSolver, $rTests) = @_;

	my $startTime = Time::HiRes::time;
	foreach my $rTest (@$rTests) {
		STATUS "*** [%4d-%2d] Running test [%s]", $Year, $Day, $rTest->{NAME};

		my $runPart = 'ALLPARTS';
		$runPart    = 'PART2ONLY' unless (exists $rTest->{RESULT1});
		$runPart    = 'PART1ONLY' unless (exists $rTest->{RESULT2});

		open my $inputFh, "<", \$rTest->{INPUT} or die "Cannot open test input, $!";
		my ($result1, $result2) = &$rSolver($inputFh, $runPart, $rTest->{ATTRIBUTE1}, $rTest->{ATTRIBUTE2});
		close $inputFh;
		STATUS "TEST [$rTest->{NAME}]: PART1 [%d] - PART2 [%d]", $result1, $result2;

		if ((exists $rTest->{RESULT1} && $result1 != $rTest->{RESULT1}) || (exists $rTest->{RESULT2} && $result2 != $rTest->{RESULT2})) {
			STATUS " FAILED. Expected: [%s] [%s]\n", 
				exists $rTest->{RESULT1} ? $rTest->{RESULT1} : "-" , 
				exists $rTest->{RESULT2} ? $rTest->{RESULT2} : "-" ;
			exit;
		}
		#STATUS " SUCCESS.";
	}
	my $duration = Time::HiRes::time - $startTime;
	STATUS "**************** Test time %.3f *****************", $duration;
	$Statistics->{$Day}{NROFTESTS} = scalar @$rTests;
	$Statistics->{$Day}{TESTTIME} = $duration;
}

sub Solve {
	my $rSolver = shift;

	STATUS "!!! [%4d-%2d] Running real puzzle [$InputFile]", $Year, $Day;
	open my $inputFh, "<", $InputFile or die "Cannot open [$InputFile]: $!";
	my $startTime = Time::HiRes::time;
	my ($result1, $result2) = &$rSolver($inputFh);
	my $duration = Time::HiRes::time - $startTime;
	close $inputFh;
	STATUS "RESULT [Puzzle $Year/$Day]: PART1 [%d] - PART2 [%d]", $result1, $result2;
	STATUS "!!!!!!!!!!!!! Solving time %.3f !!!!!!!!!!!!!!!", $duration;

	$Statistics->{$Day}{SOLVETIME} = $duration;
	$Statistics->{$Day}{NAME} = $NAME;
	$Statistics->{$Day}{DIFFICULTY} = $DIFFICULTY;
	$Statistics->{$Day}{TIMEUSED} = $TIMEUSED;
	$Statistics->{$Day}{LEARNED} = $LEARNED;
	my $statfile = "$Year.stat";
	store $Statistics, $statfile;
}

# Download a day's input
sub getMyInput { my ($year, $day, $fname) = @_;
	# Check if already downloaded
	if (-e $fname) {
		TRACE("AOC getMyInput: [$fname] already available");
		return;
	}

	# Make sure puzzle is available: 06:00 CET
	my $now = time; #my $now = timelocal(59, 59, 05, 07 , 11, 2023);
	my $puzzleTime = timegm(0, 0, 5, $day, 11,$year-1900);
	#DEBUG "getMyInput now [%s - %d], puzzle [%s - %d]", scalar(localtime($now)), $now, scalar(localtime($puzzleTime)), $puzzleTime;
	if ($now < $puzzleTime) {
		DEBUG("AOC getMyInput: [$fname] not yet available, wait for another %d seconds", $puzzleTime - $now);
		return;
	}

	if (! $ENV{AOC_SESSION}) {
		INFO("AOC getMyInput: no session key set in 'ENV{AOC_SESSION}'");
		return;
	}

	my $inputUrl = sprintf $AocUrl, $year, $day;
    $inputUrl = "http://localhost:1234/2015/day/11/input";
	INFO("AOC getMyInput: reading input for $year, $day: [$inputUrl] -> [$fname]");

	open(FH, '>', $fname) or die $!;
	print FH getUrl($inputUrl, $ENV{AOC_SESSION});
	close FH;
}

sub getUrl { my ($url, $session) = @_;
  DEBUG "Downloading [$url]... ";
  if (HTTP::Tiny::can_ssl()) {
    my $response = HTTP::Tiny->new->get($url, { headers => {"Cookie" => "session=$session"} } );
    DEBUG "$response->{status} $response->{reason}";
    # while ( my ( $k, $v ) = each %{ $response->{headers} } ) {
    # 		for ( ref $v eq 'ARRAY' ? @$v : $v ) {
    # 				print "$k: $_\n";
    # 		}
    # }
    return $response->{content};
  }
  else {
    my $curlCmd = "curl -s --header \"Cookie: session=$session\" $url";
    my $response = `$curlCmd` || INFO "Could not curl [$url]";
    return $response;
  }
}
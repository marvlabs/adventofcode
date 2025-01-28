use strict;
use warnings;
use Scalar::Util 'blessed';
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");

use Test::Simple tests => 33;
use XY::XY qw(XY);
use XY::Board;

##################
# XY Tests
my $xy1 = XY::XY->new(x=>5, y=>3);

ok blessed($xy1) eq "XY::XY",					"Blessed XY class";
ok $xy1->x() == 5,										"XY getter X";
ok $xy1->y() == 3,										"XY getter Y";

ok XY(11,21)->toString() eq "[11/21]", "XY XY constructor";

my $xy2 = XY(2,2);
my $xyResult = $xy1->add($xy2);
ok $xyResult->x() == 7 && $xyResult->y() == 5,	"XY add";

$xyResult = $xyResult->subt($xy2);
ok $xyResult->x() == 5 && $xyResult->y() == 3,	"XY subt";
ok $xyResult->equal($xy1),											"XY equal";
ok $xy1->copy()->equal($xy1),										"XY copy";
ok $xyResult->toString() eq "[5/3]",						"XY toString";

$xyResult = $xy1->add(XY::XY::aim('N'));
ok $xyResult->toString() eq "[5/2]",						"XY head north";
ok $xyResult->add(XY::XY::aim('E'))->add(XY::XY::aim('S'))->add(XY::XY::aim('W'))->equal($xy1), "XY east south west";

ok XY::XY::aim('NE')->mult(3)->toString() eq "[3/-3]",	"XY mult";
ok $xy1->neighbours()->{'NE'}->toString() eq "[6/2]",		"XY Neighbours";

##################
# Board Tests
my ($dimX, $dimY) = (10, 15);
my $cEmpty	= $XY::Board::cEmpty;
my $cFull		= 1;
my $c2			= 2;
my $c3			= 3;
my $c4			= 4;

my $board = XY::Board->new($dimX, $dimY, $cEmpty);

ok blessed($board)    eq "XY::Board",	"Blessed Board class";
ok $board->getSizeX() == $dimX,				"Board getter X";
ok $board->getSizeY() == $dimY,				"Board getter Y";
ok $board->area()     == $dimX*$dimY,	"Board area";

ok $board->valid($XY::XY::zero) && !$board->valid($XY::XY::north),			"Board valid";
ok $board->getAt($xy1)   eq $cEmpty,	"Board one tile";
$board->setAt($xy1, $cFull);
ok $board->getAt($xy1)   eq $cFull,		"Board one tile";

$board->moveRel($xy1, $XY::XY::ne, $cEmpty);
ok $board->getAt($xy1->add(XY::XY::aim('NE'))) eq $cFull && $board->getAt($xy1) eq $cEmpty,	"Board move";

ok $board->isEmpty($xy1),							"Board isEmpty";
$board->setAt($xy2, $c2);
ok $board->is($xy2, $c2),							"Board is";

ok join('', map ({ chr($_+ ord 'a') } $board->getRowValues(2))) eq "aacaaabaaa",			"Board getRowValues";
ok join('', map ({ chr($_+ ord 'a') } $board->getColValues(2))) eq "aacaaaaaaaaaaaa",	"Board getColValues";

ok $board->neighbours(XY(2,1))->{'S'} == $c2,	"Board neighbours";

$board->setAll([values(%{$xy2->neighbours()})], $c3);
$board->setAll([values(%{$xy1->directNeighbours()})], $c4);
ok $board->is($xy2->add(XY::XY::aim('NE')), $c3) && $board->is($xy1->add(XY::XY::aim('NE')), $cFull) && $board->is($xy1->add(XY::XY::aim('W')), $c4),							"Board setAll";

$board->setAll([values(%{$XY::XY::zero->neighbours()})], $c4);
ok $board->is($xy2->add(XY::XY::aim('NW')), $c4),	"Board neighbours border";

$board->placeBoard(XY::Board->new(3, 5, $cFull), XY(8,7), $cFull);
ok $board->is(XY(8,7), $cFull),	"Board placeBoard at border";

$board = $board->resize($dimX+5, $dimY+2, XY(1,1), $c2);
ok $board->is($XY::XY::zero, $c2) && $board->is(XY(7,3), $cFull),	"Board resize";
ok $board->rowIs(0, $c2) && !$board->rowIs(1, $c2),																"Board rowIs";
ok $board->colIs(0, $c2) && !$board->colIs(1, $c2),																"Board colIs";

### Print the board
binmode(STDOUT, ":encoding(UTF-8)");
printf ("Board: %d x %d :\n%s", $board->getSizeX(), $board->getSizeY(), $board->toString());
my $board90 = $board->rotate90();
ok $board90->is(XY(13,7), $cFull),	"Board rotate 90";

### Print the board
binmode(STDOUT, ":encoding(UTF-8)");
printf ("Board: %d x %d :\n%s", $board90->getSizeX(), $board90->getSizeY(), $board90->toString());

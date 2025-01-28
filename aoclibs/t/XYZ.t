use strict;
use warnings;
use Scalar::Util 'blessed';
use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");

use Test::Simple tests => 5;
use XY::XYZ qw(XYZ);

##################
# XY Tests
my $xyz1 = XY::XYZ->new(x=>5, y=>3, z=>2);

ok blessed($xyz1) eq "XY::XYZ",					"Blessed XYZ class";
ok $xyz1->x() == 5,										"XYZ getter X";
ok $xyz1->y() == 3,										"XYZ getter Y";
ok $xyz1->z() == 2,										"XYZ getter Z";

ok XYZ(11,21,42)->toString() eq "[11/21/42]", "XY XYZ constructor";

__END__
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


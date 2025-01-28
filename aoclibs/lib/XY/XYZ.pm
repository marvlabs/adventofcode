package XY::XYZ;
use strict;
use warnings;

use parent 'Exporter';

use lib ("$ENV{HOME}/dev/div/adventofcode/aoclibs/lib", "$ENV{HOME}/AdventOfCode/lib");
use XY::XY qw(XY);

our @EXPORT_OK = qw(XYZ);

BEGIN {  
}
END {
	# printf "DEBUG XY::XY CLASS END: EXPORT_OK [%s]\n", join (":", (@EXPORT_OK));
	# printf "DEBUG XY::XY CLASS END: EXPORT    [%s]\n", join (":", (@EXPORT));
	# printf "DEBUG XY::XY CLASS END: ISA       [%s]\n", join (":", (@ISA));
}
# Constructor method to create a new object of the class
sub new { my ($class, %args) = @_;
	my $self = {
		x => $args{x},
		y => $args{y},
		z => $args{z},
	};
	# Bless the reference as an object of the class
	bless $self, $class;
	return $self;
}
sub x { my ($self) = @_;
	return $self->{x};
}
sub y { my ($self) = @_;
	return $self->{y};
}
sub z { my ($self) = @_;
	return $self->{z};
}
sub xy { my ($self) = @_;
	return XY($self->x(), $self->y());
}
## Constants
our $zero  = XY::XYZ->new(x =>  0, y =>  0, z =>  0);
our $up    = XY::XYZ->new(x =>  0, y =>  0, z =>  1);
our $down  = XY::XYZ->new(x =>  0, y =>  0, z => -1);

# Class method
# sub aim { my ($direction) = @_;
# 	return $compassFull{$direction};
# }
sub down { return $down; }
sub up   { return $up;   }

########
## Methods
# Alternate constructor: instead of XY::XY->new(x=>$x, y=>$y) it's shorter to use XY($x, $y) (if imported via: use XY::XY qw(XY);)
sub XYZ { my ($x, $y, $z) = @_;
	return XY::XYZ->new(x=>$x, y=>$y, z=>$z);
}

sub copy { my ($self) = @_;
	return $self->add($zero);
}

sub add { my ($self, $xyz2) = @_;
	ref($xyz2) ne "XY::XYZ" && die "XY::XYZ::add called with non-XYZ";
	return XYZ($self->x() + $xyz2->x(), $self->y() + $xyz2->y(), $self->z() + $xyz2->z());
}

sub subt { my ($self, $xyz2) = @_;
	return XYZ($self->x() - $xyz2->x(), $self->y() - $xyz2->y(), $self->z() - $xyz2->z());
}
sub manhattanDist { my ($self, $xyz2) = @_;
	return (abs($self->x() - $xyz2->x()) + abs($self->y() - $xyz2->y()) + abs($self->z() - $xyz2->z()));
}

sub mult { my ($self, $f) = @_;
	return XYZ($self->x() * $f, $self->y() * $f, $self->z() * $f);
}

sub equal { my ($self, $xyz2) = @_;
	return $self->x() == $xyz2->x() && $self->y() == $xyz2->y() && $self->z() == $xyz2->z();
}

# # perform multiple add on this XY with a list of operands, returning all results
# sub addList { my ($self, $rList) = @_;
# 	my %result;
# 	while(my($key, $xy) = each %$rList) {
# 		$result{$key} = $self->add($xy);
# 	}
# 	return \%result;
# }

# sub neighbours { my ($self) = @_;
# 	return $self->addList(\%compassFull);
# }
# sub directNeighbours { my ($self) = @_;
# 	return $self->addList(\%compassMain);
# }


sub toString { 	my $self = shift;
	sprintf("[%d/%d/%d]", $self->x(), $self->y(), $self->z());
}


1;
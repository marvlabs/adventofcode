package XY::XY;
use strict;
use warnings;

use parent 'Exporter';
our @EXPORT_OK = qw(XY);

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
## Constants
our $zero  = XY::XY->new(x =>  0, y =>  0);
our $north = XY::XY->new(x =>  0, y => -1 );
our $east  = XY::XY->new(x =>  1, y =>  0 );
our $south = XY::XY->new(x =>  0, y =>  1 );
our $west  = XY::XY->new(x => -1, y =>  0 );
our $ne = $north->add($east);
our $nw = $north->add($west);
our $se = $south->add($east);
our $sw = $south->add($west);

my %compassMain = (
	'N'  => $north,
	'E'  => $east,
	'S'  => $south,
	'W'  => $west,
);

my %compassFull = (
	%compassMain,
	'NE' => $ne,
	'SE' => $se,
	'SW' => $sw,
	'NW' => $nw,
);

# Class method
sub aim { my ($direction) = @_;
	return $compassFull{$direction};
}

########
## Methods
# Alternate constructor: instead of XY::XY->new(x=>$x, y=>$y) it's shorter to use XY($x, $y) (if imported via: use XY::XY qw(XY);)
sub XY { my ($x, $y) = @_;
	return XY::XY->new(x=>$x, y=>$y);
}

sub copy { my ($self) = @_;
	return $self->add($zero);
}

sub add { my ($self, $xy2) = @_;
	#ref($xy2) ne "XY::XY" && die "XY::XY::add called with non-XY";
	return XY($self->x() + $xy2->x(), $self->y() + $xy2->y());
}

sub subt { my ($self, $xy2) = @_;
	return XY($self->x() - $xy2->x(), $self->y() - $xy2->y());
}
sub manhattanDist { my ($self, $xy2) = @_;
	return (abs($self->x() - $xy2->x()) + abs($self->y() - $xy2->y()));
}

sub mult { my ($self, $f) = @_;
	return XY($self->x() * $f, $self->y() * $f);
}

sub equal { my ($self, $xy2) = @_;
	return $self->x() == $xy2->x() && $self->y() == $xy2->y();
}

# perform multiple add on this XY with a list of operands, returning all results
sub addList { my ($self, $rList) = @_;
	my %result;
	while(my($key, $xy) = each %$rList) {
		$result{$key} = $self->add($xy);
	}
	return \%result;
}

sub neighbours { my ($self) = @_;
	return $self->addList(\%compassFull);
}
sub directNeighbours { my ($self) = @_;
	return $self->addList(\%compassMain);
}


sub toString { 	my $self = shift;
	sprintf("[%d/%d]", $self->x(), $self->y());
}


1;
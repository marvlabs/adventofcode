package XY::Board;
use strict;
use warnings;
use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw();
our @EXPORT_OK = qw();

use XY::XY qw(XY);;

# Start, Exit
BEGIN {
}
END {
}

#############
## Constants
our $cEmpty = 0;


#############
# Constructor method to create a new object of the class
sub new { my $class = shift;
	my $self = {
		_sizeX => shift,
		_sizeY => shift,
		_initC => shift || $cEmpty
	};
	# Bless the reference as an object of the class
	bless $self, $class;
	$self->init();
	return $self;
}

# Init
sub init { my ($self) = @_;
	#$self->{newVar} = 42;
	$self->{tiles} = [ ($self->{_initC}) x $self->area() ];

	$self->{outputMap} = {
		0				=> chr(128998), # https://www.w3schools.com/charsets/ref_utf_geometric.asp
		1				=> chr(128997),
		2				=> chr(128994),
		3				=> chr(129002),
		4				=> chr(129003),
	};
}

# Set an external hook function for drawing one field
# If such a function is set, it gets called with the x/y and value every time a field changes (needs to be redrawn)
# Used to hook in an external GUI for printing out the board instead of stdout'ing.
sub setDrawFunction {
	my ($self, $rDrawFunc) = @_;
	$self->{_drawTile} = $rDrawFunc;
}

sub setTiles { my ($self, $initStr) = @_;
	length($initStr) == $self->area() || return undef;
	# print "DEBUG setTiles: ", map(ord, (split //, $initStr)), "\n";
	$self->{tiles} = [ map ( ord, ( split //, $initStr))  ];
	# printf "DEBUG setTiles at 0: %d\n", @{$self->{tiles}}[0];
	# printf "DEBUG setTiles ref: %s\n", ref $self->{tiles};
	# printf "DEBUG setTiles size: %s\n", scalar @{$self->{tiles}};
}

# sub initWindow {
# 	my ($self) = @_;
# 	initscr;
# 	$self->{win} = stdscr; # newwin($LINES, $COLS, 0, 0,40); 
# 	addstr(30,20, sprintf "╮╮╮SCREEN %d x %d", $Curses::COLS, $Curses::LINES );
# 	refresh($self->{win});
# }
# sub toWin { 	my $self = shift;
# 	#print "TO WIN called\n";
# 	addstr(30,40, "...drawing...");
# 		refresh($self->{win});

# 	for (my $y = 0; $y < $self->getSizeY(); $y++) {
# 		for (my $x = 0; $x < $self->getSizeX(); $x++) {
# 			addch($y, $x, $self->mapValue($self->getAt(XY::XY->new(x=>$x, y=>$y))));
# 		}
# 	}
# 	refresh($self->{win});
# }
#############
# helpers
sub _idx { my ($self, $xy) = @_;
	return $xy->x() + $self->getSizeX()*$xy->y();
}
#############
# methods
sub area { my ($self) = @_;
	return $self->{_sizeX} * $self->{_sizeY};
}

sub valid { my ($self, $xy) = @_;
	return $self->validX($xy->x()) && $self->validY($xy->y());
}
sub validX { my ($self, $x) = @_;
 	return $x >= 0 && $x < $self->{_sizeX};
}
 sub validY { my ($self, $y) = @_;
 	return $y >= 0 && $y < $self->{_sizeY};
 }

sub getAt { my ($self, $xy) = @_;
	$self->valid($xy) || return undef;
	return @{$self->{tiles}}[$self->_idx($xy)];
}
sub setAt { my ($self, $xy, $char) = @_;
	$self->valid($xy) || return undef;
	@{$self->{tiles}}[$self->_idx($xy)] = $char;
	
	# if (defined $self->{win}) {
	# 	Curses::addstring($xy->y, $xy->x, chr($char));
	# 	refresh($self->{win});
	# }
	if (defined $self->{_drawTile}) {
		&{$self->{_drawTile}}($xy, chr($self->getAt($xy)));
	}
}
sub setAll { my ($self, $rFields, $char) = @_;
	foreach (@$rFields) {
		$self->setAt($_, $char);
	}
}

sub is { my ($self, $xy, $char) = @_;
	$self->valid($xy) || return undef;
	return $self->getAt($xy) == $char;
}
sub isEmpty { my ($self, $xy) = @_;
	$self->valid($xy) || return undef;
	return $self->is($xy, $cEmpty)
}

sub rowIs { my ($self, $y, $char) = @_;
	$self->validY($y) || return undef;
	for (my $x = 0; $x < $self->getSizeX(); $x++) {
		return 0 unless $self->is(XY::XY->new(x=>$x, y=>$y), $char);
	}
	return 1;
}
sub colIs { my ($self, $x, $char) = @_;
	$self->validX($x) || return undef;
	for (my $y = 0; $y < $self->getSizeY(); $y++) {
		return 0 unless $self->is(XY::XY->new(x=>$x, y=>$y), $char);
	}
	return 1;
}

sub getRowValues { my ($self, $y) = @_;
	$self->validY($y) || return undef;
	my @values;
	for (my $x = 0; $x < $self->getSizeX(); $x++) {
		push @values, $self->getAt(XY($x, $y));
	}
	return @values;
}
sub getColValues { my ($self, $x) = @_;
	$self->validX($x) || return undef;
	my @values;
	for (my $y = 0; $y < $self->getSizeY(); $y++) {
		push @values, $self->getAt(XY($x, $y));
	}
	return @values;
}


sub moveTo { my ($self, $xy, $newXy, $char) = @_;
	$self->valid($xy) || return undef;
	$self->valid($newXy) || return undef;
	$self->setAt($newXy, $self->getAt($xy));
	$self->setAt($xy, $char);
}
sub moveRel { my ($self, $xy, $diffXy, $char) = @_;
	$self->moveTo($xy, $xy->add($diffXy), $char);
}


sub neighbours { my ($self, $xy) = @_;
	my %result;
	my $rFieldsAround = $xy->neighbours();
	while(my($key, $field) = each %$rFieldsAround) {
		my $char = $self->getAt($field);
		#printf("Debug Board neighbours: field %s %s is %d\n", $key, $field->toString(), $char);
		$result{$key} = $char if $char;
	}
	return \%result;
}
sub directNeighbours { my ($self, $xy) = @_;
	my %result;
	my $rFieldsAround = $xy->directNeighbours();
	while(my($key, $field) = each %$rFieldsAround) {
		my $char = $self->getAt($field);
		#printf("Debug Board neighbours: field %s %s is %d\n", $key, $field->toString(), $char);
		$result{$key} = $char if $char;
	}
	return \%result;
}

# Copy another board into our space at xy
sub placeBoard { my ($self, $board, $xy) = @_;
	#printf("Debug Board placeBoard: place %s, board %d x  %d\n", $xy->toString(), $board->getSizeX(), $board->getSizeY());
	for (my $y = 0; $y < $board->getSizeY(); $y++) {
		for (my $x = 0; $x < $board->getSizeX(); $x++) {
			my $field = XY::XY->new(x=>$x, y=>$y);
			#printf("Debug Board placeBoard: source field %s, target field %s, value %d\n", $field->toString(), $xy->add($field)->toString(), $board->getAt($field));
			$self->setAt($xy->add($field), $board->getAt($field));
		}
	}
}

# Return copy
sub duplicate { my $self = shift;
	return $self->resize($self->getSizeX(), $self->getSizeY(), XY(0,0));
}

# Create new board and place old board at xy -> like a resize
sub resize { my ($self, $sizeX, $sizeY, $xy, $char) = @_;
	my $newBoard = XY::Board->new($sizeX, $sizeY, $char);
	$newBoard->placeBoard($self, $xy);
	return $newBoard;
}

# Flip the board clockwise
sub rotate90 { my $self = shift;
	my $newBoard = XY::Board->new($self->getSizeY(), $self->getSizeX());
	for (my $y = 0; $y < $self->getSizeY(); $y++) {
		for (my $x = 0; $x < $self->getSizeX(); $x++) {
			$newBoard->setAt(XY($newBoard->getSizeX() - $y - 1, $x), $self->getAt(XY($x, $y)));
		}
	}
	return $newBoard;
}

# sub printBoard {
# 	my $self = shift;
# 	if (defined $self->{_drawTile}) {
# 		for (my $y = 0; $y < $self->getSizeY(); $y++) {
# 			for (my $x = 0; $x < $self->getSizeX(); $x++) {
# 				my $pos = XY($x, $y);
# 				&{$self->{_drawTile}}($pos, chr($self->getAt($pos)));
# 			}
# 		}
# 	}
# 	else {
# 		return $self->toString();
# 	}
# }

sub toString { my $self = shift;
	my $str;
	for (my $y = 0; $y < $self->getSizeY(); $y++) {
		for (my $x = 0; $x < $self->getSizeX(); $x++) {
			$str .= $self->mapValue($self->getAt(XY::XY->new(x=>$x, y=>$y)));
		}
		$str .= "\n";
	}
	return $str;
}

sub mapValue { my ($self, $val) = @_;
	#printf("DEBUG mapValue: val [$val]\n");
	return $self->{outputMap}{$val} if exists $self->{outputMap}{$val};
	return chr($val);
}
sub setOutputMapping { my ($self, $rMap) = @_;
	$self->{outputMap} = $rMap;
}



#############
# Accessors
sub getSizeX { 	my ($self) = @_; 	return $self->{_sizeX}; }
sub getSizeY { 	my ($self) = @_; 	return $self->{_sizeY}; }
#sub getArea  { 	my ($self) = @_; 	return $self->{_area}; }


#############
# End of package declaration, required in Perl ('use' and 'require' will eval the code, thus they need a success exit code)
1;



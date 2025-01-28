#!python3
'''Grid class for two dimensional field problems
base: (x,y) tuples for coordinates
'''
_DIR4 = { 'E' : (1,0), 'S' : (0,1), 'W' : (-1,0), 'N' : (0,-1), }
_DIR8 = _DIR4.copy()
_DIR8.update({ 'NE' : (1,-1), 'NW' : (-1,-1), 'SE' : (1,1), 'SW' : (-1,1), })

def go(dir) :
    return _DIR8[dir]

def step(pos, dir) :
    return (pos[0]+go(dir)[0], pos[1]+go(dir)[1])


class Grid:
    def __init__(self, x, y, val=None):
        self.dim_x = x
        self.dim_y = y
        self._rows = [ [val]*x for _ in range(y) ]
    
    @classmethod
    def from_string(cls, init_string):
        row_list = [ row for row in init_string.splitlines() if row != '' ]
        g = cls(len(row_list[0]), len(row_list))
        for i, row in enumerate(row_list):
            g.set_row(i, list(row))
        return g

    @classmethod
    def from_grid(cls, g):
        g_new = cls(g.dim_x, g.dim_y)
        for i, row in enumerate(g._rows):
            g_new._rows[i] = row.copy()
        return g_new

    def copy(self) :
        return Grid.from_grid(self)

    def set_row(self, y, l) :
        self._rows[y] = l

    def valid_x(self, x):
        return x >= 0 and x < self.dim_x

    def valid_y(self, y):
        return y >= 0 and y < self.dim_y
    
    def valid(self, pos):
        return self.valid_x(pos[0]) and self.valid_y(pos[1])

    def is_border(self, pos):
        return pos[0] == 0 or pos[1] == 0 or pos[0] == self.dim_x-1 or pos[1] == self.dim_y-1

    def set(self, pos, val):
        self._rows[pos[1]][pos[0]] = val

    def get(self, pos):
        return self._rows[pos[1]][pos[0]] if self.valid(pos) else None

    '''get all values from pos in direction dir'''
    def get_line(self, pos, dir) :
        line = ''
        while self.valid(pos) :
            line += self.get(pos)
            pos = step(pos, dir)
        return line

    def at_is(self, pos, val):
        return self.get(pos) == val
    
    def all_pos(self):
        return ((x,y) for x in range(self.dim_x) for y in range(self.dim_y))

    def neighbours(self, pos):
        return { dir: self.get(step(pos, dir)) for dir in _DIR8.keys() }

    def neighbours90(self, pos):
        return { dir: self.get(step(pos, dir)) for dir in _DIR4.keys() }

    def neighbour_pos(self, pos):
        return { dir: step(pos, dir) for dir in _DIR8.keys() }

    def __str__(self):
        return '\n'.join(''.join(row) for row in self._rows ) 
        
class SparseGrid(Grid):
    pass




#############
if __name__ == '__main__' :
    pos = (0,0)
    pos = step(pos,'SE')
    assert pos == (1,1)

    g = Grid(5,3, 'o')
    assert g.is_border((0,2))
    g.set(pos, 'x')
    assert g.get(pos) == 'x'
    assert g.get_line(pos, 'E') == 'xooo'
    assert g.get_line(pos, 'NW') == 'xo'
    assert g.neighbours(step(pos, 'E'))['W'] == 'x'
    assert g.valid(pos)
    assert not g.valid((g.dim_x, g.dim_y))
    assert not g.valid((-1, -1))

    g2_string = '''
.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''
    g2 = Grid.from_string(g2_string)
    assert g2.get((5,5)) == '.'
    assert g2.get((1,0)) == '#'
    g2.set(pos, '=')
    g3 = g2.copy()
    g3.set(pos, 'X')
    assert g2.get(pos) == '='
    assert g3.get(pos) == 'X'
    assert g3.get((5,5)) == '.'
    assert g3.get((1,0)) == '#'
    assert g3.at_is(pos, 'X')
    assert not g3.at_is(pos, '=')
    #print(g3);



# naglib screen: pygame implementation
import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from time import sleep
import itertools as it
from os import system
import tempfile

class AnimGrid:

    def __init__(self, screen, x, y, use_chars=True, status_area=0, title=None,  movie=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.title = title
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.scale = screen.width // x
        self.use_chars = use_chars
        self.color_map = { '.': 'GRAY', '#': 'ORANGE', 'X': 'TEAL', ' ': 'DARK_GRAY', 'default': 'PINK' }
        self.movie = movie
        if movie:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.frame = 0

    def __repr__(self):
        return(f'x={self.x}, y={self.y}, radius={self.radius}, color={self.color}')


    def set(self, pos, value):
        self.fields[pos] = value

    def draw(self, g, delay=50, text=None):
        self.screen.clear()
        if self.title:
            self.screen.status_text(self.title, 10, self.screen_height - 40, 'YELLOW')
        if text:
            self.screen.status_text(text, 10, self.screen_height - 20, 'WHITE')
        for pos in g.all_pos():
            color = self.color_map.get(g.get(pos), self.color_map['default'])
            #self.screen.circle(pos[0]*self.scale+self.scale//2, pos[1]*self.scale+self.scale//2, self.scale//2, color)
            self.screen.square(pos[0]*self.scale+1, pos[1]*self.scale+1, self.scale-2, color)
            if self.use_chars: 
                self.screen.text(g.get(pos), pos[0]*self.scale+self.scale//5, pos[1]*self.scale+self.scale//5, 'WHITE')
        self.show()
        if delay > 1000 :
            for i in range(delay//33) :
                self.show()
                sleep(0.030)
        else:
            sleep(delay/1000)

    def show(self):
        self.screen.show()
        if self.movie:
            self.screen.save(f'{self.temp_dir.name}/frame_{self.frame:08d}.png')
            self.frame += 1
    
    def save_movie(self, fps=30):
        if self.movie:
            #system(f'ls -alrt {self.temp_dir.name}/')
            system(f'ffmpeg -framerate {fps} -i {self.temp_dir.name}/frame_%08d.png -y -c:v libx264 -pix_fmt yuv420p {self.movie}.mp4')



class Screen ():

    def __init__(self, width, height, name='naglib pygame screen', fontsize=10):
        print("DEBUG: naglib_screen_pygame: Screen init")
        self.width = width
        self.height = height
        self.name = name
        self.lcd = pygame.display.set_mode((width, height))
        self.font = pygame.freetype.Font(None, fontsize)
        self.status_font = pygame.freetype.Font(None, 15)
        pygame.display.set_caption(name)

    def fill(self, color):
        self.lcd.fill(COLORS[color])

    def clear(self):
        self.fill("BLACK")

    def text(self, text, x, y, color):
        self.font.render_to(self.lcd, (x, y), text, COLORS[color])

    def status_text(self, text, x, y, color):
        self.status_font.render_to(self.lcd, (x, y), text, COLORS[color])

    def square(self, x, y, width, color):
        pygame.draw.rect(self.lcd, COLORS[color], pygame.Rect(x, y, width, width))

    def circle(self, x, y, radius, color):
        pygame.draw.circle(self.lcd, COLORS[color], (x, y), radius)

    def polygon(self, x, y, points, color):
        #pygame.draw.aalines(self.lcd, COLORS[color], False, translate(points, x, y))
        pygame.draw.polygon(self.lcd, COLORS[color], translate(points, x, y))

    def show(self):
        pygame.display.update()
        #pygame.event.pump()
        for event in pygame.event.get():
            if(event.type == QUIT):
                raise KeyboardInterrupt

    def save(self, filename):
        pygame.image.save(self.lcd, filename)

    def finish(self):
        pygame.quit()
        #sys.exit(0)


def translate(points, tx, ty):
    return [(x+tx,y+ty) for (x,y) in points]

def scale(points, factor):
    return [(x*factor,y*factor) for (x,y) in points]

# Color is RGBA (constructed here from RGB)
COLORS = { name: pygame.Color(rgb) for name, rgb in THECOLORS.items() }

###
print("DEBUG: naglib_screen_pygame: pygame init")
pygame.init()



COLORS =  {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "DARK_BLUE": (0, 0, 150),
    "YELLOW": (255, 255, 0),
    "CYAN": (0, 255, 255),
    "MAGENTA": (255, 0, 255),
    "ORANGE": (255, 165, 0),
    "PURPLE": (128, 0, 128),
    "PINK": (255, 192, 203),
    "BROWN": (165, 42, 42),
    "GRAY": (128, 128, 128),
    "DARK_GRAY": (64, 64, 64),
    "LIGHT_GRAY": (192, 192, 192),
    "BEIGE": (245, 245, 220),
    "TEAL": (0, 128, 128),
    "CORAL": (255, 127, 80),
    "SALMON": (250, 128, 114),
    "TURQUOISE": (64, 224, 208)
}

def make_color_gradient(name, start, end, nr=10):
    colors = {}
    
    #rg = lambda a,b : [a + (b-a)//nr*x for x in range(nr)]
    #color_rg = lambda c1, c2, channel : rg(COLORS[c1][channel], COLORS[c2][channel])
    #for i, color in enumerate(zip(color_rg(start, end, 0), color_rg(start, end, 1), color_rg(start, end, 2))):
    #    colors[f'{name}_{i}'] = color

    c_start_r, c_start_g, c_start_b = COLORS[start]
    c_end_r, c_end_g, c_end_b = COLORS[end]
    for i in range(nr):
        colors[f'{name}_{i}'] = (c_start_r+i*(c_end_r-c_start_r)//nr, c_start_g+i*(c_end_g-c_start_g)//nr, c_start_b+i*(c_end_b-c_start_b)//nr)

    return colors


if __name__ == '__main__' :
    from grid import Grid, step
    g = Grid.from_string('''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
''')
    
    Turns = {
        'N' : 'E',
        'E' : 'S',
        'S' : 'W',
        'W' : 'N',
    }

    #print(make_color_gradient('gb', 'GREEN', 'BLUE'))

    anim = AnimGrid(Screen(500,550, 'Test', fontsize=500/g.dim_x/2), g.dim_x, g.dim_y, use_chars=True, status_area=50, title='Grid Animation Test')
    anim.color_map = { '.': 'DARK_GRAY', '#': 'ORANGE', 'X': 'TEAL', 'default': 'PINK' }
    try: 
        pos = (4,6)
        dir = 'N'
        count = 0
        while True:
            count += 1
            anim.draw(g, 10, f'{count:6d} ({pos[0]:3}, {pos[1]:3})')

            been_here = {} # Store all positions we've gone through with the direction
            pos_dir = lambda : pos+(dir,) # Tuple as key is faster than creating string keys like : f'{pos[0]}{pos[1]}{dir}'
            
            g.set(pos, 'X')
            been_here[pos_dir()] = True
            next_pos = step(pos, dir)
            if not g.valid(next_pos) :
                #print (f'guard_walk: out of bounds at {pos}, {dir} after {steps}')
                continue
            if g.at_is(next_pos, '#') : 
                dir = Turns[dir]
                continue
            pos = next_pos



    except KeyboardInterrupt:
        anim.screen.finish()



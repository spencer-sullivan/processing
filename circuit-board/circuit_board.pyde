from itertools import permutations
from math import floor, ceil, pow
from collections import defaultdict

cell_size = 10
cut_off_length = 2
max_wire_length = 20
# directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
directions = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1 , 1], [-1, 0]]
straightness = 0.01
grid_width = 0
grid_height = 0
grid = []
available = []
wires = []

def no_cross_over(index, x, y):
    global grid

    if index == 0:
        return grid[x+1][y].available or grid[x][y+1].available
    if index == 2:
        return grid[x-1][y].available or grid[x][y+1].available
    if index == 4:
        return grid[x-1][y].available or grid[x][y-1].available
    if index == 6:
        return grid[x+1][y].available or grid[x][y-1].available
    return True

def find_open_dir(x, y):
    global grid, directions
    
    checks = list(range(len(directions)))
    while len(checks) > 0:
        index = checks.pop(int(random(len(checks))))
        direction = directions[index]
        x2 = x + direction[0]
        y2 = y + direction[1]
        if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]) and grid[x2][y2].available:
            return index
    return 0

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = True
    
    def draw(self):
        global cell_size
        fill(0)
        strokeWeight(cell_size/6)
        ellipse((self.x + 0.5)*cell_size, (self.y + 0.5)*cell_size, cell_size * 0.7, cell_size * 0.7)
    
class Wire:
    def __init__(self, cell):
        self.cells = [cell]
        self.last = find_open_dir(cell.x, cell.y)
    
    def generate(self):
        global grid, max_wire_length, directions
    
        has_space = True
        while len(self.cells) < max_wire_length and has_space:
            previous_cell = self.cells[-1]        
            tries = [0, -1, 1] if random(2) > 1 else [0, 1, -1]
            found = False
            has_space = False
            while len(tries) > 0 and not found:
                mod = tries.pop(len(tries) * int(pow(random(1), straightness)))
                index = (self.last+4+mod) % len(directions)
                direction = directions[index]
                x = direction[0] + previous_cell.x
                y = direction[1] + previous_cell.y
                if 0 <= x < len(grid) - 1 and 0 <= y < len(grid[0]) - 1:
                    cell = grid[x][y]
                    if cell.available and no_cross_over(index, x, y):
                        self.cells.append(cell)
                        cell.available = False
                        has_space = found = True
                        self.last = (self.last + mod) % len(directions)
    
    def draw(self):
        global cell_size
        if self.cells is None or len(self.cells) == 0:
            return
        noFill()
        strokeWeight(2)
        beginShape()
        for cell in self.cells:
            vertex((cell.x + 0.5)*cell_size, (cell.y + 0.5)*cell_size)
        endShape()
        self.cells[0].draw()
        self.cells[-1].draw()
        
def reset():
    size(1600, 1000)
    colorMode(HSB, 360, 100, 100)
    background(120, 70, 30)
    global grid, available
    grid_width = int(ceil(width/cell_size)+1)
    grid_height = int(ceil(height/cell_size)+1)
    
    grid = [[Cell(j, i) for i in range(grid_height)] for j in range(grid_width)]
    available = [cell for row in grid for cell in row]
    

def setup():
    size(1600, 1000)
    colorMode(HSB, 360, 100, 100)
    background(120, 70, 30)
    global grid, available
    grid_width = int(ceil(width/cell_size)+1)
    grid_height = int(ceil(height/cell_size)+1)
    
    grid = [[Cell(j, i) for i in range(grid_height)] for j in range(grid_width)]
    available = [cell for row in grid for cell in row]
    
    while len(available) > 0:
        start_cell = available[int(random(len(available)))]
        start_cell.available = False
        wire = Wire(start_cell)
        wire.generate()
        wires.append(wire)
        
        for cell in wire.cells:
            available.remove(cell)
    
def draw():
    global available
    stroke(45, 60, 60)
    
    first_time = True
    while first_time or len(wire.cells) <= cut_off_length:
        if len(available) == 0:
            reset()
        first_time = False
        start_cell = available[int(random(len(available)))]
        start_cell.available = False
        wire = Wire(start_cell)
        wire.generate()
        wires.append(wire)
        
        for cell in wire.cells:
            available.remove(cell)
        
        if len(wire.cells) > cut_off_length:
            wire.draw()


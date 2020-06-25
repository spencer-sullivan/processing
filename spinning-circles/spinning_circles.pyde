from math import pow

num_rows = 11
num_columns = 17
arcs = []

class SpinningArc():
    def __init__(self, x, y, ring_distance):
        self.x = x
        self.y = y
        self.ring_distance = ring_distance
        self.num_arcs = 4 #3 + int(random(2))
        self.arc_lengths = [PI / 4 + random(PI) for i in range(self.num_arcs)]
        self.arc_offsets = [2 * PI / (i + 0.00001) for i in range(self.num_arcs)]
        self.arc_spin_verlocities = [random(0.05) * pow(-1, i) for i in range(self.num_arcs)]
        print(self.__dict__)
        
    def draw(self):
        for arc_num in range(self.num_arcs):
            r = self.ring_distance * (arc_num + 1)
            arc_length = self.arc_lengths[arc_num]
            arc_offset = self.arc_offsets[arc_num]
             
            self.draw_arc(self.x, self.y, r, arc_length, arc_offset)
            
            # spin
            self.arc_offsets[arc_num] += self.arc_spin_verlocities[arc_num]
            
            
    def draw_arc(self, x, y, r, arc_length, offset):
        arc(x, y, r, r, offset, offset+arc_length)

def setup():
    size(1600, 1000)
    for x in range(num_rows):
        for y in range(num_columns):
            arcs.append(SpinningArc((2*y+1) * width/(num_columns * 2), (2*x+1) * height/(num_rows*2), 20))        

def draw():
    global rotation
    rand = 0
    if rand == 0:
        background(255)
    else:
        background(184, 30, 22)
    noFill()
    if rand == 0:
        stroke(186, 231, 255)
    else:
        stroke(250, 98, 90)
    strokeWeight(7)
    for arc in arcs:
        arc.draw()


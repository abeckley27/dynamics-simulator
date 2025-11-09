import math

class Ball(object):

    def __init__(self, pos_, vel_, r, c, m_ = 1):
        self.pos = pos_
        self.vel = vel_
        self.acc = [0.0, 0.0, 0.0]
        self.ax = 0
        self.ay = 0
        self.radius = r
        self.color = c
        self.mass = m_

    def __repr__(self):
        output = '(' + str(self.pos[0])+ ", " + str(self.pos[1]) + ", "
        output = output + str(self.pos[2]) + ') ' + str(self.radius) + " "
        output = output + self.color + "\t speed = " + str(self.speed()) 
        output = output + ' ' + str(self.accel())
        return output

    def check_intersect(self, b2):
        x1 = self.pos[0]
        y1 = self.pos[1]
        z1 = self.pos[2]
        x2 = b2.pos[0]
        y2 = b2.pos[1]
        z2 = b2.pos[2]
        dist = math.sqrt((y2 - y1)**2 + (x2 - x1)**2 + (z2 - z1)**2)
        r1 = abs(self.rad())
        r2 = abs(b2.rad())
        return dist <= r1 + r2

    def distance(self, b2):
        x_dist = abs(self.pos[0] - b2.pos[0])
        y_dist = abs(self.pos[1] - b2.pos[1])
        z_dist = abs(self.pos[2] - b2.pos[2])
        return math.sqrt(x_dist**2 + y_dist**2 + z_dist**2)

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    def get_color(self):
        return self.color

    def bounding_box(self):
        box = (self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius )
        return box

    def some_inside(self, maxx, maxy):
        return 0 < self.x + self.radius and self.x - self.radius < maxx and 0 < self.y + self.radius and self.y - self.radius < maxy

    #For checking collisions with walls
    def check_and_reverse(self, maxx, maxy, maxz):
        if self.x <= 0: 
            self.vx = self.vx * -1
            self.x = abs(self.x)
            
        if self.x >= maxx:
            self.vx = self.vx * -1
            self.x = 2 * maxx - self.x
            
        if self.y <= 0:
            self.vy = self.vy * -1
            self.y = abs(self.y)
            
        if self.y >= maxy:
            self.vy = self.vy * -1
            self.y = 2 * maxy - self.y
            

    def speed(self):
        return math.sqrt(self.vel[0]**2 + self.vel[1]**2 + self.vel[2]**2)
    
    def accel(self):
        return math.sqrt(self.acc[0]**2 + self.acc[1]**2 + self.acc[2]**2)

    def area(self):
        return (self.radius ** 2) * math.pi

    def rad(self):
        return self.radius

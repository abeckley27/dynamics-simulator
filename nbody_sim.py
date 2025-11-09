import Ball3d
import numpy as np


G = 6.674e-11

def vector_magnitude(v):
    return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

# Change the necessary values if two balls are colliding
def collision(b1, b2):
    #todo: implement this
    return 0
    

def calculate_acceleration(ball_list):
    output = []
    for b in ball_list:
        a = np.zeros(3)
        
        for b2 in ball_list:
            r12 = b.distance(b2)
            if r12 > 0:
                a_magnitude = G * b2.mass / (r12 * r12)
                u = np.array(b2.pos) - np.array(b.pos)
                u = u / (vector_magnitude(u))
                a += (a_magnitude * u)
        
        output.append(a)
    return output
    

def print_balls(lst):
    for k in lst:
        print(k)


maxx = 1000
maxy = 1000
maxz = 1000

t_max = 100


filename = input('Enter the name of the data file: ')
print ('==> ' + filename)

f1 = open(filename, 'r')
ball_init = []

# Set up ball_init as a two dimensional list containing all of the
# information about that balls in the simulation.

for line in f1:
    ball_init.append(line.split('\t'))

f1.close()
ball_list = []
print(ball_init)     #For testing purposes

#Import the data from the file into ball objects
for line in ball_init:
    position = [float(line[0]), float(line[1]), float(line[2])]
    velocity = [float(line[3]), float(line[4]), float(line[5])]
    radius = float(line[6])
    mass = float(line[7])
    color = line[8]
    new_obj = Ball3d.Ball(position, velocity, radius, color, mass)
    ball_list.append(new_obj)



print ('Initial ball configuration:')
print_balls(ball_list)
frame = 0


#Start main simulation loop
while (frame < t_max):
    
    #for root in ball_list:
        #Move the ball based on its velocity
        #move(root)
        
        #Check collisions with walls
        #root.check_and_reverse(maxx, maxy, maxz)

        #Check for collisions between balls
        #for b in ball_list:
        #    if (root != b) and root.check_intersect(b):
        #        collision(root, b)
    
    frame += 1 

#print ('Ends at maximum number of iterations, %d, with the following state:' %frame)
#print_balls()

































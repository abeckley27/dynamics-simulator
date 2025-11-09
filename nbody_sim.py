import Ball3d
import numpy as np


G = 6.674e-11

maxx = 10000
maxy = 10000
maxz = 10000

dt = 10.0
t_max = 100000


def vector_magnitude(v):
    return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

# Change the necessary values if two balls are colliding
def collision(i, j, ball_list):
    m1 = ball_list[i].mass
    m2 = ball_list[j].mass
    v1 = ball_list[i].vel
    v2 = ball_list[j].vel
    frame_shift = v2
    v1 -= v2
    v1f = ((m1 - m2) / (m1 + m2)) * v1
    v2f = (2*m1 / (m1 + m2)) * v1
    v1f += frame_shift
    v2f += frame_shift
    
    #elastic collisions in 3d


def calculate_acceleration(ball_list, index):
    a = np.zeros(3)
    b = ball_list[index]
    for b2 in ball_list:
        r12 = b.distance(b2)
        if r12 > 0:
            a_magnitude = G * b2.mass / (r12 * r12)
            u = np.array(b2.pos) - np.array(b.pos)
            u = u / (vector_magnitude(u))
            a += (a_magnitude * u)
    return a

def comp_acc(ball_list):
    output = []
    for k in range(len(ball_list)):
        output.append(calculate_acceleration(ball_list, k))
    return output

def move(ball_list, i):
    b = ball_list[i]
    b.pos = b.pos + b.vel * dt + 0.5 * dt * dt * b.acc
    new_acc = calculate_acceleration(ball_list, i)
    b.vel = b.vel + 0.5 * (b.acc + new_acc) * dt
    b.acc = new_acc
    
def K(ball_list):
    result = 0.0
    for i in range(len(ball_list)):
        v = vector_magnitude(ball_list[i].vel)
        result += (0.5 * v * v)
    return result

def U(ball_list):
    output = 0.0
    for i in range(len(ball_list)):
        for j in range(len(ball_list)):
            if i != j:
                Uij = -1 * G * ball_list[i].mass * ball_list[j].mass
                Uij /= ball_list[i].distance(ball_list[j])
                output += Uij
    return output
    

def print_balls(lst):
    for k in lst:
        print(k)

#filename = input('Enter the name of the data file: ')
filename = "nbody_data1.txt"
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
    position = np.array([float(line[0]), float(line[1]), float(line[2])])
    velocity = np.array([float(line[3]), float(line[4]), float(line[5])])
    radius = float(line[6])
    mass = float(line[7])
    color = line[8]
    new_obj = Ball3d.Ball(position, velocity, radius, color, mass)
    ball_list.append(new_obj)


for k in range(len(ball_list)):
    ball_list[k].acc = calculate_acceleration(ball_list, k)

print ('Initial ball configuration:')
print_balls(ball_list)
frame = 0
DEBUG = False

print("Kinetic energy: \t", K(ball_list))
print("Potential energy: \t", U(ball_list))


#Start main simulation loop
while (frame < t_max and DEBUG == False):
    
    for root in range(len(ball_list)):
        #Move the ball based on its velocity
        move(ball_list, root)
        
        #Check collisions with walls
        #root.check_and_reverse(maxx, maxy, maxz)

        #Check for collisions between balls
        for j in range(len(ball_list)):
            if ball_list[root].check_intersect(ball_list[j]) and root != j:
                print(root, j, frame)
                #print_balls(ball_list)
                DEBUG = True
                collision(root, j, ball_list)
    
    frame += 1 

print ('Ends at time %d, with the following state:' %(frame*dt))
print_balls(ball_list)
print("Kinetic energy: \t", K(ball_list))
print("Potential energy: \t", U(ball_list))































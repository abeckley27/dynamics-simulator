import Ball3d
import time
import numpy as np
import numpy.linalg as npla
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numba

G = 6.674e-11
dt = 10
t_max = 30000
snapshot_interval = 10000

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
    for b2 in range(len(ball_list)):
        if b2 != index:
            a_magnitude = G * ball_list[b2].mass / (b.distance(ball_list[b2])**2)
            u = ball_list[b2].pos - b.pos
            a += (a_magnitude / vector_magnitude(u)) * u
    return a

def comp_acc(ball_list):
    output = []
    for k in range(len(ball_list)):
        output.append(calculate_acceleration(ball_list, k))
    return output

def move(ball_list, i):
    ball_list[i].pos = ball_list[i].pos + (dt * ball_list[i].vel) + 0.5*dt*dt * ball_list[i].acc
    new_acc = calculate_acceleration(ball_list, i)
    ball_list[i].vel = ball_list[i].vel + 0.5 * (ball_list[i].acc + new_acc) * dt
    ball_list[i].acc = new_acc

    
def K(ball_list):
    result = 0.0
    for i in range(len(ball_list)):
        v = vector_magnitude(ball_list[i].vel)
        result += (0.5 * ball_list[i].mass * v * v)
    return result

def U(ball_list):
    output = 0.0
    for i in range(len(ball_list)):
        for j in range(i):
            if i != j:
                Uij = -1.0 * G * ball_list[i].mass * ball_list[j].mass
                Uij /= ball_list[i].distance(ball_list[j])
                output += Uij
    return output
    

def print_balls(lst):
    for k in lst:
        print(k)

#filename = input('Enter the name of the data file: ')
filename = "nbody_data1.txt"
print ('==> ' + filename)


# Set up ball_init as a two dimensional list containing all of the
# information about that balls in the simulation.
f1 = open(filename, 'r')
ball_init = []
for line in f1:
    ball_init.append(line.split('\t'))

f1.close()

#Once the file operations are done, start a timer
t0 = time.time()
ball_list = []
#print(ball_init)     #For testing purposes

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
DEBUG = False

print("Kinetic energy: \t", K(ball_list))
print("Potential energy: \t", U(ball_list))
K0 = K(ball_list)
U0 = U(ball_list)
E0 = K0 + U0

position_data = np.zeros((len(ball_list), int(t_max) + 1, 3))

def get_path(i, tstop):
    x = np.zeros(tstop)
    y = np.zeros(tstop)
    z = np.zeros(tstop)
    for k in range(tstop):
        x[k] = position_data[i][k][0]
        y[k] = position_data[i][k][1]
        z[k] = position_data[i][k][2]
    
    return (x, y, z)


def plot_paths(tstop):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    x0, y0, z0 = get_path(0, tstop)
    x1, y1, z1 = get_path(1, tstop)
    x2, y2, z2 = get_path(2, tstop)
    ax.plot(x0, y0, z0)
    ax.plot(x1, y1, z1)
    ax.plot(x2, y2, z2)

#Start main simulation loop
t = 0
while (t < t_max and DEBUG == False):
    
    for root in range(len(ball_list)):
        move(ball_list, root)
        

        #Check for collisions between balls
        for j in range(len(ball_list)):
            if ball_list[root].check_intersect(ball_list[j]) and root != j:
                print("Collision Detected")
                print(root, j, t)
                DEBUG = True
                collision(root, j, ball_list)
        position_data[root][t][0] = ball_list[root].pos[0]
        position_data[root][t][1] = ball_list[root].pos[1]
        position_data[root][t][2] = ball_list[root].pos[2]
    t += 1 
    if (t % snapshot_interval == 0):
        plot_paths(max(0, t - 1))

print ('Ends at time %d, with the following state:' %(t*dt))
print_balls(ball_list)
print("Kinetic energy: \t", K(ball_list))
print("Potential energy: \t", U(ball_list))
print("Change in energy: \t", (K(ball_list)+U(ball_list) - E0) )

#print(U(ball_list) - U0)
#print(K(ball_list) - K0)

t1 = time.time()
print("Time taken: \t", t1 - t0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line1, = ax.plot([], [], [], 'b-', lw=2)
line2, = ax.plot([], [], [], 'g-', lw=2)
line3, = ax.plot([], [], [], 'r-', lw=2)
ax.set_xlim(-100, 500)
ax.set_ylim(-100, 500)
ax.set_zlim(-100, 500)
xdata1, ydata1, zdata1 = get_path(0, t)
xdata2, ydata2, zdata2 = get_path(1, t)
xdata3, ydata3, zdata3 = get_path(2, t)


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line1.set_3d_properties([])
    line2.set_3d_properties([])
    line3.set_3d_properties([])
    return line1, line2, line3

n = 25
def update(frame):
    x1 = xdata1[:frame*n]
    y1 = ydata1[:frame*n]
    z1 = zdata1[:frame*n]
    line1.set_data(x1, y1)
    line1.set_3d_properties(z1)
    
    x2 = xdata2[:frame*n]
    y2 = ydata2[:frame*n]
    z2 = zdata2[:frame*n]
    line2.set_data(x2, y2)
    line2.set_3d_properties(z2)
    
    x3 = xdata3[:frame*n]
    y3 = ydata3[:frame*n]
    z3 = zdata3[:frame*n]
    line3.set_data(x3, y3)
    line3.set_3d_properties(z3)
    
    return line1, line2, line3


ani = animation.FuncAnimation(
    fig, update, frames=900, init_func=init, blit=True
)

ani.save("3body.mp4", writer="ffmpeg", fps=30)
t2 = time.time()

print("Animation time: \t", (t2 - t1))















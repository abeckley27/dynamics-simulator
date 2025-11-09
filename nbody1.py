import tkinter as tk
import Ball
import random
import math
import sys

G = 1

# Change the necessary values if two balls are colliding
def collision(b1, b2):
    initial_values = (b1.vx, b1.vy, b2.vx, b2.vy)
    #if the masses are the same, the balls trade velocities
    b1.vx = initial_values[2]
    b1.vy = initial_values[3]
    b2.vx = initial_values[0]
    b2.vy = initial_values[1]

def calculate_acceleration(ball_list):
    for b in ball_list:
        indices = list(range(len(ball_list)))
        indices.remove(ball_list.index(b))
        b.ax = 0
        b.ay = 0
        for j in indices:
            acceleration = G * ball_list[j].mass / math.pow(b.distance(ball_list[j]), 2)
            angle = math.atan( (ball_list[j].y - b.y) / (ball_list[j].x - b.x) )
            b.ax += acceleration * math.cos(angle)
            b.ay += acceleration * math.sin(angle)
            
    
def print_balls():
    for b in range(0, len(balls)):
        current = balls[b]
        xpos = current.position()[0]
        ypos = current.position()[1]
        rad = current.radius
        dx = current.velocity()[0]
        dy = current.velocity()[1]
        color = current.color
        print ('Ball: %d: position (%d, %d), radius %d, motion (%d, %d), color %s' %(b,xpos, ypos, rad, dx, dy, color))
    print ('')

if __name__ == "__main__":
    pretty_colors = input('Enter y to run graphical simulation: ')
    print ('==> ' + pretty_colors.lower())

    source = input('Enter y to generate random ball positions: ')
    print ('==> ' + source.lower())
    
    filename = input('Enter the name of the data file: ')
    print ('==> ' + filename)
    
    f1 = open(filename, 'r')
    ball_init = []

    # Set up ball_init as a two dimensional list containing all of the
    # information about that balls in the simulation.

    for line in f1:
        ball_init.append(line.split())

    balls = []
    #print ball_init     #For testing purposes
    
    '''
    The data from the input file are now stored as integers in a 2D list, 
    called ball_init.
    
    element     | meaning
    0           | x position
    1           | y position
    2           | x velocity
    3           | y velocity
    4           | size (radius)
    5           | color
    '''

    if source == 'y':
        print ('Generating random data for simulation...')
        color_lst = ["black", "blue", "red", "green", "magenta", "orange", "pink", \
    "purple", "yellow"]
        
        #Convert the text from the file into integers
        for y in range(0, len(ball_init)):
            for z in range(0,len(ball_init[y]) - 1):
                ball_init[y][z] = int(ball_init[y][z])
        ball_init[0][-1] = int(ball_init[0][-1])
        
        #Setting the bounds of the canvas
        maxx = int(ball_init[0][2])
        maxy = int(ball_init[0][3])
        minr = int(ball_init[1][1])
        maxr = int(ball_init[1][2])
        max_v = int(ball_init[1][0])
        
        for k in range(0, int(ball_init[0][0])):
            xpos = random.randint(maxr, maxx - maxr)
            ypos = random.randint(maxr, maxy - maxr)
            dx = random.randint(-1 * max_v, max_v)
            dy = random.randint(-1 * max_v, max_v)
            radius = random.randint(5,10)
            color = random.choice(color_lst)
            balls.append(Ball.Ball(xpos, ypos, dx, dy, radius, color))

    else:  
        for k in ball_init[1:]:
            if len(k) > 5:
                balls.append(Ball.Ball(int(k[0]), int(k[1]), int(k[2]), int(k[3]), int(k[4]), k[5]))


    ##  Create a canvas, like an image, that we can draw objects on.
    ##  This canvas is called chart_1.  By passing root in the call
    ##  before, chart_1 is attached to the root canvas.
    ##
    maxx = int(ball_init[0][2])  # canvas width, in pixels
    maxy = int(ball_init[0][3]) # canvas height, in pixels

    if pretty_colors.lower() == 'y':
        chart_1 = tk.Canvas(width=maxx, height=maxy, background="white")
        chart_1.grid(row=0, column=0)

    frame = 0

    # Print inital data to screen

    print ('Initial ball configuration:')
    print_balls()
    
    #Initial Canvas setup
    
    #  Here is the time in milliseconds between consecutive instances
    #  of drawing the root.  If this time is too small the root will
    #  zip across the canvas in a blur.
    wait_time = 5
    
    for b in balls:
        # Draw an oval on the canvas within the bounding box
        bound = b.bounding_box()
    
        #Update the canvas if graphics are turned on
        if (pretty_colors.lower() == 'y'):
            chart_1.create_oval(bound, fill = b.get_color())
            chart_1.update()      # Actually refresh the drawing on the canvas.
            chart_1.after(wait_time)
    
    
    #Start main simulation loop
    while True:

        if pretty_colors.lower() == 'y':
            chart_1.delete(tk.ALL)
        
        for root in balls:
            #Move the ball based on its velocity
            root.move()
            
            #Check collisions with walls
            root.check_and_reverse(maxx, maxy)

            #Check for collisions between balls
            for b in balls:
                if (root != b) and root.check_intersect(b):
                    collision(root, b)
            
            # Draw an oval on the canvas within the bounding box
            bound = root.bounding_box()

            #Update the canvas if graphics are turned on
            if (pretty_colors.lower() == 'y'):
                chart_1.create_oval(bound, fill = root.get_color())
                chart_1.update()      # Actually refresh the drawing on the canvas.

                chart_1.after(wait_time)
            
        frame = frame + 1
        if frame >= int(ball_init[0][1]):
            break

    print ('Ends at maximum number of iterations, %d, with the following state:' %frame)
    print_balls()

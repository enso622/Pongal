# ---------------------------------------------------- #
# File: hw5.py
# ---------------------------------------------------- #
# Author(s): Michael Casterlin & Nita Soni, mcasterlin
# ---------------------------------------------------- #
# Plaftorm:    {Windows 7}
# Environment: Python 2.7.8
# Libaries:    numpy 1.9.0
#              matplotlib 1.4.0
#              scipy 0.14.0-Py2.7
#              Tkinter
# ---------------------------------------------------- #
# Keys:
# Player 1: up   - 'w'
#           down - 's'
#           open portals - 'a' and 'd'
#
# Player 2: up   - '<Up>'
#           down - '<Down>'
#           open portals - '<Left>' and '<Right>'
#
# ---------------------------------------------------- #
# TODO:
# - 
# ---------------------------------------------------- #
#
#               .,-:;//;:=,
#           . :H@@@MM@M#H/.,+%;,
#        ,/X+ +M@@M@MM%=,-%HMMM@X/,
#      -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
#     ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
#   ,%MM@@MH ,@%=             .---=-=:=,.
#   =@#@@@MX.,                -%HX$$%%%:;
#  =-./@M@M$                   .;@MMMM@MM:
#  X@/ -$MM/                    . +MM@@@M$
# ,@M@H: :@:                    . =X#@@@@-
# ,@@@MMX, .                    /H- ;@M@M=
# .H@@@@M@+,                    %MM+..%#$.
#  /MMMM@MMH/.                  XM@MH; =;
#   /%+%$XHH@$=              , .H@@@@MX,
#    .=--------.           -%H.,@@@@@MX,
#    .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
#      =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
#        =%@M@M#@$-.=$@MM@@@M; %M%=
#          ,:+$+-,/H#MMMMMMM@= =,
#                =++%%%%+/:-.

'''
#Psuedocode/Outline
import tKinter, numpy, random, tkFont
class GUI(Frame):
    __init__: create grid, create Pong game, bind keys, create widgets, create field space
    bindkeys: control vertical paddle movements
    createWidgets: make New Game reset button, make quit button
    draw: draw all elements at current iteration onto canvas
class Paddle(object):
    __init__: height, upbutton, downbutton
    lower: move paddle down
    lift: move paddle up
class Ball(object):
    __init__: position(x,y), speed, velocity(x,y), size
    reflect: physics of bounce ball off object [scaled dot product of surface vector and velocity vector]
    hitPaddle: calls reflect and increments number of hits tally; if tally>=5, increase ball speed
    move: update position by adding velocity to current position
    strike/reset: Handles scoring and New Game; updates score, resets ball parameters
class Pong(object):
    __init__: create paddles, create ball, define game events and responses
        ball hitting upper and lower walls, left and right walls (scoring), and paddles
    step: update position/velocities/properties of each item in game every n seconds concurrent with mainloop
class Score(object):
    __init__ score keeping object
    update: increment appropriate player's score
'''

import Tkinter as tk
from numpy import sin, pi, cos, arctan
import random
import tkFont

class GUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
 
        # Set up the grid space for the application
        self.grid()
        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pong = Pong()

        self.bindKeys(master)
        self.createWidgets()
        self.pack()

        self.field = tk.Canvas(master, width=1000, height=500, bg = "black")

    # keybindings to control the positioning of the paddles
    def bindKeys(self, master):
        master.bind("w", self.pong.paddle_left.lift)
        master.bind("<KeyRelease-w>", self.pong.paddle_left.stop_left)
        master.bind("s", self.pong.paddle_left.lower)
        master.bind("<KeyRelease-s>", self.pong.paddle_left.stop_left)
        master.bind("<Up>", self.pong.paddle_right.lift)
        master.bind("<KeyRelease-Up>", self.pong.paddle_right.stop_right)
        master.bind("<Down>", self.pong.paddle_right.lower)
        master.bind("<KeyRelease-Down>", self.pong.paddle_right.stop_right)
        master.bind("d", lambda event: self.pong.enable_left_warp(0))
        master.bind("a", lambda event: self.pong.enable_left_warp(1))
        master.bind("<KeyRelease-d>", self.pong.disable_left_warp)
        master.bind("<KeyRelease-a>", self.pong.disable_left_warp)
        master.bind("<Left>", lambda event: self.pong.enable_right_warp(0))
        master.bind("<Right>", lambda event: self.pong.enable_right_warp(1))
        master.bind("<KeyRelease-Left>", self.pong.disable_right_warp)
        master.bind("<KeyRelease-Right>", self.pong.disable_right_warp)

    # creates buttons to exit the game or reset the field conditions
    def createWidgets(self):
        self.quit = tk.Button(self, text="Quit", command=self.quit).grid(column=1,row=0)
        self.play = tk.Button(self, text="New Game", command=self.pong.ball.reset).grid(column=0,row=0)

    # draw the updated boundaries of all relevant game elements (paddles, ball, etc) on the canvas game field
    def draw(self):
        app.field.delete("all")
        #Create paddles
        if self.pong.lwarp_enable == True:
            p1_color = self.pong.lwarp
        else:
            p1_color = "green"
        if self.pong.rwarp_enable == True:
            p2_color = self.pong.rwarp
        else:
            p2_color = "green"

        self.field.create_rectangle(20, self.pong.paddle_left.height, 50, (self.pong.paddle_left.height-100), fill=p1_color)
        self.field.create_rectangle(950, self.pong.paddle_right.height, 980, (self.pong.paddle_right.height-100), fill=p2_color)
        #Display score
        ourFont = tkFont.Font(family='Helvetica',size=20)
        app.field.create_text(250, 25, text=str(score.scoreP1), fill = "dark green", font=ourFont)
        app.field.create_text(750, 25, text=str(score.scoreP2), fill = "dark green", font=ourFont)
        #Create field details
        self.field.create_line(500, 0, 500, 500, fill="dark green", width=3)
        self.field.create_oval(400,150,600,350, outline ="dark green", width=3)
        #Create ball
        self.field.create_oval(self.pong.ball.position[0]-self.pong.ball.size, 
            self.pong.ball.position[1]-self.pong.ball.size, 
            self.pong.ball.position[0]+self.pong.ball.size, 
            self.pong.ball.position[1]+self.pong.ball.size,
            fill="green")
        #Indicating gravity change, simplification in progress
        # for notification in ["3...  ", "2...  ", "1...  ", "Reversing Gravity! "]:
        #     for timestamp in [8500, 9000, 9500, 10000, 1000]:
        #         if timestamp > 1000
            # self.field.create_text(500,50,text = str(i), fill="Red", font=ourFont)
        if self.pong.gravity_cooldown > 8500 and self.pong.gravity_cooldown < 9000:
            self.field.create_text(500,50,text=str("3..."), fill="Red", font=ourFont)
            self.pong.start_check = False
        if self.pong.gravity_cooldown >= 9000 and self.pong.gravity_cooldown <= 9500:
            self.field.create_text(500,50,text = str("2..."), fill="Red", font=ourFont)
        if self.pong.gravity_cooldown > 9500 and self.pong.gravity_cooldown < 10000:
            self.field.create_text(500,50,text = str("1..."), fill="Red", font=ourFont)
        if self.pong.gravity_cooldown <= 1000 and self.pong.start_check == False:
            self.field.create_text(500,50,text=str("Reversing Gravity!"), fill="Red", font=ourFont)
        #Paddle Portals
        self.field.create_rectangle(self.pong.orange_portal.space[0][0], self.pong.orange_portal.space[0][1], self.pong.orange_portal.space[1][0], self.pong.orange_portal.space[1][1], fill="orange")
        self.field.create_rectangle(self.pong.cyan_portal.space[0][0], self.pong.cyan_portal.space[0][1], self.pong.cyan_portal.space[1][0], self.pong.cyan_portal.space[1][1], fill = "cyan")
        self.field.create_rectangle(self.pong.red_portal.space[0][0], self.pong.red_portal.space[0][1], self.pong.red_portal.space[1][0], self.pong.red_portal.space[1][1], fill = "red")
        self.field.create_rectangle(self.pong.blue_portal.space[0][0], self.pong.blue_portal.space[0][1], self.pong.blue_portal.space[1][0], self.pong.blue_portal.space[1][1], fill = "blue")
        self.field.pack()

#Class for creatting the two paddle objects use to interact with the game
class Paddle(object):
    def __init__(self, position, upbutton, downbutton):
        """
        Create a pong paddle with the given position and keybindings
        """
        self.height = position
        self.KeyUp = upbutton
        self.KeyDown = downbutton
        self.move_up = False
        self.move_down = False

    def lower(self,event):
        """
        Given appropriate keypress, move paddle down.
        """
        self.move_down = True

    def lift(self,event):
        """
        Given appropriate keypress, move paddle up.
        """
        self.move_up = True

    def stop_left(self,event):
        """
        Stop paddle when key is released.
        """
        if event.char == "w":
            self.move_up = False
        if event.char == "s":
            self.move_down = False

    def stop_right(self,event): # stop should be one function - fix later
        self.move_up = False
        self.move_down = False

    def operate(self):
        """
        Runs all immediate paddle conditions.
        """
        if self.move_up == True and self.height >= 100:
            self.height -= 10

        if self.move_down == True and self.height <= 500:
            self.height += 10
        
        app.draw()

#Class that defines the properties of the game ball
class Ball(object):
    def __init__(self, position, size, speed):
        """
        Create a pong ball with the given position, size, and speed. 
        """
        self.initPosition = position 
        self.initSpeed = speed
        self.velocity = (0,0)
        self.size = size # Radius
        self.player = 0 # For score/new game reset

        self.reset()

    def reflect(self, surface):
        """
        Alter the ball's velocity for a perfectly elastic
        collision with a surface defined by the unit normal surface.
        """
        diagonal = -2 * dot(surface, self.velocity)
        self.velocity = add(self.velocity, scale(surface, diagonal))

    def hitPaddle(self, surface):
        """
        Manage collision of ball and paddle. Reflect ball and increase
        ball's speed every 5 hits.
        """
        self.reflect(surface)
        self.hitTally+=1
        if self.hitTally>=5:
            self.speed+=1
            self.velocity=(self.velocity[0]*self.speed/(self.speed-1),self.velocity[1]*self.speed/(self.speed-1))
            self.hitTally=0

    def hitPortal(self, exit):
        self.position = pong.portals[exit].center

    def move(self):
        """
        Increment ball position, assuming no collisions.
        """
        self.position = add(self.position, self.velocity)

    def strike(self, player):
        """
        Set player to update score.
        """
        self.player = player
        self.reset()

    def accelerate(self, gravity):
        adt = (gravity[0]*cos(gravity[1]), gravity[0]*sin(gravity[1]))
        self.velocity = add(self.velocity, adt)

    def reset(self):
        """
        Handle game reset in case of goal or New Game button. Update scores and reset ball and paddle parameters.
        """
        score.update(self.player)
        self.position = self.initPosition
        self.speed = self.initSpeed

        polar_options = range(0, 13) + range(37, 63) + range(87,100)
        scalar = float(random.choice(polar_options))/100.
        angle = scalar*2*pi
        vx = self.speed*cos(angle)
        vy = self.speed*sin(angle)  
        self.velocity = (vx, vy)
        self.hitTally = 0
        self.player = 0


#Class that controls the interaction between game and field elements
class Pong(object):
    def __init__(self):
        """
        Create a pong game. Create standard pong objects, events, and
        responses.
        """
        self.paddle_left = Paddle(300,"w","s")
        self.paddle_right = Paddle(300,"<Up>","<Down>")
        self.ball = Ball((500,250), 10, 4)
        self.randomize_portals()
        self.catcher = None
        self.portal_cooldown = 300
        self.random_cooldown = 0
        self.gravity_cooldown = 0
        self.gravity = 0.1
        self.start_check = True
        self.lwarp_enable = False
        self.rwarp_enable = False
        self.lwarp = None
        self.rwarp = None

        # Game events: Ball hits [upper wall, lower wall, left paddle, right paddle, left wall, right wall]
        self.events = [lambda: self.ball.position[1] > 10,
                       lambda: self.ball.position[1] < 490,
                       self.hits_left_paddle,
                       self.hits_right_paddle, # preliminary check for paddle warp
                       self.hits_left_paddle,
                       self.hits_right_paddle,
                       lambda: self.ball.position[0] > 995,
                       lambda: self.ball.position[0] < 5,
                       self.hits_portal,
                       lambda: self.random_cooldown > 5000,
                       lambda: self.gravity_cooldown >= 10000]
        # Game responses: [bounce back in appropriate direction x4, score ball x2]
        self.responses = [lambda: self.ball.reflect( (0, -1) ),
                          lambda: self.ball.reflect( (0,  1) ),
                          lambda: self.warp("left"),
                          lambda: self.warp("right"),
                          lambda: self.ball.hitPaddle( (1,  0) ),
                          lambda: self.ball.hitPaddle( (-1, 0) ),
                          lambda: self.ball.strike(1),
                          lambda: self.ball.strike(2),
                          self.teleport,
                          self.randomize_portals,
                          self.change_gravity]

    # Pong event for ball collision with left paddle
    def hits_left_paddle(self):
        if self.ball.velocity[0]<0:
            return self.ball.position[0] < 50 and self.ball.position[1] <= self.paddle_left.height and self.ball.position[1] >= self.paddle_left.height-100
    
    # Pong event for ball collision with right paddle
    def hits_right_paddle(self):
        if self.ball.velocity[0]>0:
            return self.ball.position[0] > 950 and self.ball.position[1] <= self.paddle_right.height and self.ball.position[1] >= self.paddle_right.height-100

    def hits_portal(self):
        for i in self.portals:
            if self.portal_cooldown >= 100 and self.ball.position[0] < self.portals[i].space[1][0] and self.ball.position[0] > self.portals[i].space[0][0] and self.ball.position[1] > (self.portals[i].center[1]-10) and self.ball.position[1] < (self.portals[i].center[1]+10):
                self.catcher = self.portals[i].color_in
                self.portal_cooldown = 0
                return True               

    def change_gravity(self):
        self.gravity = -self.gravity
        self.gravity_cooldown = 0
        
    def teleport(self):
        self.ball.position = self.portals[self.portals[self.catcher].color_out].center
        if self.portals[self.catcher].center[1] == self.portals[self.portals[self.catcher].color_out].center[1]:
            self.ball.velocity = (-self.ball.velocity[0], -self.ball.velocity[1])

    def randomize_portals(self):
        y_positions = [10,490]
        self.orange_portal = Portal("orange", "cyan", (random.randrange(100,900), random.choice(y_positions)))
        self.cyan_portal = Portal("cyan", "orange", (random.randrange(100,900),random.choice(y_positions)))
        self.red_portal = Portal("red", "blue", (random.randrange(100,900),random.choice(y_positions)))
        self.blue_portal = Portal("blue", "red", (random.randrange(100,900), random.choice(y_positions)))
        self.portals = {"orange":self.orange_portal, "cyan":self.cyan_portal, "red":self.red_portal, "blue":self.blue_portal}
        self.random_cooldown = 0
        self.start_check = False

    def enable_left_warp(self, event):
        self.lwarp_enable = True
        if event == 0:
            self.lwarp = "orange"
        elif event == 1:
            self.lwarp = "cyan"

    def disable_left_warp(self, event):
        self.lwarp_enable = False
        self.lwarp = None

    def enable_right_warp(self, event):
        self.rwarp_enable = True
        if event == 0:
            self.rwarp = "red"
        elif event == 1:
            self.rwarp = "blue"

    def disable_right_warp(self, event):
        self.rwarp_enable = False
        self.rwarp = None

    def warp(self, side):
        self.ball.hitTally +=1

        if self.blue_portal.center[1] == 10:
            theta_added = (3*pi/2)
        elif self.blue_portal.center[1] == 490:
            theta_added = (pi/2)

        if side == "left" and self.lwarp_enable == True: # Combine these at some point
            self.ball.position = self.portals[self.lwarp].center
            theta_in = arctan(self.ball.velocity[1]/self.ball.velocity[0])
            self.ball.velocity = (self.ball.speed*cos(theta_added+theta_in), (self.ball.speed*sin(theta_added+theta_in)))
        elif side == "right" and self.rwarp_enable == True:
            self.ball.position = self.portals[self.rwarp].center
            theta_in = arctan(self.ball.velocity[1]/self.ball.velocity[0])
            self.ball.velocity = (self.ball.speed*cos(theta_added+theta_in), (self.ball.speed*sin(theta_added+theta_in)))

    def step(self):
        """
        Calculate the next game state.
        """
        self.paddle_right.operate()
        self.paddle_left.operate()
        self.ball.accelerate((self.gravity,(pi/2)))
        self.ball.move()
        self.portal_cooldown += 5
        self.random_cooldown += 5
        self.gravity_cooldown += 5

        # Check for events
        for event, response in zip(self.events, self.responses):
            if event():
                response()
                app.draw() 
        # Run pong game with time step size of 0.005 seconds
        root.after(5, self.step)

#Class to create the object which stores information about game results
class Score(object):
    def __init__(self):
        """
        Create 2-player score keeping object.
        """
        self.scoreP1 = 0
        self.scoreP2 = 0

    def update(self, player):
        """
        Increment a player's score.
        """
        if player == 1:
            self.scoreP1 += 1
        elif player == 2:
            self.scoreP2 += 1
        elif player == 0:
            self.scoreP1 = 0
            self.scoreP2 = 0

class Portal(object):
    def __init__(self, color_in, color_out, center):
        self.color_in = color_in
        self.color_out = color_out # portal which serves as exit
        self.center = center
        self.space = ((self.center[0]-50, self.center[1]+5),(self.center[0]+50, self.center[1]-5))


def dot(x, y):
    """
    2D dot product
    """
    return x[0]*y[0] + x[1]*y[1]

def scale(x, a):
    """
    2D scalar multiplication
    """
    return (x[0]*a, x[1]*a)

def add(x, y):
    """
    2D vector addition
    """
    return (x[0]+y[0], x[1]+y[1])

root = tk.Tk()
score = Score()
app = GUI(master=root)
app.master.title("Chaos Pong")
app.pong.step()
app.mainloop()
root.destroy()
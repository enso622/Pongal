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
import math
import time
import thread
import winsound

class GUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
 
        # Set up the grid space for the application
        self.grid()
        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.ourFont = tkFont.Font(family='fixedsys',size=20)
        self.ourFont2 = tkFont.Font(family='fixedsys',size=50)

        self.pong = Pong()

        self.bindKeys(master)
        self.createWidgets()
        self.pack()

        self.field = tk.Canvas(master, width=1000, height=500, bg = "black")
        self.importGraphics()

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
        master.bind("<Key>", self.pong.begin_game)

    # creates buttons to exit the game or reset the field conditions
    def createWidgets(self):
        self.quit = tk.Button(self, text="Quit", command=self.quit, font = self.ourFont).grid(column=1,row=0)
        self.restart = tk.Button(self, text="New Game", command=self.pong.new_game, font = self.ourFont).grid(column=0,row=0, padx=335, sticky="E")

    # draw the updated boundaries of all relevant game elements (paddles, ball, etc) on the canvas game field
    def importGraphics(self):
        self.cube_img = tk.PhotoImage(file="comp_cube.gif")
        self.cube_img = self.cube_img.subsample(4,4)
        self.ball_img = tk.PhotoImage(file="space_core.gif")
        self.ball_img = self.ball_img.subsample(30,30)
        self.paddle_img = tk.PhotoImage(file="caution2.gif")
        self.paddle_img = self.paddle_img.subsample(4,4)
        self.bg_img = tk.PhotoImage(file="background.gif")
        self.creature_img = tk.PhotoImage(file="currupt_cube.gif")
        self.creature_img = self.creature_img.subsample(4,4)
        #self.life_img = tk.PhotoImage(file="heart.gif")
        #self.life_img = self.life_img.subsample(4,4)     

    def draw(self):
        app.field.delete("all")

        self.field.create_image(500,250,image=self.bg_img)

        if self.pong.restart_delay < 1000 and self.pong.begin == True:
            timer_angle = -359*(self.pong.restart_delay/1000.)
            self.field.create_arc(451,86,551,186, start = 90, extent = timer_angle, outline = "purple", style = "arc", width = 10)
        
        #Create paddles
        if self.pong.lwarp_enable == True:
            p1_color = self.pong.lwarp
        else:
            p1_color = "green"
        if self.pong.rwarp_enable == True:
            p2_color = self.pong.rwarp
        else:
            p2_color = "green"

        self.field.create_rectangle(20, self.pong.paddle_left.height+10, 50, (self.pong.paddle_left.height-110), fill=p1_color)
        self.field.create_rectangle(950, self.pong.paddle_right.height+10, 980, (self.pong.paddle_right.height-110), fill=p2_color)

        # New paddle code (old above to be erased)
        self.field.create_image(self.pong.paddle_left.center, image = self.paddle_img)
        self.field.create_image(self.pong.paddle_right.center, image = self.paddle_img)
        if self.pong.lwarp_enable == True:
            self.field.create_oval(37, (self.pong.paddle_left.height+10), 52, (self.pong.paddle_left.height-110), fill = p1_color)
            self.field.create_oval(40, (self.pong.paddle_left.height-5), 49, (self.pong.paddle_left.height-95), fill = "gray11")
        if self.pong.rwarp_enable == True:
            self.field.create_oval(948, (self.pong.paddle_right.height+10), 963, (self.pong.paddle_right.height-110), fill=p2_color)     
            self.field.create_oval(951, (self.pong.paddle_right.height-5), 960, (self.pong.paddle_right.height-95), fill="gray11")
        # end paddle code

        #Create field details
        #self.field.create_line(500, 0, 500, 500, fill="dark green", width=3)
        #self.field.create_oval(400,150,600,350, outline ="dark green", width=3)
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
        #Paddle Portals
        if self.pong.cyan_portal.override == False:
            self.field.create_oval(self.pong.orange_portal.space[0][0]-13,self.pong.orange_portal.space[0][1]-13,self.pong.orange_portal.space[1][0]+13,self.pong.orange_portal.space[1][1]+13, fill = self.pong.orange_portal.color_in)
            self.field.create_oval(self.pong.orange_portal.space[0][0], self.pong.orange_portal.space[0][1], self.pong.orange_portal.space[1][0], self.pong.orange_portal.space[1][1], fill=self.pong.orange_portal.fill_color)
        if self.pong.orange_portal.override == False:
            self.field.create_oval(self.pong.cyan_portal.space[0][0]-13,self.pong.cyan_portal.space[0][1]-13,self.pong.cyan_portal.space[1][0]+13,self.pong.cyan_portal.space[1][1]+13, fill = self.pong.cyan_portal.color_in)
            self.field.create_oval(self.pong.cyan_portal.space[0][0], self.pong.cyan_portal.space[0][1], self.pong.cyan_portal.space[1][0], self.pong.cyan_portal.space[1][1], fill = self.pong.cyan_portal.fill_color)
        if self.pong.blue_portal.override == False:   
            self.field.create_oval(self.pong.red_portal.space[0][0]-13,self.pong.red_portal.space[0][1]-13,self.pong.red_portal.space[1][0]+13,self.pong.red_portal.space[1][1]+13, fill = self.pong.red_portal.color_in)
            self.field.create_oval(self.pong.red_portal.space[0][0], self.pong.red_portal.space[0][1], self.pong.red_portal.space[1][0], self.pong.red_portal.space[1][1], fill = self.pong.red_portal.fill_color)
        if self.pong.red_portal.override == False:
            self.field.create_oval(self.pong.blue_portal.space[0][0]-13,self.pong.blue_portal.space[0][1]-13,self.pong.blue_portal.space[1][0]+13,self.pong.blue_portal.space[1][1]+13, fill = self.pong.blue_portal.color_in)
            self.field.create_oval(self.pong.blue_portal.space[0][0], self.pong.blue_portal.space[0][1], self.pong.blue_portal.space[1][0], self.pong.blue_portal.space[1][1], fill = self.pong.blue_portal.fill_color)
        
        #self.field.create_rectangle(((self.pong.block1.space[0][0], self.pong.block1.space[0][1]), (self.pong.block1.space[1][0], self.pong.block1.space[1][1])), fill = self.pong.block1.color)
        
        self.field.create_image(self.pong.block1.center[0],self.pong.block1.center[1], image = self.cube_img, state = self.pong.block1.state)
        self.field.create_image(self.pong.creature.center[0],self.pong.creature.center[1], image = self.creature_img, state = self.pong.creature.state)        

        #Display score
        app.field.create_text(275, 38, text=str(score.scoreP1), fill = "dark green", font=self.ourFont)
        app.field.create_text(725, 38, text=str(score.scoreP2), fill = "dark green", font=self.ourFont)
        #Relay information to players
        if self.pong.gravity_cooldown > 4500 and self.pong.gravity_cooldown < 5000:
            self.field.create_text(500,135,text=str("3"), fill="yellow", font=self.ourFont2)
            self.pong.start_check = False
        if self.pong.gravity_cooldown >= 5000 and self.pong.gravity_cooldown <= 5500:
            self.field.create_text(500,135,text = str("2"), fill="yellow", font=self.ourFont2)
        if self.pong.gravity_cooldown > 5500 and self.pong.gravity_cooldown < 6000:
            self.field.create_text(500,135,text = str("1"), fill="yellow", font=self.ourFont2)
        if self.pong.gravity_cooldown <= 1000 and self.pong.start_check == False:
            self.field.create_text(500,135,text=str("Reversing Gravity!"), fill="yellow", font=self.ourFont)
        
        if self.pong.begin == False and self.pong.blink_time < 250:
            self.field.create_text(500,350,text=str("<Press any key to begin Testing>"), fill="yellow", font = self.ourFont)

        self.field.create_image(self.pong.ball.position[0], self.pong.ball.position[1], image = self.ball_img)
        
        if self.pong.cloud.exists == True:
            for i in self.pong.cloud.points:
                self.field.create_oval(i[0]-random.randrange(30,self.pong.cloud.size), i[1]-random.randrange(30,self.pong.cloud.size), i[0]+random.randrange(30,self.pong.cloud.size), i[1]+random.randrange(30,self.pong.cloud.size), fill = "#476042", outline = "dark green")
        if self.pong.cloud.exists == True and self.pong.cloud_cooldown <= 1000:
            self.field.create_text(500, 75, text = str("It's your old friend: Deadly Neurotoxin!"), fill = "yellow", font = self.ourFont)

        self.field.pack()

#Class for creatting the two paddle objects use to interact with the game
class Paddle(object):
    def __init__(self, height, x_location, upbutton, downbutton):
        """
        Create a pong paddle with the given position and keybindings
        """
        self.initHeight = height
        self.height = self.initHeight
        self.x = x_location
        self.center = (self.x, (self.height - 50))
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

    def reset(self):
        self.height = self.initHeight
        self.center = (self.x, (self.height - 50))

    def operate(self):
        """
        Runs all immediate paddle conditions.
        """
        if self.move_up == True and self.height >= 100:
            self.height -= 12

        if self.move_down == True and self.height <= 500:
            self.height += 12

        self.center = (self.x, self.height-50)
        
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
        self.reset_mode = False

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
        self.speed = (self.velocity[0]**2 + self.velocity[1]**2)**0.5

    def randomize_direction(self, polar_options):
        scalar = float(random.choice(polar_options))/100.
        angle = scalar*2*pi
        vx = self.speed*cos(angle)
        vy = self.speed*sin(angle)
        self.velocity = (vx, vy)

    def reset(self):
        """
        Handle game reset in case of goal or New Game button. Update scores and reset ball and paddle parameters.
        """
        score.update(self.player)
        self.position = self.initPosition
        self.speed = self.initSpeed
        polar_range = range(0, 13) + range(37, 63) + range(87,100)

        self.randomize_direction(polar_range)
        
        self.hitTally = 0
        self.player = 0

        self.reset_mode = True

#Class that controls the interaction between game and field elements
class Pong(object):
    def __init__(self):
        """
        Create a pong game. Create standard pong objects, events, and
        responses.
        """
        self.game_time = 0
        self.restart_delay = 0
        self.blink_time = 0
        self.begin = False
        self.paddle_left = Paddle(300, 35, "w","s")
        self.paddle_right = Paddle(300, 965, "<Up>","<Down>")
        self.block1 = Block((0,0), 0, "purple")
        self.creature = Creature((0,0),0,"yellow",0.1)
        self.cloud = Cloud((0,0), 0, "dark green")
        self.ball = Ball((500,135), 10, 3)
        self.reset_game(None)

        # Game events: Ball hits [upper wall, lower wall, left paddle, right paddle, left wall, right wall]
        self.events = [lambda: self.ball.position[1] < 10 and self.ball.velocity[1] < 0,
                        lambda: self.ball.position[1] > 490 and self.ball.velocity[1] > 0,
                        self.hits_left_paddle,                  #Hit paddle: portal check
                        self.hits_right_paddle,                 #Hit paddle: portal check
                        self.hits_left_paddle,                  #Hits paddle: normal
                        self.hits_right_paddle,                 #Hits paddle: normal
                        lambda: self.ball.position[0] > 995,    #Score on right edge
                        lambda: self.ball.position[0] < 5,      #Score on left edge
                        self.hits_portal,                       #Hits portal
                        lambda: self.portal_cooldown >= 6000,   #Time: Randomize portal
                        lambda: self.gravity_cooldown >= 6000,  #Time: Randomize gravity
                        lambda: self.block_cooldown >= 3000,    #Time: Randomize block
                        self.hits_block,                        #Hits block
                        lambda: self.creature_cooldown >= 1000, #Time: Randomize creature
                        lambda: self.creature.center[1] < 10 and self.creature.velocity[1] < 0,
                        lambda: self.creature.center[1] > 490 and self.creature.velocity[1] > 0,
                        self.hits_creature,                     #Hits creature
                        lambda: self.cloud_cooldown >= 9000,    #Time: Randomize cloud
                        self.enters_cloud,                      #Hits cloud
                        lambda: self.cloud_cooldown >= 3000,    #Time: Kill cloud
                        lambda: self.game_over == True]
                        #TODO: ball_left..right..etc; crea_left..right..etc

        # Game responses: [bounce back in appropriate direction x4, score ball x2]
        self.responses = [lambda: self.ball.reflect((0,-1)),
                        lambda: self.ball.reflect((0,1)),
                        lambda: self.warp("left"),              #Hit paddle: portal
                        lambda: self.warp("right"),             #Hit paddle: portal
                        lambda: self.ball.hitPaddle((1,0)),     #Hits paddle: normal
                        lambda: self.ball.hitPaddle((-1,0)),    #Hits paddle: normal
                        lambda: self.reset_game(1),             #Score on right edge
                        lambda: self.reset_game(2),             #Score on left edge
                        self.teleport,                          #Hits portal
                        self.randomize_portals,                 #Time: Randomize portal
                        self.change_gravity,                    #Time: Randomize gravity
                        self.generate_blocks,                   #Time: Randomize block
                        self.block_bounce,                      #Hits block
                        self.generate_creature,                 #Time: Randomize creature
                        lambda: self.creature.reflect((0,-1)),
                        lambda: self.creature.reflect((0,1)),
                        self.creature_bounce,                   #Hits creature
                        self.generate_cloud,                    #Time: Randomize cloud
                        self.unleash_chaos,                     #Hits cloud
                        self.cloud.destroy,                     #Time: Kill cloud
                        lambda:self.reset_game(0)]
                        #TODO: ball_left..right..etc; crea_left..right..etc

#Game run methods
    def begin_game(self, event):
        if self.begin == False:
            self.begin = True
            self.restart_delay = 0

    def new_game(self):

        self.game_over = True

    def step(self):
        """
        Calculate the next game state.
        """
        if self.ball.reset_mode == True:
            self.restart_delay = 0
            self.ball.reset_mode = False

        self.paddle_right.operate()
        self.paddle_left.operate()
        if self.begin == True and self.restart_delay > 1000:
            self.ball.accelerate((self.gravity,(pi/2)))
            self.ball.move()
            self.portal_cooldown += 5
            self.portal_cooldown += 5
            self.gravity_cooldown += 5
            self.block_cooldown += 5
            self.creature_cooldown +=5
            self.creature.move()
            self.cloud_cooldown += 5
            self.chaos_cooldown += 5

        if self.restart_delay <= 1000:
            self.restart_delay += 5

        # Check for events
        self.blink_time+= 5
        if self.blink_time >= 500:
            self.blink_time = 0

        else:
            for event, response in zip(self.events, self.responses):
                if event():
                    response()
                    app.draw() 
        # Run pong game with time step size of 0.005 seconds
        root.after(5, self.step)
        self.game_time += 5

#Events
    def hits_left_paddle(self):
        if self.ball.velocity[0]<0:
            return self.ball.position[0] < 50 and self.ball.position[1] <= self.paddle_left.height+10 and self.ball.position[1] >= self.paddle_left.height-110

    def hits_right_paddle(self):
        if self.ball.velocity[0]>0:
            return self.ball.position[0] > 950 and self.ball.position[1] <= self.paddle_right.height+10 and self.ball.position[1] >= self.paddle_right.height-110

    def hits_portal(self):
            for i in self.portals:
                if self.ball.position[0] < self.portals[i].space[1][0] and self.ball.position[0] > self.portals[i].space[0][0] and self.ball.position[1] > (self.portals[i].center[1]-10) and self.ball.position[1] < (self.portals[i].center[1]+10):
                    self.catcher = self.portals[i].color_in
                    if self.catcher != self.lwarp and self.catcher != self.rwarp:
                        return True   
    
    def hits_block(self):

        return self.ball.position[0] > self.block1.space[0][0] and self.ball.position[0] < self.block1.space[1][0] and self.ball.position[1] < self.block1.space[1][1] and self.ball.position[1] > self.block1.space[0][1]

    def hits_creature(self):
        return self.ball.position[0] > self.creature.space[0][0] and self.ball.position[0] < self.creature.space[1][0] and self.ball.position[1] < self.creature.space[1][1] and self.ball.position[1] > self.creature.space[0][1]

    def enters_cloud(self):

        return self.ball.position[0] > self.cloud.space[0][0] and self.ball.position[0] < self.cloud.space[1][0] and self.ball.position[1] < self.cloud.space[1][1] and self.ball.position[1] > self.cloud.space[0][1]
    
    def enable_left_warp(self, event):
        self.lwarp_enable = True
        if event == 0:
            self.lwarp = "orange"
            self.cyan_portal.override = True
        elif event == 1:
            self.lwarp = "cyan"
            self.orange_portal.override = True
        #self.portals[lwarp].close()

    def disable_left_warp(self, event):
        self.lwarp_enable = False
        self.lwarp = None
        self.orange_portal.override = False
        self.cyan_portal.override = False
        #self.portals[lwarp].open()

    def enable_right_warp(self, event):
        self.rwarp_enable = True
        self.override = True
        if event == 0:
            self.rwarp = "red"
            self.blue_portal.override = True
        elif event == 1:
            self.rwarp = "blue"
            self.red_portal.override = True
        #self.portals[rwarp].close()

    def disable_right_warp(self, event):
        self.rwarp_enable = False
        self.rwarp = None
        self.red_portal.override = False
        self.blue_portal.override = False
        #self.portals[rwarp].open()

#Responses
    def warp(self, side):
        if self.portal_cooldown >= 100:
            self.ball.hitTally +=1
            if side == "left" and self.lwarp_enable == True: # Combine these at some point
                if self.portals[self.lwarp].center[1] == 10:
                    theta_added = (3*pi/2)
                elif self.portals[self.lwarp].center[1] == 490:
                    theta_added = (pi/2)
                self.portal_cooldown = 0
                self.ball.position = self.portals[self.portals[self.lwarp].color_out].center
                theta_in = arctan(self.ball.velocity[1]/self.ball.velocity[0])       
                self.ball.velocity = (self.ball.speed*cos(theta_added+theta_in), (self.ball.speed*sin(theta_added+theta_in)))
            elif side == "right" and self.rwarp_enable == True:
                if self.portals[self.rwarp].center[1] == 10:
                    theta_added = (3*pi/2)
                elif self.portals[self.rwarp].center[1] == 490:
                    theta_added = (pi/2)
                self.portal_cooldown = 0
                self.ball.position = self.portals[self.portals[self.rwarp].color_out].center
                theta_in = arctan(self.ball.velocity[1]/self.ball.velocity[0])
                self.ball.velocity = (self.ball.speed*cos(theta_added+theta_in), (self.ball.speed*sin(theta_added+theta_in)))
    
    def reset_game(self, player):
        self.ball.strike(player)
        #self.paddle_left.reset()
        #self.paddle_right.reset()
        self.block1.destroy()
        self.creature.destroy()
        self.cloud.destroy()

        self.randomize_portals()
        self.catcher = None
        self.portal_cooldown = 300
        self.portal_cooldown = 0
        self.gravity_cooldown = 0
        self.block_cooldown = 0
        self.creature_cooldown = 0
        self.cloud_cooldown = 0
        self.chaos_cooldown = 0
        self.gravity = 0.1
        self.start_check = True
        self.lwarp_enable = False
        self.rwarp_enable = False
        self.lwarp = None
        self.rwarp = None
        self.game_over = False
      
    def teleport(self):
        if self.portal_cooldown >= 100:
            if self.portals[self.catcher].override == True:
                theta_in = arctan(self.ball.velocity[1]/self.ball.velocity[0])
                if self.catcher == "cyan" or self.catcher == "orange":
                    self.ball.position = self.paddle_left.center
                    theta_out = sign(theta_in)*((pi/2)-abs(theta_in))
                elif self.catcher == "red" or self.catcher == "blue":
                    self.ball.position = self.paddle_right.center
                    theta_out = sign(theta_in)*((pi/2)-abs(theta_in))+pi
                self.ball.velocity = (self.ball.speed*cos(theta_out), (self.ball.speed*sin(-theta_out)))
            else:
                self.ball.position = self.portals[self.portals[self.catcher].color_out].center
                if self.portals[self.catcher].center[1] == self.portals[self.portals[self.catcher].color_out].center[1]:
                    self.ball.velocity = (-self.ball.velocity[0], -self.ball.velocity[1])
            self.portal_cooldown = 0

    def randomize_portals(self):
        y_positions = [10,490]
        x_positions = range(100,901)
        resulting_positions = []

        for portal in range(4):
            selection = random.choice(x_positions)
            resulting_positions.append(selection)
            x_positions.remove(selection)

            for i in range(1,121):
                if (selection-i) in x_positions:
                    x_positions.remove(selection-i)
                if (selection+i) in x_positions:
                    x_positions.remove(selection+i)

        self.orange_portal = Portal("orange", "cyan", (resulting_positions[0], random.choice(y_positions)))
        self.cyan_portal = Portal("cyan", "orange", (resulting_positions[1], random.choice(y_positions)))
        self.red_portal = Portal("red", "blue", (resulting_positions[2], random.choice(y_positions)))
        self.blue_portal = Portal("blue", "red", (resulting_positions[3], random.choice(y_positions)))
        self.portals = {"orange":self.orange_portal, "cyan":self.cyan_portal, "red":self.red_portal, "blue":self.blue_portal}
        self.portal_cooldown = 0
        self.start_check = False
    
    def change_gravity(self):
        self.gravity = -self.gravity
        self.gravity_cooldown = 0
    
    def generate_blocks(self):
        if self.block1.exists == False:
            self.block1.generate(35)
            self.block1.exists = True
            self.block_cooldown = 0

    def block_bounce(self):
        edge = self.block1.breakout(self.ball.position[0], self.ball.position[1])
        self.ball.reflect(edge)
        self.block_cooldown = 0

    def generate_creature(self):
        if self.creature.exists == False:
            self.creature.generate(35)
            self.creature.exists = True
            self.creature_cooldown = 0

    def creature_bounce(self):
        edge = self.creature.breakout(self.ball.position[0],self.ball.position[1])
        self.ball.reflect(edge)
        self.creature_cooldown = 0

    def generate_cloud(self):
        self.cloud.exists = True
        self.cloud.generate(75)
        self.cloud.generate_points()
        self.cloud_cooldown = 0

    def unleash_chaos(self):
        if self.chaos_cooldown >= 100:
            self.ball.randomize_direction(range(100))
            self.chaos_cooldown = 0

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
        self.override = False
        self.color_in = color_in
        self.color_out = color_out # portal which serves as exit
        self.fill_color = "gray11"
        self.center = center
        self.space = ((self.center[0]-50, self.center[1]+5),(self.center[0]+50, self.center[1]-5))

class Obstacle(object):
    def __init__(self, coordinates, dimension, color):
        self.center = coordinates
        self.color = color
        self.size = dimension
        self.update_space()
        self.exists = False
        self.state = "hidden"

    def update_space(self):
        self.space = (((self.center[0] - self.size), (self.center[1] - self.size)), ((self.center[0] + self.size), (self.center[1] + self.size)))

    def generate(self, dimension):
        self.center = (random.randrange(100,900),random.randrange(100,400))
        self.size = dimension
        self.update_space()
        self.state = "normal"

    def destroy(self):
        self.center = (0,0)
        self.size = 0
        self.update_space()
        self.exists = False
        self.state = "hidden"

class Block(Obstacle):
    def breakout(self, ball_x, ball_y):
        x_contact = abs(ball_x - self.center[0])
        y_contact = abs(ball_y - self.center[1])
        theta_contact = arctan(y_contact / x_contact)
        self.destroy()
        self.exists = False
        if theta_contact > 0.7854:
            return (0 , 1)
        else:
            return (1 , 0)

class Cloud(Obstacle):
    def generate_points(self):
        self.points = []
        low_x = self.center[0] - self.size
        high_x = self.center[0] + self.size
        low_y = self.center[1] - self.size
        high_y = self.center[1] + self.size
        for i in range(20):
            random_x = random.randrange(low_x, high_x)
            random_y = random.randrange(low_y, high_y)
            self.points.append((random_x, random_y))

class Creature(Obstacle):
    def __init__(self, coordinates, dimension, color,speed):
        Obstacle.__init__(self, coordinates, dimension, color)
        self.velocity = (0,speed)

    def breakout(self, ball_x, ball_y):
        x_contact = abs(ball_x - self.center[1])
        y_contact = abs(ball_y - self.center[0])
        theta_contact = arctan(y_contact / x_contact)
        if theta_contact > 0.7854:
            return (0 , 1)
        else:
            return (1 , 0)

    def move(self):
        self.center = add(self.center,self.velocity)
        self.update_space()

    def reflect(self, surface):
        diagonal = -2 * dot(surface, self.velocity)
        self.velocity = add(self.velocity, scale(surface, diagonal))
        
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

def sign(x):
    """
    determines the sign of a given value
    """
    return math.copysign(1, x)

def play_music(filename, mode):
    while True:
        winsound.PlaySound(filename, mode)

root = tk.Tk()
score = Score()
app = GUI(master=root)
app.master.title("Pongal")
app.pong.step()
thread.start_new_thread(play_music, ("CaraMia.wav",winsound.SND_LOOP))
app.mainloop()
root.destroy()
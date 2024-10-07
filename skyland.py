from tkinter import *
import tkinter.font as font
from random import random, randint # optional
from math import sin, cos, pi # optional
import math
import subprocess
#from pygame import mixer # do not use it in the submitted version

WIDTH, HEIGHT = 600, 400 # global variables (constants) go here
CLOCK_RATE = 15
START_X, START_Y = 20, 350
END_X, END_Y = 400, 350

class Skyland:
    
    def __init__(self, canvas):
        
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.canvas.bind_all('<KeyPress-x>', self.restart)

        self.paused = False
        self.score = 0
        self.time = 0
        self.land = Land(canvas)
        self.trophy = Trophy(canvas)
        self.spider1 = AI(canvas, x=50, y=218)
        self.spider2 = AI(canvas, x=500, y=145)
        self.avatar = Avatar(canvas)
        self.text = canvas.create_text(150, 370, text='Score ?  Time ? ',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
        #self.play_music() # do not include it in the submitted version
        self.update()


    def restart(self, event=None):
        self.avatar.replace()
        self.trophy.replace()
        self.time = 0
        self.score = 0
        self.paused = False
        self.canvas.delete(self.text)  # Delete the "YOU WIN" text if it exists
        self.text = canvas.create_text(150, 370, text='Score ?  Time ? ',
                                       font=font.Font(family='Helveca', size=15, weight='bold'))

    def pause(self, event=None):
        self.paused = not self.paused

    def update(self):
        if not self.paused:
            self.avatar.update(self.land, self.trophy)
            self.spider1.update(False)  # Call update method for spider 1
            self.spider2.update(False)
            self.land.update()
            self.canvas.bind_all('<KeyPress-space>', self.pause)
            self.time += 1
            if self.avatar.find_trophy(self.trophy.get_trophy()):
                self.score += 1

            # Calculate minutes and seconds
            minutes = self.time // 60
            seconds = self.time % 60

            self.canvas.itemconfigure(self.text, text='Score: {}  Time: {:02d}:{:02d} sec'.format(self.score, minutes, seconds))

        self.canvas.after(CLOCK_RATE, self.update)
        if self.score == 6:
            self.canvas.delete(self.text)
            self.text = canvas.create_text(150, 370, text='YOU WON!!    PRESS X TO RESTART',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
            self.paused = True
            self.canvas.unbind_all('<KeyPress-space>')
        avatar_coords = self.canvas.coords(self.avatar.head)  # Replace with the appropriate way to get avatar's head coordinates
        if self.spider1.check_collision(avatar_coords):
            self.canvas.delete(self.text)
            self.text = canvas.create_text(150, 370, text='YOU DIED!!    PRESS X TO RESTART',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
            self.paused = True
            self.canvas.unbind_all('<KeyPress-space>')
        if self.spider2.check_collision(avatar_coords):
            self.canvas.delete(self.text)
            self.text = canvas.create_text(150, 370, text='YOU DIED!!    PRESS X TO RESTART',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
            self.paused = True
            self.canvas.unbind_all('<KeyPress-space>')
        avatar_coords = self.canvas.coords(self.avatar.torso)  # Replace with the appropriate way to get avatar's head coordinates
        if self.spider1.check_collision(avatar_coords):
            self.canvas.delete(self.text)
            self.text = canvas.create_text(150, 370, text='YOU DIED!!    PRESS X TO RESTART',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
            self.paused = True
            self.canvas.unbind_all('<KeyPress-space>')
        if self.spider2.check_collision(avatar_coords):
            self.canvas.delete(self.text)
            self.text = canvas.create_text(150, 370, text='YOU DIED!!    PRESS X TO RESTART',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
            self.paused = True
            self.canvas.unbind_all('<KeyPress-space>')
        

class Land:
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.direction =1

        self.canvas.create_rectangle( 0, 0, WIDTH, START_Y-100,
                                 fill='lightblue',outline='black')
        self.canvas.create_rectangle( 0, START_Y-120, WIDTH, START_Y,
                                 fill='limegreen',outline='black')

        self.make_hill( 50, 230, 250, 230, height=100, delta=3)
        self.make_hill(150, 300, 350, 300, height=100, delta=3)
        self.make_hill(250, 250, 450, 250, height=100, delta=3)
        self.make_hill(350, 300, 550, 300, height=100, delta=3)

        cloud1 = self.make_cloud(150, 140)
        cloud2 = self.make_cloud(380, 100)
        cloud3 = self.make_cloud(550, 150)
        self.clouds = [cloud1, cloud2, cloud3]
        self.obstacles = []

        self.leftwall = canvas.create_rectangle(0, 0, 10, HEIGHT-45, outline='black', fill='coral', width=1)
        self.rightwall = canvas.create_rectangle(WIDTH-10, 0, WIDTH, HEIGHT-45, outline='black', fill='coral', width=1)
        self.wood1=canvas.create_rectangle(0, HEIGHT/2-50, 150, HEIGHT/2-46, outline='black', fill='coral', width=1)
        self.wood2=canvas.create_rectangle(0, HEIGHT/2+46, 50, HEIGHT/2+50, outline='black', fill='coral', width=1)
        self.wood3=canvas.create_rectangle(WIDTH-100, HEIGHT/2-50, WIDTH, HEIGHT/2-46, outline='black', fill='coral', width=1)

        self.canvas.create_arc(90, 240, 110, 250, start=180, extent=180, outline='brown', width=10, style="arc")
        self.canvas.create_arc(310, 150, 330, 160, start=180, extent=180, outline='brown', width=10, style="arc")
        self.canvas.create_arc(560, 140, 580, 150, start=180, extent=180, outline='brown', width=10, style="arc")

        rect_height = 105
        rect_y = 150
        rect_start_x = 325
        rect_end_x = 330
        self.tree2 = canvas.create_rectangle(rect_start_x, rect_y, rect_end_x, rect_y + rect_height, fill='coral', outline='black')

        start_x = 330  
        end_x = 360  

        for i in range(0, 6):
            start_y = 150 + (i * 10)  
            end_y = start_y + 32 


            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='green', width=5)

        rect_height = 105
        rect_y = HEIGHT - 50 - rect_height +5
        rect_start_x = 240
        rect_end_x = 330
        self.block1=canvas.create_rectangle(rect_start_x, rect_y, rect_end_x, rect_y + rect_height, fill='coral', outline='black')

        rect_height = 35
        rect_y = HEIGHT - 50 - rect_height +5
        rect_start_x = 325
        rect_end_x = 450
        self.block2=canvas.create_rectangle(rect_start_x, rect_y, rect_end_x, rect_y + rect_height, fill='coral', outline='black')

        self.canvas = canvas
        self.rect_height = 6
        self.rect_y = 100
        self.rect_start_x = 360
        self.rect_end_x = 410
        self.platform = self.canvas.create_rectangle(
            self.rect_start_x,
            self.rect_y,
            self.rect_end_x,
            self.rect_y + self.rect_height,
            fill='coral',
            outline='black'
        )

        rect_height = 40
        rect_y = 250
        rect_start_x = 325
        rect_end_x = 420
        self.block3=canvas.create_rectangle(rect_start_x, rect_y, rect_end_x, rect_y + rect_height, fill='coral', outline='black')

        rect_height = 119
        rect_y = 235
        rect_start_x = 90
        rect_end_x = 95
        self.tree1 = canvas.create_rectangle(rect_start_x, rect_y, rect_end_x, rect_y + rect_height, fill='coral', outline='black')

        start_x = 95  
        end_x = 125  
        for i in range(0, 6):
            start_y = 235 + (i * 10)  
            end_y = start_y + 32  

            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='green', width=5)
        start_x = 89  
        end_x = 59  
        for i in range(0, 6):
            start_y = 235 + (i * 10) 
            end_y = start_y + 32 

            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='green', width=5)

        self.ground = canvas.create_rectangle(0, HEIGHT-50, WIDTH, HEIGHT-45, outline='black', fill='coral', width=1)
        start_x = 324  
        end_x = 294  
        for i in range(0, 6):
            start_y = 150 + (i * 10) 
            end_y = start_y + 32  

            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='green', width=5)
        self.canvas.create_arc(10, 50, 300, -30, start=180, extent=60, outline='green', width=10, style="arc")
        self.canvas.create_arc(10, 80, 300, 0, start=180, extent=65, outline='green', width=10, style="arc")
        self.canvas.create_arc(10, 110, 300, 30, start=180, extent=72, outline='green', width=10, style="arc")
        self.canvas.create_arc(10, 140, 300, 60, start=180, extent=78, outline='green', width=10, style="arc")


        self.canvas.create_arc(520, 40, 605, -30, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.canvas.create_arc(490, 70, 610, 0, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.canvas.create_arc(460, 100, 610, 30, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.canvas.create_arc(430, 130, 610, 60, start=-30, extent=-120, outline='green', width=10, style="arc")
        self.obstacles.append(self.tree1)
        self.obstacles.append(self.tree2)
        self.obstacles.append(self.block1)
        self.obstacles.append(self.block2)
        self.obstacles.append(self.block3)
        self.obstacles.append(self.wood1)
        self.obstacles.append(self.wood2)
        self.obstacles.append(self.wood3)
        self.obstacles.append(self.platform)
        self.obstacles.append(self.ground)
        self.obstacles.append(self.leftwall)
        self.obstacles.append(self.rightwall)


        center_x = 70
        center_y = 100
        num_lines = 8
        line_length = 65
        angle_increment = 360 / num_lines
        octagon_vertices = []
        for i in range(num_lines):
            angle = math.radians(i * angle_increment)  
            end_x = center_x + line_length * math.cos(angle)
            end_y = center_y + line_length * math.sin(angle)
            octagon_vertices.append((end_x, end_y))
            self.canvas.create_line(center_x, center_y, end_x, end_y, fill='ivory2', width=3)
        for i in range(num_lines-8):
            start_x, start_y = octagon_vertices[i]
            end_x, end_y = octagon_vertices[(i + 1) % num_lines]
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='ivory2', width=3)
        for j in range(6):
            line_length -= 20  
            inner_octagon_vertices = []  
            for i in range(num_lines):
                angle = math.radians(i * angle_increment)  
                end_x = center_x + line_length * math.cos(angle)
                end_y = center_y + line_length * math.sin(angle)
                inner_octagon_vertices.append((end_x, end_y))
                self.canvas.create_line(center_x, center_y, end_x, end_y, fill='ivory2', width=3)
            for i in range(num_lines):
                start_x, start_y = inner_octagon_vertices[i]
                end_x, end_y = inner_octagon_vertices[(i + 1) % num_lines]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill='ivory2', width=3)

        center_x = 540
        center_y = 200
        num_lines = 8
        line_length = 65
        angle_increment = 360 / num_lines
        octagon_vertices = []
        for i in range(num_lines):
            angle = math.radians(i * angle_increment) 
            end_x = center_x + line_length * math.cos(angle)
            end_y = center_y + line_length * math.sin(angle)
            octagon_vertices.append((end_x, end_y))
            self.canvas.create_line(center_x, center_y, end_x, end_y, fill='ivory2', width=3)
        for i in range(num_lines-8):
            start_x, start_y = octagon_vertices[i]
            end_x, end_y = octagon_vertices[(i + 1) % num_lines]
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill='ivory2', width=3)
        for j in range(6):
            line_length -= 20 
            inner_octagon_vertices = []  

            for i in range(num_lines):
                angle = math.radians(i * angle_increment)  
                end_x = center_x + line_length * math.cos(angle)
                end_y = center_y + line_length * math.sin(angle)
                inner_octagon_vertices.append((end_x, end_y))
                self.canvas.create_line(center_x, center_y, end_x, end_y, fill='ivory2', width=3)
            for i in range(num_lines):
                start_x, start_y = inner_octagon_vertices[i]
                end_x, end_y = inner_octagon_vertices[(i + 1) % num_lines]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill='ivory2', width=3)
        
    def make_hill(self, x1, y1, x2, y2, height=100, delta=3):
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2 - height
            self.canvas.create_polygon(x1, y1, mid_x, mid_y, x2, y2, fill='brown') 

    def make_cloud(self, x, y):
        cloud_radius_x = 15  
        cloud_radius_y = 12 
        cloud_color = 'white'
        cloud_circles = []

        for i in range(3):
            circle_x = x + (i - 1) * cloud_radius_x * 0.8
            circle_y = y - cloud_radius_y * 1
            circle = self.canvas.create_oval(circle_x - cloud_radius_x, circle_y - cloud_radius_y, circle_x + cloud_radius_x, circle_y + cloud_radius_y, fill=cloud_color, outline='black')
            cloud_circles.append(circle)

        for i in range(5):
            circle_x = x + (i - 2) * cloud_radius_x * 0.8
            circle_y = y
            circle = self.canvas.create_oval(circle_x - cloud_radius_x, circle_y - cloud_radius_y, circle_x + cloud_radius_x, circle_y + cloud_radius_y, fill=cloud_color, outline='black')
            cloud_circles.append(circle)

        for i in range(3):
            circle_x = x + (i - 1) * cloud_radius_x * 0.8
            circle_y = y + cloud_radius_y * 1
            circle = self.canvas.create_oval(circle_x - cloud_radius_x, circle_y - cloud_radius_y, circle_x + cloud_radius_x, circle_y + cloud_radius_y, fill=cloud_color, outline='black')
            cloud_circles.append(circle)

        return cloud_circles
    
    def get_obstacles(self):
        return self.obstacles
    
    def update(self):
        rect_coords = self.canvas.coords(self.platform)
        rect_x1, rect_y1, rect_x2, rect_y2 = rect_coords

        min_x = 300  
        max_x = 500  

        if rect_x2 >= max_x and self.direction == 1:
            self.direction = -1  
        elif rect_x1 <= min_x and self.direction == -1:
            self.direction = 1  

        self.canvas.move(self.platform, self.direction, 0)


class Trophy:
    
    def __init__(self, canvas):

        self.canvas = canvas
        purple_egg = self.canvas.create_oval(12, 140, 32, 150, fill='orchid',outline= 'black')
        pink_egg = self.canvas.create_oval(92, 240, 110, 250, fill='pink',outline= 'black')
        red_egg = self.canvas.create_oval(310, 150, 330, 160, fill='red',outline= 'black')
        blue_egg = self.canvas.create_oval(22, 235, 42, 245, fill='blue',outline= 'black')
        yellow_egg = self.canvas.create_oval(330, 308, 350, 318, fill='yellow',outline= 'black')
        turquoise_egg = self.canvas.create_oval(560, 140, 580, 150, fill='turquoise',outline= 'black')
        
        self.trophies = [purple_egg, pink_egg,red_egg,blue_egg,yellow_egg,turquoise_egg]

    def get_trophy(self):
        return self.trophies

    def replace(self):
        for trophy_obj in self.trophies:
            self.canvas.delete(trophy_obj)  

        purple_egg = self.canvas.create_oval(12, 140, 32, 150, fill='orchid',outline= 'black')
        pink_egg = self.canvas.create_oval(92, 240, 110, 250, fill='pink',outline= 'black')
        red_egg = self.canvas.create_oval(310, 150, 330, 160, fill='red',outline= 'black')
        blue_egg = self.canvas.create_oval(22, 235, 42, 245, fill='blue',outline= 'black')
        yellow_egg = self.canvas.create_oval(330, 308, 350, 318, fill='yellow',outline= 'black')
        turquoise_egg = self.canvas.create_oval(560, 140, 580, 150, fill='turquoise',outline= 'black')


        self.trophies = [purple_egg, pink_egg, red_egg, blue_egg, yellow_egg, turquoise_egg]
 
class AI:

    def __init__(self, canvas, x, y):

        self.canvas = canvas
        self.spider = self.make_spider(x, y)
        self.thread = self.canvas.create_line(x+10, -180, x+10, y+5,
                                          fill='ivory2', width=3)
        self.x, self.y = 0, 0.5

    def make_spider(self, x, y):
        self.direction = 1
        color1 = 'black'
        head = self.canvas.create_oval(5, 5, 15, 13, fill=color1,outline= 'black')
        torso = self.canvas.create_oval(0, 10, 20, 40, fill=color1,outline='black')
        legs = [self.canvas.create_line(-5-i*5, 10*i+5, 5, 10*i+15,
                                        fill=color1, width=4) for i in range(2)] + \
            [self.canvas.create_line(15, 10*i+15, 25+i*5, 10*i+5,
                                        fill=color1, width=4) for i in range(2)] + \
            [self.canvas.create_line(-10+i*5, 10*i+35, 5, 10*i+25,
                                        fill=color1, width=4) for i in range(2)] + \
            [self.canvas.create_line(15, 10*i+25, 30-i*5, 10*i+35,
                                        fill=color1, width=4) for i in range(2)]

        spider = [head, torso] + legs
        for part in spider:
            self.canvas.move(part, x, y)
        return spider
    
    def update(self, eatable):
        spider_head_pos = self.canvas.coords(self.spider[0])
        spider_head_x = spider_head_pos[0]
        spider_head_y = spider_head_pos[1]
        new_x = spider_head_x + self.x
        new_y = spider_head_y + self.y
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if new_y >= canvas_height - 195: 
            self.y = -1.75 
        elif new_y <= 0:
            self.y = 1.75
        move_x = new_x - spider_head_x
        move_y = new_y - spider_head_y
        for part in self.spider:
            self.canvas.move(part, move_x, move_y)

        thread_coords = self.canvas.coords(self.thread)
        thread_x1, thread_y1, thread_x2, thread_y2 = thread_coords
        self.canvas.coords(self.thread, thread_x1 + move_x, thread_y1 + move_y, thread_x2 + move_x, thread_y2 + move_y)

    def check_collision(self, avatar_coords):
        oval_coords = self.canvas.coords(self.spider[1])
        if (
                avatar_coords[0] < oval_coords[2] and
                avatar_coords[2] > oval_coords[0] and
                avatar_coords[1] < oval_coords[3] and
                avatar_coords[3] > oval_coords[1]
            ):
                return True
        return False

class Avatar:
    
    def __init__(self, canvas):
        self.is_jumping = False
        self.falling = False
        self.gravity = 0.05
        color1 = 'lime'
        color2 = 'sandybrown'
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2, outline='black')
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20,fill=color1,outline='black')
        self.canvas.move(self.head, START_X, START_Y-20)
        self.canvas.move(self.torso, START_X, START_Y-20)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.x = 1
        self.y = 0
    
    def update(self, land, trophy):
        self.hit_object(land)
        x1, y1, x2, y2 = self.canvas.bbox(self.head)

        if x1 + self.x < 0 or x2 + self.x > WIDTH:
            self.x = 0

        if y1 + self.y < 0 or y2 + self.y > HEIGHT-60:
            self.y = 0

        if self.is_jumping:
            if self.y >= 0:
                self.is_jumping = False
                self.y = 3
                return
        if self.y > 0:
            self.falling = True
        else:
            self.falling = False
            

        if self.falling:
            self.y = 2
        else:
            self.y += self.gravity

            if y2 + self.y >= HEIGHT-60:
                self.y = 0
        self.canvas.move(self.head, self.x, self.y)
        self.canvas.move(self.torso, self.x, self.y)


    def move(self, event=None):
        if event.keysym == 'Left':
            self.x = -1
        elif event.keysym == 'Right':
            self.x = 1
        elif event.keysym == 'Up':
            self.y = -2
        elif event.keysym == 'Down':
            self.y = 1


    def hit_object(self, lands):
        torso_coords = tuple(self.canvas.coords(self.torso))
        torso_x1, torso_y1, torso_x2, torso_y2 = torso_coords
        obstacles = lands.get_obstacles()
        for obstacle in obstacles:
            object_x1, object_y1, object_x2, object_y2 = self.canvas.coords(obstacle)
            if torso_x2 >= object_x1 and torso_x1 <= object_x2 and torso_y2 >= object_y1 and torso_y1 <= object_y2:
                if torso_x1 < object_x1:
                    self.canvas.move(self.torso, -(torso_x2 - object_x1), 0)
                    self.canvas.move(self.head, -(torso_x2 - object_x1), 0)
                elif torso_x2 > object_x2:
                    self.canvas.move(self.torso, object_x2 - torso_x1, 0)
                    self.canvas.move(self.head, object_x2 - torso_x1, 0)
                if torso_y1 < object_y1:
                    self.canvas.move(self.torso, 0, -(torso_y2 - object_y1))
                    self.canvas.move(self.head, 0, -(torso_y2 - object_y1))
                elif torso_y2 > object_y2:
                    self.canvas.move(self.torso, 0, object_y2 - torso_y1)
                    self.canvas.move(self.head, 0, object_y2 - torso_y1)
   
    def find_trophy(self, trophy):
        avatar_coords = self.canvas.coords(self.torso)

        for troph in trophy:
            trophy_coords = self.canvas.coords(troph)
            if len(avatar_coords) >= 4 and len(trophy_coords) >= 4:
                if (
                    avatar_coords[0] < trophy_coords[2] and
                    avatar_coords[2] > trophy_coords[0] and
                    avatar_coords[1] < trophy_coords[3] and
                    avatar_coords[3] > trophy_coords[1]
                ):
                    self.canvas.delete(troph)
                    return True 
        return False 
    
    def replace(self):
        self.canvas.delete(self.head)
        self.canvas.delete(self.torso)
        self.is_jumping = False
        self.falling = False
        self.gravity = 0.05
        color1 = 'lime'
        color2 = 'sandybrown'
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2, outline='black')
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20,fill=color1,outline='black')
        self.canvas.move(self.head, START_X, START_Y-20)
        self.canvas.move(self.torso, START_X, START_Y-20)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.x = 1
        self.y = 0

if __name__ == '__main__':
    
    tk = Tk()
    tk.title('Skyland')
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
    canvas.pack()
    game = Skyland(canvas)
    mainloop()


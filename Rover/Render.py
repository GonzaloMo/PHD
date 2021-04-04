from ipycanvas import Canvas, hold_canvas
from ipywidgets import Image
import numpy as np
import matplotlib.pyplot as plt
import math
from time import sleep

class Render(object):
    def __init__(self, wall_thickness=0.1, scale=50, mx=600, my=600):
        self.scale = scale
        self.mx = mx
        self.my = my
        self.wall_th = wall_thickness

    def update_env(self, Rooms):
        self.Rooms = Rooms
        self.number_of_rooms = len(Rooms)
        self.n_grid = math.ceil(self.number_of_rooms**.5)
        self.max_x = self.n_grid*self.mx*(self.scale/100) 
        self.max_y = self.n_grid*self.my*(self.scale/100)
        self.x = np.arange(start=0, stop=1, step=1/self.n_grid)*self.max_x
        self.y = np.arange(start=0, stop=1, step=1/self.n_grid)*self.max_y
        self.offset = []
        k = 0
        for i in range(0,self.n_grid):
            for j in range(0,self.n_grid):
                if k < self.number_of_rooms:
                    self.offset.append([self.x[i],self.y[j]])
                k += 1

    def Single_Room(self, Room, fig=None):
        room_w = Room.x_delta  * self.scale
        room_h = Room.y_delta  * self.scale
        wall_width = self.wall_th * self.scale
        canvas_w = room_w + 2*wall_width
        canvas_h = room_h + 2*wall_width

        if fig==None:
            canvas = Canvas(width=canvas_w, height=canvas_h)
        else:
            canvas = fig
        
        

        # Draw Room
        canvas.fill_rect(0, 0, canvas_w, height=canvas_h)
        canvas.clear_rect(wall_width, wall_width, room_w, height=room_h)
        
        # Name of thr room
        canvas.font = '16px serif'
        canvas.stroke_text(Room.room_name, room_w/2, room_h/2)

        # Draw object insised the room 
        if Room.type_r == 'Initial':
            charging = Room.charging * self.scale
            trash_bin = Room.bin * self.scale
            m_w = Room.x_delta/10 
            m_h = 2*m_w
            canvas.fill_style = 'green'
            canvas.fill_rect(charging[0]+wall_width, charging[1]+wall_width, m_w*self.scale, height=m_w*self.scale)
            canvas.fill_style = 'blue'
            canvas.fill_rect(trash_bin[0]+wall_width, trash_bin[1]+wall_width, m_w*self.scale, height=m_h*self.scale)
        else:
            canvas.fill_style = 'brown'
            p_r = 0.1
            x, y, radius = [], [], []
            for i in range(0,Room.max_piece):
                x.append(Room.pieces_loc[i,0]*self.scale + wall_width)
                y.append(Room.pieces_loc[i,1]*self.scale + wall_width)
                radius.append(p_r*self.scale)
            canvas.fill_circles(x, y, radius)
        for i in Room.connections['Location']:
            size = 4*wall_width
            canvas.fill_style = 'red' 
            ncoord = Room.Location_2_norm_coordinate[i]
            x = (ncoord[0]*(room_w-size)) 
            y = (ncoord[1]*(room_h-size)) 
            canvas.fill_rect(x+wall_width, y+wall_width, size)
        return canvas

    def all_rooms(self,canvas=None):
        if canvas == None:
            canvas = Canvas(width=self.max_x, height=self.max_y)
        k=0
        for i in range(0,self.n_grid):
            for j in range(0,self.n_grid):
                if k < self.number_of_rooms:
                    canvas2 = self.Single_Room(self.Rooms[k])
                    canvas.draw_image(canvas2, self.x[i], self.y[j])
                k += 1
        return canvas

    def Single_connection(self, canvas, room_1, room_2, color='red'):
        room_id_1 = room_1.room_id
        room_id_2 = room_2.room_id
        ind_1 = room_1.connections['id'].index(room_id_2)
        ind_2 = room_2.connections['id'].index(room_id_1)
        
        room_w_1 = room_1.x_delta  * self.scale
        room_h_1 = room_1.y_delta  * self.scale
        room_w_2 = room_2.x_delta  * self.scale
        room_h_2 = room_2.y_delta  * self.scale

        loc_1 = room_1.connections['Location'][ind_1]
        loc_2 = room_2.connections['Location'][ind_2]
        ncoord_1 = room_1.Location_2_norm_coordinate[loc_1]
        ncoord_2 = room_2.Location_2_norm_coordinate[loc_2]
        x_1_l = ncoord_1[0]*room_w_1
        y_1_l = ncoord_1[1]*room_h_1
        x_2_l = ncoord_2[0]*room_w_2
        y_2_l = ncoord_2[1]*room_h_2

        x_1_g = x_1_l + self.offset[room_id_1][0] + self.wall_th * self.scale
        y_1_g = y_1_l + self.offset[room_id_1][1] + self.wall_th  * self.scale
        x_2_g = x_2_l + self.offset[room_id_2][0] + self.wall_th * self.scale
        y_2_g = y_2_l + self.offset[room_id_2][1] + self.wall_th * self.scale
        
        canvas.stroke_style = color
        canvas.stroke_line(x_1_g, y_1_g, x_2_g, y_2_g)

        return canvas

    def all_connections(self, canvas):
        for room in self.Rooms:
            for i in range(0, len(room.connections['id'])):
                connected_room_id = room.connections['id'][i]
                room_c = self.Rooms[connected_room_id]
                canvas = self.Single_connection(canvas, room, room_c)
        return canvas
    
    def robot(self, canvas, x, y, room):
        rbt_img = Image.from_file('Images/robot.jpg')
        x = x * self.scale
        y = y * self.scale
        x += self.offset[room][0] + self.wall_th * self.scale
        y += self.offset[room][1] + self.wall_th * self.scale

        canvas3 = Canvas(width=1000, height=1000)
        canvas3.draw_image(rbt_img, 0, 0)
        canvas3.scale(0.1*self.scale/50)

        canvas.clear_rect(x, y, self.wall_th)
        canvas.draw_image(canvas3, x, y)
        
        return canvas

    def env_render(self, canvas=None):
        canvas = self.all_rooms(canvas=canvas)
        canvas = self.all_connections(canvas)
        return canvas

    def full_render(self, x, y, room, canvas=None):
        canvas = self.env_render(canvas)
        canvas = self.robot(canvas, x, y, room)
        return canvas
    
    def animate(self, x, y, room, t):
        canvas = self.full_render(x[0], y[0], room[0])
        for i in range(1,len(t)):
            with hold_canvas(canvas):
                # Clear the old animation step
                canvas.clear()
                canvas = self.full_render(x[i], y[i], room[i], canvas=canvas)
            # Animation frequency ~50Hz = 1./50. seconds
            sleep(0.02)
            canvas
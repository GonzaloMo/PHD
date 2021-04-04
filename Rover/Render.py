from ipycanvas import Canvas, hold_canvas, MultiCanvas
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
        self.margin = 0.5
        self.wall_th = wall_thickness

    def problem_2_canvas(self, x):
        x = (x + self.wall_th + self.margin) * self.scale 
        return x

    def update_env(self, Zones):
        self.Zones = Zones
        self.number_of_Zones = len(Zones)
        self.max_x = 0
        self.max_y = 0
        for i in range(0,self.number_of_Zones):
            offset = self.Zones[i].coordinates * self.scale
            max_x = offset[0] + (Zones[i].x_delta  + 2*self.margin + 2*self.wall_th) * self.scale
            max_y = offset[1] + (Zones[i].y_delta  + 2*self.margin + 2*self.wall_th) * self.scale
            if max_x > self.max_x:
                self.max_x = int(max_x)
            if max_y > self.max_y:
                self.max_y = int(max_y)
        self.max_x+=200
        self.max_y+=200
        
    def Single_Zone(self, Zone, fig=None, offset=np.array([0,0])):
        w = self.margin
        wall_width = self.wall_th * self.scale
        Zone_w = (Zone.x_delta  + 2*w)* self.scale
        Zone_h = (Zone.y_delta  + 2*w)* self.scale
        canvas_w = Zone_w + 2*wall_width
        canvas_h = Zone_h + 2*wall_width
        w = w * self.scale
        if fig==None:
            canvas = MultiCanvas(4, width=canvas_w, height=canvas_h)
            """
            Mars_img = Image.from_file('Images/Mars_surface.jpeg')
            canvas3 = Canvas(width=1000, height=1000)
            canvas3.draw_image(Mars_img, 0, 0)
            canvas3.scale(0.1*self.scale/50)
            canvas[0].draw_image(canvas3, 0, 0)
            """
            
        else:
            canvas = fig
        
        # Draw Zone
        canvas[1].translate(offset[0], offset[1])
        canvas[1].fill_rect(0, 0, canvas_w, height=canvas_h)
        canvas[1].clear_rect(wall_width, wall_width, Zone_w, height=Zone_h)

        # Name of thr Zone
        canvas[1].font = '16px serif'
        canvas[1].stroke_text(Zone.name, Zone_w/2, 4*wall_width)
        canvas[1].translate(-offset[0], -offset[1])

        # Draw object insised the Zone 
        canvas[2].translate(offset[0], offset[1])
        if Zone.type == 'Landing_zone':
            charging = self.problem_2_canvas(Zone.charger)
            trash_bin = self.problem_2_canvas(Zone.deposit)
            canvas[2].fill_style = 'green'
            canvas[2].fill_rect(charging[0]-w/2, charging[1]-w/2, w)
            canvas[2].fill_style = 'blue'
            canvas[2].fill_rect(trash_bin[0]-w/2, trash_bin[1]-w/2, w)
        else:
            canvas[2].fill_style = 'brown'
            p_r = 0.1
            x, y, radius = [], [], []
            for i in range(0,Zone.max_sample):
                sam_coord = self.problem_2_canvas(Zone.samples_loc[i,:])
                x.append(sam_coord[0])
                y.append(sam_coord[1])
                radius.append(p_r*self.scale)
            canvas[2].fill_circles(x, y, radius)
        for i in Zone.connections['Location']:
            canvas[2].fill_style = 'red' 
            c_coord = self.problem_2_canvas(Zone.Location_2_coordinate[i])
            x = c_coord[0]
            y = c_coord[1]
            canvas[2].fill_rect(x-w/2, y-w/2, w)
        canvas[2].translate(-offset[0], -offset[1])
        return canvas

    def all_Zones(self,canvas=None):
        if canvas == None:
            canvas = MultiCanvas(4, width=self.max_x, height=self.max_y)
        for i in range(0,self.number_of_Zones):
            offset = self.Zones[i].coordinates * self.scale
            canvas = self.Single_Zone(self.Zones[i], fig=canvas, offset=offset)

        return canvas

    def Single_connection(self, canvas, Zone_1, Zone_2, color='red'):
        Zone_id_1 = Zone_1.id
        Zone_id_2 = Zone_2.id
        ind_1 = Zone_1.connections['id'].index(Zone_id_2)
        ind_2 = Zone_2.connections['id'].index(Zone_id_1)
        
        offset_1 = Zone_1.coordinates * self.scale
        offset_2 = Zone_2.coordinates * self.scale

        loc_1 = Zone_1.connections['Location'][ind_1]
        loc_2 = Zone_2.connections['Location'][ind_2]
        print('z = '+str(Zone_id_1)+' loc '+loc_1+' --- z = '+str(Zone_id_2)+' loc '+loc_2)
        coord_1 = self.problem_2_canvas(Zone_1.Location_2_coordinate[loc_1])
        coord_2 = self.problem_2_canvas(Zone_2.Location_2_coordinate[loc_2])

        x_1 = coord_1[0] + offset_1[0]
        y_1 = coord_1[1] + offset_1[1]
        x_2 = coord_2[0] + offset_2[0]
        y_2 = coord_2[1] + offset_2[1]
        canvas[2].stroke_style = color
        canvas[2].stroke_line(x_1, y_1, x_2, y_2)

        return canvas

    def all_connections(self, canvas):
        for Zone in self.Zones:
            for i in range(0, len(Zone.connections['id'])):
                connected_Zone_id = Zone.connections['id'][i]
                Zone_c = self.Zones[connected_Zone_id]
                canvas = self.Single_connection(canvas, Zone, Zone_c)
        return canvas
    
    def rover(self, canvas, coord, Zone):
        rvr_img = Image.from_file('Images/rover.jpg')
        canvas3 = Canvas(width=1000, height=1000)
        canvas3.draw_image(rvr_img, 0, 0)
        canvas3.scale(0.025*self.scale/50)
    
        coord_rvr = self.problem_2_canvas(coord)
        x = coord_rvr[0] - 0.25*self.scale
        y = coord_rvr[1] - 0.25*self.scale
        offset = Zone.coordinates * self.scale
        canvas[3].translate(offset[0],offset[1])
        canvas[3].clear_rect(x, y, self.wall_th)
        canvas[3].draw_image(canvas3, x, y)
        canvas[3].translate(-offset[0],-offset[1])
        
        return canvas

    def env_render(self, canvas=None):
        canvas = self.all_Zones(canvas=canvas)
        canvas = self.all_connections(canvas)
        return canvas

    def full_render(self, coord, Zone, canvas=None):
        canvas = self.env_render(canvas)
        canvas = self.robot(canvas, coord, Zone)
        return canvas
    
    def animate(self, coord, Zone, t):
        canvas = self.full_render(coord[0], Zone[0])
        for i in range(1,len(t)):
            with hold_canvas(canvas):
                # Clear the old animation step
                canvas.clear()
                canvas = self.full_render(coord[i], Zone[i], canvas=canvas)
            # Animation frequency ~50Hz = 1./50. seconds
            sleep(0.02)
            canvas
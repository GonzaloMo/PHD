import numpy as np
import matplotlib.pyplot as plt
import random

class Zone(object):
    """
    
    Input variable:

    """
    def __init__(self, zone_name, zone_id, zone_type, zone_coordinates, x_lim=[0, 5], y_lim=[0, 5], margin_s=0.7, mean=3, sd=1):
        self.name = zone_name
        self.id = zone_id
        self.type = zone_type
        self.coordinates = zone_coordinates

        self.x_lim = np.asarray(x_lim)
        self.x_delta = x_lim[1] - x_lim[0]  
        self.y_lim = np.asarray(y_lim)
        self.y_delta = y_lim[1] - y_lim[0]  
        
        self.Possible_Locations = ['NW', 'W', 'SW', 'N', 'S', 'NE', 'E', 'SE']
        self.Location_2_coordinate = {}
        
        k = 0
        for x in [0, 0.5, 1]:
            for y in [0, 0.5, 1]:
                if not(x==0.5 and y==0.5):
                    self.Location_2_coordinate[self.Possible_Locations[k]] = np.array([x*self.x_delta,y*self.y_delta])
                    k += 1
        
        self.connections = {'id': [], 'Location': [],  'Battery Consumption': [], 'Duration': []}

        if self.type == 'Landing_zone':
            self.max_sample = 0
            self.charger = np.array([self.x_delta/2, self.y_delta/2]) 
            self.deposit = np.array([self.x_delta/2 + 2, self.y_delta/2 + 2])
        elif self.type == '4-corners':
            self.max_sample = 4
            self.samples_loc = np.array([[self.x_lim[0]+margin_s, self.y_lim[0]+margin_s], [self.x_lim[0]+margin_s, self.y_lim[1]-margin_s], [self.x_lim[1]-margin_s, self.y_lim[0]+margin_s], [self.x_lim[1]-margin_s, self.y_lim[1]-margin_s]])
        elif self.type == 'Random-corners':
            sample = np.random.rand(4)
            samples = np.array([[self.x_lim[0]+margin_s, self.y_lim[0]+margin_s], [self.x_lim[0]+margin_s, self.y_lim[1]-margin_s], [self.x_lim[1]-margin_s, self.y_lim[0]+margin_s], [self.x_lim[1]-margin_s, self.y_lim[1]-margin_s]])
            samples_loc = []
            self.max_sample = 0
            for i in range(0,4):
                if sample[i] > 0.5:
                    samples_loc.append(samples[i,:]) 
                    self.max_sample += 1
            self.samples_loc = np.asarray(samples_loc)
        elif self.type == 'Normal-Distribution':
            self.max_sample =int( sd*np.random.normal() + mean)
            sample = []
            for i in range(0,self.max_sample):
                x = (self.x_delta-2*margin_s) * random.random() + self.x_lim[0]+margin_s
                y = (self.y_delta-2*margin_s) * random.random() + self.y_lim[0]+margin_s
                sample.append([round(x,2), round(y,2)]) 
            self.samples_loc = np.asarray(sample)
        else:
           raise Exception("Not a valid type of Zone choose:\n Initial\n Set-location-number\n Set-location\n Normal-Distribution") 

    def connect(self, r_id, Loc, Bat_C, Dt):
        self.connections['id'].append(r_id)
        self.connections['Location'].append(Loc)
        self.connections['Battery Consumption'].append(Bat_C)
        self.connections['Duration'].append(Dt)
import Env_utils as env_util
import numpy as np
import random

class Rover_PG(object):
    def __init__(self):
        self.Zone_setup = ['Landing_zone', '4-corners','Random-corners','Normal-Distribution']
        self.Zone_names = []
        self.Zone_name2index = {}
        self.Zones = []
        self.number_of_Zones = 0

    def generate_1_Zone(self, Zone_name, setup, zone_coord):
        self.number_of_Zones += 1
        self.Zone_names.append(Zone_name)
        self.Zone_name2index[Zone_name] = self.number_of_Zones-1
        self.Zones.append(env_util.Zone(Zone_name, self.number_of_Zones-1, self.Zone_setup[setup], zone_coord))
    
    def generate_1_connection(self, Zone_1, Zone_2, loc_1, loc_2, Bat_C, dt):
        self.Zones[Zone_1].connect(Zone_2, loc_1, Bat_C, dt)
        self.Zones[Zone_2].connect(Zone_1, loc_2, Bat_C, dt)
    
    def Gen_Problem(self, PS):
        self.clear()
        n_of_Zones = len(PS['Type']) 
        for i in range(0,n_of_Zones):
            self.generate_1_Zone(PS['Names'][i], PS['Type'][i], np.asarray(PS['Coordinates'][i]))
        
        n_of_connestion =len(PS['Battery_consumption'])
        for i in range(0,n_of_connestion):
            self.generate_1_connection(PS['from_to'][i][0], PS['from_to'][i][1],
                                       PS['Location'][i][0], PS['Location'][i][1],
                                       PS['Battery_consumption'][i],
                                       PS['Duration'][i])
    def clear(self):
        self.Zone_names = []
        self.Zones = []
        self.Zone_name2index = {}
        self.number_of_Zones = 0        





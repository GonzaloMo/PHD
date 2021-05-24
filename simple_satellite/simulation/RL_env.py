import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from simulation.Simulation import SatelliteSim
from simulation.Reward_functions import Reward_v1 as Reward
from simulation.DrawSim import SatelliteView 
import pygame

# import the gym class and spaces
import gym
from gym import spaces

import numpy as np
class SimpleSat(gym.Env):

    def __init__(self, sim: SatelliteSim, time_step: float, degug=False):
        super(SimpleSat, self).__init__()
        
        # start render enviroment
        self.view = SatelliteView()
        # save the satelite enviroment
        self.SatSim = sim 
        self.t = 0
        self.dt= time_step

        # The actions available are:
        #  - 0: take picture
        #  - 1: analyze picture 
        #  - 2: Dump picture
        #  - 3: Do Nothing
        self.action_space = spaces.Discrete(4)

        # Observation space is composed as:
        # state = [time(continous), theta(continous), busy(binary), memory_picture(discrete), memory_analyze_pic(discrete), locations of targets, locations of ground station]
        max_memory = self.SatSim.MEMORY_SIZE
        self.observation_space = spaces.Box(low=np.array([0.0, 0.0, 0, 0, 0]), high=np.array([999999999, 360.0, 1, max_memory, max_memory]),
                                            shape=(5,), dtype=np.float)
        self.state = self.SatSim.get_state()
        self.Total_reward = 0

    def step(self, action, dt=1):

        next_state, done = self.SatSim.update(action, self.dt)
        reward = Reward(next_state, self.state, action)

        self.state = next_state
        self.Total_reward += reward
        info = {}
        observation = np.array(self.state)
        if not(observation.shape == self.observation_space.shape):
            print('Observation_space')
            print(self.observation_space.shape)
            print('Observation')
            print(observation.shape)
        return observation, reward, done, info

    def reset(self):
        self.SatSim.reset()
        self.state = self.SatSim.get_state()
        self.Total_reward = 0
        observation = np.array(self.state)
        return observation 

    def render(self):
        self.view.drawSim(self.SatSim)

    def close (self):
        pygame.quit()
import numpy as np

class rover_env(object):

  def __init__(self, Zones):
      self.zones = Zones
          
  def step(self, action):
    ...
    return observation, reward, done, info
  def reset(self):
    ...
    return observation  # reward, done, info can't be included
  def render(self, mode='human'):
    ...
  def close (self):
    ...
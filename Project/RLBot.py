import math
import numpy as np
import random

from Agent import Agent

class RLBot(Agent):
    def __init__(self):
        self.state = []
        self.Q = []

    def decide(self, pastCloses, observation, sold, action):
        action = random.getrandbits(1)
        if(action==1):
            sold = False
        else:
            sold = True

        return action, sold

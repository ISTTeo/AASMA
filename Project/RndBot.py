import random

from Agent import Agent

class RndBot(Agent):

    def decide(self, pastCloses,observation,sold,action):
        action = random.getrandbits(1)
        if(action==0):
            sold = True
        else:
            sold = False

        return action, sold
import random

from Agent import Agent

class RndBot(Agent):

    def decide(self, pastCloses, observation, sold):
        action = random.getrandbits(1)
        if(action==0):
            sold = 1
        else:
            sold = 0

        return action, sold
import numpy as np
from scipy.special import softmax
from RedTrainingEnv import *
from RLBot import *
from RndBot import *

class RedBot:

    def __init__(self, bots, wealth):
        print("Hey Komrade!")
        #self.weights = np.random.randn(len(bots))
        self.weights = [.5 for i in range(len(bots))]
        self.wealth = wealth
        self.profits = []
        self.bots = bots
        for b in bots:
            self.profits.append(display(b))

    def decide(self):
        investments = softmax(self.weights)*self.wealth
         
        for eI in range(len(self.profits[0])):
            for bI in range(len(self.bots)):
                print(investments)
                profit = self.profits[bI][eI]
                self.wealth += investments[bI]*profit
                if(profit > 0):
                    self.weights[bI] += 1
                elif(profit <0):
                    self.weights[bI] -= 1
                investments = softmax(self.weights)*self.wealth
        print(self.wealth)


red = RedBot([RLBot, RndBot],1000)
red.decide()



import numpy as np
from scipy.special import softmax

class RedBot:

    def __init__(self, bots, wealth):
        print("Hey Komrade!")
        self.weights = np.random.randn(len(bots))
        self.wealth = wealth
        
    def decide():
        investments = softmax(self.weights)*self.wealth
        for bI in range(len(bots)):
            self.wealth -= investments[bI]
            profit, returns = bots[bi].decide(investments[bi])
            self.wealth += returns
            if(profit):
                self.weights[bi] += 1


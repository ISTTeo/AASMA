import numpy as np
from scipy.special import softmax
from RedTrainingEnv import *
from RLBot2 import *
from RLBot1 import *
from RndBot import *
from TurtleBot import *
import itertools

botLst = [TurtleBot,RLBot1,RLBot2]
allCombs = []
for L in range(2, len(botLst)+1):
    for subset in itertools.combinations(botLst, L):
        allCombs.append(subset)


class RedBot:

    def __init__(self, bots, initWealth):
        print("Hey Komrade!")
        #self.weights = np.random.randn(len(bots))
        self.weights = [.5 for i in range(len(bots))]
        self.wealth = initWealth
        self.profits = []
        self.bots = bots
        for b in bots:
            self.profits.append(display(b))
        self.wealthHistory = [initWealth]

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
            
            self.wealthHistory.append(self.wealth)

        
        return self.wealthHistory

initWealth = 1000

for comb in allCombs:
    red = RedBot(comb ,initWealth)
    wealthHistory = red.decide()
    xAxis = [i*30 for i in range(len(wealthHistory)) ] 
    plt.xticks(xAxis)
    plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
    plt.title(str(comb))
    plt.plot(xAxis,wealthHistory)
    plt.show()

print(allCombs)

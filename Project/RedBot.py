import numpy as np
from scipy.special import softmax
from RedTrainingEnv import *
from RLBot2 import *
from RLBot1 import *
from RndBot import *
from TurtleBot import *
import itertools
import matplotlib.patches as mpatches

botLst = [TurtleBot,RLBot1,RLBot2]
allCombs = []
for L in range(2, len(botLst)+1):
    for subset in itertools.combinations(botLst, L):
        allCombs.append(subset)


class RedBot:

    def __init__(self, bots, initWealth,testN=0):
        print("Hey Komrade!")
        #self.weights = np.random.randn(len(bots))
        self.weights = [.5 for i in range(len(bots))]
        self.wealth = initWealth
        self.profits = []
        self.bots = bots
        for b in bots:
            self.profits.append(display(b,testN=testN))
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

#https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


colors = ['b','g','r','c','m','y']

epochSize = 30
intervalSize = testSets[0][1] - testSets[0][0]
nTicks = intervalSize//epochSize + 1
xAxis = [i*epochSize for i in range(nTicks) ] #Make sure x axis is lined up with epochs

for comb in allCombs:
    patches = []

    plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
    plt.title("Agents: " + str([i.__name__ for i in comb]))
    plt.xticks(xAxis)

    for iTest in range(len(testSets)):
        red = RedBot(comb ,initWealth,testN=iTest)
        wealthHistory = red.decide()
        plt.plot(xAxis,wealthHistory,colors[iTest])
        patches.append(mpatches.Patch(color=colors[iTest], label="Interval "+str(iTest+1)))
    patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
    plt.legend(handles=patches)
    plt.ylabel("Wealth")
    plt.xlabel("Time (days)")
    
    plt.show() 

for iTest in range(len(testSets)):
    patches = []
    
    plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
    plt.title("Interval: " + str(iTest+1))
    plt.xticks(xAxis)

    for iComb in range(len(allCombs)):
        comb = allCombs[iComb]
        red = RedBot(comb ,initWealth,testN=iTest)
        wealthHistory = red.decide()
        
        plt.plot(xAxis,wealthHistory,colors[iComb])
        
        patches.append(mpatches.Patch(color=colors[iComb], label=str([i.__name__ for i in comb])))
    patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
    plt.legend(handles=patches)
    plt.ylabel("Wealth")
    plt.xlabel("Time (days)")
    xAxis = [i*30 for i in range(len(wealthHistory)) ] 
    plt.xticks(xAxis)
    plt.show() 


print(allCombs)

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
for L in range(1, len(botLst)+1):
    for subset in itertools.combinations(botLst, L):
        allCombs.append(subset)

initWealth = 1000

colors = ['b','g','r','c','m','y', 'violet', 'lightcoral', 'saddlebrown', 'lime']

epochSize = 30

class RedBot:

    def __init__(self, bots, initWealth,testN=0):
        self.weights = [.5 for i in range(len(bots))]
        self.wealth = initWealth
        self.bots = bots
        self.trades = self.getTrades(testN)
        self.wealthHistory = [initWealth]
        

    def decide(self):
        
        investments = softmax(self.weights)*self.wealth
        
        for eI in range(len(self.trades[0])):
            for bI in range(len(self.bots)):
               
                epochTrades = self.trades[bI][eI]
                epochMoney = investments[bI]
                self.wealth -= epochMoney
                gotProfit, epochMoney = self.getEpochTradeResults(epochTrades,epochMoney)
                self.wealth += epochMoney
                if(gotProfit):
                    self.weights[bI] += 1
                else:
                    self.weights[bI] -= 1
                investments = softmax(self.weights)*self.wealth
            
            self.wealthHistory.append(self.wealth)

        
        return self.wealthHistory
    
    def getEpochTradeResults(self,trades,epochMoney):
        initEpochMoney = epochMoney
        for t in trades:
            if(epochMoney > 0):
                epochMoney = self.tradeResult(t,epochMoney)
                
            else:
                break;
        return epochMoney>initEpochMoney,epochMoney
    
    def tradeResult(self,trade,investment):
        nBought = investment//trade[0]
        diff = trade[1]-trade[0] 
        return nBought*diff + investment


    def getTrades(self, testN):
        trades = []
        for b in range(len(self.bots)):
            trades.append(display(self.bots[b],testN=testN))

        return trades


def wealthPerComb():
    intervalSize = testSets[0][1] - testSets[0][0]
    nTicks = intervalSize//epochSize + 1
    xAxis = [i*epochSize for i in range(nTicks) ] #Make sure x axis is lined up with epochs

    for comb in allCombs:
        patches = []

        plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
        names = str([i.__name__ for i in comb])
        plt.title("Agents: " + names)
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
        
        plt.savefig("graphs/Red_WpC_" + names)
        plt.show() 


def wealthPerInterval():
    intervalSize = testSets[0][1] - testSets[0][0]
    nTicks = intervalSize//epochSize + 1
    xAxis = [i*epochSize for i in range(nTicks) ] #Make sure x axis is lined up with epochs

    for iTest in range(len(testSets)):
        patches = []
        
        plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
        plt.title("Interval: " + str(iTest+1))
        plt.xticks(xAxis)

        for iComb in range(len(allCombs)):
            comb = allCombs[iComb]
            red = RedBot(comb, initWealth, testN=iTest)
            wealthHistory = red.decide()
            plt.plot(xAxis,wealthHistory,colors[iComb])
            patches.append(mpatches.Patch(color=colors[iComb], label=str([i.__name__ for i in comb])))

        patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
        plt.legend(handles=patches)
        plt.ylabel("Wealth")
        plt.xlabel("Time (days)")
        xAxis = [i*30 for i in range(len(wealthHistory)) ] 
        plt.xticks(xAxis)
        
        plt.savefig("graphs/Red_WpI_I" + str(iTest + 1))
        plt.show()

def redTest():
    wealthPerComb()
    wealthPerInterval()

redTest()

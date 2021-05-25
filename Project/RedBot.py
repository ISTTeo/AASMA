import numpy as np
import itertools
import matplotlib.patches as mpatches
from scipy.special import softmax

from RedTrainingEnv import *
from RLBot2 import *
from RLBot1 import *
from RndBot import *
from TurtleBot import *

epochSize = 30
initWealth = 1000
botLst = [TurtleBot, RLBot1, RLBot2]
intervalSize = testSets[0][1] - testSets[0][0]
colors = ['b','g','r','c','m','y', 'violet', 'lightcoral', 'lime', 'pink', 'deeppink', 'teal', 'tan', 'seagreen']

allCombs = [(RndBot,)]
for L in range(1, len(botLst)+1):
    for subset in itertools.combinations(botLst, L):
        allCombs.append(subset)

print(allCombs)

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
                break
        return epochMoney>initEpochMoney,epochMoney
    
    def tradeResult(self,trade,investment):
        nBought = investment//trade[0]
        diff = trade[1]-trade[0] 
        return nBought*diff + investment


    def getTrades(self, testN):
        trades = []
        for b in range(len(self.bots)):
            trades.append(redDisplay(self.bots[b],testN=testN))

        return trades


def train(agent):
    display(agent, train=True)


def test():
    setWealthHists = {}
    intervalSize = testSets[0][1] - testSets[0][0]
    randIter = 100
    rlIter = 10

    for testN in range(len(testSets)):
        wealthHist = {}
        print("------------------------------")
        print("Interval " + str(testN + 1))
        for comb in allCombs:
            botnames = str([i.__name__ for i in comb])
            print(botnames)
            if(len(comb) == 1):
                if(comb[0] == RndBot):
                    wealthHist[botnames] = [0 for n in range(intervalSize)]
                    for i in range(randIter):
                        red = RedBot(comb, initWealth, testN=testN)
                        wealthHist[botnames] = [x + y for x, y in zip(wealthHist[botnames], red.decide())]
                    wealthHist[botnames] = [x/(i+1) for x in wealthHist[botnames]]

                elif(comb[0] == TurtleBot):
                    red = RedBot(comb, initWealth, testN=testN)
                    wealthHist[botnames] = red.decide()

                else:
                    botN = 1 if(comb[0] == RLBot1) else 2
                    qFile = "q" + str(botN) + ".p"
                    wealthHist[botnames] = [0 for n in range(intervalSize)]
                    for i in range(rlIter):
                        red = RedBot(comb, initWealth, testN=testN)
                        wealthHist[botnames] = [x + y for x, y in zip(wealthHist[botnames], red.decide())]
                    wealthHist[botnames] = [x/(i+1) for x in wealthHist[botnames]]
            else:
                red = RedBot(comb, initWealth, testN=testN)
                wealthHist[botnames] = red.decide()

            profit = round(((wealthHist[botnames][-1] - wealthHist[botnames][0])/wealthHist[botnames][0]) * 100, 2)
            maxDrawdown = round(((wealthHist[botnames][0] - min(wealthHist[botnames]))/wealthHist[botnames][0]) * 100, 2)
            print("Final Profit: " + str(profit) + "%")
            print("Maximum Drawdown: " + str(maxDrawdown) + "%")
            print()

        print()
        setWealthHists[testN] = wealthHist
    
    plotWealthPerInterval(setWealthHists)
    plotWealthPerComb(setWealthHists)


def plotWealthPerComb(setWealthHists):
    nTicks = intervalSize//epochSize + 1
    xAxis = [i*epochSize for i in range(nTicks) ] #Make sure x axis is lined up with epochs

    for comb in allCombs:
        patches = []

        plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
        names = str([i.__name__ for i in comb])
        plt.title("Agents: " + names)
        plt.xticks(xAxis)
        
        for iTest in range(len(testSets)):
            wealthHistory = setWealthHists[iTest][names]
            plt.plot(xAxis,wealthHistory,colors[iTest])
            patches.append(mpatches.Patch(color=colors[iTest], label="Interval "+str(iTest+1)))

        patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
        plt.legend(handles=patches)
        plt.ylabel("Wealth")
        plt.xlabel("Time (days)")
        
        plt.savefig("graphs/Red_WpC_" + names)
        plt.show() 


def plotWealthPerInterval(setWealthHists):
    nTicks = intervalSize//epochSize + 1
    xAxis = [i*epochSize for i in range(nTicks) ] #Make sure x axis is lined up with epochs

    for iTest in range(len(testSets)):
        #lengths = [len(i) for i in allCombs]
        byLen = {} 
        
        for i in range(len(allCombs)):
            length = len(allCombs[i])
            if(not(length in byLen.keys())):        
                byLen[length] = []
            byLen[length].append(allCombs[i])

        
        


        for length in byLen.keys():
            patches = []
        
            plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
            plt.title("Interval "+ str(iTest+1) + " for length " + str(length)) 
            plt.xticks(xAxis)
            
            for iComb in range(len(byLen[length])):
                comb = byLen[length][iComb]
                names = str([i.__name__ for i in comb])
                wealthHistory = setWealthHists[iTest][names] 
                plt.plot(xAxis,wealthHistory,colors[iComb])
                patches.append(mpatches.Patch(color=colors[iComb], label=names))
            
            patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
            plt.legend(handles=patches)
            plt.ylabel("Wealth")
            plt.xlabel("Time (days)")
            xAxis = [i*epochSize for i in range(len(wealthHistory)) ] 
            plt.xticks(xAxis)
            plt.savefig("graphs/Red_WpI_I" + str(iTest + 1) + "_" + str(length+1))
            plt.show()


        """
        for iComb in range(len(allCombs)):
            
            comb = allCombs[iComb]
            names = str([i.__name__ for i in comb])
            wealthHistory = setWealthHists[iTest][names]
            plt.plot(xAxis,wealthHistory,colors[iComb])
            patches.append(mpatches.Patch(color=colors[iComb], label=names))
        
        patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
        plt.legend(handles=patches)
        plt.ylabel("Wealth")
        plt.xlabel("Time (days)")
        xAxis = [i*epochSize for i in range(len(wealthHistory)) ] 
        plt.xticks(xAxis)
        
        plt.savefig("graphs/Red_WpI_I" + str(iTest + 1))
        plt.show()
        """
test()

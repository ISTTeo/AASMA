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
colors = ['b','g','r','c','m','y',  'lime','darkorange', 'seagreen']

allCombs = [(RndBot,)]
for L in range(1, len(botLst)+1):
    for subset in itertools.combinations(botLst, L):
        allCombs.append(subset)


class RedBot:

    def __init__(self, bots, initWealth,testN=0):
        self.weights = [.5 for i in range(len(bots))]
        self.wealth = initWealth
        self.bots = bots
        self.trades = self.getTrades(testN)
        self.wealthHistory = [initWealth]
        self.moneyChanges = []
        

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
                beforeTrade = epochMoney
                epochMoney = self.tradeResult(t,epochMoney)
                if(beforeTrade != epochMoney):
                    self.moneyChanges.append((beforeTrade, epochMoney))
                
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


def train(agent, seed=21):
    display(agent, train=True, seed=seed)


def test():
    setWealthHists = {}
    intervalSize = testSets[0][1] - testSets[0][0]
    randIter = 100
    rlIter = 10

    for testN in range(len(testSets)):
        wealthHist = {}
        print("------------------------------")
        print("------------------------------")
        print("Interval " + str(testN + 1))
        print("------------------------------")
        print("------------------------------")
        print()
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
                else:
                    red = RedBot(comb, initWealth, testN=testN)
                    wealthHist[botnames] = red.decide()
            else:
                red = RedBot(comb, initWealth, testN=testN)
                wealthHist[botnames] = red.decide()

            trades = red.moneyChanges
            wins = 0
            wonAmount = 0
            lostAmount = 0
            largestWin = 0
            largestLoss = 0

            for t in trades:
                change = t[1] - t[0]

                if change > 0:
                    wins += 1
                    wonAmount += change
                else:
                    lostAmount += abs(change)

                if change > largestWin:
                    largestWin = change
                if change <= 0 and abs(change) > largestLoss:
                    largestLoss = abs(change)

            largestWin = round(largestWin, 2)
            largestLoss = round(largestLoss, 2)
            percentWin = round(wins/len(trades) * 100, 2)
            percentLose = round(100 - percentWin, 2)
            avgWin = wonAmount/wins if wins > 0 else wonAmount
            avgWin = round(avgWin, 2)
            avgLoss = lostAmount/(len(trades) - wins) if (len(trades) - wins) > 0 else lostAmount
            avgLoss = round(avgLoss, 2)
            profit = round(((wealthHist[botnames][-1] - wealthHist[botnames][0])/wealthHist[botnames][0]) * 100, 2)
            maxDrawdown = round(((wealthHist[botnames][0] - min(wealthHist[botnames]))/wealthHist[botnames][0]) * 100, 2)
            
            print("Number of Trades: " + str(len(trades)))
            print("Final Profit: " + str(profit) + "%")
            print("Maximum Drawdown: " + str(maxDrawdown) + "%")
            print("Percentage of wins: " + str(percentWin) + "% | Percentage of losses: " + str(percentLose) + "%")
            print("Average won amount: " + str(avgWin) + " | Average lost amount: " + str(avgLoss))
            print("Largest won amount: " + str(largestWin) + " | Largest lost amount: " + str(largestLoss))
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
        names = str([i.__name__ for i in comb])

        plt.axhline(initWealth,0,360,color='k',linestyle='dashed')        
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
    sets = [allCombs[0:len(botLst)+1], allCombs[len(botLst)+1:]] 
    
    for iTest in range(len(testSets)):     
        for iSet in range(len(sets)):
            patches = []
            
            length = "1 agent" if iSet==0 else "combinations of 2 and 3 agents"
            plt.axhline(initWealth,0,360,color='k',linestyle='dashed')
            plt.title("Interval "+ str(iTest+1) + " for " + length) 
            plt.xticks(xAxis)
            
            for iComb in range(len(sets[iSet])):
                comb = sets[iSet][iComb]
                names = str([i.__name__ for i in comb])
                wealthHistory = setWealthHists[iTest][names] 
                iColor = iComb if iSet==0 else iComb + len(sets[0])

                plt.plot(xAxis,wealthHistory,colors[iColor])    
                patches.append(mpatches.Patch(color=colors[iColor], label=names))
            
            patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
            plt.legend(handles=patches)
            plt.ylabel("Wealth")
            plt.xlabel("Time (days)")
            xAxis = [i*epochSize for i in range(len(wealthHistory)) ] 
            plt.xticks(xAxis)
            length = "1" if iSet==0 else "2and3"
            plt.savefig("graphs/Red_WpI_I" + str(iTest + 1) + "_" + length)
            plt.show()


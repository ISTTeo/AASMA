import gym
import gym_anytrading
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import matplotlib.patches as mpatches
import numpy.random as rnd 

from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL

from RLBot2 import *
from RLBot1 import *
from RndBot import *
from TurtleBot import *


nTrain = 3000

#lists of type [beginDay, endDay] for testing
testSets = [[3100, 3465], [3465, 3830], [3830, 4195], [4195, 4560], [4560, 4925]]

botLst = [RndBot, TurtleBot, RLBot1, RLBot2]

colors = ['b','g','r','c','m','y']

def display(agentType, train=False, qFile=None, testN=0, seed=21):
    df = pd.read_csv("EURCADDAILY.csv")
    env = gym.make('forex-v0', df=df,frame_bound=(testSets[testN][0] + 1, testSets[testN][1]), window_size=1)   

    pastCloses = list(df['Close'][testSets[testN][0] - 60:testSets[testN][0]])
    observation = env.reset()
    sold = 0
    profit = []
    agent = agentType()

    if(train and agent.isRL()):
        rnd.seed(seed)
        Q = agent.qLearning(nTrain, list(df['Close']), 50)
        fname = "q" + str(agent.agentType()) + ".p"
        pickle.dump(Q, open(fname, "wb"))
    
    elif(qFile and agent.isRL()):
        rnd.seed(seed)
        Q = pickle.load(open(qFile, "rb"))
        agent.loadQ(Q)

    while(True):
        action, sold = agent.decide(pastCloses,observation,sold)

        profit.append(env._total_profit)

        pastCloses.append(observation[0][0])
        observation, reward, done, info = env.step(action)

        if done:
            pastCloses.append(observation[0][0])
            break

    plotProfit(profit)
    
    return profit

def plotProfit(profit):
    #plot the profit
    plt.plot(profit)
    plt.title("Profit by day")
    plt.ylabel("Profit")
    plt.xlabel("Trading day")
    plt.show() 

def test():
    setProfits = {}
    intervalSize = testSets[0][1] - testSets[0][0]
    randIter = 100
    rlIter = 10

    for setN in range(len(testSets)):
        profits = {}
        print("------------------------------")
        print("Interval " + str(setN + 1))
        for bot in botLst:
            botname = bot.__name__
            print(botname)
            if(bot == RndBot):
                profits[botname] = [0 for n in range(intervalSize)]
                for i in range(randIter):
                    profits[botname] = [x + y for x, y in zip(profits[botname], display(bot, testN=setN))]
                profits[botname] = [x/(i+1) for x in profits[botname]]
            else:
                if(bot == TurtleBot):
                    profits[botname] = display(bot, testN=setN)

                else:
                    botN = 1 if(bot == RLBot1) else 2
                    qFile = "q" + str(botN) + ".p"
                    profits[botname] = [0 for n in range(intervalSize)]
                    for i in range(rlIter):
                        profits[botname] = [x + y for x, y in zip(profits[botname], display(bot, qFile=qFile, testN=setN))]
                    profits[botname] = [x/(i+1) for x in profits[botname]]

            profit = round(profits[botname][-1] * 100, 2)
            maxDrawdown = round((1 - min(profits[botname])) * 100, 2)
            print("Final Profit: " + str(profit) + "%")
            print("Maximum Drawdown: " + str(maxDrawdown) + "%")
            print()

        print()
        setProfits[setN] = profits
    
    plotProfitPerInterval(setProfits)
    plotProfitPerBot(setProfits)

def plotProfitPerInterval(setProfits):
    for iTest in range(len(testSets)):
        patches = []
        plt.axhline(1,0,360,color='k',linestyle='dashed')
        plt.title("Interval: " + str(iTest+1))

        for iBot in range(len(botLst)):
            botName = botLst[iBot].__name__
            profits = setProfits[iTest][botName]
            
            plt.plot(profits,colors[iBot])
            
            patches.append(mpatches.Patch(color=colors[iBot], label=botName))

        patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
        plt.legend(handles=patches)
        plt.ylabel("Relative Profit")
        plt.xlabel("Time (days)")
        
        plt.savefig("graphs/PpI_" + str(iTest + 1))
        plt.show()

def plotProfitPerBot(setProfits):
    for iBot in range(len(botLst)):
        botName = botLst[iBot].__name__
        patches = []
        plt.axhline(1,0,360,color='k',linestyle='dashed')
        plt.title(botName)

        for iTest in range(len(testSets)):
            profits = setProfits[iTest][botName]
            
            plt.plot(profits,colors[iTest])
            
            patches.append(mpatches.Patch(color=colors[iTest], label="Interval: " + str(iTest + 1)))

        patches.append(mpatches.Patch(color='k', label="Profit Threshold"))
        plt.legend(handles=patches)
        plt.ylabel("Relative Profit")
        plt.xlabel("Time (days)")

        plt.savefig("graphs/PpB_" + botName)
        plt.show()

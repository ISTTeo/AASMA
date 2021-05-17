import gym
import gym_anytrading
import matplotlib.pyplot as plt
import pandas as pd

from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL

from RndBot import *
from TurtleBot import *
from RLBot import *

def display(agentType):
    #df = pd.read_csv("FOREX_EURUSD_1H_ASK_DAILY.csv")
    df = pd.read_csv("EURCADDAILY.csv")
    env = gym.make('forex-v0', df=df,frame_bound=(51, 3000), window_size=1)

    pastCloses = list(df['Close'][0:50])
    observation = env.reset()
    sold = 0
    previousSold = 0
    profit = []
    agent = agentType()
    bought = 0 
    
    profits = []
    profitEpoch = 0
    steps = 0
    while True:
        steps += 1

        previousSold = sold
        action, sold = agent.decide(pastCloses,observation,sold)
        
        if(action==1 and previousSold==1):
            bought = len(pastCloses)
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            #print("Bought at " + str(observation[0][0]))
        elif(action==0 and previousSold==0):
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            #print("Sold at " + str(observation[0][0]))
            #print("Profit in trade " + str(observation[0][0] - pastCloses[bought]))
            profitEpoch += observation[0][0] - pastCloses[bought]
        
        if(steps == 200):
            profits.append(profitEpoch)
            steps = 0
            profitEpoch = 0

        profit.append(env._total_profit)
        
        pastCloses.append(observation[0][0])
        observation, reward, done, info = env.step(action)
        if done:
            pastCloses.append(observation[0][0]) 
            break

    #print(pastCloses) #== 
    #print(list(df['Close'][0:199]))
    #plt.cla()
    #env.render_all()
    #plt.show()

    #plotProfit(profit)
    return profits

def plotProfit(profit):
    #plot the profit
    plt.plot(profit)
    plt.title("Profit by day")
    plt.ylabel("Profit")
    plt.xlabel("Trading day")
    plt.show()
#print("Turtle: " + str(turtleProfits))

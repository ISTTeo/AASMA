import gym
import gym_anytrading
import matplotlib.pyplot as plt
import pandas as pd
import pickle 
from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL

from RndBot import *
from TurtleBot import *
from RLBot2 import *

EPOCH_SIZE = 30
DATAFILE = "EURCADDAILY.csv"

testSets = [[3100, 3465], [3465, 3830], [3830, 4195], [4195, 4560], [4560, 4925]]

nTrain = 3000

def redDisplay(agentType, testN=0):
    df = pd.read_csv(DATAFILE)
    env = gym.make('forex-v0', df=df,frame_bound=(testSets[testN][0] + 1, testSets[testN][1]), window_size=1)
    env.trade_fee=0
    pastCloses = list(df['Close'][testSets[testN][0] - 60:testSets[testN][0]])
    observation = env.reset()
    sold = 0
    previousSold = 0
    profit = []
    agent = agentType()

    buyPrice = pastCloses[-1]  
    
    profits = []
    tradesEpoch = []
    steps = 0
    
    if(agent.isRL()):
        qFile = "q" + str(agent.agentType()) + ".p"
        Q = pickle.load(open(qFile, "rb"))
        agent.loadQ(Q)


    while True:
        steps += 1

        previousSold = sold
        action, sold = agent.decide(pastCloses,observation,sold)
        
        
        if(action==1 and previousSold==1):
            #Save last time you bought
            buyPrice = observation[0][0]
        elif(action==0 and previousSold==0):
            #Get profit using the last time you bought
            
            tradesEpoch.append((buyPrice,observation[0][0]))
        
        if(steps == EPOCH_SIZE):
            profits.append(tradesEpoch)
            steps = 0
            tradesEpoch = []

        profit.append(env._total_profit)
        
        pastCloses.append(observation[0][0])
        observation, reward, done, info = env.step(action)
        if done:
            #pastCloses.append(observation[0][0]) 
            break

    return profits

def display(agentType, train=False, qFile=None, testN=0):
    df = pd.read_csv("EURCADDAILY.csv")
    env = gym.make('forex-v0', df=df,frame_bound=(testSets[testN][0] + 1, testSets[testN][1]), window_size=1)

    pastCloses = list(df['Close'][testSets[testN][0] - 60:testSets[testN][0]])
    observation = env.reset()
    sold = 0
    profit = []
    agent = agentType()

    if(train and agent.isRL()):
        Q = agent.qLearning(nTrain, list(df['Close']), 50)
        fname = "q" + str(agent.agentType()) + ".p"
        pickle.dump(Q, open(fname, "wb"))
    
    elif(qFile and agent.isRL()):
        Q = pickle.load(open(qFile, "rb"))
        agent.loadQ(Q)

    while(not train):
        action, sold = agent.decide(pastCloses,observation,sold)

        profit.append(env._total_profit)

        pastCloses.append(observation[0][0])
        observation, reward, done, info = env.step(action)

        if done:
            pastCloses.append(observation[0][0])
            break

    return profit


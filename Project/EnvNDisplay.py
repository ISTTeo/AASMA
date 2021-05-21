import gym
import gym_anytrading
import matplotlib.pyplot as plt
import pandas as pd
import pickle

from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL


nTrain = 3000

#lists of type [beginDay, endDay] for testing
testSets = [[3100, 3465], [3465, 3830], [3830, 4195], [4195, 4560], [4560, 4925]]


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

    while True:
        action, sold = agent.decide(pastCloses,observation,sold)

        profit.append(env._total_profit)

        pastCloses.append(observation[0][0])
        observation, reward, done, info = env.step(action)

        if done:
            pastCloses.append(observation[0][0])
            break

    plt.cla()
    env.render_all()
    plt.show()

    plotProfit(profit)

def plotProfit(profit):
    #plot the profit
    plt.plot(profit)
    plt.title("Profit by day")
    plt.ylabel("Profit")
    plt.xlabel("Trading day")
    plt.show()
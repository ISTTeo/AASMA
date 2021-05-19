import gym
import gym_anytrading
import matplotlib.pyplot as plt
import pandas as pd
import pickle

from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL


def display(agentType, train=False, qFile=None):
    df = pd.read_csv("EURCADDAILY.csv")
    env = gym.make('forex-v0', df=df,frame_bound=(3101, 3465), window_size=1)

    pastCloses = list(df['Close'][3010:3100])
    observation = env.reset()
    sold = 0
    profit = []
    agent = agentType()

    print(len(df['Close']))

    if(train and agent.isRL()):
        Q = agent.qLearning(3000, list(df['Close']), 50)
        pickle.dump(Q, open("q.p", "wb"))
    
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
            #print("info:", info)
            break

    #print(pastCloses) #== 
    #print(list(df['Close'][0:199]))
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
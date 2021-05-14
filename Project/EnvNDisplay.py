import gym
import gym_anytrading
import matplotlib.pyplot as plt
import pandas as pd

from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL


def display(agentType):
    df = pd.read_csv("FOREX_EURUSD_1H_ASK_DAILY.csv")
    env = gym.make('forex-v0', df=df,frame_bound=(21, 200), window_size=1)

    pastCloses = list(df['Close'][0:20])
    observation = env.reset()
    sold = 0
    profit = []
    agent = agentType()

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
import gym
import gym_anytrading
from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL
import matplotlib.pyplot as plt
import pandas as pd
def display(decide):
    df = pd.read_csv("FOREX_EURUSD_1H_ASK_DAILY.csv")
    env = gym.make('forex-v0', df=df,frame_bound=(21, 200), window_size=1)
    # env = gym.make('stocks-v0', frame_bound=(50, 100), window_size=10)

    pastCloses = list(df['Close'][0:20])
    observation = env.reset()
    sold = False
    action = 0
    while True:

        action, sold = decide(pastCloses,observation,sold,action)

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

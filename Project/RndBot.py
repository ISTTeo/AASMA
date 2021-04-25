import gym
import gym_anytrading
from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("FOREX_EURUSD_1H_ASK_DAILY.csv")
env = gym.make('forex-v0', df=df,frame_bound=(21, 200), window_size=1)
# env = gym.make('stocks-v0', frame_bound=(50, 100), window_size=10)

obs = []

observation = env.reset()
while True:
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    obs.append({"obs":observation[0]})
    #env.render()
    if done:
        print("info:", info)
        break

plt.cla()
env.render_all()
plt.show()

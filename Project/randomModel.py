import gym
import gym_anytrading
import matplotlib.pyplot as plt

from gym_anytrading.envs import TradingEnv, ForexEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK

# Short: Red 
# Long:  Green

env = gym.make('forex-v0', frame_bound=(50, 100), window_size=10)

# env = gym.make(df=FOREX_EURUSD_1H_ASK, 
#                 frame_bound=(50, len(FOREX_EURUSD_1H_ASK)), 
#                 window_size=30)

env = gym.make('forex-v0',
               df = FOREX_EURUSD_1H_ASK,
               window_size = 10,
               frame_bound = (10, len(FOREX_EURUSD_1H_ASK)),
               unit_side = 'right')

observation = env.reset()
while True:
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    # env.render()
    if done:
        print("info:", info)
        break

plt.cla()
env.render_all()
plt.show()
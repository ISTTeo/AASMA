import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from stable_baselines import A2C
from stable_baselines.common.vec_env import DummyVecEnv

import gym
import gym_anytrading
from gym_anytrading.envs import TradingEnv, ForexEnv, Actions, Positions 
# from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK

df = pd.read_csv('./FOREX_EURUSD_1H_ASK.csv')

print(df.head)


# env = gym.make('forex-v0', frame_bound=(50, 100), window_size=10)

# # env = gym.make(df=FOREX_EURUSD_1H_ASK, 
# #                 frame_bound=(50, len(FOREX_EURUSD_1H_ASK)), 
# #                 window_size=30)

# env = gym.make('forex-v0',
#                df = FOREX_EURUSD_1H_ASK,
#                window_size = 10,
#                frame_bound = (10, len(FOREX_EURUSD_1H_ASK)),
#                unit_side = 'right')

# observation = env.reset()
# policy_kwargs = dict(net_arch=[64, 'lstm', dict(vf=[128, 128, 128], pi=[64, 64])])
# model = A2C('MlpLstmPolicy', env, verbose=1, policy_kwargs=policy_kwargs)
# model.learn(total_timesteps=1000)


# plt.cla()
# env.render_all()
# plt.show()
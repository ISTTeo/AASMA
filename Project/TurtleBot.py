import gym
import gym_anytrading
from gym_anytrading.envs import TradingEnv, ForexEnv, StocksEnv, Actions, Positions 
from gym_anytrading.datasets import FOREX_EURUSD_1H_ASK, STOCKS_GOOGL
import matplotlib.pyplot as plt
import pandas as pd#System 1 
#Not considering units
#Not considering intraday pricing
#Not trading amounts TODO apparently you just buy or sell ?!
df = pd.read_csv("FOREX_EURUSD_1H_ASK_DAILY.csv")
env = gym.make('forex-v0', df=df,frame_bound=(21, 200), window_size=1)
# env = gym.make('stocks-v0', frame_bound=(50, 100), window_size=10)

pastCloses = list(df['Close'][0:20])
observation = env.reset()
sold = False
action = 0
while True:
    #print(observation)
    #print()
    lastClose = observation[0][0]
    min20 = min(pastCloses[-20:])
    max20 = max(pastCloses[-20:])
    
    breakout = False
    if(lastClose > max20 or  lastClose < min20): #Looks for breakout
        breakout = True #useless
        if(sold):
            action = 1 #buy
            sold = False #smarter way to do this just flip 0 and 1
        else:
            action = 0
            sold = True
    
    #action = env.action_space.sample()
    pastCloses.append(observation[0][0])
    observation, reward, done, info = env.step(action)

    if done:
        pastCloses.append(observation[0][0])
        print("info:", info)
        break
print(pastCloses) #== 
#print(list(df['Close'][0:199]))
plt.cla()
env.render_all()
plt.show()

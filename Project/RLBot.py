import math
import numpy as np
import random 
import numpy.random as rnd 

from Agent import Agent


class Actions(Enum):
    Sell = 0
    Buy = 1

timeInterval = [10,50]
percentages = [0,1,2,3,4,5,6,7,8,9,10,666]
qEntries = []
for k in range(len(percentages)):
    qEntries.append(str((timeInterval[0],percentages[k],timeInterval[1],percentages[k],0)))
    qEntries.append(str((timeInterval[0],percentages[k],timeInterval[1],percentages[k],1)))
    qEntries.append(str((timeInterval[0],percentages[k],timeInterval[1],percentages[k],0)))
    qEntries.append(str((timeInterval[0],percentages[k],timeInterval[1],percentages[k],1)))
qTable = {}

for key in qEntries:
    qTable[key] = np.array([0,0])

def egreedy(Q, eps=0.1):
    N = Q.shape[0]
    r = rnd.random()

    if r < eps:
        return rnd.randint(N)

    else:
        prob = np.zeros((N,))
        min_indexes = np.where(Q == Q.min())
        for i in min_indexes:
            prob[i] = 1/len(min_indexes[0])
        return rnd.choice(N, p = prob)

def qlearning(Q, lr, gamma, n, prices, index):

    s = getState(prices, index, 1)
    sold = 1
    last_trade = index - 1

    for i in range(n):
        a = egreedy(Q[s], 0.15)
        r = reward(a, sold, prices, index, last_trade)

        if(hasTraded(a, sold)):
            last_trade = index

        sold = 0 if a==Actions.Buy.value else 1
        index += 1
        sNew = getState(prices, index, sold)

        Q[s][a] = Q[s][a] + lr * (r + gamma * np.max(Q[sNew]) - Q[s][a])
        s = sNew

    return Q

def hasTraded(action, sold):
    if ((action == Actions.Buy.value and sold) or
        (action == Actions.Sell.value and not sold)):
        return True
    
    return False


def getState(prices, index, sold):
    var1 = round((prices[index]/prices[index - timeInterval[0]]) * 100)
    if(var1 > 10):
        var1 = 666
    
    var2 = round((prices[index]/prices[index - timeInterval[1]]) * 100)
    if(var2 > 10):
        var2 = 666

    return str((timeInterval[0], var1, timeInterval[1], var2, sold))


def reward(action, sold, prices, index, last_trade):
    step_reward = 0

    trade = hasTraded(action, sold)

    if trade:
        current_price = prices[index]
        last_trade_price = prices[last_trade]
        price_diff = current_price - last_trade_price

        if action == Actions.Buy.value:
            step_reward += -price_diff * 10000
        else:
            step_reward += price_diff * 10000

    return step_reward



class RLBot(Agent):
    def __init__(self):
        self.state = []
        self.Q = []

    def decide(self, pastCloses, observation, sold, action, env):
        action = random.getrandbits(1)
        if(action==0):
            sold = True
        else:
            sold = False

        return action, sold

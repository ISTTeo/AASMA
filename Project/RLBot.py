import math
import numpy as np
import random 
import numpy.random as rnd 
from enum import Enum
from Agent import Agent


timeInterval = [10,50]
percentages = [0,2,4,6,8,10,666]
percentagesShort = [0,2,4,666]
percentagesLong = [0,4,8,12,666]
lr = 0.1
gamma = 0.9

class Actions(Enum):
    Sell = 0
    Buy = 1

def initQ():

    qEntries = []
    for k in range(len(percentagesShort)):
        for i in range(len(percentagesLong)):
            qEntries.append(str((timeInterval[0],percentagesShort[k],timeInterval[1],percentagesLong[i],0)))
            qEntries.append(str((timeInterval[0],-percentagesShort[k],timeInterval[1],-percentagesLong[i],0)))
            qEntries.append(str((timeInterval[0],percentagesShort[k],timeInterval[1],-percentagesLong[i],0)))
            qEntries.append(str((timeInterval[0],-percentagesShort[k],timeInterval[1],percentagesLong[i],0)))
            qEntries.append(str((timeInterval[0],percentagesShort[k],timeInterval[1],percentagesLong[i],1)))
            qEntries.append(str((timeInterval[0],-percentagesShort[k],timeInterval[1],-percentagesLong[i],1)))
            qEntries.append(str((timeInterval[0],percentagesShort[k],timeInterval[1],-percentagesLong[i],1)))
            qEntries.append(str((timeInterval[0],-percentagesShort[k],timeInterval[1],percentagesLong[i],1)))
        


    qTable = {}

    for key in qEntries:
        qTable[key] = np.array([0,0])
    
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(qTable)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return qTable

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

def qLearning(n, prices, index):

    Q = initQ()

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
    var1 = round((prices[index]/prices[index - timeInterval[0]]) * 100 - 100)
    
    var1 = (min(percentagesShort, key=lambda x:abs(x-var1)))
    if(var1<0):
        var1 *= -1
    
    if(abs(var1) > percentagesShort[-2]):
        var1 = 666
    
    var2 = round((prices[index]/prices[index - timeInterval[1]]) * 100 - 100)

    var2 = min(percentagesLong, key=lambda x:abs(x-var2))
    
    if(var2<0):
        var2 *= -1
    
    if(abs(var2) > percentagesLong[-2]):
        var2 = 666

    return str((timeInterval[0], var1, timeInterval[1], var2, sold))

#Roubado ao ambiente depois mudar sidjfaisdjfsa]
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
        self.Q = initQ()
        self.lastState = None
        self.lastAction = 0
        self.lastTrade = 0
    
    def decide(self, pastCloses, observation, sold):
        price = observation[0][0]
        pastCloses.append(price)
        currentState = getState(pastCloses, len(pastCloses) - 1, sold)

        if(self.lastState):
            r = reward(self.lastAction, sold, pastCloses, len(pastCloses) - 2, self.lastTrade)
            self.Q[lastState][lastAction] =  self.Q[lastState][lastAction] + lr * (r + gamma * max(self.Q[currentState]) - self.Q[lastState][lastAction])
        
        action = np.argmax(self.Q[currentState])
        sold = 0 if action==Actions.Buy.value else 1

        self.lastAction = action
        self.lastState = currentState

        if hasTraded(action, sold):
            self.lastTrade = price

        return action, sold

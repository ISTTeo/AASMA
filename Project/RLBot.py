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
#percentages = [10,20,60,70,80,90,95,666]

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

def qLearning(lr, gamma, n, prices, index):

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
        i *= -1
    
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
        self.lastActionIndex = 0
        self.lastTrade = 0
    
    def decide(self, pastCloses, observation, sold, action,iterIndex, prices, env=None):
        action = random.getrandbits(1)
    
        if(action==0):
            sold = True
        else:
            sold = False
        
        #TODO Cant depend on lastState 
        currentState = getState(prices,iterIndex,0)
        if(self.lastState):
            currentState = getState(prices,iterIndex,self.lastState[-1])
            lastState = str(self.lastState)

            r = reward(self.lastActionIndex,self.lastState[-1],prices,iterIndex, self.lastTrade)
            Q[lastState][lastActionIndex] =  Q[lastState][lastActionIndex] + lr * (r + gamma *max(Q[currentState])  - Q[lastState][lastActionIndex])

        self.lastActionIndex = action
        self.lastState = currentState
        self.lastTrade = prices[iterIndex]

        return action, sold

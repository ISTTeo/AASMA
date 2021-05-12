import math
import numpy as np
import random 
import numpy.random as rnd 

from Agent import Agent

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

def qlearning(Q,lr,gamma, n, qinit,env):
    nStates = len(Q[0])

    s = rnd.choice(nStates)

    for i in range(n):
        a = egreedy(Q[s], 0.15)
        trans = sample_transition(mdp, s, a) #TODO calculate ratio 
        c = trans[2]
        sNew = trans[3]

        Q[s][a] = Q[s][a] + lr * (c + gamma * np.min(Q[sNew]) - Q[s][a])
        s = sNew

    return Q

class RLBot(Agent):
    def __init__(self):
        self.state = []
        self.Q = []

        

    def decide(self, pastCloses, observation, sold, action,env):
        action = random.getrandbits(1)
        if(action==1):
            sold = False
        else:
            sold = True

        return action, sold

import random
def rndCide(pastCloses,observation,sold,action):
    action = random.getrandbits(1)
    if(action==1):
        sold = False
    else:
        sold = True

    return action, sold
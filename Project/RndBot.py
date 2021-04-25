import random
def rndCide(pastCloses,observation,sold,action):
    action =random.getrandbits(1)
    if(sold and action==1):
        sold = False
    elif(not sold and action==0):
        sold = True

    return action, sold



#System 1 
#Not considering units
#Not considering intraday pricing
#Not trading amounts TODO apparently you just buy or sell ?!
def turtleCide(pastCloses,observation,sold,action):
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

    return action, sold

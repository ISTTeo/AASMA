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

    if(lastClose > max20):
        if(sold):
            action = 1 #buy
            sold = False #smarter way to do this just flip 0 and 1
    elif(lastClose < min20):
        if(not sold):
            action = 0#sell
            sold = True

    else:#hold
        action = 0 if sold else 1

    return action, sold

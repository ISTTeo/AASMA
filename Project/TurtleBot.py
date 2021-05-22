from Agent import Agent

class TurtleBot(Agent):
    def decide(self, pastCloses, observation, sold):
        lastClose = observation[0][0]
        min20 = min(pastCloses[-20:])
        max20 = max(pastCloses[-20:])

        if(lastClose > max20):
            if(sold):
                action = 1 #buy
                sold = 0
            else:
                action = 0 if sold else 1

        elif(lastClose < min20):
            if(not sold):
                action = 0#sell
                sold = 1
            else:
                action = 0 if sold else 1

        else:#hold
            action = 0 if sold else 1

        return action, sold

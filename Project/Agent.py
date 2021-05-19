class Agent():
    def decide(self, pastCloses, observation, sold):
        raise NotImplementedError
    
    def isRL(self):
        return False
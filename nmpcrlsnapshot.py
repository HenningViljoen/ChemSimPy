

class nmpcrlsnapshot(object):
    def __init__(self, astate, anaction, areward, anewstate):
        self.state = astate
        self.action = anaction
        self.reward = areward #the reward signal as saved
        self.newstate = anewstate #the CVs are sampled from the world in the next time instant
        


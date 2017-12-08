

class point(object):
    def __init__(self, ax, ay):
        self.setxy(ax, ay)
        self.highlighted = False


    def copyfrom(self, pointcopyfrom):
        self.setxy(pointcopyfrom.x, pointcopyfrom.y)
        self.highlighted = pointcopyfrom.highlighted


    def setxy(self, ax, ay):
        self.x = ax
        self.y = ay


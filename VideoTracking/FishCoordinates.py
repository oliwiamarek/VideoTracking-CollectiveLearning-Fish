#
# Fish coordinates to be used throughout the program. Stores x and y values of coordinates.
#


class FishCoordinates(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

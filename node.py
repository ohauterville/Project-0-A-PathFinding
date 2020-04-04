import numpy as np


class Node():

    def __init__(self, x, y, beg_x, beg_y, end_x,end_y):
        self.x = x
        self.y = y
        self.g = self.dist(self.x, self.y, beg_x, beg_y)
        self.f = self.heuris(end_x, end_y)

    def heuris(self, end_y, end_x):
        h = self.dist(self.x, self.y, end_x, end_y)
        return self.g + h

    def dist(self, x1, y1, x2,y2):
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def get_voisin(self, limr, limc):
        voisins = []
        if self.x > 0:
            voisins.append( (self.x - 1, self.y) )
        if self.y > 0:
            voisins.append( (self.x, self.y - 1) )
        if self.x < limc - 1:
            voisins.append( (self.x + 1, self.y) )
        if self.y < limr - 1:
            voisins.append( (self.x, self.y + 1) )
        return voisins

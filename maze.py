import pygame
from operator import attrgetter
import numpy as np
from node import Node


class Maze:

    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.size = size
        if self.width%self.size != 0 or self.height%self.size != 0:
            self.width = 1200
            self.height = 1000
            self.size = 20
            print("Wrong dimension, override.")

        self.win = pygame.display.set_mode((self.width, self.height))
        self.matrix = np.zeros((int(self.height/self.size), int(self.width/self.size)))
        self.beg_x, self.beg_y = int(0/self.size), int(0/self.size)
        self.end_x, self.end_y = int(self.height/self.size)-1, int(self.width/self.size)-1
        self.wall = []
        self.openl = []
        self.closed = []
        self.best = []
        self.parent = []

    def create_matrix(self):
        for wall in self.wall:
            x, y = wall
            self.matrix[int(y/self.size), int(x/self.size)] = -1


    def solve(self):
        limrow, limcol = self.matrix.shape

        n = Node(self.beg_x, self.beg_y, self.beg_x, self.beg_y, self.end_x, self.end_y)
        self.openl.append(n)

        unsolved = True

        while self.openl:

            i = self.openl.index(min(self.openl, key=attrgetter('f')))
            cnode = self.openl.pop(i)
            list_voisins = cnode.get_voisin(limrow, limcol)

            if cnode.x == self.end_y and cnode.y == self.end_x:
                unsolved = False
                break
            else:
                for i in range(len(list_voisins)):

                    vx, vy = list_voisins[i]

                    if self.matrix[vy, vx] == 0:
                        if not ((vx, vy) in self.closed):
                            vnode = Node( vx, vy, self.beg_x, self.beg_y, self.end_x, self.end_y)

                            temp_g = cnode.g +1
                            v_g = vnode.g
                            done = False

                            for item in self.openl:
                                if item.x == vnode.x and item.y == vnode.y:
                                    if v_g > temp_g :
                                        vnode.g = temp_g
                                        vnode.f = vnode.g + vnode.heuris( self.end_x, self.end_y )
                                        #self.parent.remove(self.parent.index(vnode.x, vnode.y))
                                        #self.parent.append((vnode.x, vnode.y, cnode.x, cnode.y))
                                    self.openl.remove(item)
                                    self.openl.append(vnode)
                                    done = True

                                    break

                            if not done:
                                vnode.g = temp_g
                                vnode.f = vnode.g + vnode.heuris(self.end_x, self.end_y)
                                self.openl.append(vnode)
                                self.parent.append( (vnode.y, vnode.x, cnode.y, cnode.x) )


                if not (cnode.x, cnode.y) in self.closed:
                    self.closed.append((cnode.x, cnode.y))

                self.redraw()
                text = "Solving..."
                pygame.display.set_caption( text )
                clock.tick(60)


        self.closed.append((self.end_x, self.end_y))
        return unsolved

    def best_path(self):

        self.best.append((self.end_y, self.end_x))
        now = len(self.best)
        prev = 0
        while prev != now:

            prev = now
            for item in self.parent:
                x, y, px, py = item
                if (y,x) == self.best[-1]:
                    self.best.append((py,px))
                    now = len(self.best)
                    self.parent.remove(item)


        self.openl = []
        self.closed = []


    def redraw(self):

        self.win.fill(black)

        for cnodes in self.closed:
            x, y = cnodes
            pygame.draw.rect(self.win, dark_red, (x*self.size, y*self.size, self.size, self.size))

        for onodes in self.openl:
            pygame.draw.rect(self.win, blue , (onodes.x*self.size, onodes.y*self.size, self.size, self.size))

        for wall in self.wall:
            x, y = wall
            pygame.draw.rect(self.win, white, (x, y, self.size, self.size))

        """for i in range(int(self.width/self.size)):
            pygame.draw.line(win, white, (i*self.size, 0), (i*self.size, self.height))

        for i in range(int(self.height/self.size)):
            pygame.draw.line(win, white, (0, i*self.size), (self.width, self.size*i))"""

        pygame.draw.rect( self.win, red, (self.beg_y * self.size, self.beg_x * self.size, self.size, self.size) )
        pygame.draw.rect( self.win, green, (self.end_y * self.size, self.end_x * self.size, self.size, self.size) )
        pygame.display.update()


        for i in range(len(self.best)):
            for ii in reversed(range(i)):
                x, y = self.best[len(self.best)-ii-1]
                pygame.draw.rect(self.win, dark_red, (x*self.size, y*self.size, self.size, self.size))
            pygame.display.update()
            clock.tick(40)


    def random_wall(self, p):

        x, y = self.matrix.shape
        for i in range(x):
            for j in range(y):
                if np.random.uniform() < p and (i, j) != (self.beg_y, self.beg_x) and (i,j) != (self.end_y, self.end_x):
                    self.wall.append((j*self.size,i*self.size))

    def build_wall(self):

        mdown = True
        while mdown:
            m_pos = pygame.mouse.get_pos()
            x = m_pos[0] - m_pos[0]%self.size
            y = m_pos[1] - m_pos[1]%self.size

            if (x, y) != (self.beg_x, self.beg_y) and (x, y) != (self.end_x, self.end_y):
                if not (x, y) in self.wall:
                    self.wall.append((x, y))
            self.redraw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mdown = False


black = (0, 0, 0)
white = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)
dark_red = (128, 0, 0)
blue = (0, 0, 255)

clock = pygame.time.Clock()
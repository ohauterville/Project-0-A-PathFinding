""""
Hi welcome to the maze solver.

You can either draw your maze or randomly generate blocks, you can choose the with the height and the size of the squares.

If you want to draw your maze put maximum 3 arguments exemple run:
    - python astar.py WIDTH HEIGHT SIZE
    - python astar.py WIDTH SIZE         ### will create a square

If the dimension are not good, not divisible integer they will be ignored.

IF you want to generate a maze
    -python astar.py WIDTH HEIGHT SIZE DENSITY

    Density is a float number between 0 and 1
"""
import pygame
import sys
import time
from maze import Maze


if len(sys.argv)==5:

    width = int(sys.argv[1])
    height = int(sys.argv[2])
    size = int( sys.argv[3])
    p = float(sys.argv[4])

elif len(sys.argv)==4:
    width = int( sys.argv[1] )
    height = int( sys.argv[2] )
    size = int( sys.argv[3] )
    p = -1

elif len(sys.argv)==3:
    width = int( sys.argv[1] )
    height = width
    size = int( sys.argv[2] )
    p = -1

else:
    width = 1200
    height = 1000
    size = 20
    p = -1



def main():

    pygame.init()
    clock = pygame.time.Clock()

    maze = Maze(width, height, size)

    pygame.display.set_caption( "The maze will be solved, starts at green, ends at red." )

    run_init = True
    run = False

    if p >= 0 and p < 1:
        maze.random_wall(p)
    
    while run_init:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run, run_init = False, False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and p < 0:
                maze.build_wall()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True
                    run_init = False

        maze.redraw()
    
    maze.create_matrix()

    tb = time.time()
    success = maze.solve()
    te = time.time()

    text = "Solved : " + str(not success) + ", in " + str(round((te - tb), 1)) +  " seconds. Press space bar to quit."
    pygame.display.set_caption(text)

    if not success:
        maze.best_path()

    while run:

        maze.redraw()
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:

                run = False
                pygame.quit()


main()

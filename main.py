import pygame
import astar
import dfs
import bfs
import dijkstra
import ucs
import math

WIDTH = 800 # set the width of the window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Visual Search")

RED = (204, 0, 0) # for closed nodes
GREEN = (0, 204, 0) # for open nodes
BLUE = (0, 0, 255) # for ending node
WHITE = (255, 255, 255) # for empty nodes
BLACK = (0, 0,0) # for walls
PURPLE = (136, 3, 185) # for starting node
GREY = (128, 128, 128) # for grid lines
PINK = (249, 19, 180)  # for path
class Node:
    def __init__(self, row, col, width,  total_rows):
        self.row = row
        self.col = col
        self.x = row *  width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.distance_from_start = 0

    def get_position(self): 
        return self.row, self.col
    
    def is_closed(self): 
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == PURPLE
    
    def is_end(self):
        return self.color == BLUE
    
    def reset(self):
        self.color = WHITE

    def make_open(self): 
        self.color = GREEN

    def make_barrier(self): 
        self.color = BLACK

    def make_start(self): 
        self.color = PURPLE

    def make_end(self): 
        self.color = BLUE

    def make_path(self):
        self.color = PINK

    def make_closed(self, distance_from_start):
        self.distance_from_start = distance_from_start # store the distance from the start node
        self.set_distance_color(distance_from_start) # set the node's color based on its distance from the start node

    def set_distance_color(self, distance):
        max_intensity = 150 
        intensity = max(0, max_intensity - distance * 4) # calculate the intensity based on the distance
        
        base_color = (255, 128, 128) # light red
        dark_red = (128, 0, 0)

        red_component = max(dark_red[0], base_color[0] - intensity)  
        green_component = max(dark_red[1], base_color[1] - intensity)  
        blue_component = max(dark_red[2], base_color[2] - intensity)  

        self.color = (red_component, green_component, blue_component)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__  (self, other):
        return False

def make_grid(rows, width):
    grid  = []
    gap = width // rows 
    for  i in range(rows):
        grid.append([])
        for j in  range(rows):
             node = Node(i, j, gap, rows)
             grid[i].append(node)
    return grid

def draw_grid(win, rows, width, show_grid):
    gap = width // rows
    if show_grid == True:
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j  in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, show_grid):
    win.fill(WHITE)
    for  row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width, show_grid)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    gap  = width // rows
    i, j = pos
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    pygame.init() 

    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    running = True
    started = False
    algorithm = False
    show_grid = True

    while running:
        draw(win, grid, ROWS, width, show_grid)

        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                running = False
            
            if pygame.mouse.get_pressed()[0]: # left button of the mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                if row < ROWS and col < ROWS:
                    node = grid[row][col]

                    if not start and node != end: # set start node
                        start = node
                        start.make_start()
                    elif not end and node !=  start: # set end note
                        end = node
                        end.make_end()
                    elif node != end and node != start: # make barrier
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right button of the mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                if row < ROWS and col < ROWS:
                    node = grid[row][col]
                    node.reset() # reset node to default state

                    if node == start: # clear start node
                        start = None
                    elif node == end: # clear end node
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: 
                    algorithm = astar.astar
                    pygame.display.set_caption("Visual Search: A* Path Finding Algorithm")
                elif event.key == pygame.K_b: 
                    algorithm = bfs.bfs
                    pygame.display.set_caption("Visual Search: BFS Algorithm")
                elif event.key == pygame.K_u:
                    algorithm = ucs.ucs
                    pygame.display.set_caption("Visual Search: UCS Algorithm")
                elif event.key == pygame.K_d:
                    algorithm = dfs.dfs
                    pygame.display.set_caption("Visual Search: DFS Algorithm")
                elif event.key ==  pygame.K_s:
                    algorithm = dijkstra.dijkstra
                    pygame.display.set_caption("Visual Search: Dijkstra Algorithm")

                if algorithm and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width, show_grid), grid, start, end)
                
                if event.key == pygame.K_r: # reset the grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                elif event.key == pygame.K_g: # toggle the grid
                    show_grid = not show_grid

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)

import pygame
import astar
import dfs
import bfs
import dijkstra
import ucs
import threading

WIDTH = 750  # set the width of the window
SIDEBAR_WIDTH = 120
BUTTON_OFFSET = 60 
WIN = pygame.display.set_mode((WIDTH * 2, WIDTH))
pygame.display.set_caption("Visual Search")

RED = (204, 0, 0)  # for closed nodes
GREEN = (0, 204, 0)  # for open nodes
BLUE = (0, 0, 255)  # for ending node
WHITE = (255, 255, 255)  # for empty nodes
BLACK = (0, 0, 0)  # for walls
PURPLE = (136, 3, 185)  # for starting node
GREY = (128, 128, 128)  # for grid lines
PINK = (249, 19, 180)  # for path
BACKGROUND = (192, 182, 196)

pygame.font.init()
CAPTION_FONT = pygame.font.SysFont('Arial', 24)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = BACKGROUND
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
        self.color = BACKGROUND

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
        self.distance_from_start = distance_from_start  # store the distance from the start node
        self.set_distance_color(distance_from_start)  # set the node's color based on its distance from the start node

    def set_distance_color(self, distance):
        max_intensity = 150
        intensity = max(0, max_intensity - distance * 4)  # calculate the intensity based on the distance
        
        base_color = (255, 128, 128)  # light red
        dark_red = (128, 0, 0)

        red_component = max(dark_red[0], base_color[0] - intensity)
        green_component = max(dark_red[1], base_color[1] - intensity)
        blue_component = max(dark_red[2], base_color[2] - intensity)

        self.color = (red_component, green_component, blue_component)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # right
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = PURPLE
        self.action = action
        self.font = pygame.font.SysFont('Arial', 18)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        win.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                 self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width, show_grid, offset=0):
    gap = width // rows
    if show_grid:
        for i in range(rows):
            pygame.draw.line(win, GREY, (offset, i * gap), (offset + width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap + offset, 0), (j * gap + offset, width))

def draw(win, grid1, grid2, rows, width, show_grid, caption1, caption2, buttons):
    win.fill(BACKGROUND)  

    for row in grid1:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width, show_grid)

    for row in grid2:
        for node in row:
            node.x += width  # shift x-coordinates for the second grid
            node.draw(win)
        for node in row:
            node.x -= width  # reset x-coordinates after drawing
    draw_grid(win, rows, width, show_grid, offset=width)

    separator_x = width  # line separator at the midpoint
    pygame.draw.line(win, BLACK, (separator_x, 0), (separator_x, width), 2)  # 2-pixel thick line

    caption1_text = CAPTION_FONT.render(caption1, True, BLACK)
    caption2_text = CAPTION_FONT.render(caption2, True, BLACK)
    win.blit(caption1_text, (width // 2 - caption1_text.get_width() // 2, 10))  # center caption for grid1
    win.blit(caption2_text, (3 * width // 2 - caption2_text.get_width() // 2, 10))  # center caption for grid2

    for button in buttons:
        button.draw(win)

    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    # determine which grid the click is in
    if x < width:  # left grid
        col = x // gap
        row = y // gap
        if row < rows and col < rows:
            return row, col, 'left'
    else:  # right grid
        x -= width
        col = x // gap
        row = y // gap
        if row < rows and col < rows:
            return row, col, 'right'

    return None  # if the click is out of bounds

def main(win, width):
    pygame.init()

    ROWS = 50
    grid1 = make_grid(ROWS, width)
    grid2 = make_grid(ROWS, width)
    start1 = end1 = None
    start2 = end2 = None
    running = True
    show_grid = True
    caption1 = "Choose Algorithm for Left Grid"
    caption2 = "Choose Algorithm for Right Grid"
    algorithm1 = algorithm2 = None

    # create buttons for algorithms
    button_width = SIDEBAR_WIDTH - 20
    button_height = 40
    buttons = [
        Button("A*", 20, BUTTON_OFFSET, button_width, button_height, lambda: set_algorithm('astar', 1)),
        Button("BFS", 20, BUTTON_OFFSET + 50, button_width, button_height, lambda: set_algorithm('bfs', 1)),
        Button("DFS", 20, BUTTON_OFFSET + 100, button_width, button_height, lambda: set_algorithm('dfs', 1)),
        Button("Dijkstra", 20, BUTTON_OFFSET + 150, button_width, button_height, lambda: set_algorithm('dijkstra', 1)),
        Button("UCS", 20, BUTTON_OFFSET + 200, button_width, button_height, lambda: set_algorithm('ucs', 1)),
        Button("A*", WIDTH + 20, BUTTON_OFFSET, button_width, button_height, lambda: set_algorithm('astar', 2)),
        Button("BFS", WIDTH + 20, BUTTON_OFFSET + 50, button_width, button_height, lambda: set_algorithm('bfs', 2)),
        Button("DFS", WIDTH + 20, BUTTON_OFFSET + 100, button_width, button_height, lambda: set_algorithm('dfs', 2)),
        Button("Dijkstra", WIDTH + 20, BUTTON_OFFSET + 150, button_width, button_height, lambda: set_algorithm('dijkstra', 2)),
        Button("UCS", WIDTH + 20, BUTTON_OFFSET + 200, button_width, button_height, lambda: set_algorithm('ucs', 2)),
    ]

    def set_algorithm(algorithm, grid_num):
        nonlocal algorithm1, algorithm2, caption1, caption2
        if grid_num == 1:
            if algorithm == 'astar':
                algorithm1 = astar.astar
                caption1 = "A* Path Finding Algorithm"
            elif algorithm == 'bfs':
                algorithm1 = bfs.bfs
                caption1 = "BFS Algorithm"
            elif algorithm == 'dfs':
                algorithm1 = dfs.dfs
                caption1 = "DFS Algorithm"
            elif algorithm == 'dijkstra':
                algorithm1 = dijkstra.dijkstra
                caption1 = "Dijkstra Algorithm"
            elif algorithm == 'ucs':
                algorithm1 = ucs.ucs
                caption1 = "UCS Algorithm"
        elif grid_num == 2:
            if algorithm == 'astar':
                algorithm2 = astar.astar
                caption2 = "A* Path Finding Algorithm"
            elif algorithm == 'bfs':
                algorithm2 = bfs.bfs
                caption2 = "BFS Algorithm"
            elif algorithm == 'dfs':
                algorithm2 = dfs.dfs
                caption2 = "DFS Algorithm"
            elif algorithm == 'dijkstra':
                algorithm2 = dijkstra.dijkstra
                caption2 = "Dijkstra Algorithm"
            elif algorithm == 'ucs':
                algorithm2 = ucs.ucs
                caption2 = "UCS Algorithm"
        
        # check if both algorithms are selected along with start and end nodes
        if start1 and end1 and start2 and end2 and algorithm1 and algorithm2:
            for row in grid1:
                for node in row:
                    node.update_neighbors(grid1)
            for row in grid2:
                for node in row:
                    node.update_neighbors(grid2)
            algorithm1(lambda: draw(win, grid1, grid2, ROWS, width, show_grid, caption1, caption2, buttons), grid1, start1, end1)
            algorithm2(lambda: draw(win, grid1, grid2, ROWS, width, show_grid, caption1, caption2, buttons), grid2, start2, end2)

    while running:
        draw(win, grid1, grid2, ROWS, width, show_grid, caption1, caption2, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # left button of the mouse
                pos = pygame.mouse.get_pos()
                clicked_pos = get_clicked_pos(pos, ROWS, width)

                if clicked_pos:
                    row, col, grid_side = clicked_pos

                    if grid_side == 'left':  # left half (first grid)
                        node = grid1[row][col]
                        if not start1 and node != end1:  # set start node
                            start1 = node
                            start1.make_start()
                        elif not end1 and node != start1:  # set end note
                            end1 = node
                            end1.make_end()
                        elif node != end1 and node != start1:  # make barrier
                            node.make_barrier()
                    else:  # right half (second grid)
                        node = grid2[row][col]
                        if not start2 and node != end2:  # set start node
                            start2 = node
                            start2.make_start()
                        elif not end2 and node != start2:  # set end note
                            end2 = node
                            end2.make_end()
                        elif node != end2 and node != start2:  # make barrier
                            node.make_barrier()

                # Check if any button was clicked
                for button in buttons:
                    if button.is_clicked(pos):
                        button.action()

            elif pygame.mouse.get_pressed()[2]:  # right button of the mouse
                pos = pygame.mouse.get_pos()
                clicked_pos = get_clicked_pos(pos, ROWS, width)

                if clicked_pos:
                    row, col, grid_side = clicked_pos

                    if grid_side == 'left':
                        node = grid1[row][col]
                        node.reset()  # reset node to default state
                        if node == start1:  # clear start node
                            start1 = None
                        elif node == end1:  # clear end node
                            end1 = None
                    else:
                        node = grid2[row][col]
                        node.reset()  # reset node to default state
                        if node == start2:  # clear start node
                            start2 = None
                        elif node == end2:  # clear end node
                            end2 = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # reset the grid
                    start1 = end1 = None
                    start2 = end2 = None
                    grid1 = make_grid(ROWS, width)
                    grid2 = make_grid(ROWS, width)
                elif event.key == pygame.K_g:  # toggle the grid
                    show_grid = not show_grid

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)

import pygame
import math
from queue import PriorityQueue
from utils import reconstruct_path, print_path

# calculates the distance between two points (Manhattan distance)
def heuristic(point1, point2):
    x1, y1 = point1
    x2,  y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def astar(draw, grid, start, end):
    #print("Hello astar")
    count = 0
    open_set = PriorityQueue() # priority queue to hold nodes to explore
    open_set.put((0, count, start)) # start with the initial node
    came_from = {}  # dictionary to store the path from start to current node

    # initialize the cost of reaching each node (g_score)
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # cost to reach the start node is zero

    # initialize the estimated total cost (f_score) for each node
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())

    open_set_hash = {start} # set to keep track of nodes in the open set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
        current_node  = open_set.get()[2] # get the node with the lowest f_score
        open_set_hash.remove(current_node) # remove the node from the open set

        if current_node == end: # if the current node is the end node, reconstruct the path
            path = reconstruct_path(came_from, end, start, draw)
            end.make_end()
            start.make_start()
            print_path(path)
            draw()
            return True
        
        for neighbor in current_node.neighbors: # explre the neighbors of the current node
            temp_g_score = g_score[current_node] + 1 # compute the temporary g_score for the neighbor
            if temp_g_score < g_score[neighbor]: # if the new path to the neighbor is shorter, update its scores
                came_from[neighbor] = current_node # record where the neighbor came from
                g_score[neighbor] = temp_g_score # update the cost to reach the neighbor
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())  # update the estimated total cost to reach the end node

                # if the neighbor is not already in the open set, add it for exploration
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current_node != start:
            current_node.make_closed() # mark processed nodes as closed
    
    return False


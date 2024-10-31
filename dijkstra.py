import pygame
from queue import PriorityQueue
from utils import reconstruct_path, print_path

def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue() # priority queue to explore nodes with minimum distance
    open_set.put((0, start)) # start with the initial node and its cost (0)
    came_from = {}  # dictionary to store the path from start to current node

    # initialize the shortest path cost for all nodes to infinity, except the start node
    shortest_path_cost = {node: float("inf") for row in grid for node in row}
    shortest_path_cost[start] = 0 # the cost to reach the start node is 0
    in_open_set = {start}  # set to track nodes currently in the open set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current_node = open_set.get()[1] # get the node with the lowest cost from the priority queue
        in_open_set.remove(current_node) # remove the current node from the open set

        # if we've reached the end node, reconstruct and display the path
        if current_node == end:
            path = reconstruct_path(came_from, end, start, draw)
            end.make_end()
            start.make_start()
            print_path(path)
            draw()
            return True

        # explore each neighboring node of the current node
        for neighbor in current_node.neighbors:
            tentative_cost = shortest_path_cost[current_node] + 1 # moving to a neighbor costs 1

            # if this path to the neighbor is shorter, update the path and cost for that neighbor
            if tentative_cost < shortest_path_cost[neighbor]:
                came_from[neighbor] = current_node
                shortest_path_cost[neighbor] = tentative_cost

                # if the neighbor is not in open_set, add it to explore later
                if neighbor not in in_open_set:
                    open_set.put((shortest_path_cost[neighbor], neighbor))
                    in_open_set.add(neighbor)
                    neighbor.make_open()  #
        
        draw()
        
        if current_node != start:
            current_node.make_closed()

    return False

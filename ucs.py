import pygame
from queue import PriorityQueue
from utils import reconstruct_path, print_path

def ucs(draw, grid, start, end):
    nodes = PriorityQueue()  # priority queue to hold nodes based on cost
    nodes.put((0, start))  # start with the starting node at cost 0
    visited = set()  # set to track visited nodes
    came_from = {}  # track the path back from each node

    # initialize all nodes with an infinite cost, except the start node
    cost_so_far = {node: float("inf") for row in grid for node in row}
    cost_so_far[start] = 0

    while not nodes.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # get the current node with the lowest cost
        current_cost, current_node = nodes.get()

        if current_node == end: # if the end node is reached, reconstruct the path
            path = reconstruct_path(came_from, end, start, draw)
            end.make_end()
            start.make_start()
            print_path(path)
            draw()
            return True
         
        if current_node in visited: # if the current node has already been visited, skip it
            continue
        visited.add(current_node)  # mark current node as visited

        for neighbor in current_node.neighbors: # explore the neighbors of the current node
            new_cost = cost_so_far[current_node] + 1  # cost to move to a neighbor is 1
            # if the new path to the neighbor is cheaper, update the path and cost for that neighbor
            if new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current_node
                nodes.put((new_cost, neighbor))
                neighbor.make_open()

        draw()

        if current_node != start:
            current_node.make_closed()

    return False  # No path found

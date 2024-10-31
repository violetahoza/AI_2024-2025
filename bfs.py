import pygame
from utils import reconstruct_path, print_path

def bfs(draw, grid, start, end):
    visited = [] # list to keep track of visited nodes
    queue = [] # initialize a queue for BFS
    queue.append(start) # add the start node to the queue
    visited.append(start) # mark the start node as visited
    came_from = {}  # dictionary to store the path from start to current node

    while queue: # loop to visit each node
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
        current_node = queue.pop(0) # dequeue the first node in the queue

        if current_node == end: # if the current node is the end node, return the path
            path = reconstruct_path(came_from, end, start, draw)
            end.make_end()
            start.make_start()
            print_path(path)
            draw()
            return True
        
        for neighbor in current_node.neighbors: # explore the neighbors of the current node
            if neighbor not in visited : # if the neighbor hasn't been visited
                visited.append(neighbor) # mark it as visited
                came_from[neighbor] = current_node 
                queue.append(neighbor)
                neighbor.make_open()

        draw()

        if current_node != start:
            current_node.make_closed()  # mark processed nodes as closed

    return False
import pygame
from utils import reconstruct_path, print_path

def dfs(draw, grid, start, end):
    stack = [] # initialize a stack to keep track of nodes to explore
    visited = [] # list to keep track of visited nodes
    stack.append(start) # push the start node onto the stack
    visited.append(start) # mark the start node as visited
    came_from = {} # dictionary to store the path from start to current node
    distance_from_start = {start: 0}  
    
    while stack: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        current_node = stack.pop() # pop the last node added to the stack

        if current_node == end: # if the current node is the end node, return the path
            path = reconstruct_path(came_from, end, start, draw)
            end.make_end()
            start.make_start()
            print_path(path)
            draw()
            return True
        
        if current_node not in visited: # if the current node hasn't been visited yet, mark it as visited
            visited.append(current_node)

        for neighbor in current_node.neighbors: # explore the neighbors
            if neighbor not in visited : # if the neighbor is not visited
                came_from[neighbor] = current_node # record where it came from
                stack.append(neighbor)
                neighbor.make_open()
                distance_from_start[neighbor] = distance_from_start[current_node] + 1
                
        draw()

        if current_node != start:
            current_node.make_closed(distance_from_start[current_node])  # mark processed nodes as closed

    return False
    
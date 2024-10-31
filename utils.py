def reconstruct_path(came_from, current, start, draw): # reconstructs the path from the start node to the current node
    path = [] # initialize an empty list to store the path coordinates
    while current in came_from:  # loop until we reach the start node
        path.append(current.get_position()) # add the position of the current node to the path
        current = came_from[current] # move to the node from which the current node was reached
        current.make_path() # mark the current node as part of the path
        draw() # redraw the grid to show the updated path
    path.append(start.get_position()) # append the start position to the path
    path.reverse() # reverse the path to get it in the correct order (from start to end)

    return path

def print_path(path):
    if not path: # check if the path is empty
        print("No path found")
        return
    print("Path:\nStart:")
    for coord  in path: #  print the path coordinates
        print(coord)
    print("Goal")
    print(f"Length: {len(path)} steps")
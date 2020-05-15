from room import Room
from player import Player
from world import World

from util import Queue, Stack, Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def traverse_maze(world, traversal_path):

    s = Stack()
    reverse_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}
    curr = 0
    visited = {0: {}}
    curr_room = world.rooms[curr]  

    def find_unvisited_rooms(rooms):
        for room in rooms:
            if "?" in rooms[room].values():
                return True
        return False

    def find_possible_move(visited, current_room):
        curr_room = current_room.id
        room_exits = visited[curr_room]

        for direction in room_exits:
            if room_exits[direction] == "?" and current_room.get_room_in_direction(direction).id not in visited:
                return direction
        return None

    def find_next_room(visited, traversal_path, curr_room, s, reverse_directions):

        while True:
            next_move = s.pop()
            traversal_path.append(next_move)
            next_room = curr_room.get_room_in_direction(next_move)

            if "?" in visited[next_room.id].values():
                return next_room.id

            curr_room = next_room  

    for direction in curr_room.get_exits():
        visited[curr_room.id][direction] = "?"

    while len(visited) < len(world.rooms) and find_unvisited_rooms(visited):
        curr_room = world.rooms[curr]
        
        if curr_room not in visited:
            visited[curr_room.id] = {}

            for direction in curr_room.get_exits():
                visited[curr_room.id][direction] = "?"
        
        next_move = find_possible_move(visited, curr_room)

        if not next_move:
            curr = find_next_room(visited, traversal_path, curr_room, s, reverse_directions)
    
        else:
            traversal_path.append(next_move)
            next_room = curr_room.get_room_in_direction(next_move)
            visited[curr][next_move] = next_room.id

            if next_room.id not in visited:
                visited[next_room.id] = {}

                for direction in next_room.get_exits():
                    visited[next_room.id][direction] = "?"
            
            visited[next_room.id][reverse_directions[next_move]] = curr_room.id
            s.push(reverse_directions[next_move])
            curr = next_room.id

traverse_maze(world, traversal_path)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


    # s.push([curr_room])
    # room_exits = player.current_room.get_exits()
    # room_directions = player.current_room.get_room_in_direction(direction)
    # visited.add(curr_room)
    # unvisited rooms, with direction value of "?"
    # check current room and see if it's in visited, if not, get direction of possible moves in that room
    # loop through directions, and add next room to traversal path, if "?" is in the rooms directions, make next room the current room
    #check and see if there are still rooms
    #if not in visited, add current room to visited
    # if there are still rooms, add next move direction to the traversal path and set next room
    # print("Visited: ", visited)
    # print("Player current room 1: ", player.current_room)
    # while s.size() > 0:
    #     path = s.pop()
    #     print("Path: ", path)
    #     room = path[-1]
    #     print("Room: ", room)
        
        # if room not in visited:
        #     curr_room = player.current_room.id
        #     # player.travel('n')
        #     # print("Player current room 2: ", player.current_room)
        #     # print(room_exits)
        #     visited.add(curr_room)
        #     print("Visited: ", visited)
        #     print("Visited: ", visited)
        #     print("Player current room 1: ", player.current_room)
        #     room_exits = player.current_room.get_exits()
        #     travel_direction = random.choice(room_exits)
        #     travel_direction = get_random_room()

        #     print("Random Direction: ", travel_direction)

        #     traversal_path.append(travel_direction)
        #     player.travel(travel_direction)

        #     player.travel('n')
        #     print("Player current room 2: ", player.current_room)
        #     print(room_exits)

        # player_move()
            
        # for next_room in room:
        #     new_path = list(path)
        #     new_path.append(next_room)
        #     s.push(new_path)


# def get_random_room():
#     room_exits = player.current_room.get_exits()
#     travel_direction = random.choice(room_exits)
#     return travel_direction

# def player_move():
#     room_exits = player.current_room.get_exits()
#     travel_direction = random.choice(room_exits)
#     print("Random Direction: ", travel_direction)
#     traversal_path.append(travel_direction)
#     player.travel(travel_direction)
#     curr_room = player.current_room
#     s.push([curr_room])

# move in first random direction

# add that room as visited, add to stack
# move in random available direction
# repeat til deadend
# if deadend, backup and see if there's an available direction
# if so move that direction, add that room as visited, add to stack
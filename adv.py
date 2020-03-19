from room import Room
from player import Player
from world import World
import random
from ast import literal_eval


traversal_path = []


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


visited = {}
reverse = {'n': 's',
           's': 'n',
           'e': 'w',
           'w': 'e'}

"""
def find_traversal(graph):
    '''
    breadth first
    '''
    explored = []
    steps = []
    q = Queue()
    q.enqueue(world.starting_room)
    visited = {}
    room_visit = [False] * len(room_graph)

    while q.size() > 0:
        path = q.dequeue()
        node = path
        node_id = node.id
        if node not in visited:
            visited[node] = path
            neighbours = node.get_exits()

            for neighbour in neighbours:
                neighbour_room = node.get_room_in_direction(neighbour)
                path_copy = path.copy()
                path_copy.append(neighbour_room)
                q.enqueue(path_copy)
                room_visit[node_id, path_copy]
    print('steps', steps)
    print('explored', explored)
    print('room_visit', room_visit)
    return explored
"""


def find_traversal(graph):
    node = world.starting_room
    q = [node]
    explored_id = {}
    explored = []
    while q:

        node = q.pop(0)
        if node.id not in explored_id.keys():
            explored.append(node)
            explored_id[node.id] = node

            adjacent_doors = node.get_exits()
            for direction in adjacent_doors:
                q.append(node.get_room_in_direction(direction))
    directions = []
    node_id_list = []
    for node in explored_id:
        node_id_list.append(node)

    for node_id in range(len(node_id_list)-1):
        path_to_node = shortest_path(
            graph,
            explored_id[node_id_list[node_id]],
            explored_id[node_id_list[node_id+1]]
            )
        path_directions(directions, path_to_node)
    print(directions)
    return directions


def shortest_path(graph, start, goal):
    explored = []
    q = [[start]]
    if start == goal:
        return
    while q:
        path = q.pop(0)
        node = path[-1]
        if node not in explored:
            adjacent_doors = node.get_exits()
            neighbours = []
            for direction in adjacent_doors:
                neighbours.append(
                    node.get_room_in_direction(direction)
                    )
            for neighbour in neighbours:

                new_path = list(path)
                new_path.append(neighbour)
                q.append(new_path)

                if neighbour == goal:
                    return new_path
            explored.append(node)


def path_directions(directions, path):
    for x in range(len(path)-1):
        node = path[x]
        x += 1
        if node.n_to == path[x]:
            directions.append('n')
        if node.s_to == path[x]:
            directions.append('s')
        if node.e_to == path[x]:
            directions.append('e')
        if node.w_to == path[x]:
            directions.append('w')


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


# find_traversal(traversal_path, visited, world.room_grid, world.starting_room)

traversal_path = find_traversal(world.room_grid)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# print('traversal path', traversal_path)
# print('visited', visited)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, "
        f'{len(visited_rooms)} rooms visited'
        )
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

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


def path_directions(directions, path):
    for x in range(len(path)-1):
        node = path[x]
        node.visited = True
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

traversal_path = []


def traversal(path, room_graph, player, world):
    import random
    from time import sleep
    revs = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
    clockwise_directions = ['n', 'e', 's', 'w']
    backtrack_path = []
    backtrack_rooms = []
    current = player.current_room.id
    visited = {current}
    while len(visited) < 500:
        # get dictionary of neighboring rooms
        options = room_graph[current][1]

        # optional: sort dictionary by decreasing room id
        options = {
            k: v for k, v
            in sorted(options.items(), key=lambda i: i[1], reverse=True)
            }

        # choose a direction
        choice = None
        backtracking = False

        # choose directions going clockwise
        for way in clockwise_directions:
            # pick first unvisited neighbor, moving clockwise
            if (way in options.keys()) and (options[way] not in visited):
                choice = way
                break

        # optional for loop: choose highest numbered neighbor
        for way, neighbor in options.items():
            # pick largest unvisited neighbor
            if neighbor not in visited:
                choice = way
                break

        # if all neighbors are visited, backtrack a step.
        if choice is None:
            backtracking = True
            choice = revs[backtrack_path.pop()]
            backtrack_rooms.pop()

        # make the move
        current = options[choice]
        # mark the new room as visited
        visited.add(current)
        # keep track of your path
        path.append(choice)
        # if we're not backtracking, add to the backtrack path
        if not backtracking:
            backtrack_path.append(choice)
            backtrack_rooms.append(current)


traversal(traversal_path, room_graph, player, world)

visited_rooms = set()
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

import random
from collections import namedtuple
from enum import Enum
from queue import Queue


Starter = namedtuple('Starter', 'mode length width')
DetailedElement = namedtuple('DetailedElement', 'matrix_element x y direction')
Element = namedtuple('Element', 'x y direction')
Coord = namedtuple('Coord', 'x y')


class Cell:           # We're drawing labyrinth with cells
    low_string = "_"  # initially each one is "walled"
    left_string = "|"
    right_string = "|"
    is_visited = False
    distance = 0
    UNDERLINED_HASH = "\u0332#"
    UNDERLINED_EXCLAMATION = "\u0332!"
    UNDERLINED_STAR = "\u0332*"

    def delete_lower_bound(self):  # crashing particular walls
        if self.low_string == self.UNDERLINED_HASH:
            self.low_string = "#"
        elif self.low_string == self.UNDERLINED_EXCLAMATION:
            self.low_string = "!"
        else:
            self.low_string = " "

    def delete_left_bound(self):
        self.left_string = " "

    def delete_right_bound(self):
        self.right_string = " "

    def start(self):  # marking as start
        self.low_string = self.UNDERLINED_HASH

    def finish(self):  # as finish
        if self.low_string == "_":
            self.low_string = self.UNDERLINED_EXCLAMATION
        else:
            self.low_string = "!"

    def route_mark(self):  # as part of the route between start and finish
        if self.low_string == self.UNDERLINED_HASH or self.low_string == "#" or \
                self.low_string == self.UNDERLINED_EXCLAMATION or self.low_string == "!":
            pass
        else:
            if self.low_string == "_":
                self.low_string = self.UNDERLINED_STAR
            elif self.low_string == " ":
                self.low_string = "*"

    def __str__(self):
        return self.left_string + self.low_string + self.right_string


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def greeting():
    print("Hello there. It's an amazing maze generator")
    print("Enter its size: length width")
    length = int(input())
    width = int(input())
    print("Choose mode")
    print("1 for DFS generator, 2 for spanning tree")
    mode = int(input())
    starters = Starter(mode=mode, length=length, width=width)
    return starters


def get_neighbours(current, matrix):  # checking all the cases # I do not think, that it sorted out the problem
    i = current[1]                    # cannot define them separately cause "list out of range"
    j = current[2]
    neighbours = []
    if i > 0:
        up_de = DetailedElement(matrix_element=matrix[i - 1][j], x=i - 1, y=j, direction=Direction.UP)
        neighbours.append(up_de)
    if i < len(matrix) - 1:
        down_de = DetailedElement(matrix_element=matrix[i + 1][j], x=i + 1, y=j, direction=Direction.DOWN)
        neighbours.append(down_de)
    if j > 0:
        left_de = DetailedElement(matrix_element=matrix[i][j - 1], x=i, y=j - 1, direction=Direction.LEFT)
        neighbours.append(left_de)
    if j < len(matrix[0]) - 1:
        right_de = DetailedElement(matrix_element=matrix[i][j + 1], x=i, y=j + 1, direction=Direction.RIGHT)
        neighbours.append(right_de)
    return neighbours


def visited(neighbours):  # pretty obvious
    for each in neighbours:
        if not each[0].is_visited:
            return False
    return True


def delete_border(last, current):
    if current[3] == Direction.LEFT:
        last[0].delete_left_bound()
        current[0].delete_right_bound()
    elif current[3] == Direction.RIGHT:
        last[0].delete_right_bound()
        current[0].delete_left_bound()
    elif current[3] == Direction.DOWN:
        last[0].delete_lower_bound()
    else:
        current[0].delete_lower_bound()


def mark_start(start):
    start.start()


def mark_finish(last):
    last[0].finish()


def dfs_generator(starters):  # namedtuple usage!
    matrix = [[Cell() for i in range(starters[2])] for j in range(starters[1])]  # initialization of labyrinth matrix
    random.seed(version=2)
    mark_start(matrix[0][0])
    current = (matrix[0][0], 0, 0)
    matrix[current[1]][current[2]].is_visited = True  # mark the visited one
    route_stack = [current]
    route = [(current[1], current[2])]
    while not (visited(get_neighbours(current, matrix))):  # generate a correct route somewhere
        last = current
        current = random.choice([el for el in get_neighbours(current, matrix) if not el[0].is_visited])
        matrix[current[1]][current[2]].is_visited = True
        delete_border(last, current)
        route_stack.append(current)
        route.append((current[1], current[2]))
    mark_finish(route_stack[len(route_stack) - 1])
    while len(route_stack) > 0:
        current = route_stack.pop()
        while visited(get_neighbours(current, matrix)) and len(route_stack) > 0:  # going back
            current = route_stack.pop()
        while not (visited(get_neighbours(current, matrix))):
            last = current
            current = random.choice(
                [el for el in get_neighbours(current, matrix) if not el[0].is_visited])  # going through missed ones
            matrix[current[1]][current[2]].is_visited = True
            delete_border(last, current)
            route_stack.append(current)
    print("dfs_generator: Done")
    return matrix, route


def kruskal_fill_edges_from_matrix(edges, length, width):  # const direction # named tuple
    for i in range(length):
        for j in range(width):
            if i > 0:
                edges.add((i * width + j, (i - 1) * width + j, Direction.UP))
                edges.add(((i - 1) * width + j, i * width + j, Direction.DOWN))
                # encoding every cell and adding edges to edge set
            if i < length - 1:
                edges.add((i * width + j, (i + 1) * width + j, Direction.DOWN))
                edges.add(((i + 1) * width + j, i * width + j, Direction.UP))
            if j > 0:
                edges.add((i * width + j, i * width + j - 1, Direction.LEFT))
                edges.add((i * width + j - 1, i * width + j, Direction.RIGHT))
            if j < width - 1:
                edges.add((i * width + j, i * width + j + 1, Direction.RIGHT))
                edges.add((i * width + j + 1, i * width + j, Direction.LEFT))


def kruskal_find(subset, list_of_id_sets):
    index = list_of_id_sets.index(subset)
    if index != -1:
        return index


def kruskal_get_neighbours(current, matrix):  # watching for crashed walls around current # const direction
    neighbours = []
    for el in get_neighbours(current, matrix):
        if el.direction == Direction.DOWN and (current[0].low_string == " " or current[0].low_string == "!" or current[0].low_string == "#"):
            neighbours.append(el)
        if el.direction == Direction.UP and (el.matrix_element.low_string == " " or el.matrix_element.low_string == "#"):
            neighbours.append(el)
        if el.direction == Direction.LEFT and el.matrix_element.right_string == " ":
            neighbours.append(el)
        if el.direction == Direction.RIGHT and el.matrix_element.left_string == " ":
            neighbours.append(el)
    return neighbours


def kruskal_get_route(start, finish, matrix):  # Lee algorithm
    current = (matrix[start[0]][start[1]], start[0], start[1])
    current[0].distance = 0
    current[0].is_visited = True
    route_queue = Queue()
    route_queue.put(current)
    route = []
    matrix[start[0]][start[1]].distance = 0
    while (current[1], current[2]) != finish:
        for el in kruskal_get_neighbours(current, matrix):
            if not el[0].is_visited:
                el[0].is_visited = True
                route_queue.put(el)
                el[0].distance = current[0].distance + 1
        current = route_queue.get()
    while (current[1], current[2]) != start:
        for el in kruskal_get_neighbours(current, matrix):
            if el[0].distance == current[0].distance - 1:
                route.append((el[1], el[2]))
                current = el
    route.append(finish)
    return route


def kruskal_generator(starters):  # Creating a minimum spanning tree using Kruskal algorithm # named tuple?
    matrix = [[Cell() for i in range(starters[2])] for j in range(starters[1])]  # initialization of labyrinth matrix
    random.seed(version=2)
    edges = set()
    index_dict = {i * starters[2] + j: (i, j) for i in range(starters[1]) for j in range(starters[2])}
    list_of_id_sets = [set([i * starters[2] + j]) for i in range(starters[1]) for j in range(starters[2])]
    kruskal_fill_edges_from_matrix(edges, starters[1], starters[2])
    edges = list(edges)
    start = True
    route = []
    while len(edges) > 0 and len(list_of_id_sets) > 1:
        current_edge = random.choice(edges)
        edges.remove(current_edge)
        dom = kruskal_find(current_edge[0], list_of_id_sets)
        ran = kruskal_find(current_edge[1], list_of_id_sets)
        if dom == ran:
            continue
        list_of_id_sets[dom] = set.union(list_of_id_sets[ran], list_of_id_sets[dom])
        for i in range(ran, len(list_of_id_sets) - 1):
            list_of_id_sets[i] = list_of_id_sets[i + 1]
        list_of_id_sets.pop()
        indexes_0 = index_dict[current_edge[0]]
        indexes_1 = index_dict[current_edge[1]]
        if start:
            mark_start(matrix[indexes_0[0]][indexes_0[1]])
            route.append((indexes_0[0], indexes_0[1]))
            start = False
        delete_border(([matrix[indexes_0[0]][indexes_0[1]]]), ([matrix[indexes_1[0]][indexes_1[1]],
                                                                0, 0, current_edge[2]]))
    mark_finish(([matrix[indexes_1[0]][indexes_1[1]]]))
    start = route[0]
    route = kruskal_get_route(start, (indexes_1[0], indexes_1[1]), matrix)
    return matrix, route


def show_route(matrix, route):
    for i in range(len(route)):
        matrix[route[i][0]][route[i][1]].route_mark()  # marking the route
    print(" _ " * len(labyrinth[0]))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end="")
        print()


def file_load(labyrinth, condition):  # condition = 1 for pure lab., condition = 0 for routed lab.
    file = open("labyrinth.txt", "a")
    file.write("Generated labyrinth\n") if condition == 1 else file.write("Labyrinth with route\n")
    for i in range(len(labyrinth)):
        for j in range(len(labyrinth[i])):
            file.write(labyrinth[i][j])
        file.write("\n")


# main
starters = greeting()
labyrinth, route = dfs_generator(starters) if starters.mode == 1 else kruskal_generator(starters)
print(" _ " * len(labyrinth[0]))
for i in range(len(labyrinth)):
    for j in range(len(labyrinth[i])):
        print(labyrinth[i][j], end="")
    print()
print("Wanna download?")
if input() == "YES":
    file_load(labyrinth, 1)
print("Show route?")
if input() == "YES":
    show_route(labyrinth, route)
    print("Wanna download?")
    if input() == "YES":
        file_load(labyrinth, 0)

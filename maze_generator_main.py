import random
from queue import Queue

class Cell:           # We're drawing labyrinth with cells
    low_string = "_"  # initially each one is "walled"
    left_string = "|"
    right_string = "|"
    visited = False
    distance = 0

    def DeleteLowerBound(self):  # crashing particular walls
        if self.low_string == "\u0332#":
            self.low_string = "#"
        elif self.low_string == "\u0332!":
            self.low_string = "!"
        else:
            self.low_string = " "

    def DeleteLeftBound(self):
        self.left_string = " "

    def DeleteRightBound(self):
        self.right_string = " "

    def Start(self):  # marking as start
        self.low_string = "\u0332#"

    def Finish(self):  # as finish
        if self.low_string == "_":
            self.low_string = "\u0332!"
        else:
            self.low_string = "!"

    def RouteMark(self):  # as part of the route between start and finish
        if self.low_string == "\u0332#" or self.low_string == "#" or self.low_string == "\u0332!" or \
                self.low_string == "!":
            pass
        else:
            if self.low_string == "_":
                self.low_string = "\u0332*"
            elif self.low_string == " ":
                self.low_string = "*"

    def __str__(self):
        return self.left_string + self.low_string + self.right_string


def Greeting():
    print("Hello there. It's an amazing maze generator")
    print("Enter its size: length width")
    length = int(input())
    width = int(input())
    print("Choose mode")
    print("1 for DFS generator, 2 for spanning tree")
    mode = int(input())
    return (mode, length, width)


def GetNeighbours(current, matrix):  # checking all the cases
    i = current[1]
    j = current[2]
    if i == 0 and j == 0:
        return [(matrix[i + 1][j], i + 1, j, "down"), (matrix[i][j + 1], i, j + 1, "right")]
    if i == len(matrix) - 1 and j == len(matrix[0]) - 1:
        return [(matrix[i - 1][j], i - 1, j, "up"), (matrix[i][j - 1], i, j - 1, "left")]
    if i == 0 and j == len(matrix[0]) - 1:
        return [(matrix[i + 1][j], i + 1, j, "down"), (matrix[i][j - 1], i, j - 1, "left")]
    if i == len(matrix) - 1 and j == 0:
        return [(matrix[i - 1][j], i - 1, j, "up"), (matrix[i][j + 1], i, j + 1, "right")]
    if i == 0:
        return [(matrix[i + 1][j], i + 1, j, "down"), (matrix[i][j + 1], i, j + 1, "right"),
                (matrix[i][j - 1], i, j - 1, "left")]
    if j == 0:
        return [(matrix[i + 1][j], i + 1, j, "down"), (matrix[i][j + 1], i, j + 1, "right"),
                (matrix[i - 1][j], i - 1, j, "up")]
    if i == len(matrix) - 1:
        return [(matrix[i][j + 1], i, j + 1, "right"), (matrix[i - 1][j], i - 1, j, "up"),
                (matrix[i][j - 1], i, j - 1, "left")]
    if j == len(matrix[0]) - 1:
        return [(matrix[i + 1][j], i + 1, j, "down"), (matrix[i - 1][j], i - 1, j, "up"),
                (matrix[i][j - 1], i, j - 1, "left")]
    return [(matrix[i + 1][j], i + 1, j, "down"), (matrix[i][j + 1], i, j + 1, "right"),
            (matrix[i - 1][j], i - 1, j, "up"), (matrix[i][j - 1], i, j - 1, "left")]


def Visited(neighbours):  # pretty obvious
    for each in neighbours:
        if not each[0].visited:
            return False
    return True


def DeleteBorder(last, current):
    if current[3] == "left":
        last[0].DeleteLeftBound()
        current[0].DeleteRightBound()
    elif current[3] == "right":
        last[0].DeleteRightBound()
        current[0].DeleteLeftBound()
    elif current[3] == "down":
        last[0].DeleteLowerBound()
    else:
        current[0].DeleteLowerBound()


def MarkStart(start):
    start.Start()


def MarkFinish(last):
    last[0].Finish()


def DfsGenerator(starters):  # add Cell use
    matrix = [[Cell() for i in range(starters[2])] for j in range(starters[1])]  # initialization of labyrinth matrix
    random.seed(version=2)
    MarkStart(matrix[0][0])
    current = (matrix[0][0], 0, 0)
    matrix[current[1]][current[2]].visited = True  # mark the visited one
    route_stack = [current]
    route = [(current[1], current[2])]
    while not (Visited(GetNeighbours(current, matrix))):  # generate a correct route somewhere
        last = current
        current = random.choice([el for el in GetNeighbours(current, matrix) if el[0].visited == False])
        matrix[current[1]][current[2]].visited = True
        DeleteBorder(last, current)
        route_stack.append(current)
        route.append((current[1], current[2]))
    MarkFinish(route_stack[len(route_stack) - 1])
    while len(route_stack) > 0:
        current = route_stack.pop()
        while Visited(GetNeighbours(current, matrix)) and len(route_stack) > 0:  # going back
            current = route_stack.pop()
        while not (Visited(GetNeighbours(current, matrix))):
            last = current
            current = random.choice(
                [el for el in GetNeighbours(current, matrix) if el[0].visited == False])  # going through missed ones
            matrix[current[1]][current[2]].visited = True
            DeleteBorder(last, current)
            route_stack.append(current)
    print("DfsGenerator: Done")
    return (matrix, route)


def KruskalFillEdgesFromMatrix(edges, length, width, matrix):
    for i in range(length):
        for j in range(width):
            if i > 0:
                edges.add((i * width + j, (i - 1) * width + j, "up"))
                edges.add(((i - 1) * width + j, i * width + j, "down"))
                # encoding every cell and adding edges to edge set
            if i < length - 1:
                edges.add((i * width + j, (i + 1) * width + j, "down"))
                edges.add(((i + 1) * width + j, i * width + j, "up"))
            if j > 0:
                edges.add((i * width + j, i * width + j - 1, "left"))
                edges.add((i * width + j - 1, i * width + j, "right"))
            if j < width - 1:
                edges.add((i * width + j, i * width + j + 1, "right"))
                edges.add((i * width + j + 1, i * width + j, "left"))


def KruskalFind(subset, list_of_id_sets):
    for i in range(len(list_of_id_sets)):
        if subset in list_of_id_sets[i]:
            return i


def KruskalGetNeighbours(current, matrix):  # watching for crashed walls around current
    neighbours = []
    for el in GetNeighbours(current, matrix):
        if el[3] == "down" and (current[0].low_string == " " or current[0].low_string == "!" or current[0].low_string == "#"):
            neighbours.append(el)
        if el[3] == "up" and (el[0].low_string == " " or el[0].low_string == "#"):
            neighbours.append(el)
        if el[3] == "left" and el[0].right_string == " ":
            neighbours.append(el)
        if el[3] == "right" and el[0].left_string == " ":
            neighbours.append(el)
    return neighbours


def KruskalGetRoute(start, finish, matrix):  # Lee algorithm
    current = (matrix[start[0]][start[1]], start[0], start[1])
    current[0].distance = 0
    current[0].visited = True
    route_queue = Queue()
    route_queue.put(current)
    route = []
    matrix[start[0]][start[1]].distance = 0
    while (current[1], current[2]) != finish:
        for el in KruskalGetNeighbours(current, matrix):
            if not el[0].visited:
                el[0].visited = True
                route_queue.put(el)
                el[0].distance = current[0].distance + 1
        current = route_queue.get()
    while (current[1], current[2]) != start:
        for el in KruskalGetNeighbours(current, matrix):
            if el[0].distance == current[0].distance - 1:
                route.append((el[1], el[2]))
                current = el
    route.append(finish)
    return route


def KruskalGenerator(starters):  # Creating a minimum spanning tree using Kruskal algorithm
    matrix = [[Cell() for i in range(starters[2])] for j in range(starters[1])]  # initialization of labyrinth matrix
    random.seed(version=2)
    edges = set()
    index_dict = {i * starters[2] + j: (i, j) for i in range(starters[1]) for j in range(starters[2])}
    list_of_id_sets = [set([i * starters[2] + j]) for i in range(starters[1]) for j in range(starters[2])]
    KruskalFillEdgesFromMatrix(edges, starters[1], starters[2], matrix)
    edges = list(edges)
    start = True
    route = []
    while len(edges) > 0 and len(list_of_id_sets) > 1:
        print("Length: ", len(list_of_id_sets))
        current_edge = random.choice(edges)
        edges.remove(current_edge)
        dom = KruskalFind(current_edge[0], list_of_id_sets)
        ran = KruskalFind(current_edge[1], list_of_id_sets)
        print(dom, " ", ran)
        if dom == ran:
            continue
        list_of_id_sets[dom] = set.union(list_of_id_sets[ran], list_of_id_sets[dom])
        for i in range(ran, len(list_of_id_sets) - 1):
            list_of_id_sets[i] = list_of_id_sets[i + 1]
        list_of_id_sets.pop()
        indexes_0 = index_dict[current_edge[0]]
        indexes_1 = index_dict[current_edge[1]]
        if start:
            MarkStart(matrix[indexes_0[0]][indexes_0[1]])
            route.append((indexes_0[0], indexes_0[1]))
            start = False
        DeleteBorder(([matrix[indexes_0[0]][indexes_0[1]]]), ([matrix[indexes_1[0]][indexes_1[1]],
                                                               0, 0, current_edge[2]]))
    MarkFinish(([matrix[indexes_1[0]][indexes_1[1]]]))
    start = route[0]
    route = KruskalGetRoute(start, (indexes_1[0], indexes_1[1]), matrix)
    return (matrix, route)


def ShowRoute(matrix, route):
    for i in range(len(route)):
        matrix[route[i][0]][route[i][1]].RouteMark()  # marking the route
    print(" _ " * len(labyrinth[0]))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end="")
        print()


def FileLoad(labyrinth, condition):  # condition = 1 for pure lab., condition = 0 for routed lab.
    file = open("labyrinth.txt", "a")
    file.write("Generated labyrinth\n") if condition == 1 else file.write("Labyrinth with route\n")
    for i in range(len(labyrinth)):
        for j in range(len(labyrinth[i])):
            file.write(labyrinth[i][j])
        file.write("\n")


# main
starters = Greeting()
labyrinth, route = DfsGenerator(starters) if starters[0] == 1 else KruskalGenerator(starters)
print(" _ " * len(labyrinth[0]))
for i in range(len(labyrinth)):
    for j in range(len(labyrinth[i])):
        print(labyrinth[i][j], end="")
    print()
print("Wanna download?")
if input() == "YES":
    FileLoad(labyrinth, 1)
print("Show route?")
if input() == "YES":
    ShowRoute(labyrinth, route)
    print("Wanna download?")
    if input() == "YES":
        FileLoad(labyrinth, 0)
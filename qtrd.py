import interval_graph
import itertools


def dominated(graph, v, V1, V2):
    if v in V1 + V2:
        return True
    else:
        for u in V2:
            if v in interval_graph.neighbor(graph, u):
                return True
    return False


def isolated(graph, v, V1, V2):
    for u in interval_graph.neighbor(graph, v):
        if u in V1 + V2:
            return False
    return True


def v2InNeighborhood(graph, v, V2):
    neighbor = interval_graph.neighbor(graph, v)
    res = []
    for interval in neighbor:
        if interval in V2:
            res.append(interval)
    return res


def qtrd_v1(graph):
    res = {0: graph.copy(), 1: [], 2: []}
    sorted_graph = sorted(graph, key=lambda x: x[1])
    sorted_graph = sorted(sorted_graph, key=lambda x: len(interval_graph.closedNeighbor(graph, x)))
    already_dominated = []

    for interval in sorted_graph:
        if not dominated(graph, interval, res[1], res[2]):
            u = max(interval_graph.closedNeighbor(graph, interval),
                    key=lambda x: len(set(interval_graph.closedNeighbor(graph, x)) - set(already_dominated)))
            if len(set(interval_graph.closedNeighbor(graph, u)) - set(already_dominated)) >= 3 - len(
                    v2InNeighborhood(graph, u, res[2])):
                res[2].append(u)
                res[0].remove(u)
                already_dominated.extend(interval for interval in interval_graph.closedNeighbor(graph, u))
            else:
                res[1].append(interval)
                res[0].remove(interval)

    res[2] = sorted(res[2], key=lambda x: x[1])
    for v in res[2]:
        if isolated(graph, v, res[1], res[2]):
            u = max(interval_graph.neighbor(graph, v), key=lambda x: x[1])
            res[1].append(u)
            res[0].remove(u)
    return res


def qtrdChecker(graph, solution):
    v0, v1, v2 = solution[0], solution[1], solution[2]
    qtrdNumber = len(v1) + 2 * len(v2)
    for interval in graph:
        if interval not in v0 + v1 + v2:
            return -1
        if not dominated(graph, interval, v1, v2):
            return -1
    for v in v2:
        if isolated(graph, v, v1, v2):
            return -1
    return qtrdNumber


def qtrdBruteForce(graph):
    minSolution = float("inf")
    possibilities = itertools.product([0, 1, 2], repeat=len(graph))
    for possibility in possibilities:
        solution = {0: [], 1: [], 2: []}
        type = list(possibility)
        for i in range(len(graph)):
            solution[type[i]].append(graph[i])
        value = qtrdChecker(graph,solution)
        if value != -1:
            minSolution = min(value,minSolution)
    return minSolution


def drawWithSolution(solution):
    v0,v1,v2 = solution[0],solution[1],solution[2]
    colors = []
    labels = []
    for v in v0:
        colors.append('steelblue')
        labels.append('V0')
    for v in v1:
        colors.append('forestgreen')
        labels.append('V1')
    for v in v2:
        colors.append('firebrick')
        labels.append('V2')
    interval_graph.drawGraphWindow(v0 + v1 + v2, colors, labels)


if __name__ == '__main__':
    order = int(input("Please enter the graph order : "))
    graph = interval_graph.intervalGraphGen(order)
    sorted_graph = sorted(graph, key=lambda x: x[1])
    sorted_graph = sorted(sorted_graph, key=lambda x: len(interval_graph.closedNeighbor(graph, x)))
    #interval_graph.drawGraphWindow(sorted_graph)

    res = qtrd_v1(graph)
    print("V0 : ", res[0])
    print("V1 : ", res[1])
    print("V2 : ", res[2])
    print("Graph : ", graph)
    drawWithSolution(res)

    check = qtrdChecker(graph, res)
    print("Check Value : ", check)

    minSolution = qtrdBruteForce(graph)
    print("Minimum solution : ",minSolution)
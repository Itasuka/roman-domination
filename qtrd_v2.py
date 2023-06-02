import argparse
import os.path
import random

import matplotlib.pyplot as plt
from tqdm import tqdm

import interval_graph
import qtrd


def removeMultiple(list, *elem):
    res = list.copy()
    for e in elem:
        res.remove(e)
    return res


def rightGrowingSort(graph):
    sorted_graph = sorted(graph, key=lambda x: x[1])
    return sorted_graph


def firstNonDominated(graph, v):
    tab = list(filter(lambda x: v[1] < x[0], graph))
    return min(tab, key=lambda x: x[1], default=None)


def secondNonDominated(graph, v):
    u = firstNonDominated(graph, v)
    tab = list(filter(lambda x: v[1] < x[0], graph))
    tab.remove(u)
    return min(tab, key=lambda x: x[1], default=None)


def thirdNonDominated(graph, v):
    u = firstNonDominated(graph, v)
    w = secondNonDominated(graph, v)
    tab = list(filter(lambda x: v[1] < x[0], graph))
    tab.remove(u)
    tab.remove(w)
    return min(tab, key=lambda x: x[1], default=None)


def greaterClosedNeighbor(graph, v):
    neighbors = interval_graph.closedNeighbor(graph, v)
    return max(neighbors, key=lambda x: x[1])


def firstVertex(graph):
    return min(graph, key=lambda x: x[1])


def lastVertex(graph):
    return max(graph, key=lambda x: x[1])


def updateSolution(sol, preV, preB, newV, newB, addedV):
    preSol = sol[preV, preB].copy()
    newSol = {0: preSol[0].copy(), 1: preSol[1].copy(), 2: preSol[2].copy()}
    for i in range(3):
        for c in addedV[i]:
            newSol[i].append(c)
            newSol[0].remove(c)
    sol[newV, newB] = newSol


def first_option_true(graph, v, opt, sol):
    i1 = firstNonDominated(graph, v)
    if i1 is not None:
        i12 = secondNonDominated(graph, v)
        if i12 is not None:
            w = thirdNonDominated(graph, v)
            if w is not None:
                if w != i12:
                    i22 = greaterClosedNeighbor(graph, i12)
                    if i22 != i12 and i22 not in interval_graph.closedNeighbor(graph,i1):
                        if opt[i22, True] > opt[v, True] + 4:
                            opt[i22, True] = opt[v, True] + 4
                            updateSolution(sol, v, True, i22, True, {0: [], 1: [i1, i12], 2: [i22]})
                    i2 = greaterClosedNeighbor(graph, w)
                    if i2 not in interval_graph.closedNeighbor(graph, i1):
                        if i2 not in interval_graph.closedNeighbor(graph, i12):
                            if opt[i2, False] > opt[v, True] + 4:
                                opt[i2, False] = opt[v, True] + 4
                                updateSolution(sol, v, True, i2, False, {0: [], 1: [i1, i12], 2: [i2]})
                        else:
                            if opt[i2, True] > opt[v, True] + 4:
                                opt[i2, True] = opt[v, True] + 4
                                updateSolution(sol, v, True, i2, True, {0: [], 1: [i1, i12], 2: [i2]})
            else:
                n = lastVertex(graph)
                if opt[n, True] > opt[v, True] + 2:
                    opt[n, True] = opt[v, True] + 2
                    updateSolution(sol, v, True, n, True, {0: [], 1: [i1, i12], 2: []})


def second_option_true(graph, v, opt, sol):
    i1 = firstNonDominated(graph, v)
    if i1 is not None:
        w = secondNonDominated(graph, v)
        if w is not None:
            if w != i1:
                i22 = greaterClosedNeighbor(graph, i1)
                if i22 != i1:
                    if opt[i22, True] > opt[v, True] + 3:
                        opt[i22, True] = opt[v, True] + 3
                        updateSolution(sol, v, True, i22, True, {0: [], 1: [i1], 2: [i22]})
                i2 = greaterClosedNeighbor(graph, w)
                if i2 not in interval_graph.closedNeighbor(graph, i1):
                    if opt[i2, False] > opt[v, True] + 3:
                        opt[i2, False] = opt[v, True] + 3
                        updateSolution(sol, v, True, i2, False, {0: [], 1: [i1], 2: [i2]})
                else:
                    if opt[i2, True] > opt[v, True] + 3:
                        opt[i2, True] = opt[v, True] + 3
                        updateSolution(sol, v, True, i2, True, {0: [], 1: [i1], 2: [i2]})
        else:
            n = lastVertex(graph)
            if opt[n, True] > opt[v, True] + 1:
                opt[n, True] = opt[v, True] + 1
                updateSolution(sol, v, True, n, True, {0: [], 1: [i1], 2: []})


def third_option_true(graph, v, opt, sol):
    w = firstNonDominated(graph, v)
    if w is not None:
        i22 = greaterClosedNeighbor(graph, v)
        if i22 != v:
            if opt[i22, True] > opt[v, True] + 2:
                opt[i22, True] = opt[v, True] + 2
                updateSolution(sol, v, True, i22, True, {0: [], 1: [], 2: [i22]})
        i2 = greaterClosedNeighbor(graph, w)
        if i2 not in interval_graph.closedNeighbor(graph, v):
            if opt[i2, False] > opt[v, True] + 2:
                opt[i2, False] = opt[v, True] + 2
                updateSolution(sol, v, True, i2, False, {0: [], 1: [], 2: [i2]})
        else:
            if opt[i2, True] > opt[v, True] + 2:
                opt[i2, True] = opt[v, True] + 2
                updateSolution(sol, v, True, i2, True, {0: [], 1: [], 2: [i2]})
    else:
        n = lastVertex(graph)
        if opt[n, True] > opt[v, True]:
            opt[n, True] = opt[v, True]
            updateSolution(sol, v, True, n, True, {0: [], 1: [], 2: []})


def first_option_false(graph, v, opt, sol):
    i1 = greaterClosedNeighbor(graph, v)
    if i1 is not None:
        i12 = firstNonDominated(graph, v)
        if i12 is not None:
            w = secondNonDominated(graph, v)
            if w is not None:
                if w != i12:
                    i22 = greaterClosedNeighbor(graph, i12)
                    if i22 != i12 and i22 in interval_graph.closedNeighbor(graph,w) and i22 not in interval_graph.closedNeighbor(graph,i1):
                        if opt[i22, True] > opt[v, False] + 4:
                            opt[i22, True] = opt[v, False] + 4
                            updateSolution(sol, v, False, i22, True, {0: [], 1: [i1, i12], 2: [i22]})
                    i2 = greaterClosedNeighbor(graph, w)
                    if i2 not in interval_graph.closedNeighbor(graph, i1):
                        if i2 not in interval_graph.closedNeighbor(graph, i12):
                            if opt[i2, False] > opt[v, False] + 4:
                                opt[i2, False] = opt[v, False] + 4
                                updateSolution(sol, v, False, i2, False, {0: [], 1: [i1, i12], 2: [i2]})
                        else:
                            if opt[i2, True] > opt[v, False] + 4:
                                opt[i2, True] = opt[v, False] + 4
                                updateSolution(sol, v, False, i2, True, {0: [], 1: [i1, i12], 2: [i2]})
            else:
                n = lastVertex(graph)
                if opt[n, True] > opt[v, False] + 2:
                    opt[n, True] = opt[v, False] + 2
                    updateSolution(sol, v, False, n, True, {0: [], 1: [i1, i12], 2: []})


def second_option_false(graph, v, opt, sol):
    i1 = greaterClosedNeighbor(graph, v)
    if i1 is not None:
        w = firstNonDominated(graph, v)
        if w is not None:
            if w != i1:
                i22 = greaterClosedNeighbor(graph, i1)
                if i22 != i1 and i22 in interval_graph.closedNeighbor(graph,w):
                    if opt[i22, True] > opt[v, False] + 3:
                        opt[i22, True] = opt[v, False] + 3
                        updateSolution(sol, v, False, i22, True, {0: [], 1: [i1], 2: [i22]})
                i2 = greaterClosedNeighbor(graph, w)
                if i2 not in interval_graph.closedNeighbor(graph, i1):
                    if opt[i2, False] > opt[v, False] + 3:
                        opt[i2, False] = opt[v, False] + 3
                        updateSolution(sol, v, False, i2, False, {0: [], 1: [i1], 2: [i2]})
                else:
                    if opt[i2, True] > opt[v, False] + 3:
                        opt[i2, True] = opt[v, False] + 3
                        updateSolution(sol, v, False, i2, True, {0: [], 1: [i1], 2: [i2]})
        else:
            n = lastVertex(graph)
            if opt[n, True] > opt[v, False] + 1:
                opt[n, True] = opt[v, False] + 1
                updateSolution(sol, v, False, n, True, {0: [], 1: [i1], 2: []})


def third_option_false(graph, v, opt, sol):
    i2 = greaterClosedNeighbor(graph, v)
    if i2 != v:
        if opt[i2, True] > opt[v, False] + 2:
            opt[i2, True] = opt[v, False] + 2
            updateSolution(sol, v, False, i2, True, {0: [], 1: [], 2: [i2]})


def connectedGraphs(graph):
    res = []
    interval_began = 0
    subGraph = []
    for i in range(0, 2 * len(graph)):
        l = list(filter(lambda x: x[0] == i, graph))
        r = list(filter(lambda x: x[1] == i, graph))
        if len(l) != 0:
            interval_began += 1
            subGraph.append(l[0])
        if len(r) != 0:
            if interval_began == 1:
                res.append(subGraph.copy())
                subGraph.clear()
            interval_began -= 1
    return res


def connectedQtrd_v2(graph):
    max_value = 2 * len(graph)
    init = (-1, -1)
    opt = {(init, True): 0, (init, False): max_value}
    sol = {(init, True): {0: graph, 1: [], 2: []}}
    for v in graph:
        if v != init:
            opt[v, True] = max_value
            opt[v, False] = max_value
            sol[v, True] = {0: [], 1: [], 2: []}
            sol[v, False] = {0: [], 1: [], 2: []}
    first_option_true(graph, init, opt, sol)
    second_option_true(graph, init, opt, sol)
    third_option_true(graph, init, opt, sol)
    sorted_graph = rightGrowingSort(graph)
    for v in sorted_graph:
        if opt[v, True] != max_value:
            first_option_true(graph, v, opt, sol)
            second_option_true(graph, v, opt, sol)
            third_option_true(graph, v, opt, sol)
        if opt[v, False] != max_value:
            first_option_false(graph, v, opt, sol)
            second_option_false(graph, v, opt, sol)
            third_option_false(graph, v, opt, sol)
    return sol[lastVertex(graph), True], opt[lastVertex(graph), True]


def qtrd_v2(graph):
    subgraphs = connectedGraphs(graph)
    qtrd = {0: [], 1: [], 2: []}
    qtrd_value = 0
    for subgraph in subgraphs:
        tmp_sol, tmp_val = connectedQtrd_v2(subgraph)
        for i in range(3):
            qtrd[i].extend(tmp_sol[i].copy())
        qtrd_value += tmp_val
    return qtrd, qtrd_value


def counter_example(graph, saveExample=False):
    """
    Compare the second version of QTRD algorithm to the Brute Force

    :param graph: a graph
    :return: True if QTRDV2 solution is minimal
    """
    qtrd_sol, qtrdValue = qtrd_v2(graph)
    # qtrdValue = qtrd.qtrdChecker(graph, qtrd)
    bruteForce = qtrd.qtrdBruteForce(graph)
    bruteForceValue = qtrd.qtrdChecker(graph, bruteForce)
    if qtrdValue != bruteForceValue:
        print(graph)
        print("QTRD value from algorithm : ", qtrdValue, "\n", qtrd_sol)
        print("QTRD value from brute force :", bruteForceValue, "\n", bruteForce)
        qtrd.drawWithSolution(qtrd_sol, "QTRD from Algorithm")
        path = "qtrdv1/"
        if saveExample and not os.path.exists(path):
            os.makedirs(path)
        if saveExample:
            plt.savefig(path + "algo_" + saveExample)
            print("Algorithm solution for counter example saved at : \"", path, "algo_", saveExample, "\"")
        qtrd.drawWithSolution(bruteForce, "QTRD from brute force")
        if saveExample:
            plt.savefig(path + "bruteforce_" + saveExample)
            print("Brute force solution for counter example saved at : \"", path, "bruteforce_", saveExample, "\"")
        plt.show()
        return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare QTRD function value with Brute Force on interval graph')
    parser.add_argument('-s', '--samples', type=int, help='the samples number', default=1)
    parser.add_argument('-o', '--order', type=int, help='the graphs order for the generation, no value --> randomly '
                                                        'generated', default=-1)
    parser.add_argument('-se', '--saveExample', type=str, dest='saveExample', help='save with the name the counter '
                                                                                   'example if exist')
    args = vars(parser.parse_args())

    cpt = 1

    if args['order'] < 1:
        for i in tqdm(range(args['samples'])):
            order = random.randint(1, 12)
            graph = interval_graph.intervalGraphGen(order)
            if not counter_example(graph, args['saveExample']):
                break
            cpt += 1
    else:
        graphsPos = interval_graph.intervalGraphBruteForceGenerator(args['order'])
        graphs = []
        for graphPos in graphsPos:
            graph = interval_graph.graphFromPosition(graphPos)
            graphs.append(graph)
        for graph in tqdm(graphs):
            if not counter_example(graph, args['saveExample']):
                break
            cpt += 1

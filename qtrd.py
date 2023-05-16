#!/usr/bin/env python3

import argparse
import os.path
import random

from matplotlib import pyplot as plt

import interval_graph
import itertools


def dominated(graph, v, V1, V2):
    """
    test if an interval v is dominated in graph based of the V1 and V2 set
    :param graph: a graph
    :param v: an interval
    :param V1: a list of V1 intervals
    :param V2: a list of V2 intervals
    :return: True if v is dominated by V1 union V2 in graph
    """
    if v in V1 + V2:
        return True
    else:
        for u in V2:
            if v in interval_graph.neighbor(graph, u):
                return True
    return False


def isolated(graph, v, V1, V2):
    """
    test if an interval v is isolated in graph based of the V1 and V2 list

    :param graph: a graph
    :param v: an interval
    :param V1: a list of V1 intervals
    :param V2: a list of V2 intervals
    :return: True if v is isolated by V1 union V2 in graph
    """
    for u in interval_graph.neighbor(graph, v):
        if u in V1 + V2:
            return False
    return True


def v2InNeighborhood(graph, v, V2):
    """
    Search the neighbor of v that are in V2
    :param graph: a graph
    :param v: an interval
    :param V2: a list of V2 intervals
    :return: a list of neighbor of v that are also in V2
    """
    neighbor = interval_graph.neighbor(graph, v)
    res = []
    for interval in neighbor:
        if interval in V2:
            res.append(interval)
    return res


def qtrd_v1_u(graph, v, alreadyDominated):
    """
    Get the u for the first version of QTRD. u is a neighbor of v that have the most non dominated neighbor. if
    conflicted, u is the interval which has the most neighbor

    :param graph: a graph :param v: an interval :param alreadyDominated: a list of dominated intervals in graph
    :return: the u corresponding to the neighbor of v with the most non dominated neighbor and the most neighbor in
    conflict
    """
    u = v
    closedNeighbor = interval_graph.closedNeighbor(graph,v)
    for neighbor in closedNeighbor:
        nonDominatedNeighbor = set(interval_graph.closedNeighbor(graph,neighbor)) - set(alreadyDominated)
        if len(nonDominatedNeighbor) > len(set(interval_graph.closedNeighbor(graph,u)) - set(alreadyDominated)):
            u = neighbor
        elif len(nonDominatedNeighbor) == len(set(interval_graph.closedNeighbor(graph, u)) - set(alreadyDominated)):
            if len(interval_graph.closedNeighbor(graph,neighbor)) > len(interval_graph.closedNeighbor(graph,u)):
                u = neighbor
    return u


def qtrd_v1(graph):
    """
    First version of the QTRD algorithm not proved

    :param graph: a graph
    :return: the qtrd solution for the graph
    """
    res = {0: graph.copy(), 1: [], 2: []}
    sorted_graph = sorted(graph, key=lambda x: x[1]) # sort by right growing
    sorted_graph = sorted(sorted_graph, key=lambda x: len(interval_graph.closedNeighbor(graph, x))) # sort by neighborhood growing
    already_dominated = []

    for interval in sorted_graph:
        if not dominated(graph, interval, res[1], res[2]):
            u = qtrd_v1_u(graph, interval, already_dominated)
            # if length of non dominated neighborhood of u >= 3 - number of v2 in u neighborhood
            if len(set(interval_graph.closedNeighbor(graph, u)) - set(already_dominated)) >= 3 - len(v2InNeighborhood(graph, u, res[2])):
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
    """
    Check a QTRD solution for a graph

    :param graph: a graph
    :param solution: a solution to check
    :return: True if solution is a solution of QTRD for the graph
    """
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
    """
    Try all the possibilities for QTRD and keep the minimum value based of solution = 2 * |V2| + |V1|

    :param graph: a graph
    :return: the minimal QTRD solution for the graph
    """
    minSolution = {0: [], 1: [], 2: []}
    minSolutionValue = float("inf")
    possibilities = itertools.product([0, 1, 2], repeat=len(graph))
    for possibility in possibilities:
        solution = {0: [], 1: [], 2: []}
        type = list(possibility)
        for i in range(len(graph)):
            solution[type[i]].append(graph[i])
        value = qtrdChecker(graph, solution)
        if value != -1 and value < minSolutionValue:
            minSolutionValue = value
            minSolution = solution
    return minSolution


def drawWithSolution(solution, title="QTRD Solution"):
    """
    Configure the plot for a QTRD solution

    :param solution: a QTRD solution
    :param title: the Title of the plot
    """
    v0, v1, v2 = solution[0], solution[1], solution[2]
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
    interval_graph.drawGraphWindow(v0 + v1 + v2, colors, labels, title)


def counter_example(graph, saveExample=False):
    """
    Compare the first version of QTRD algorithm to the Brute Force

    :param graph: a graph
    :return: True if QTRDV1 solution is minimal
    """
    qtrd = qtrd_v1(graph)
    qtrdValue = qtrdChecker(graph, qtrd)
    bruteForce = qtrdBruteForce(graph)
    bruteForceValue = qtrdChecker(graph, bruteForce)
    if qtrdValue != bruteForceValue:
        print(graph)
        print("QTRD value from algorithm : ", qtrdValue, "\n", qtrd)
        print("QTRD value from brute force :", bruteForceValue, "\n", bruteForce)
        drawWithSolution(qtrd, "QTRD from Algorithm")
        path = "qtrdv1/"
        if saveExample and not os.path.exists(path):
            os.makedirs(path)
        if saveExample:
            plt.savefig(path+"algo_"+saveExample)
            print("Algorithm solution for counter example saved at : \"", path, "algo_", saveExample, "\"")
        drawWithSolution(bruteForce, "QTRD from brute force")
        if saveExample:
            plt.savefig(path+"bruteforce_"+saveExample)
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
        for i in range(args['samples']):
            order = random.randint(1, 9)
            graph = interval_graph.intervalGraphGen(order)
            if not counter_example(graph, args['saveExample']):
                break
            print("TEST ", cpt, " SUCCESSFUL")
            cpt += 1
    else:
        graphsPos = interval_graph.intervalGraphBruteForceGenerator(args['order'])
        graphs = []
        for graphPos in graphsPos:
            graph = interval_graph.graphFromPosition(graphPos)
            graphs.append(graph)
        for graph in graphs:
            if not counter_example(graph, args['saveExample']):
                break
            print("TEST ", cpt, " SUCCESSFUL")
            cpt += 1
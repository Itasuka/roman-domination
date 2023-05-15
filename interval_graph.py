#!/usr/bin/env python3
import argparse
import random
import timeit
from collections import OrderedDict

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def intervalGraphGen(order):
    remaining = [i for i in range(2 * order)]
    graph = []
    while remaining:
        i = random.randint(0, len(remaining) - 2)
        left = remaining.pop(i)
        right = remaining.pop(random.randint(i, len(remaining) - 1))
        graph.append((left, right))
    return graph


def drawGraphTerminal(graph):
    for interval in graph:
        left = interval[0]
        right = interval[1]
        res = ""
        for i in range(2 * len(graph)):
            if i == left:
                res += "|"
            elif i == right:
                res += ">"
            elif left < i < right:
                res += "-"
            else:
                res += " "
        print(res)


def graphWindow(graph, colors=None, labels=None, title="Interval Graph"):
    if labels is None:
        labels = []
    if colors is None:
        colors = ['steelblue']

    fig, ax = plt.subplots()
    y_pos = range(len(graph))
    longueurs = [end - start for start, end in graph]
    start_points = [start for start, end in graph]
    end_points = [end for start, end in graph]
    ax.set_xticks(start_points + end_points, start_points + end_points)
    ax.grid(axis='x', linestyle='--', linewidth=0.5)
    ax.set_yticks([])
    ax.set_ylabel('')

    legend_elements = []
    unique_colors = OrderedDict()
    for color, label in zip(colors, labels):
        if color not in unique_colors:
            unique_colors[color] = label
            legend_elements.append(Patch(facecolor=color))
    for i, color in enumerate(unique_colors.keys()):
        legend_elements[i].set_label(unique_colors[color])
    ax.set_title(title)
    ax.barh(y_pos, longueurs, left=start_points, color=colors)
    ax.legend(handles=legend_elements)

def neighbor(graph, v):
    l_v = v[0]
    r_v = v[1]
    neighbor = []
    for interval in graph:
        l_i = interval[0]
        r_i = interval[1]
        if l_v < l_i < r_v or l_v < r_i < r_v or l_i < l_v and r_v < r_i:
            neighbor.append(interval)
    return neighbor


def closedNeighbor(graph, v):
    return neighbor(graph, v) + [v]


def neighborhood(graph):
    neighborhood = []
    for interval in graph:
        neighborhood.append(neighbor(graph, interval))
    return neighborhood


def closedNeighborhood(graph):
    closedNeighborhood = []
    for interval in graph:
        closedNeighborhood.append(closedNeighbor(graph, interval))
    return closedNeighborhood


def intervalGraphBruteForceGenerator(order):
    graphs = []
    if (order < 1):
        return graphs
    graphs.append([0])
    for i in range((2 * order)- 1):
        newGraphs = []
        for j in range(len(graphs)):
            graph = graphs[j]
            maxPossibility = max(graph)+1
            if maxPossibility > order - 1:
                maxPossibility = order - 1
            possibilities = [i for i in range(maxPossibility+1)]
            for n in range(maxPossibility+1):
                if graph.count(n) > 1:
                    possibilities.remove(n)
            for possibility in possibilities:
                g = graph.copy()
                g.append(possibility)
                newGraphs.append(g)
        graphs = newGraphs.copy()
    return graphs

def graphFromPosition(positions):
    graph = []
    res = {i : [] for i in range(len(positions)//2)}
    for i in range(len(positions)):
        res[positions[i]].append(i)
    for i in range(len(res)):
        graph.append((res[i][0],res[i][1]))
    return graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate an interval graph')
    parser.add_argument('-o', '--order', type=int, help='the order of the graph', default=1)
    parser.add_argument('-a', '--all', dest='allGraph', action='store_true', help='generate all graph from order')
    parser.add_argument('-dt', '--draw-terminal', dest='drawTerminal', action='store_true', help='draw the graph on terminal instead of matplotlib')
    parser.add_argument('-t', '--time', dest='time', action='store_true', help='show the run time')
    args = vars(parser.parse_args())

    start = timeit.default_timer()
    if args['allGraph']:
        graphsPos = intervalGraphBruteForceGenerator(args['order'])
        graphs = []
        for graphPos in graphsPos:
            graph = graphFromPosition(graphPos)
            graphs.append(graph)
        if args['drawTerminal']:
            for graph in graphs:
                drawGraphTerminal(graph)
        else:
            for graph in graphs:
                graphWindow(graph)
    else:
        graph = intervalGraphGen(args['order'])
        if args['drawTerminal']:
            drawGraphTerminal(graph)
        else:
            graphWindow(graph)
    stop = timeit.default_timer()
    if (args['time']):
        print('Run time : ', stop-start)
    plt.show()
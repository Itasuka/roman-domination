import itertools
import random
import timeit
from collections import OrderedDict

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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


def drawGraphWindow(graph, colors=None, labels=None):
    if labels is None:
        labels = []
    if colors is None:
        colors = ['steelblue']
    y_pos = range(len(graph))
    longueurs = [end - start for start, end in graph]
    start_points = [start for start, end in graph]
    end_points = [end for start, end in graph]
    plt.xticks(start_points + end_points, start_points + end_points)
    plt.grid(axis='x', linestyle='--', linewidth=0.5)
    plt.yticks([])
    plt.ylabel('')
    legend_elements = []
    unique_colors = OrderedDict()
    for color, label in zip(colors, labels):
        if color not in unique_colors:
            unique_colors[color] = label
            legend_elements.append(Patch(facecolor=color))
    for i, color in enumerate(unique_colors.keys()):
        legend_elements[i].set_label(unique_colors[color])
    plt.barh(y_pos, longueurs, left=start_points, color=colors)
    plt.legend(handles=legend_elements)
    plt.show()


def order(graph):
    return len(graph)


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


if __name__ == '__main__':
    order = int(input("Please enter the graph order : "))
    start = timeit.default_timer()
    graph = intervalGraphGen(order)
    stop = timeit.default_timer()
    print("time : ", stop - start)
    for interval in graph:
        print("left : ", interval[0], "; right : ", interval[1])
        print("neighbor = ", neighbor(graph, interval))
        print("closedneighbor = ", closedNeighbor(graph, interval))
    drawGraphTerminal(graph)
    sorted_graph = sorted(graph, key=lambda x: len(closedNeighbor(graph, x)))
    print("Result : ", sorted_graph)
    for interval in sorted_graph:
        print("Interval = ", interval, "\nDegree : ", len(closedNeighbor(sorted_graph, interval)))
    drawGraphWindow(sorted_graph)
    allGraphFromOrder(order)

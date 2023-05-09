import random
import matplotlib.pyplot as plt
def intervalGraphGen(order):
    remaining = [i for i in range(2 * order)]
    graph = []
    while remaining :
        i = random.randint(0,len(remaining)-2)
        left = remaining.pop(i)
        right = remaining.pop(random.randint(i,len(remaining)-1))
        graph.append((left,right))
    return graph


def drawGraphTerminal(graph):
    for interval in graph:
        left = interval[0]
        right = interval[1]
        res = ""
        for i in range(2*len(graph)):
            if i == left:
                res += "|"
            elif i == right:
                res += ">"
            elif left < i < right:
                res += "-"
            else:
                res += " "
        print(res)

def drawGraphWindow(graph):
    y_pos = range(len(graph))
    longueurs = [end - start for start, end in graph]
    start_points = [start for start, end in graph]
    end_points = [end for start, end in graph]
    plt.xticks(start_points+end_points, "")
    plt.grid(axis='x', linestyle='--', linewidth = 0.5)
    plt.yticks([])
    plt.ylabel('')
    plt.barh(y_pos, longueurs, left=start_points)
    plt.show()


if __name__ == '__main__':
    order = int(input("Please enter the graph order : "))
    graph = intervalGraphGen(order)
    for interval in graph:
        print("left : ", interval[0], "; right : ",interval[1])
    drawGraphTerminal(graph)
    drawGraphWindow(graph)
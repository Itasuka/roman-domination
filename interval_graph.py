import random
def intervalGraphGen(order):
    remaining = [i for i in range(2 * order)]
    graph = []
    while remaining :
        i = random.randint(0,len(remaining)-2)
        left = remaining.pop(i)
        right = remaining.pop(random.randint(i,len(remaining)-1))
        graph.append((left,right))
    return graph

if __name__ == '__main__':
    order = int(input("Please enter the graph order : "))
    graph = intervalGraphGen(order)
    for interval in graph:
        print("left : ", interval[0], "; right : ",interval[1])
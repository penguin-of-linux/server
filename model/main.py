import networkx as nx
import collections
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from model import *

def create_graph(NODE_COUNT = 20, BLOCK_COUNT = 20, P = 0.6):
    # return nx.gnm_random_graph(n, m)
    g = nx.gnp_random_graph(NODE_COUNT, P)
    # return nx.complete_graph(n)
    # return nx.path_graph(n)
    # return nx.dense_gnm_random_graph(n, m)
    # return nx.star_graph(n)

    rnd = random.Random()
    for node in range(NODE_COUNT):
        g.node[node]["packets"] = {}
        for n in g.neighbors(node):
            g.node[node]["packets"][n] = collections.deque()

        g.node[node]["data"] = set()
    for block_number in range(BLOCK_COUNT):
        for i in range(0, 3):
            node = rnd.randint(0, NODE_COUNT - 1)
            g.node[node]["data"].add(block_number)
    return g

def create_tasks(NODE_COUNT = 20, BLOCK_COUNT = 20, TIME = 100):
    res = []
    rnd = random.Random()
    for _ in range(TIME):
        target = rnd.randint(0, NODE_COUNT - 1)
        block_number = rnd.randint(0, BLOCK_COUNT - 1)
        res.append(Task(block_number, target))
    return res


def create_nodes_for_create(NODE_COUNT = 20, TIME = 100):
    res = []
    rnd = random.Random()
    for _ in range(TIME):
        res.append(rnd.randint(0, NODE_COUNT - 1))
    return res

def print_stats(stats):
    average_max = sum(stats.max.values()) / len(stats.max)
    average_average = sum(stats.average.values()) / len(stats.average)
    # print("Max:", stats.max)
    # print("Average:", stats.average)
    print("Average max:", average_max)
    print("Average average:", average_average)

def print_overall_stats(stats):
    maximum = 0
    average = 0
    for s in stats:
        maximum += sum(s.max.values()) / len(s.max)
        average += sum(s.average.values()) / len(s.average)
    maximum /= len(stats)
    average /= len(stats)

    print("Max:", maximum)
    print("Average:", average)
    return (maximum, average)


def experiment(NODE_COUNT = 20,
               BLOCK_COUNT = 20,
               P = 0.6,
               DUPLICATION_DEGREE = 5,
               TIME = 100,
               TRIES = 50):
  print("n: {0}, p: {1}, time: {2}".format(NODE_COUNT, P, TIME))

  p2p_stats = []
  m2p_stats = []

  for i in range(TRIES):
    tasks = create_tasks(NODE_COUNT, BLOCK_COUNT, TIME)
    nodes_for_block_create = create_nodes_for_create(NODE_COUNT, TIME)

    graph = create_graph(NODE_COUNT, BLOCK_COUNT, P)
    graph_copy = copy.deepcopy(graph)
    # print("Сгенерировано ребер: %d" % len(graph.edges))

    p2p_model = Model(NODE_COUNT, BLOCK_COUNT, TIME, graph,
                      P2PAssigner(),
                      tasks, nodes_for_block_create)

    m2p_model = Model(NODE_COUNT, BLOCK_COUNT, TIME, graph_copy,
                      M2PAssigner(DUPLICATION_DEGREE),
                      tasks, nodes_for_block_create)

    p2p_stats.append(p2p_model.calculate())
    m2p_stats.append(m2p_model.calculate())
    # print(i)

  a = print_overall_stats(p2p_stats)
  b = print_overall_stats(m2p_stats)

#   p2p_maxs.append(a[0])
#   p2p_avgs.append(a[1])
#   m2p_maxs.append(b[0])
#   m2p_avgs.append(b[1])

  p2p_max = a[0]
  p2p_avg = a[1]
  m2p_max = b[0]
  m2p_avg = b[1]

  return ("n{0}_p{1}_d{2}_t{3}.svg".format(NODE_COUNT, P, DUPLICATION_DEGREE, TIME),
          p2p_max,
          p2p_avg,
          m2p_max,
          m2p_avg)
  
def show_svg(name, xs, p2p_maxs, p2p_avgs, m2p_maxs, m2p_avgs):
  print(nm)

  line1, = plt.plot(xs, p2p_maxs, "lightgray", label="p2p max")
  line2, = plt.plot(xs, p2p_avgs, "lightgray", label="p2p average")
  line3, = plt.plot(xs, m2p_maxs, "black", label="m2p max")
  line4, = plt.plot(xs, m2p_avgs, "black", label="m2p average")

  plt.grid(True)
  plt.legend(handles=[line1, line2, line3, line4])
  plt.tight_layout()
  plt.plot()
  plt.savefig(name, format="svg")

if __name__ == "__main__":
    xs = []
    ys = []
    p2p_maximums = []
    p2p_averages = []
    m2p_maximums = []
    m2p_averages = []
    
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    p_values = [0.6]
    degree_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for time in range(100, 2100, 100):
        for p in p_values:
            xs.append(time)
            ys.append(p)

            (nm,
             p2p_max,
             p2p_avg,
             m2p_max,
             m2p_avg) = experiment(NODE_COUNT = 10, TIME = time, P = p, TRIES = 1)
 
            p2p_maximums.append(p2p_max)
            p2p_averages.append(p2p_avg)
            m2p_maximums.append(m2p_max)
            m2p_averages.append(m2p_avg)

            print() 

    show_svg(nm, xs, p2p_maximums, p2p_averages, m2p_maximums, m2p_averages)


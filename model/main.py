import os
import sys
import signal
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

  return (p2p_max, p2p_avg, m2p_max, m2p_avg)
  
def show_svg(name, xs, p2p_maxs, p2p_avgs, m2p_maxs, m2p_avgs):
  line1, = plt.plot(xs, p2p_maxs, "lightgray", label="p2p max", dashes=[8, 2])
  line2, = plt.plot(xs, p2p_avgs, "lightgray", label="p2p average")
  line3, = plt.plot(xs, m2p_maxs, "black", label="m2p max")
  line4, = plt.plot(xs, m2p_avgs, "black", label="m2p average", dashes=[8, 2])

  plt.grid(True)
  plt.legend(handles=[line1, line2, line3, line4])
  plt.tight_layout()
  plt.plot()
  plt.savefig(name, format="svg")

def experiment_one():
  # Эксперимент 1: различное количество узлов с разной плотностью рёбер.
  # Количество повторов 50. Время эксперимента 500

  pids = []
  p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
  for n_count in range(10, 110, 10):
    pid = os.fork()

    if pid != 0:
      pids.append(pid)
    else:
      xs = []
      p2p_maxs = []
      p2p_avgs = []
      m2p_maxs = []
      m2p_avgs = []

      for p in p_values:
        xs.append(p)

        (p2p_max,
         p2p_avg,
         m2p_max,
         m2p_avg) = experiment(NODE_COUNT = n_count,
                               BLOCK_COUNT = 2000,
                               TIME = 500,
                               P = p,
                               TRIES = 10)

        p2p_maxs.append(p2p_max)
        p2p_avgs.append(p2p_avg)
        m2p_maxs.append(m2p_max)
        m2p_avgs.append(m2p_avg)
        
        print() 
        sys.stdout.flush()

      show_svg("n{0}_p{1}_d{2}_t{3}.svg".format(n_count, "var", 5, 500),
               xs, p2p_maxs, p2p_avgs, m2p_maxs, m2p_avgs)

  for pid in pids:
    os.waitpid(pid, 0)


if __name__ == "__main__":
  os.setpgrp()
  try:
    experiment_one()
  finally:
    os.killpg(0, signal.SIGTERM)

import networkx as nx
import collections

from model import *

NODE_COUNT = -1
BLOCK_COUNT = 20
P = -1
DUPLICATION_DEGREE = -1
GENERATE_COMMAND_PROBABILITY = 0.5
TIME = -1


def create_graph():
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


def create_tasks():
    res = []
    rnd = random.Random()
    for _ in range(TIME):
        target = rnd.randint(0, NODE_COUNT - 1)
        block_number = rnd.randint(0, BLOCK_COUNT - 1)
        res.append(Task(block_number, target))
    return res


def create_nodes_for_create():
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


if __name__ == "__main__":
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    for node_count in range(5, 55, 10):
        for p in p_values:
            for duplication_degree in range(3, 6):
                for time in range(100, 1100, 100):
                    NODE_COUNT = node_count
                    P = p
                    DUPLICATION_DEGREE = duplication_degree
                    TIME = time
                    print("n: {0}, p: {1}, dup: {2}, time: {3}".format(NODE_COUNT, P, duplication_degree, time))
                    p2p_stats = []
                    m2p_stats = []
                    for i in range(20):
                        tasks = create_tasks()
                        nodes_for_block_create = create_nodes_for_create()

                        graph = create_graph()
                        graph_copy = copy.deepcopy(graph)
                        # print("Сгенерировано ребер: %d" % len(graph.edges))

                        p2p_model = Model(NODE_COUNT, BLOCK_COUNT, TIME, graph, P2PAssigner(),
                                          tasks, nodes_for_block_create)
                        m2p_model = Model(NODE_COUNT, BLOCK_COUNT, TIME, graph_copy, M2PAssigner(DUPLICATION_DEGREE),
                                          tasks, nodes_for_block_create)

                        p2p_stats.append(p2p_model.calculate())
                        m2p_stats.append(m2p_model.calculate())
                        # print(i)

                    print_overall_stats(p2p_stats)
                    print_overall_stats(m2p_stats)
                    print()

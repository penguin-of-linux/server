import random

from model import *


if __name__ == "__main__":
    rnd = random.Random()
    n = rnd.randint(5, 10)
    m = rnd.randint(0, n * (n - 1))
    p = rnd.random()
    print("n: {0}, m: {1}, p: {2}".format(n, m, p))
    time = 1000
    p2p_generator = P2PCommandGenerator()
    m2p_generator = M2PCommandGenerator(1)

    def generate():
        # return nx.gnm_random_graph(n, m)
        return nx.gnp_random_graph(n, p)
        # return nx.complete_graph(n)
        # return nx.path_graph(n)
        # return nx.dense_gnm_random_graph(n, m)
        # return nx.star_graph(n)

    graph = generate()
    copy = graph.copy()
    edges_count = len(graph.edges)
    print("Сгенерировано ребер: %d" % edges_count)

    p2p_model = Model(n, time, graph, p2p_generator)
    m2p_model = Model(n, time, copy, m2p_generator)

    stats = p2p_model.calculate()
    print("P2P:")
    #print("Max:", stats.max)
    #print("Average:", stats.average)
    print("Max max:", max(stats.max.values()))
    print("Max average:", max(stats.average.values()))

    print("M2P:")
    stats = m2p_model.calculate()
    #print("Max:", stats.max)
    #print("Average:", stats.average)
    print("Max max:", max(stats.max.values()))
    print("Max average:", max(stats.average.values()))

# state, псевдотаймер, случайные операции, случайные графы
# подробное описание - ссылки, алгоритмы рандомизации
# 2 способа генерирования команд
# умные передачи

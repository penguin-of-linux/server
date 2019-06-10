import networkx.algorithms.shortest_paths as shortest_paths
import random
import math
import copy

PACKET_WEIGHT = 10


class Model:
    def __init__(self, node_count, block_count, time, graph, assigner, tasks, nodes_for_block_create):
        self.graph = graph
        self.time = time
        self.node_count = node_count
        self.block_count = block_count
        self.assigner = assigner
        self.tasks = tasks
        self.nodes_for_block_create = nodes_for_block_create
        self.paths = {}
        for node in range(self.node_count):
            self.paths[node] = {}
            for path_target in range(self.node_count):
                if node == path_target:
                    continue
                if shortest_paths.has_path(self.graph, node, path_target):
                    path = shortest_paths.unweighted.bidirectional_shortest_path(self.graph, node, path_target)
                    if len(path) > 1:
                        self.paths[node][path_target] = path[1]

    def calculate(self):
        stats = Statistics()
        for node in range(self.node_count):
            stats.max[node] = stats.average[node] = 0

        for t in range(self.time):
            # генерируем задачу
            # найти узлы с нужными данные
            # передать задачу в параметризованную модель
            # передавать по одному пакету
            # для каждой связи своя очередь
            # пакет делим на несколько еденичных пакетов
            # за 1 такт обарбатываем каждую очередь

            # для разных n, матожидание, дисперсия, разные вероятности p, все параметры подвигать
            # можно рассказать об алгоритмах рандомизации
            task = self.tasks[t]
            hosts = self.get_hosts(task.block_number)
            packets = self.assigner.assign(task, hosts)
            for packet in packets:
                if packet.task.target in self.paths[packet.sender]:
                    self.add_packet(packet.sender, packet)

            self.create_new_block(t)

            nodes = list(range(self.node_count))
            random.shuffle(nodes)
            for node in nodes:
                for link_node in self.graph.node[node]["packets"]:
                    queue = self.graph.node[node]["packets"][link_node]

                    if not queue:
                        continue

                    packet = queue.pop()
                    next_node = self.paths[node][packet.task.target]
                    if next_node != packet.task.target:
                        self.add_packet(next_node, packet)
                    else:
                        self.graph.node[next_node]["data"].add(packet.task.block_number)

                self.calculate_statistics(stats, node)
        return stats

    def get_hosts(self, block_number):
        hosts = []
        for node in range(self.node_count):
            if block_number in self.graph.node[node]["data"]:
                hosts.append(node)
        return hosts

    def add_packet(self, sender, packet):
        next_node = self.paths[sender][packet.task.target]
        self.graph.node[sender]["packets"][next_node].appendleft(packet)

    def create_new_block(self, t):
        new_block_number = self.block_count
        self.block_count += 1
        host = self.nodes_for_block_create[t]
        self.graph.node[host]["data"].add(new_block_number)

    def calculate_statistics(self, stats, node):
        current_packets = [p for packets in self.graph.node[node]["packets"].values() for p in packets]
        count = len(current_packets)
        stats.average[node] += count / self.time
        stats.max[node] = stats.max[node] if stats.max[node] > count else count
        # stats.max_max = stats.max_max if stats.max_max > stats.max[node] else stats.max[node]
        # stats.max_average = stats.max_average if stats.max_average > stats.average[node] else stats.average[node]


class P2PAssigner:
    @staticmethod
    def assign(task, hosts):
        result = []
        if len(hosts) == 0:
            return result

        rnd = random.Random()
        i = rnd.randint(0, len(hosts) - 1)
        sender = hosts[i]
        for _ in range(PACKET_WEIGHT):
            result.append(Packet(sender, task))
        return result


class M2PAssigner:
    def __init__(self, duplication_degree):
        self.duplication_degree = duplication_degree

    def assign(self, task, hosts):
        result = []
        if len(hosts) == 0:
            return result
        elif len(hosts) <= self.duplication_degree:
            senders = hosts
        else:
            senders = copy.copy(hosts)
            random.shuffle(senders)
            senders = senders[:self.duplication_degree]

        for sender in senders:
            for _ in range(math.ceil(PACKET_WEIGHT / len(senders))):
                result.append(Packet(sender, task))
        return result


class Packet:
    def __init__(self, sender, task):
        self.sender = sender
        self.task = task


class Task:
    def __init__(self, block_number, target):
        self.block_number = block_number
        self.target = target


class Statistics:
    def __init__(self):
        self.average = {}
        self.max = {}
        # self.max_max = 0
        # self.max_average = 0

import networkx as nx
import networkx.algorithms.shortest_paths as shortest_paths
import random
import collections
import math


PUT_WIGHT = 30


class Model:
    def __init__(self, n, time, duplication_degree, generate_command_probability, graph, command_generator):
        self.graph = graph
        self.time = time
        self.duplication_degree = duplication_degree
        self.generate_command_probability = generate_command_probability
        self.n = n
        self.command_generator = command_generator
        self.paths = {}
        for node in range(self.n):
            self.graph.node[node]["commands"] = collections.deque()
            self.graph.node[node]["cmd_time"] = 0
            self.paths[node] = {}
            for path_target in range(self.n):
                if node == path_target:
                    continue
                if shortest_paths.has_path(self.graph, node, path_target):
                    path = shortest_paths.unweighted.bidirectional_shortest_path(self.graph, node, path_target)
                    if len(path) > 1:
                        self.paths[node][path_target] = path[1]

    def calculate(self):
        stats = Statistics()
        for node in range(self.n):
            stats.max[node] = stats.average[node] = 0

        for t in range(self.time):
            # генерируем задачу
            # найти узлы с нужными данные
            # передать задачу в параметризованную модель

            # передавать по одному пакету
            # для каждой связи своя очередь
            # пакет делим на несколько еденичных пакетов
            # за 1 такт обарбатываем каждую очередь
            for node in range(self.n):
                # self.generate_command(node)
                commands = self.graph.node[node]["commands"]
                if not commands:
                    continue
                cmd = commands[-1]

                if cmd.target == node:
                    self.del_command(node)
                    # self.handle_command(cmd, node)
                    if not commands:
                        continue
                    cmd = commands[-1]

                cmd_time = self.graph.node[node]["cmd_time"]
                # inc и dec одновременно
                cmd_time -= 1
                if cmd_time == 0:
                    if cmd.target in self.paths[node].keys():
                        self.add_command(self.paths[node][cmd.target], cmd)
                    self.del_command(node)
                else:
                    self.graph.node[node]["cmd_time"] = cmd_time
                self.calculate_statistics(stats, node, cmd)
        return stats

    def add_command(self, node, command):
        commands = self.graph.node[node]["commands"]
        if len(commands) == 0:
            self.graph.node[node]["cmd_time"] = command.weight
        commands.appendleft(command)

    def del_command(self, node):
        commands = self.graph.node[node]["commands"]
        commands.pop()
        cmd = commands[-1] if len(commands) > 0 else None
        self.graph.node[node]["cmd_time"] = cmd.weight if cmd else 0

    def generate_command(self, node):
        rnd = random.Random()
        x = rnd.random()
        if x < self.generate_command_probability:
            generated = self.command_generator.generate(node, self.n, rnd)
            for g in generated:
                self.add_command(node, g)

    def handle_command(self, cmd, node):
        if isinstance(cmd, SendCommand):
            self.add_command(node, PutCommand(cmd.receiver))
        if isinstance(cmd, LightSendCommand):
            self.add_command(node, LightPutCommand(math.ceil(PUT_WIGHT / self.duplication_degree), cmd.receiver))

    def calculate_statistics(self, stats, node, cmd):
        commands = self.graph.node[node]["commands"]
        count = len(commands)
        stats.average[node] += count / self.time
        stats.max[node] = stats.max[node] if stats.max[node] > count else count
        stats.max_max = stats.max_max if stats.max_max > stats.max[node] else stats.max[node]
        stats.max_average = stats.max_average if stats.max_average > stats.average[node] else stats.average[node]
        cmd_class_name = type(cmd).__name__
        if cmd_class_name not in stats.command_stats:
            stats.command_stats[cmd_class_name] = 0
        stats.command_stats[cmd_class_name] += 1


def generate_node(banned, n, rnd):
    result = rnd.randint(0, n)
    while result in banned:
        result = rnd.randint(0, n)
    return result


class P2PCommandGenerator:
    @staticmethod
    def generate(source, node_count, rnd):
        banned = {source}
        sender = generate_node(banned, node_count - 1, rnd)
        banned.add(sender)
        receiver = generate_node(banned, node_count - 1, rnd)
        return [SendCommand(sender, receiver)]


class M2PCommandGenerator:
    def __init__(self, duplication_degree):
        self.duplication_degree = duplication_degree

    @staticmethod
    def _generate(source, node_count, rnd):
        banned = {source}
        target = generate_node(banned, node_count - 1, rnd)
        banned.add(target)
        receiver = generate_node(banned, node_count - 1, rnd)
        return [LightSendCommand(target, receiver)]

    def generate(self, source, node_count, rnd):
        banned = {source}
        target = generate_node(banned, node_count - 1, rnd)
        banned.add(target)
        receiver = generate_node(banned, node_count - 1, rnd)
        banned.add(receiver)

        senders = set()
        while len(senders) < self.duplication_degree:
            sender = generate_node(banned, node_count - 1, rnd)
            senders.add(sender)
            banned.add(sender)

        return map(lambda s: LightSendCommand(s, receiver), senders)


class Command:
    def __init__(self, weight, target):
        self.weight = weight
        self.target = target


class Statistics:
    def __init__(self):
        self.average = {}
        self.max = {}
        self.max_max = 0
        self.max_average = 0
        self.command_stats = {}

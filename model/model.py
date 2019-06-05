import networkx as nx
import networkx.algorithms.shortest_paths as shortest_paths
import random
import collections


class Model:
    def __init__(self, n, time, graph, command_generator):
        self.graph = graph
        self.time = time
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
            for node in range(self.n):
                self.generate_command(node)
                commands = self.graph.node[node]["commands"]
                if not commands:
                    continue

                cmd = commands[-1]

                if cmd.target == node:
                    self.del_command(node)
                    self.handle_command(cmd, node)
                    continue

                cmd_time = self.graph.node[node]["cmd_time"]
                cmd_time -= 1
                if cmd_time == 0:
                    if cmd.target in self.paths[node].keys():
                        self.add_command(self.paths[node][cmd.target], cmd)
                    self.del_command(node)
                else:
                    self.graph.node[node]["cmd_time"] = cmd_time
                self.calculate_statistics(stats, node)
        return stats

    def add_command(self, node, command):
        commands = self.graph.node[node]["commands"]
        if len(commands) == 0:
            self.graph.node[node]["cmd_time"] = command.weight
        commands.append(command)

    def del_command(self, node):
        commands = self.graph.node[node]["commands"]
        commands.pop()
        cmd = commands[-1] if len(commands) > 0 else None
        self.graph.node[node]["cmd_time"] = cmd.weight if cmd else 0

    def generate_command(self, node):
        rnd = random.Random()
        x = rnd.random()
        if x < 0.6:
            generated = self.command_generator.generate(node, self.n, rnd)
            for g in generated:
                self.add_command(g.sender, g.command)

    def handle_command(self, cmd, node):
        if isinstance(cmd, SendCommand):
            self.add_command(node, PutCommand(cmd.target))
        if isinstance(cmd, LightSendCommand):
            self.add_command(node, LightPutCommand(cmd.target))

    def calculate_statistics(self, stats, node):
        commands = self.graph.node[node]["commands"]
        count = len(commands)
        stats.average[node] += count / self.time
        stats.max[node] = stats.max[node] if stats.max[node] > count else count


class P2PCommandGenerator:
    @staticmethod
    def generate(sender, node_count, rnd):
        target = rnd.randint(0, node_count - 1)
        return [GeneratedCommand(sender, SendCommand(sender, target))]


class M2PCommandGenerator:
    def __init__(self, duplication_degree):
        self.duplication_degree = duplication_degree

    @staticmethod
    def generate(sender, node_count, rnd):
        target = rnd.randint(0, node_count - 1)
        return [GeneratedCommand(sender, LightSendCommand(sender, target))]

    def _generate(self, sender, node_count, rnd):
        target = rnd.randint(0, node_count - 1)
        senders = {sender}
        while len(senders) < self.duplication_degree:
            sender = rnd.randint(0, node_count - 1)
            if sender not in senders:
                senders.add(sender)

        return map(lambda s: GeneratedCommand(s, LightSendCommand(s, target)), senders)


class GeneratedCommand:
    def __init__(self, sender, command):
        self.sender = sender
        self.command = command


class Command:
    def __init__(self, weight, target):
        self.weight = weight
        self.target = target


class PutCommand(Command):
    def __init__(self, target):
        super().__init__(3, target)


class LightPutCommand(Command):
    def __init__(self, target):
        super().__init__(1, target)


class PrepareCommand(Command):
    def __init__(self, target):
        super().__init__(1, target)


class SendCommand(Command):
    def __init__(self, sender, target):
        super().__init__(1, target)
        self.sender = sender


class LightSendCommand(Command):
    def __init__(self, sender, target):
        super().__init__(1, target)
        self.sender = sender


class Statistics:
    def __init__(self):
        self.average = {}
        self.max = {}

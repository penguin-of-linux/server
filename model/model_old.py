import networkx as nx
import networkx.algorithms.shortest_paths as shortest_paths


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.commands = []

    """
    x - negin point
    y - end point
    weight - time in ms needed to send 1Mb
    min_weight - time in ms need to send empty packet
    """
    def edge(self, x, y, weight, min_weight):
        self.graph.add_edge(x, y)
        self.graph[x][y]["total"] = 0
        self.graph[x][y]["weight"] = weight
        self.graph[x][y]["min"] = min_weight
        return self

    def put(self, sender, receiver, data_length):
        self.commands.append(Command(sender, receiver, data_length))
        return self

    def prepare(self, sender, receiver):
        self.commands.append(Command(sender, receiver))
        return self

    def send(self, initiator, sender, receiver, data_length):
        self._send(initiator, sender)
        self.prepare(initiator, receiver)
        self.put(sender, receiver, data_length)
        return self

    def _send(self, initiator, sender):
        self.commands.append(Command(initiator, sender))

    def calculate(self):
        while self.commands:
            command = self.commands.pop()
            self.graph.add_node(command.sender)
            self.graph.add_node(command.receiver)
            path = shortest_paths.unweighted.bidirectional_shortest_path(self.graph, command.sender, command.receiver)

            for i in range(0, len(path) - 1):
                edge = self.graph[path[i]][path[i + 1]]
                edge["total"] += edge["min"] + edge["weight"] * command.data_length

        info = {}
        for edge in self.graph.edges:
            info[edge] = self.graph[edge[0]][edge[1]]["total"]
        return info


class Command:
    def __init__(self, sender, receiver, data_length=0):
        self.data_length = data_length
        self.sender = sender
        self.receiver = receiver

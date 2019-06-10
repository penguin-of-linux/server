import networkx as nx
import unittest

from model_old_new import *


class ModelTests(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        generate_command_probability = 1
        time = 5
        n = 4
        generator = Generator_ForTest1()
        g = nx.Graph()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 3)
        g.add_edge(3, 2)
        model = Model(n, time, 1, generate_command_probability, g, generator)
        model.calculate()
        res = {}
        for i in range(n):
            res[i] = len(g.node[i]["commands"])
        self.assertEqual(res, {0: 0, 1: 5, 2: 0, 3: 0})

    def test2(self):
        generate_command_probability = 1
        time = 5
        n = 4
        generator = Generator_ForTest2()
        g = nx.Graph()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 3)
        g.add_edge(3, 2)
        model = Model(n, time, 2, generate_command_probability, g, generator)
        model.calculate()
        res = {}
        for i in range(n):
            res[i] = len(g.node[i]["commands"])
        self.assertEqual(res, {0: 5, 1: 3, 2: 0, 3: 2})


class Generator_ForTest1:
    @staticmethod
    def generate(sender, node_count, rnd):
        if sender == 0:
            return [SendCommand(1, 2)]
        else:
            return []


class Generator_ForTest2:
    @staticmethod
    def generate(sender, node_count, rnd):
        if sender == 0:
            return [LightSendCommand(1, 2), LightSendCommand(3, 2)]
        else:
            return []


if __name__ == "__main__":
    unittest.main()

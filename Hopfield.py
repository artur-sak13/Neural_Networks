# @author Artur Sak (sak2)

import random
from Activations import *

class Hopfield(Network):
    def __init__(self, numNodes, screen_size):
        self.numNodes = numNodes
        self.threshold = 0.0
        self.screen_size = screen_size
        self.distortions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        self.walsh = [[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                       0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                      [1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,
                       1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0],
                      [1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,
                       1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0],
                       [1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0]]

        Network.__init__(self, numNodes, screen_size)

    def train_network(self, patterns):
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0.0

        for pattern in patterns:
            for i in xrange(len(self.nodes)):
                self.nodes[i].activation = pattern[i]

        for node in self.nodes:
            for conn in node.incoming:
                conn.learn()

    def test(self, training_set):
        for pattern in training_set:
            for distortion in self.distortions:
                for unit in pattern:
                    if random.random() < distortion:
                        pass

    def hamming_dist(self,pattern):
        dist = 0
        for i in xrange(len(self.nodes)):
            if self.nodes[i].activation != pattern[i]:
                dist += 1
        return dist
            
    def toggle_random_node(self):
        node = random.choice(self.nodes)
        if node.activation > self.threshold:
            node.activation = 0.0
        elif node.activation < self.threshold:
            node.activation = 1.0

    def run(self):
        pass

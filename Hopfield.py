# @author Artur Sak
import random
from Activations import *

class Hopfield(Network):
    def __init__(self, numNodes, screen_size):
        self.numNodes = numNodes
        self.threshold = 0.0
        self.screen_size = screen_size

        self.walsh = [[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                       0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                      [1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,
                       1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0],
                      [1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,
                       1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0],
                       [1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0]]

        Network.__init__(self, numNodes, screen_size)

    def train_network(self):
        pass

    def toggle_random_node(self):
        node = random.choice(self.nodes)
        if node.activation > self.threshold:
            node.activation = 0.0
        elif node.activation < self.threshold:
            node.activation = 1.0

    def run_network(self, iterations):
        pass

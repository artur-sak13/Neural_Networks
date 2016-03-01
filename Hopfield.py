# @author Artur Sak (sak2)

import copy
from Activations import *
# from Graphics import *

def toggle(node):
    if node == 1:
        return 0.0
    else:
        return 1.0


class Hopfield(Network):
    def __init__(self, numNodes, screen_size):
        self.numNodes = numNodes
        self.threshold = 0.0
        self.energy = 0.0
        self.screen_size = screen_size
        self.distortions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

        self.walsh = [[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                       0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                      [1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,
                       1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0],
                      [1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,
                       1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0],
                       [1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,
                        1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0]]

        Network.__init__(self, numNodes, screen_size)

    def train_network(self):
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0.0

        for pattern in self.walsh:
            self.set_activations(pattern)

        for node in self.nodes:
            for conn in node.incoming:
                conn.learn()

    def test(self):
        for pattern in self.walsh:
            pattern_d = copy.deepcopy(pattern)
            for distortion in self.distortions:
                for activation in pattern_d:
                    if random.random() < distortion:
                        toggle(activation)
                for i in range(3):
                    self.run(pattern_d, pattern)

    def hamming_dist(self, pattern):
        dist = 0
        for i in xrange(len(self.nodes)):
            if self.nodes[i].activation != pattern[i]:
                dist += 1
        return dist

    def calc_energy(self):
        self.energy = 0.0
        for node in self.nodes:
            for connection in node.incoming:
                self.energy += connection.weight * (node.activation * connection.sender.activation)
        self.energy *= -0.5

    def changed(self):
        pre_energy = self.energy
        self.calc_energy()
        if pre_energy != self.energy:
            return True
        else:
            return False

    def run(self, pattern_d):
        all_done = False
        iterations_settled = 0
        self.set_activations(pattern_d,)

        while not all_done:
            self.set_inputs()
            self.update_all_activations()
            if self.changed():
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True

        print self.hamming_dist(pattern_d)

def main():
    size = (1000,700)
    net = Hopfield(16,size)
    # screen = Graphics(size=size)
    # screen.draw_graph(net.nodes)
    # screen.mainloop(net.nodes)
    net.train_network()
    net.test()

main()

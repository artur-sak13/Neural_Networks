# @author Artur Sak (sak2)

import copy
from Activations import *
# from Graphics import *

def toggle(node):
    if node == 1:
        return 0
    else:
        return 1

class Hopfield(Network):
    def __init__(self, numNodes, screen_size):
        self.numNodes = numNodes
        self.threshold = 0.0
        self.energy = 0.0
        self.screen_size = screen_size
        self.distortions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

        self.walsh = [[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                      [1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0],
                      [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
                      [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]]

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
                print "Distortion: " + str(distortion)
                for i in range(3):
                    for i in range(len(pattern_d)):
                        if random.random() < distortion:
                            pattern_d[i] = toggle(pattern_d[i])
                    self.run(pattern_d, pattern)
            print "____________________END OF PATTERN______________________" + "\n"

    def hamming_dist(self, pattern, orig):
        # print "Distorted Pattern: " + str(pattern)
        # print "Walsh function: " + str(orig)
        dist = 0
        for i in range(len(self.nodes)):
            if pattern[i] != orig[i]:
                dist += 1
        # print "Hamming Distance: " + str(dist)
        # print "\n"
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

    def run(self, pattern_d, orig):
        all_done = False
        iterations_settled = 0
        self.set_activations(pattern_d)
        self.set_inputs()

        while not all_done:
            self.update_all_activations()
            if self.changed():
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True
        print "Walsh Function: " + str(orig)
        print "Distorted: " +  str(pattern_d)
        settled = []
        for node in self.nodes:
            settled.append(node.activation)
        print "Settled: " + str(settled)
        print "Hamming Distance: " + str(self.hamming_dist(settled, orig))
        print "Energy: " + str(self.energy)
        # self.hamming_dist(pattern_d, orig)
        print "\n"

def main():
    size = (1000,700)
    net = Hopfield(16,size)
    # screen = Graphics(size=size)
    # screen.draw_graph(net.nodes)
    # screen.mainloop(net.nodes)
    net.train_network()
    net.test()

main()

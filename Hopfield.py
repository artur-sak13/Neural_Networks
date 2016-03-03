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
        self.threshold = 0
        self.energy = 0.0
        self.screen_size = screen_size
        self.distortions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

        self.walsh = [[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                      [1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0],
                      [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
                      [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]]

        Network.__init__(self, numNodes, screen_size)

    # Function trains network on all walsh function patterns
    def train_network(self):
        # Clears the net
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0
        # "Learn" every training pattern
        for pattern in self.walsh:
            self.set_activations(pattern)
            for node in self.nodes:
                for conn in node.incoming:
                    conn.learn()

    # Tests if network returns to trained patterns when loaded with a distorted pattern
    def test(self):
        for pattern in self.walsh:
            for distortion in self.distortions:
                print "Distortion: " + str(distortion)
                for i in range(3):
                    pattern_d = copy.deepcopy(pattern)
                    for j in range(len(pattern_d)):
                        if random.random() < distortion:
                            pattern_d[j] = toggle(pattern_d[j])
                    self.run(pattern_d, pattern)
            print "____________________END OF PATTERN______________________" + "\n"

    # Calculates the Hamming Distance between two patterns
    def hamming_dist(self, pattern, orig):
        dist = 0
        for i in range(len(self.nodes)):
            if pattern[i] != orig[i]:
                dist += 1
        return dist

    # Calculates the "energy" of the network
    def calc_energy(self):
        self.energy = 0.0
        for node in self.nodes:
            for connection in node.incoming:
                self.energy += connection.weight * (node.activation * connection.sender.activation)
        self.energy *= -0.5

    # Checks if current state differs from previous state
    def changed(self, orig):
        for i in range(len(self.nodes)):
            if orig[i] != self.nodes[i].activation:
                return True
        return False

    # Runs the network on the distored patterns
    def run(self, pattern_d, orig):
        all_done = False
        iterations_settled = 0
        self.set_activations(pattern_d)
        settled = []

        while not all_done:
            # self.calc_energy()
            # print "Energy: " + str(self.energy)
            del settled[:]
            for node in self.nodes:
                settled.append(node.activation)
            node = self.nodes[random.randint(0,len(self.nodes) - 1)]
            # node.update_input()
            self.set_inputs()
            node.update_activation()

            if self.changed(settled):
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True
        print "Walsh Function: " + str(orig)
        print "Distorted: " +  str(pattern_d)
        print "Settled: " + str(settled)
        print "Hamming Distance: " + str(self.hamming_dist(settled, orig))
        self.calc_energy()
        print "Energy: " + str(self.energy)
        print "\n"

# Runs the entire simulation
def main():
    size = (1000,700)
    net = Hopfield(16,size)
    # screen = Graphics(size=size)
    # screen.draw_graph(net.nodes)
    # screen.mainloop(net.nodes)
    net.train_network()
    net.test()

main()

# @author Artur Sak (sak2)

import copy
from Activations import *
import csv
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

    def random_train(self):
        training_patterns = [[random.randint(0,1) for x in range(16)] for y in range(4)]
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0

        self.walsh = training_patterns
        for pattern in self.walsh:
            self.set_activations(pattern)
            for node in self.nodes:
                for conn in  node.incoming:
                    conn.learn()

    def relational_train(self):
        base = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
        pattern_d = [[toggle(x) for x in base if random.random() < 0.125] for y in range(6)]

        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0

        for pattern in training_patterns:
            self.set_activations(pattern)
            for node in self.nodes:
                for conn in  node.incoming:
                    conn.learn()


    # Tests if network returns to trained patterns when loaded with a distorted pattern
    def test(self):
        for pattern in self.walsh:
            # for distortion in self.distortions:
            for i in range(3):
                pattern_d = copy.deepcopy(pattern)
                for j in range(len(pattern_d)):
                    if random.random() < self.distortions[0]:
                        pattern_d[j] = toggle(pattern_d[j])
                self.run(pattern_d, pattern, self.distortions[0], i)
        print "____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(pattern) + 1) + "\n"

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
    def run(self, pattern_d, orig, dist, run):
        all_done = False
        iterations_settled = 0
        total_iters = 0
        self.set_activations(pattern_d)
        settled = []
        # eng_df = []

        while not all_done:
            total_iters += 1
            del settled[:]
            for node in self.nodes:
                settled.append(node.activation)
            node = self.nodes[random.randint(0,len(self.nodes) - 1)]
            self.set_inputs()
            # self.calc_energy()
            # eng_df.append(self.energy)
            node.update_activation()

            if self.changed(settled):
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True

        self.calc_energy()

        print "Walsh Function: " + str(orig)
        print "Distorted: " +  str(pattern_d)
        print "Settled: " + str(settled)
        print "Hamming Distance: " + str(self.hamming_dist(settled, orig))
        # eng_df.append(self.energy)
        # before_settled = total_iters - iterations_settled
        # print """
        # ------------------------------------
        # |           Pattern         | {s1} |
        # ------------------------------------
        # |             Run           | {s2} |
        # ------------------------------------
        # |          Distortion       | {s3} |
        # ------------------------------------
        # |      Hamming Distance     | {s4} |
        # ------------------------------------
        # | Iterations before settled | {s5} |
        # ------------------------------------
        # |           Energy          | {s6} |
        # ------------------------------------
        # """.format(s1=str(self.walsh.index(orig) + 1).center(4), s2=str(run + 1).center(4), s3 = str(dist).center(4),
        #            s4=str(self.hamming_dist(settled, orig)).center(4),
        #            s5=str(before_settled).center(4), s6=str(int(self.energy)).center(4))

    # An alternate run
    def alt_run(self):
        pass


# Runs the entire simulation
def main():
    size = (1000,700)
    net = Hopfield(16,size)
    # net.train_network()
    # net.test()
    net.random_train()
    net.test()

main()

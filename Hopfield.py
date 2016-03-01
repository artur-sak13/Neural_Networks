# @author Artur Sak (sak2)

from Activations import *

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
                        self.run(pattern_d)

    def hamming_dist(self,pattern):
        dist = 0
        for i in xrange(len(self.nodes)):
            if self.nodes[i].activation != pattern[i]:
                dist += 1
        return dist

    def calc_energy(self):
        self.energy = 0.0
        for node in nodes:
            for connection in node.incoming:
                self.energy += connection.weight * (node.activation * connection.sender.activation)

    def changed(self):
        pre_energy = self.energy
        self.calc_energy()
        if pre_energy != self.energy:
            return True
        else:
            return False


    def toggle_random_node(self):
        node = random.choice(self.nodes)
        if node.activation > self.threshold:
            node.activation = 0.0
        elif node.activation < self.threshold:
            node.activation = 1.0

    def run(self):
        all_done = False
        iterations_settled = 0

        while not all_done:
            self.toggle_random_node()
            if self.changed():
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True

# @author Artur Sak (sak2)

import copy
from Activations import *
import Data
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
        self.data = Data.Data()

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

    def alt_train(self):
        # Clears the net
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0

        # "Learn" one training pattern
        self.set_activations(self.walsh[3])
        for node in self.nodes:
            for conn in node.incoming:
                conn.learn()

    def random_train(self):
        training_patterns = [[0 if random.random() < 0.5 else 1 for x in range(16)] for y in range(4)]
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0

        self.walsh = training_patterns
        for pattern in self.walsh:
            self.set_activations(pattern)
            for node in self.nodes:
                for conn in node.incoming:
                    conn.learn()

    def relational_train(self):
        base = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
        rel_patterns = [[toggle(x) if random.random() < 0.125 else x for x in base] for y in range(6)]
        for node in self.nodes:
            for conn in node.incoming:
                conn.weight = 0

        self.walsh = rel_patterns
        for pattern in self.walsh:
            self.set_activations(pattern)
            for node in self.nodes:
                for conn in node.incoming:
                    conn.learn()


    # Tests if network returns to trained patterns when loaded with a distorted pattern
    def test(self, distort_one = False):
        if distort_one:
          for pattern in self.walsh:
                for i in range(3):
                    pattern_d = copy.deepcopy(pattern)
                    for j in range(len(pattern_d)):
                        if random.random() < self.distortions[0]:
                            pattern_d[j] = toggle(pattern_d[j])
                    self.run(pattern_d, pattern, self.distortions[0], i)
                # self.data.save_data("\n"+"____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(pattern) + 1) + "\n")
                print "\n"+"____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(pattern) + 1) + "\n"

        else:
            for pattern in self.walsh:
                for distortion in self.distortions:
                    for i in range(3):
                        pattern_d = copy.deepcopy(pattern)
                        for j in range(len(pattern_d)):
                            if random.random() < distortion:
                                pattern_d[j] = toggle(pattern_d[j])
                        self.run(pattern_d, pattern, distortion, i)
                # self.data.save_data("\n"+"____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(pattern) + 1) + "\n")
                print "\n"+"____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(pattern) + 1) + "\n"

    def alt_test(self):
        for distortion in self.distortions:
            for i in range(3):
                pattern_d = copy.deepcopy(self.walsh[3])
                for j in range(len(pattern_d)):
                    if random.random() < distortion:
                        pattern_d[j] = toggle(pattern_d[j])
                self.alt_run(pattern_d,self.walsh[3], distortion,i, True)
            # self.data.save_data("\n"+"____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(self.walsh[3]) + 1))
            print "\n"+"____________________END OF PATTERN {d}______________________".format(d=self.walsh.index(self.walsh[3]) + 1)


    def anotha_one(self):
        # self.data.save_data("ADDED ANOTHER!")
        pattern = [1 if random.random() < 0.5 else 0 for x in range(16)]
        self.walsh.append(pattern)

        self.set_activations(pattern)
        for node in self.nodes:
            for conn in node.incoming:
                conn.learn()

    def and_anotha_one(self, iters):
        for x in range(iters):
            self.anotha_one()
            self.test(True)

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

    # Runs the network on the distorted patterns
    def run(self, pattern_d, orig, dist, run):
        all_done = False
        iterations_settled = 0
        total_iters = 0
        self.set_activations(pattern_d)
        settled = []

        while not all_done:
            total_iters += 1
            del settled[:]
            for node in self.nodes:
                settled.append(node.activation)
            node = self.nodes[random.randint(0,len(self.nodes) - 1)]
            self.set_inputs()
            node.update_activation()

            if self.changed(settled):
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True
            elif total_iters == 300:
                break

        self.calc_energy()

        if total_iters == 300:
            before_settled = "N/A"
        else:
            before_settled = total_iters - iterations_settled

        info="""
        ------------------------------------
        |           Pattern         | {s1} |
        ------------------------------------
        |             Run           | {s3} |
        ------------------------------------
        |          Distortion       | {s4} |
        ------------------------------------
        |       Hamming Distance    | {s6} |
        ------------------------------------
        | Iterations before settled | {s8} |
        ------------------------------------
        |            Energy         | {s9} |
        ------------------------------------
        |        Original Pattern          |
        ------------------------------------
        | {s2}  |
        ------------------------------------
        |       Distorted Pattern          |
        ------------------------------------
        | {s5}  |
        ------------------------------------
        |         Settled Pattern          |
        ------------------------------------
        | {s7}  |
        ------------------------------------
        """.format(s1=str(self.walsh.index(orig) + 1).center(4),s2=''.join(str(orig)[1:-1].split(',')).center(4), s3=str(run + 1).center(4), s4 = str(dist).center(4),
                   s5=''.join(str(pattern_d)[1:-1].split(',')).center(4), s6=str(self.hamming_dist(settled, orig)).center(4),s7=''.join(str(settled).split(','))[1:-1].center(4),
                   s8=str(before_settled).center(4), s9=str(int(self.energy)).center(4))

        print info
        # self.data.save_data(info)


    # An alternate run
    def alt_run(self, pattern_d, orig, dist, run, async=False):
        all_done = False
        iterations_settled = 0
        total_iters = 0
        self.set_activations(pattern_d)
        settled = []
        while not all_done:
            total_iters += 1
            del settled[:]
            for node in self.nodes:
                settled.append(node.activation)

            if async:
                for i in range(4):
                    node = self.nodes[random.randint(0,len(self.nodes) - 1)]
                    self.set_inputs()
                    node.update_activation()

            else:
                self.set_inputs()
                self.update_all_activations()

            if self.changed(settled):
                iterations_settled = 0
            else:
                iterations_settled += 1
            if iterations_settled == 30:
                all_done = True
            elif total_iters == 300:
                break

        self.calc_energy()
        if total_iters == 300:
            before_settled = "N/A"
        else:
            before_settled = total_iters - iterations_settled

        info = """
        ------------------------------------
        |           Pattern         | {s1} |
        ------------------------------------
        |             Run           | {s3} |
        ------------------------------------
        |          Distortion       | {s4} |
        ------------------------------------
        |       Hamming Distance    | {s6} |
        ------------------------------------
        | Iterations before settled | {s8} |
        ------------------------------------
        |            Energy         | {s9} |
        ------------------------------------
        |        Original Pattern          |
        ------------------------------------
        | {s2}  |
        ------------------------------------
        |       Distorted Pattern          |
        ------------------------------------
        | {s5}  |
        ------------------------------------
        |         Settled Pattern          |
        ------------------------------------
        | {s7}  |
        ------------------------------------
        """.format(s1=str(self.walsh.index(orig) + 1).center(4),s2=''.join(str(orig)[1:-1].split(',')).center(4), s3=str(run + 1).center(4), s4 = str(dist).center(4),
                   s5=''.join(str(pattern_d)[1:-1].split(',')).center(4), s6=str(self.hamming_dist(settled, orig)).center(4),s7=''.join(str(settled).split(','))[1:-1].center(4),
                   s8=str(before_settled).center(4), s9=str(int(self.energy)).center(4))
        # self.data.save_data(info)
        print info




# Runs the entire simulation
def main():
    size = (1000,700)
    net = Hopfield(16,size)
    # Regular Walsh function simulation
    # net.train_network()
    # net.test()

    # Random training pattern simulation
    # net.random_train()
    # net.test()

    # Add 4 more random patterns
    # net.and_anotha_one(4)

    # Systematically related pattern simulation
    # net.relational_train()
    # net.test(True)

    # Async and Sync Updating
    # net.alt_train()
    # net.alt_test()

# main()

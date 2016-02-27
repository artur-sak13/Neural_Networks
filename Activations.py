# @author Artur Sak (sak2)
from Structures import *

def add_t(*tuples):
    return tuple(sum(x) for x in zip(*tuples))

def mul_t_constant(t, constant):
    return tuple(x * constant for x in t)

class Network(object):
    def __init__(self, numNodes, screen_size):
        # Initializes network with numNodes attribute and list of nodes
        self.numNodes = numNodes
        self.screen_size = screen_size
        xmax, ymax = self.screen_size
        self.repulsion = 1000000
        self.attraction = 2
        self.timestep = 0.15
        self.damping = 0.5
        self.min_spring_distance = 100
        # Create n number of Unit objects in node list
        self.nodes = [Unit(x_range=(0,xmax), y_range=(0,ymax)) for i in range(numNodes)]
        # Add connections to each node's "incoming" adjacency list
        for i in range(len(self.nodes)):
            self.nodes[i].add_neighbor(Connection(recipient=self.nodes[i],
                                                  sender=self.nodes[(i+1)%numNodes],
                                                  weight=1.0))
            self.nodes[i].add_neighbor(Connection(recipient=self.nodes[i],
                                                  sender=self.nodes[(i+2)%numNodes],
                                                  weight=1.0))

    def generate_graph(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i != j:
                    self.nodes[i].neighbors.append(self.nodes[j])
        return self.nodes

    def adjust_positions(self, nodes_list):
        for node in nodes_list:
            if node.static == True:
                continue
            net_force = (0,0)

            for other in nodes_list:
                if other != node:
                    nx, ny = net_force
                    cx, cy = self.coulomb_repulsion(node, other)
                    net_force = (nx + cx, ny + cy)

            for other in node.neighbors:
                nx, ny = net_force
                hx, hy = self.hooke_attraction(node, other)
                net_force = (nx + hx, ny + hy)

            temp = mul_t_constant(net_force, self.timestep)
            node.velocity = mul_t_constant(add_t(node.velocity, temp), self.damping)
            node.position = add_t(node.position, mul_t_constant(node.velocity, self.timestep))

        return nodes_list

    def hooke_attraction(self, node, other):
        distance = self.find_distance(node, other)
        angle = self.angle(node, other)

        force = -self.attraction * (distance - self.min_spring_distance)

        x = math.cos(angle) * force
        y = math.sin(angle) * force
        return (x, y)

    def coulomb_repulsion(self, node, other):
        distance = self.find_distance(node, other)
        angle = self.angle(node, other)

        try:
            force = (self.repulsion * node.charge * other.charge) / (distance**2)
        except ZeroDivisionError:
            force = 0

        x = math.cos(angle) * force
        y = math.sin(angle) * force
        return (x, y)

    def delta(self, node, other):
        return (node.x - other.x, node.y - other.y)

    def find_distance(self, node, other):
        delta_x, delta_y = self.delta(node, other)
        distance = math.hypot(delta_x, delta_y)
        return distance

    def angle(self, node, other):
        delta_x, delta_y = self.delta(node, other)
        return math.atan2(delta_y, delta_x)


    # Sets the initial activation values for the network
    def set_activations(self, activations):
        for node in self.nodes:
            node.activation = activations[self.nodes.index(node)]

    # Update all of the activations in the network
    def update_all_activations(self, i = None):
        for node in self.nodes:
            node.update_activation()
            # node.temporal_integrator(0.5, 0.1, inhibit = i )

    # Calculate the inputs for all of the nodes in the network
    def set_inputs(self, const=None):
        if const:
            for node in self.nodes:
                node.input = const
        else:
            for node in self.nodes:
                node.update_input()

    # Reveals the input and activation values for the entire network
    def reveal_network(self):
        for node in self.nodes:
            print "Input for node %d: " %(self.nodes.index(node) + 1), node.input
        for node in self.nodes:
            print "Activation for node %d: " %(self.nodes.index(node) + 1), node.activation
        print('\n')

    # Runs the network for n number of iterations allowing for run splitting (max 2 splits)
    def run_network(self, iter1, iter2=None):
        for i in range(iter1):
            sub = [i+1," "] if (i + 1) < 10 else [i + 1 ,""]
            test_string = """
            ------------------
            |  Iteration: {d}{s} |
            ------------------
            """.format(d=sub[0],s=sub[1])
            print test_string
            self.set_inputs()
            self.update_all_activations()
            self.reveal_network()


        # Check for split iteration
        if iter2:
            for i in range(iter2):
                sub = [iter1 + i + 1," "] if (iter1 + i + 1) < 10 else [iter1 + i + 1 ,""]
                test_string = """
                ------------------
                |  Iteration: {d}{s} |
                ------------------
                """.format(d=sub[0],s=sub[1])
                print test_string
                self.set_inputs()
                self.update_all_activations()
                self.reveal_network()

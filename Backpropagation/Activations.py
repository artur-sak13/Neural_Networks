# @author Artur Sak (sak2)

from Structures import *

def add_t(*tuples):
    return tuple(sum(x) for x in zip(*tuples))

def mul_t_constant(t, constant):
    return tuple(x * constant for x in t)

class Layer(object):
    def __init__(self, num_nodes, index, bias_node = True, output_layer = False):
        self.nodes = []
        self.index = index
        self.has_bias_node = bias_node
        self.output_layer = output_layer

        for i in xrange(num_nodes):
            self.nodes.append(Unit(index, i))
        if self.has_bias_node:
            self.nodes.append(Unit(index, num_nodes, True))

class Network(object):
    def __init__(self, nodes_per_layer, screen_size=(0,0)):
        # Initializes network with numNodes attribute and list of nodes
        self.layers = []
        layer_number = 0

        for num_nodes in nodes_per_layer:
            layer_number += 1
            if layer_number == len(nodes_per_layer):
                self.layers.append(Layer(num_nodes, layer_number, False, True))
            else:
                self.layers.append(Layer(num_nodes, layer_number))

        self.connections  = []
        self.connect_nodes()
        self.global_error = 0.0
        self.learning_rate = 0.5


        self.screen_size = screen_size
        xmax, ymax = self.screen_size
        self.repulsion = 1000000
        self.attraction = 2
        self.timestep = 0.15
        self.damping = 0.5
        self.min_spring_distance = 350

    # def adjust_positions(self, nodes_list):
    #     for node in nodes_list:
    #         if node.static == True:
    #             continue
    #         net_force = (0,0)
    #
    #         for other in nodes_list:
    #             if other != node:
    #                 nx, ny = net_force
    #                 cx, cy = self.coulomb_repulsion(node, other)
    #                 net_force = (nx + cx, ny + cy)
    #
    #         for connection in node.incoming:
    #             nx, ny = net_force
    #             hx, hy = self.hooke_attraction(node, connection.sender)
    #             net_force = (nx + hx, ny + hy)
    #
    #         temp = mul_t_constant(net_force, self.timestep)
    #         node.velocity = mul_t_constant(add_t(node.velocity, temp), self.damping)
    #         node.position = add_t(node.position, mul_t_constant(node.velocity, self.timestep))
    #
    #     return nodes_list

    # def hooke_attraction(self, node, other):
    #     distance = self.find_distance(node, other)
    #     angle = self.angle(node, other)
    #
    #     force = -self.attraction * (distance - self.min_spring_distance)
    #
    #     x = math.cos(angle) * force
    #     y = math.sin(angle) * force
    #     return (x, y)
    #
    # def coulomb_repulsion(self, node, other):
    #     distance = self.find_distance(node, other)
    #     angle = self.angle(node, other)
    #
    #     try:
    #         force = (self.repulsion * node.charge * other.charge) / (distance**2)
    #     except ZeroDivisionError:
    #         force = 0
    #
    #     x = math.cos(angle) * force
    #     y = math.sin(angle) * force
    #     return (x, y)
    #
    # def delta(self, node, other):
    #     return (node.x - other.x, node.y - other.y)
    #
    # def find_distance(self, node, other):
    #     delta_x, delta_y = self.delta(node, other)
    #     distance = math.hypot(delta_x, delta_y)
    #     return distance
    #
    # def angle(self, node, other):
    #     delta_x, delta_y = self.delta(node, other)
    #     return math.atan2(delta_y, delta_x)
    #
    # # Sets the initial activation values for the network
    # def set_activations(self, activations):
    #     for node in self.nodes:
    #         node.activation = activations[self.nodes.index(node)]
    #     self.set_colors()
    #     return self.nodes
    #
    # def set_colors(self):
    #     for node in self.nodes:
    #         if node.activation == 1:
    #             node.node_color = (0,255,0)
    #         else:
    #             node.node_color = (255,0,0)

    # Connect each node in each layer to every node in next layer
    def connect_nodes(self):
        for i in range(len(self.layers) - 1):
            for node in self.layers[i].nodes:
                if self.layers[i + 1].output_layer:
                    for other in self.layers[i + 1].nodes:
                        self.connections.append(Connection(recipient=other, sender=node))
                else:
                    for j in range(len(self.layers[i + 1].nodes) - 1):
                        self.connections.append(Connection(recipient=self.layers[i + 1].nodes[j], sender=node))

        # for conn in self.connections:
        #     conn.reveal()
    def reveal_network(self):
        for conn in self.connections:
            conn.reveal()

    # Feed training pattern to network
    def feed_forward(self):
        for i in range(len(self.layers) - 1):
            self.update_all_activations(self.layers[i + 1])

    # Propagate errors backward through network
    def back_prop(self):
        #  Propagate errors backward through net based on output errors (Gradient Descent)
        for i in range(len(self.layers)):
            if not self.layers[-i].output_layer:
                self.calc_errors(self.layers[-i])

    def set_activations(self, pattern):
        for i in range(len(self.layers[0].nodes) - 1):
            self.layers[0].nodes[i].activation = float(pattern[i])

    def reveal_input(self):
        for node in self.layers[0].nodes:
            print "Node %d:" %(node.index + 1), node.activation

    # Train the network based on Backpropagation algorithm
    def train(self, sets, desired_outputs):
        epoch = 0
        while True:
            epoch += 1
            for training_set in sets:
                for category, desired_output in zip(training_set, desired_outputs):
                    for pattern in category:
                        self.set_activations(pattern)
                        # print "\n"
                        self.feed_forward()
                        self.calc_output_errors(desired_output)
                        self.back_prop()
                self.update_weights()

            self.calculate_global_error()
            print "Epoch %d Error:" %(epoch), self.global_error
            if self.global_error < 0.02 or epoch == 100:
                break
            else:
                self.global_error = 0.0

    # Update all of the activations in the network
    def update_all_activations(self, layer):
        for node in layer.nodes:
            node.update_input()
            node.update_activation()

    # Calculate the error for the output layer (based on discrepancy between original patterns and settled activations)
    def calc_output_errors(self, desired):
        for node in self.layers[-1].nodes:
            node.error = (desired[node.index] - node.activation) * node.activation * (1.0 - node.activation)
            self.accumulate_delta(node)

    # Determine the errors for hidden layer nodes
    def calc_errors(self, layer):
        for node in layer.nodes:
            node.calc_error()
            self.accumulate_delta(node)

    # Calculate the change in weight based on error and learning rate
    def delta_weight(self, conn):
        conn.delta_weight = self.learning_rate * (conn.recipient.error *  conn.sender.activation)

    def accumulate_delta(self, node):
        for conn in node.incoming:
            self.delta_weight(conn)

    # Update each weight with the change in weight
    def update_weights(self):
        for conn in self.connections:
            conn.weight += conn.delta_weight
            conn.delta_weight *= 0.5

    # Calculate the error of the entire network
    def calculate_global_error(self):
        for node in self.layers[-1].nodes:
            self.global_error += (node.error)**2

    # Calculate the inputs for all of the nodes in the network
    def set_inputs(self):
        for node in self.nodes:
            node.update_input()

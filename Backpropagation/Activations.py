# @author Artur Sak (sak2)

from Structures import *

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
    def __init__(self, nodes_per_layer):
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

    def reveal_network(self):
        for conn in self.connections:
            conn.reveal()

    # Feed training pattern to network
    def feed_forward(self):
        for i in range(len(self.layers) - 1):
            self.update_all_nodes(self.layers[i + 1])

    # Propagate errors backward through network
    def back_prop(self):
        #  Propagate errors backward through net based on output errors (Gradient Descent)
        for i in range(1, len(self.layers) - 1):
            if not self.layers[-i].output_layer:
                self.calc_errors(self.layers[-i])

    def impose_pattern(self, pattern):
        for i in range(len(self.layers[0].nodes) - 1):
            self.layers[0].nodes[i].activation = float(pattern[i])

    def reveal_input(self):
        for node in self.layers[0].nodes:
            print "Node %d:" %(node.index + 1), node.activation

    # Train the network based on Backpropagation algorithm
    def train(self, training_set, desired_outputs):
        epoch = 0
        while True:
            epoch += 1
            for category, desired_output in zip(training_set, desired_outputs):
                for pattern in category:
                    # self.global_error = 0.0
                    self.impose_pattern(pattern)
                    self.feed_forward()
                    self.calc_output_errors(desired_output)
                    self.calculate_global_error()
                    self.back_prop()
            self.update_weights()
            # self.calculate_global_error()
            # print "Epoch %d Error:" %(epoch), self.global_error
            if self.global_error <= 0.01 or epoch == 10000:
                break
            else:
                self.global_error = 0.0
        # print "Epochs to settle: ", epoch

    def test(self, pattern):
        self.impose_pattern(pattern)
        self.feed_forward()
        self.reveal_outputs()

    def reveal_outputs(self):
        # store = []
        for node in self.layers[-1].nodes:
            # store.append(node.activation)
            print "Node %d Activation: " %(node.index + 1), node.activation
        print "\n"
        # print store
    # Update all of the inputs and activations in the layer
    def update_all_nodes(self, layer):
        for node in layer.nodes:
            node.update_input()
            node.update_activation()

    # Calculate the error for the output layer (based on discrepancy between original patterns and settled activations)
    def calc_output_errors(self, desired):
        for node in self.layers[-1].nodes:
            node.unmodifed_error = (desired[node.index] - node.activation)
            node.error = (desired[node.index] - node.activation) * node.activation * (1.0 - node.activation)
            self.accumulate_delta(node)

    # Determine the errors for hidden layer nodes
    def calc_errors(self, layer):
        for node in layer.nodes:
            node.calc_error()
            self.accumulate_delta(node)

    # Calculate the change in weight based on error and learning rate
    def delta_weight(self, conn):
        conn.delta_weight += self.learning_rate * (conn.recipient.error *  conn.sender.activation)

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
            self.global_error += (node.unmodifed_error)**2

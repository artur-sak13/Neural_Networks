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
        # for layer in self.layers:
        #     for node in layer.nodes:
        #         node.info()
        #     print "\n"

    # Move up the layers and update input and activation of each node
    def feed_forward(self):
        for i in range(len(self.layers) - 1):
            self.update_all_nodes(self.layers[i + 1])

    # Propagate errors backward through network
    def back_prop(self):
        #  Propagate errors backward through net based on output errors (Gradient Descent)
        for i in range(1, len(self.layers)):
            if not self.layers[-i].output_layer:
                self.calc_errors(self.layers[-i])

    # Set the input layer activations
    def impose_pattern(self, pattern):
        for i in range(len(self.layers[0].nodes) - 1):
            self.layers[0].nodes[i].activation = float(pattern[i])

    # Show the activations of the nodes in the input layer
    def reveal_input(self):
        for node in self.layers[0].nodes:
            print "Node %d:" %(node.index + 1), node.activation

    # Train the network based on Backpropagation algorithm
    def train(self, training_set, desired_outputs):
        epoch = 0
        while True:
            epoch += 1
            # for category, desired_output in zip(training_set, desired_outputs):
            for i in range(len(training_set)):
                for pattern in training_set[i]:
                    self.impose_pattern(pattern)
                    self.feed_forward()
                    self.calc_output_errors(desired_outputs[i])
                    self.calculate_global_error()
                    self.back_prop()
            self.update_weights()
            if self.global_error <= 0.2 or epoch == 10000:
                break
            else:
                self.global_error = 0.0
        print "Epochs to settle: ", epoch, "\n"
        print "Ex-anti Error: ", self.global_error, "\n"


    # Alternate training method for the 8:3:8 encoder
    def train_encoder(self, patterns, desired_outputs):
        epoch = 0
        while True:
            epoch += 1
            for pattern, desired_output in zip(patterns, desired_outputs):
                self.impose_pattern(pattern)
                self.feed_forward()
                self.calc_output_errors(desired_output)
                self.calculate_global_error()
                self.back_prop()
            self.update_weights()
            if self.global_error <= 0.01 or epoch == 10000:
                break
            else:
                self.global_error = 0.0

        print "Epochs to settle: ", epoch, "\n"
        print "Ex-anti Error: ", self.global_error, "\n"

    # Test the network's ability to categorize
    def test(self, pattern, desired):
        self.impose_pattern(pattern)
        self.feed_forward()
        self.global_error = 0.0
        self.calc_output_errors(desired)
        self.calculate_global_error()
        print "Global Error: %s \n" %(self.global_error)
        self.reveal_outputs()

    # Show the output layer activation
    def reveal_outputs(self):
        for node in self.layers[-1].nodes:
            print "Node %d Activation: " %(node.index + 1), node.activation
        print "\n"

    # Update all of the inputs and activations in the layer
    def update_all_nodes(self, layer):
        for node in layer.nodes:
            node.update_input()
            node.update_activation()

    # Calculate the error for the output layer (based on discrepancy between original patterns and settled activations)
    def calc_output_errors(self, desired):
        for node in self.layers[-1].nodes:
            node.unmodifed_error = (desired[node.index] - node.activation)
            node.error = node.unmodifed_error * node.activation * (1.0 - node.activation)
            self.accumulate_delta(node)

    # Determine the errors for hidden layer nodes
    def calc_errors(self, layer):
        for node in layer.nodes:
            node.calc_error()
            self.accumulate_delta(node)

    # Calculate the change in weight based on error and learning rate
    def calc_delta(self, conn):
        conn.delta_weight += self.learning_rate * (conn.recipient.error *  conn.sender.activation)

    # Aggregate the deltas per epoch
    def accumulate_delta(self, node):
        for conn in node.incoming:
            self.calc_delta(conn)

    # Update each weight with the change in weight
    def update_weights(self):
        for conn in self.connections:
            conn.weight += conn.delta_weight
            conn.delta_weight *= 0.5

    # Calculate the error of the entire network (output level)
    def calculate_global_error(self):
        for node in self.layers[-1].nodes:
            self.global_error += (node.unmodifed_error)**2

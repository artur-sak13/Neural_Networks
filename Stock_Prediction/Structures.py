# @author Artur Sak (sak2)

import math, random

class Connection(object):
    # Default connection constructor with optional parameters
    def __init__(self, recipient = None, sender = None, weight = 0.0):
        self.recipient = recipient
        self.sender = sender
        self.weight = 2.0 * (random.random() - 0.5)
        self.delta_weight = 0.0

        if self.sender:
            self.sender.outgoing.append(self)
        if self.recipient:
            self.recipient.incoming.append(self)

    def reveal(self):
        print "Connection from ",str(self.sender.index + 1)," to ",str(self.recipient.index)," = %.2f" %self.delta_weight

class Unit(object):
    # Default unit constructor with optional parameters
    def __init__(self, layer, index=0, bias_node=False):
        self.input = 0.0
        self.layer = layer
        self.index = index
        self.bias_node = bias_node
        if self.bias_node:
            self.activation = 1.0
        else:
            self.activation = 0.0
        self.error = 0.0
        self.unmodifed_error = 0.0

        self.incoming = []
        self.outgoing = []

    def info(self):
        print "Node %s: " %(self.index), " with activtion ", self.activation

    # Function resets the net input based on adjacent nodes' connection weights and activations
    def update_input(self):
        self.input = 0.0
        for connection in self.incoming:
            self.input += connection.weight * connection.sender.activation

    def calc_error(self):
        self.error = 0.0
        for connection in self.outgoing:
            self.error += connection.weight * connection.recipient.error
        self.error *= (self.activation * (1.0 - self.activation))

    # Sigmoid function
    def update_activation(self):
        if self.bias_node:
            self.activation = 1.0
        else:
            self.activation = 1.0 / (1.0 + math.exp(-self.input))

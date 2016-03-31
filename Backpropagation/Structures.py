# @author Artur Sak (sak2)

import math, random
# import pygame

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
        # print "HI!"
        print "Connection from ",str(self.sender.index)," to ",str(self.recipient.index)," = %.2f" %self.weight

class Unit(object):
    # Default unit constructor with optional parameters
    def __init__(self, layer, index=0, bias_node=False, position = None, mass = 1, x_range=(0,800), y_range=(0,800)):
        self.input = 0.0
        self.activation = 0.0
        self.layer = layer
        self.index = index
        self.bias_node = bias_node
        self.error = 0.0
        self.node_color = (255,100,0)

        self.incoming = []
        self.outgoing = []

        # Node positions for PyGame Visuals
        self._position = (0,0)
        self.x_range = x_range
        self.y_range = y_range

        if not position:
            xmin, xmax = x_range
            ymin, ymax = y_range
            self.position = (random.randint(xmin, xmax), random.randint(ymin,ymax))
        else:
            self.position = position
        # Physical attributes added for visualization
        self.charge = 1
        self.velocity = (0,0)
        self.mass = mass
        self.static = False

    def _get_position(self):
        return self._position
    def _set_position(self, value):
        self.x, self.y = value
    position = property(_get_position, _set_position)

    def _get_x(self):
        x, y = self._position
        return x
    def _set_x(self, value):
        x, y = self._position
        self._position = (value, y)
    x = property(_get_x, _set_x)

    def _get_y(self):
        x, y = self._position
        return y
    def _set_y(self, value):
        x, y = self._position
        self._position = (x, value)
    y = property(_get_y, _set_y)

    def _get_rect(self):
        return pygame.Rect(self.x - 5, self.y - 5, 10, 10)
    rect = property(_get_rect)

    # Function resets the net input based on adjacent nodes' connection weights and activations
    def update_input(self):
        self.input = 0.0
        for connection in self.incoming:
            self.input += connection.weight * connection.sender.activation

    def calc_error(self):
        self.error = 0.0
        for connection in self.outgoing:
            self.error += connection.weight * connection.recipient.error
        self.error *= (self.activation * (1 - self.activation))

    # Sigmoid function
    def update_activation(self):
        if self.bias_node:
            self.activation = 1.0
        else:
            self.activation = 1.0 / (1.0 + math.exp(-self.input))

# @author Artur Sak (sak2)

import math
import random
import pygame

class Connection(object):
    # Default connection constructor with optional parameters
    def __init__(self, recipient = None, sender = None, weight = 0.0):
        self.recipient = recipient
        self.sender = sender
        self.weight = weight

    # Implements Hopfield Learning Algorithm
    def learn(self):
        if self.sender.activation == self.recipient.activation:
            self.weight += 1
        else:
            self.weight -= 1

class Unit(object):
    # Default unit constructor with optional parameters
    def __init__(self, input = 0.0, activation = 0.0, incoming = None, position = None, mass = 1, x_range=(0,800), y_range=(0,800)):
        self.input = input
        self.activation = activation
        self.threshold = 0.0
        if incoming is None:
            self.incoming = []
        else:
            self.incoming = incoming
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

    # Function updates a node's activation value based on changed net input value
    def update_activation(self):
        if self.input > self.threshold:
            self.activation = 1.0
        else:
            self.activation = 0.0

    # Logistic activation function
    def logistic_activation(self, temperature=0.0):
            self.activation = 1 / (1 + math.e**(-self.input/temperature))

    # Linear activation function
    def linear_activaton(self):
        self.activation = self.input - 0.5

    # Conditional Activation function
    def conditional_activation(self):
        if self.input > 1.0:
            self.activation = 1.0
        elif self.input < 0.75:
            self.activation = 0.0
        else:
            self.activation = float(self.input)

    # Function implements three different temporal integrator activation functions
    def temporal_integrator(self, gamma=None, delta=None, inhibit=None):
        # Simple temporal integrator
        if delta == None and inhibit == None:
            delta_act = gamma * (1.0 - self.activation) * self.input
        else:
            # Grossberg activation function
            if inhibit != None:
                delta_act = gamma * ((self.input + inhibit) * (1.0 - self.activation) - (1.0 + self.activation) * inhibit) - (delta * self.activation)
            # Leaky integrator
            else:
                delta_act = (gamma*(1.0 - self.activation)*self.input) - (delta * self.activation)
        self.activation += delta_act

    # Creates connection
    def add_neighbor(self, connection):
        self.incoming.append(connection)

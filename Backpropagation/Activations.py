# @author Artur Sak (sak2)

from Structures import *

def add_t(*tuples):
    return tuple(sum(x) for x in zip(*tuples))

def mul_t_constant(t, constant):
    return tuple(x * constant for x in t)

class Layer(object):
    def __init__(self, num_nodes, index, bias_node = True, output_layer = False)
    self.nodes = []
    self.index = index
    self.has_bias_node = has_bias_node
    self.output_layer = output_layer

    for i in xrange(num_nodes):
        self.nodes.append(Unit(i))
    if self.has_bias_node:
        self.nodes.append(Unit(num_nodes, True))

class Network(object):
    def __init__(self, nodes_per_layer, screen_size):
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

    def connect_nodes(self):
        pass

    def forward_prop(self):
        pass

    def back_prop(self):
        pass

    def train(self):
        pass

    # Update all of the activations in the network
    def update_all_activations(self, i = None):
        for node in self.nodes:
            node.update_activation()

    # Calculate the inputs for all of the nodes in the network
    def set_inputs(self, const=None):
        if const:
            for node in self.nodes:
                node.input = const
        else:
            for node in self.nodes:
                node.update_input()

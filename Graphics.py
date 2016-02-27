import sys
import pygame
import random
import math

from Hopfield import *

class Graphics(object):
    def __init__(self, size=(500,500), caption="Hopfield Network"):
        self.size = size
        self.caption = caption
        self.node_radius = 10
        self.node_color = (255,0,0)
        self.line_color = (255,255,255)
        self.screen_color = (0,0,0)

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)

    def draw_graph(self, nodes):
        self.screen.fill(self.screen_color)
        self.draw_lines(nodes)
        self.draw_nodes(nodes)

    def draw_lines(self, nodes):
        for node in nodes:
            for connection in node.incoming:
                pygame.draw.aaline(
                    self.screen,
                    self.line_color,
                    node.position,
                    connection.sender.position,
                    1)

    def draw_nodes(self, nodes):
        for node in nodes:
            intpos = (int(node.position[0]), int(node.position[1]))
            pygame.draw.circle(
                self.screen,
                self.node_color,
                intpos,
                self.node_radius,
                0)

    def render_screen(self):
        pygame.display.flip()

    def mainloop(self, nodes):
        is_running = True
        is_frozen = False
        move = False
        is_node_selected = False
        selected_node = None

        grapher = Hopfield(16, self.size)
        font = pygame.font.Font(None, 20)

        while is_running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                sys.exit(0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f: # freeze.
                    move = not move
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_node_selected == False:
                    for n in nodes:
                        if n.rect.collidepoint(event.pos):
                            is_node_selected = True
                            selected_node = n
                            selected_node.static = True
                            break
            if event.type == pygame.MOUSEMOTION:
                if is_node_selected:
                    selected_node.position = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if is_node_selected:
                    is_node_selected = False
                    selected_node.static = False
                    selected_node = None
            if not move:
                nodes = grapher.adjust_positions(nodes)
                self.draw_graph(nodes)
                self.render_screen()

            if is_frozen == False:
                self.draw_graph(nodes)
                self.render_screen()


size = (1000,700)
net = Hopfield(16,size)
for node in net.nodes:
    print len(node.incoming)
screen = Graphics(size=size)
screen.draw_graph(net.nodes)
screen.mainloop(net.nodes)

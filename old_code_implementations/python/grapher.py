# holds a graph and graphs the nodes to it.

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import logging

from committee_handler import committee_handler

def graph_tree(h: committee_handler, committees: dict):  # dict of committees
    logging.warning('generating image...')
    G = nx.Graph()
    edge_labels = {}
    colour_map = []
    for node in committees.values():
        if node.colour == 0:
            colour_map.append('red')
        elif node.colour == 1:
            colour_map.append('blue')
            G.add_edge(str(node), str(node.parent))
            edge_labels[str(node)] = node.reached_by

        else:
            colour_map.append('green')
            G.add_edge(str(node), str(node.parent))
            edge_labels[str(node)] = node.reached_by
        G.add_node(str(node))
    
    pos = graphviz_layout(G)
    labels = nx.draw_networkx_labels(G, pos = pos
        )
    nx.draw(G, pos = pos, labels = labels)

    plt.savefig('graph.png')
    logging.warning('Done!')

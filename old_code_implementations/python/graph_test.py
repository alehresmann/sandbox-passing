import networkx as nx
import matplotlib.pyplot as plt
from networkx.generators.small import krackhardt_kite_graph
from string import ascii_lowercase

G = krackhardt_kite_graph()
pos=nx.spring_layout(G)
labels = {}
for idx, node in enumerate(G.nodes()):
    labels[node] = 'dsfasdfasdfasdfas'

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, labels, font_size=16)
plt.show()

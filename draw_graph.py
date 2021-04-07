import networkx as nx
import matplotlib.pyplot as plt
from problem import *

# G = nx.DiGraph(directed=True)
# G.add_edges_from(
#     [('A', 'B'), ('A', 'C'), ('C', 'A'), ('D', 'B'), ('E', 'C'), ('E', 'F'), ('F', 'E'),
#      ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])
#
# # val_map = {'A': 1.0,
# #            'D': 0.5714285714285714,
# #            'H': 0.0}
# #
# # values = [val_map.get(node, 0.25) for node in G.nodes()]
#
# # Specify the edges you want here
# red_edges = [('A', 'C'), ('E', 'C')]
# edge_colours = ['black' if not edge in red_edges else 'red'
#                 for edge in G.edges()]
# black_edges = [edge for edge in G.edges() if edge not in red_edges]
#
# # arrows options
# options = {
#     'node_color': 'blue',
#     'node_size': 100,
#     'width': 3,
#     'arrowstyle': '-|>',
#     'arrowsize': 12,
# }
#
# # Need to create a layout when doing
# # separate calls to draw nodes and edges
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, arrows=True, **options, cmap=plt.get_cmap('jet'))
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
# nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
# plt.show()

graph = [(1, 2), (2, 3), (3, 4), (4, 5), (2, 1), (3, 2), (4, 3), (5, 4)]
variables = ['nationality', 'colour', 'drink', 'tobacco', 'animals']
domain = [1, 2, 3, 4, 5]
domains = domain * len(variables)
constraints = []
problem = Problem(graph, variables, domains, constraints)
sol = Solution(5)

G = nx.DiGraph(directed=True)
G.add_edges_from(
    problem.graph)
G.nodes[2]["colour"] = 'Red'
G.nodes[2]["animals"] = 'cats'



# Specify the edges you want here
black_edges = [edge for edge in G.edges()]

# arrows options
options = {
    # 'node_color': 'blue',
    'node_size': 500,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 150,
    'data': True,
}

print(list(G.nodes(data=True)))
labels = nx.get_node_attributes(G, 'colour')
# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, labels=labels, arrows=True, **options, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos, labels=labels)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
plt.show()

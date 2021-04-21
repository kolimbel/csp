#from einsteins_puzzle import *
from random_graph import *
from problem import *
#from map_coloring import *

# ep = EinsteinsPuzzle()
# for i in range(ep.matrix.shape[0]):
#     for j in range(ep.matrix.shape[1]):
#         ep.set_matrix_value(i, j, j)
#
# ep.print_solution()

# eps = EinsteinsPuzzleSolutions()
# print('utworzono obiekt EPS')
# temp_ep = EinsteinsPuzzle()
# eps.find_solution(0, 0 , temp_ep)
# print('zakonczono metode fnd_solutions()')
# eps.print_solutions()



random_graph = Graph(10, 10, 4)
G = nx.DiGraph(directed=True)
nodes, positions = random_graph.get_nodes()
for i in range(len(nodes)):
    G.add_node(nodes[i], pos=positions[i])
G.add_edges_from(random_graph.get_tuples())

black_edges = [edge for edge in G.edges()]

color_map = []
pos_map = []
# for node in G:
#     try:
#         color = self.map_graph_bt[str(node)]
#     except:
#         raise Exception('bledny kolor {}'.format([node, str(node)]))
#     color_map.append(color)

# arrows options
options = {
    'node_size': 500,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 10,
}

pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, node_color='grey', arrows=True, **options, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
plt.show(block=True)


# print(random_graph.strgraph)

# mc = MapColoring(30, 30, 8)
# mc.map_backtracking(k=4)
# mc.show_map()
#
# ep = EinsteinsPuzzle()
# ep.show_graph()

#plt.close('all')


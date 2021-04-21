from problem import *
from timeit import default_timer as timer
from datetime import timedelta


class MapColoring:
    def __init__(self, size_x, size_y, number_of_points):
        self.graph = Graph(size_x, size_y, number_of_points)
        self.map_graph_bt = None
        self.borders = None
        self.bindings = self.graph.strgraph

    def map_coloring(self, k):
        if k == 3:
            #print('3 kolory')
            colors = ['tomato', 'limegreen', 'lightskyblue']
        elif k == 4:
            #print('4 kolory')
            colors = ['tomato', 'limegreen', 'lightskyblue', 'yellow']
        else:
            raise Exception('parametr k moze przyjac wartosc tylko 3 albo 4')
        self.borders = self.bindings_to_dic()
        border_list = []
        for i in self.borders:
            border_list.append(i)
        domains = StaticDictionary(colors)
        return Problem(border_list, domains, self.borders, self.diff_values_const)

    def diff_values_const(self, fst_country, fst_color, snd_country, snd_color):
        if fst_country == snd_country:
            raise Exception('bledne porownanie')
        else:
            return fst_color != snd_color

    def bindings_to_dic(self):
        dictionary = {}
        splitted = []
        for sp in self.bindings.split(';'):
            s = sp.split(':')
            splitted.append(s)
        for (node, neighs) in splitted:
            node = node.strip()
            for Bin in neighs.split():
                try:
                    dictionary[node].append(Bin)
                except:
                    dictionary[node] = []
                    dictionary[node].append(Bin)
        return dictionary

    def map_backtracking(self, k, fc=False, fst_domain=True, mrv=False):
        map_graph_csp = self.map_coloring(k)
        time_start = timer()
        self.map_graph_bt = backtracking_search(map_graph_csp, fc=fc, fst_domain=fst_domain, mrv=mrv)
        time_end = timer()
        elapsed_time = timedelta(seconds=time_end-time_start)
        print('Visited = {}'.format(map_graph_csp.visited) + ' ; Time = {}'.format(elapsed_time))
        if self.map_graph_bt is None:
            raise Exception(
                'nie znaleziono rozwiąznia')  # TODO: zamiast tego ponowic dla nowego grafu i zapisac info o braku rozwiazania

    def show_map(self):
        G = nx.DiGraph(directed=True)
        nodes, positions = self.graph.get_nodes()
        for i in range(len(nodes)):
            G.add_node(nodes[i], pos=positions[i])
        G.add_edges_from(self.graph.get_tuples())

        black_edges = [edge for edge in G.edges()]

        color_map = []
        pos_map = []
        for node in G:
            try:
                color = self.map_graph_bt[str(node)]
            except:
                raise Exception('bledny kolor {}'.format([node, str(node)]))
            color_map.append(color)

        # arrows options
        options = {
            'node_size': 500,
            'width': 3,
            'arrowstyle': '-|>',
            'arrowsize': 10,
        }

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx_nodes(G, pos, node_color=color_map, arrows=True, **options, cmap=plt.get_cmap('jet'))
        nx.draw_networkx_labels(G, pos, font_size=8)
        nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
        plt.show(block=True)

        # plt.close('all')
class StaticDictionary:
    def __init__(self, value):
        self.value = value
    def __getitem__(self, k):
        return self.value



mc0 = MapColoring(100, 100, 10)
mc1 = copy.deepcopy(mc0)
print('without BT:')
mc0.map_backtracking(k=4, fst_domain=True, mrv=False, fc=False)
#mc0.show_map()
print('with FC:')
mc1.map_backtracking(k=4, fst_domain=True, mrv=False, fc=True)
#mc1.show_map()

# mc = MapColoring(20, 50, 15)
# mc.map_backtracking(k=4, fc=True)
# mc.show_map()
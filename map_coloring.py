from problem import *


class MapColoring:
    def __init__(self, size_x, size_y, number_of_points):
        self.graph = Graph(size_x, size_y, number_of_points)
        self.map_graph_bt = None
        self.borders = None
        self.bindings = self.graph.strgraph

    def map_coloring(self, k):
        """Make a CSP for the problem of coloring a map with different colors
        for any two adjacent regions. Arguments are a list of colors, and a
        dict of {region: [neighbor,...]} entries. This dict may also be
        specified as a string of the form defined by parse_neighbors."""
        if k == 3:
            colors = ['tomato', 'limegreen', 'lightskyblue']
        elif k == 4:
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
        """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
        regions to neighbors. The syntax is a region name followed by a ':'
        followed by zero or more region names, followed by ';', repeated for
        each region name. If you say 'X: Y' you don't need 'Y: X'.
        >>> bindings_to_dic('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
        True
        """
        dictionary = {}
        splitted = []
        for sp in self.bindings.split(';'):
            s = sp.split(':')
            splitted.append(s)
        for (BinMain, BinBindings) in splitted:
            BinMain = BinMain.strip()
            for Bin in BinBindings.split():
                try:
                    dictionary[BinMain].append(Bin)
                except:
                    dictionary[BinMain] = []
                    dictionary[BinMain].append(Bin)
                try:
                    dictionary[Bin].append(BinMain)
                except:
                    dictionary[Bin] = []
                    dictionary[Bin].append(BinMain)
        return dictionary

    def map_backtracking(self, k=3):
        map_graph_csp = self.map_coloring(k)
        # print(map_graph_csp)
        self.map_graph_bt = backtracking_search(map_graph_csp, fc=True)
        # print(map_graph_bt)

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

    def __getitem__(self, key):
        return self.value

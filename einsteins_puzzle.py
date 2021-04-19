import numpy as np
from problem import *


class EinsteinsPuzzle:
    def __init__(self):
        self.nationality = ['anglik', 'dunczyk', 'niemiec', 'norweg', 'szwed']
        self.color = ['bialy', 'czerwony', 'niebieski', 'zielony', 'zolty']
        self.drink = ['herbata', 'kawa', 'mleko', 'piwo', 'woda']
        self.tobacco = ['cygara', 'fajka', 'bfiltra', 'light', 'mentolowe']
        self.animal = ['konie', 'koty', 'psy', 'ptaki', 'rybki']
        self.bt = backtracking_search(self.einsteins_puzzle(), fc=False, fst_domain=True, mrv=False)

    def diff_categories_ep(self, fst_var, fst_house_number, snd_var, snd_house_number):
        diff_categories = True
        if ((fst_var in self.nationality and snd_var in self.nationality) or
                (fst_var in self.color and snd_var in self.color) or
                (fst_var in self.drink and snd_var in self.drink) or
                (fst_var in self.tobacco and snd_var in self.tobacco) or
                (fst_var in self.animal and snd_var in self.animal)):
            diff_categories = False
        #
        #
        if diff_categories is False:
            return not (fst_house_number == snd_house_number)
        else:
            pass

    def ep_constraints(self, fst_var, fst_house_number, snd_var, snd_house_number):
        vars_const = set([])
        vars_const.add(fst_var)
        vars_const.add(snd_var)

        def contains(var1, var2):
            return vars_const.__contains__(var1) and vars_const.__contains__(var2)

        if contains('anglik', 'czerwony'):  # 2. Anglik mieszka w czerwonym domu.
            return fst_house_number == snd_house_number
        if contains('bialy',
                    'zielony'):  # 3. Zielony dom znajduje się bezpośrednio po lewej stronie domu białego.
            return fst_house_number + 1 == snd_house_number  # or fst_house_number - 1 == snd_house_number
        if contains('dunczyk', 'herbata'):  # 4. Duńczyk pija herbatkę.
            return fst_house_number == snd_house_number
        if contains('light', 'koty'):  # 5. Palacz papierosów light mieszka obok hodowcy kotów.
            return abs(fst_house_number - snd_house_number) == 1
        if contains('zolty', 'cygara'):  # 6. Mieszkaniec żółtego domu pali cygara.
            return fst_house_number == snd_house_number
        if contains('niemiec', 'fajka'):  # 7. Niemiec pali fajkę.
            return fst_house_number == snd_house_number
        if contains('light', 'woda'):  # 9. Palacz papierosów light ma sąsiada, który pija wodę.
            return abs(fst_house_number - snd_house_number) == 1
        if contains('bfiltra', 'ptaki'):  # 10. Palacz papierosów bez filtra hoduje ptaki.
            return fst_house_number == snd_house_number
        if contains('szwed', 'psy'):  # 11. Szwed hoduje psy.
            return fst_house_number == snd_house_number
        if contains('norweg', 'niebieski'):  # 12. Norweg mieszka obok niebieskiego domu.
            return abs(fst_house_number - snd_house_number) == 1
        if contains('zolty', 'konie'):  # 13. Hodowca koni mieszka obok żółtego domu.
            return abs(fst_house_number - snd_house_number) == 1
        if contains('mentolowe', 'piwo'):  # 14. Palacz mentolowych pija piwo.
            return fst_house_number == snd_house_number
        if contains('zielony', 'kawa'):  # 15. W zielonym domu pija się kawę.
            return fst_house_number == snd_house_number

        return self.diff_categories_ep(fst_var, fst_house_number, snd_var, snd_house_number)

    def einsteins_puzzle(self):
        variables = [*self.nationality, *self.color, *self.drink, *self.tobacco, *self.animal]
        domains = {}
        houses = [1, 2, 3, 4, 5]
        for var in variables:
            domains[var] = houses
        domains['norweg'] = [1]  # 1. Norweg zamieszkuje pierwszy dom
        domains['mleko'] = [3]  # 8. Mieszkaniec środkowego domu pija mleko.
        bindings = {
            'anglik': ['czerwony', 'dunczyk', 'niemiec', 'norweg', 'szwed'],
            'dunczyk': ['herbata', 'anglik', 'niemiec', 'norweg', 'szwed'],
            'niemiec': ['fajka', 'anglik', 'dunczyk', 'norweg', 'szwed'],
            'norweg': ['niebieski', 'anglik', 'dunczyk', 'niemiec', 'szwed'],
            'szwed': ['psy', 'anglik', 'dunczyk', 'niemiec', 'norweg'],

            'bialy': ['zielony', 'czerwony', 'niebieski', 'zolty'],
            'czerwony': ['anglik', 'bialy', 'niebieski', 'zielony', 'zolty'],
            'niebieski': ['norweg', 'bialy', 'czerwony', 'zielony', 'zolty'],
            'zielony': ['bialy', 'kawa', 'czerwony', 'niebieski', 'zolty'],
            'zolty': ['konie', 'cygara', 'bialy', 'czerwony', 'niebieski', 'zielony'],

            'herbata': ['dunczyk', 'kawa', 'mleko', 'piwo', 'woda'],
            'kawa': ['zielony', 'herbata', 'mleko', 'piwo', 'woda'],
            'mleko': ['herbata', 'kawa', 'piwo', 'woda'],
            'piwo': ['mentolowe', 'herbata', 'kawa', 'mleko', 'woda'],
            'woda': ['light', 'herbata', 'kawa', 'mleko', 'piwo'],

            'cygara': ['zolty', 'fajka', 'bfiltra', 'light', 'mentolowe'],
            'fajka': ['niemiec', 'cygara', 'bfiltra', 'light', 'mentolowe'],
            'bfiltra': ['ptaki', 'cygara', 'fajka', 'light', 'mentolowe'],
            'light': ['koty', 'woda', 'cygara', 'fajka', 'bfiltra', 'mentolowe'],
            'mentolowe': ['piwo', 'cygara', 'fajka', 'bfiltra', 'light'],

            'konie': ['zolty', 'koty', 'psy', 'ptaki', 'rybki'],
            'koty': ['light', 'konie', 'psy', 'ptaki', 'rybki'],
            'psy': ['szwed', 'konie', 'koty', 'ptaki', 'rybki'],
            'ptaki': ['bfiltra', 'konie', 'koty', 'psy', 'rybki'],
            'rybki': ['konie', 'koty', 'psy', 'ptaki']}

        return Problem(variables, domains, bindings, self.ep_constraints)

    def show_graph(self):
        z_bt_s = sorted(self.bt.items(), key=lambda item: item[1])
        nodes = {}
        for i in z_bt_s:
            try:
                if 'rybki' in i[0]:
                    nodes[i[1]] += ';\n' + r"$\bf{" + str(i[0] + "}$")
                else:
                    nodes[i[1]] += ';\n' + str(i[0])
            except:
                nodes[i[1]] = str(i[0])

        G = nx.DiGraph(directed=True)
        nodesg = list(nodes.items())
        positionsg = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
        for i in range(len(nodesg)):
            # if 'rybki' in nodesg[i][1]:
            #     G.add_node(nodesg[i][0], pos=positionsg[i], atr=str(nodesg[i][0]) + ':\n ' + nodesg[i][1])
            #     nd = list(G.nodes())[-1]
            #     ndd = G.nodes((nd, 0)) # ['color'] = 'yellow'
            #     brekp =0
            # else:
            G.add_node(nodesg[i][0], pos=positionsg[i], atr=str(nodesg[i][0]) + ':\n ' + nodesg[i][1])
        G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])

        black_edges = [edge for edge in G.edges()]

        # arrows options
        options2 = {
            'node_size': 4500,
            'width': 3,
            'arrowstyle': '-|>',
            'arrowsize': 10,
        }

        pos = nx.get_node_attributes(G, 'pos')
        atr = nx.get_node_attributes(G, 'atr')
        nx.draw_networkx_nodes(G, pos, arrows=True, **options2, cmap=plt.get_cmap('jet'))
        nx.draw_networkx_labels(G, pos, labels=atr, font_size=9)
        nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)

        plt.show(block=True)


ep = EinsteinsPuzzle()
ep.show_graph()

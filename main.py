# from einsteins_puzzle import *

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

from random_graph import *
random_graph = Graph(10, 10, 6)
print(random_graph.strgraph)

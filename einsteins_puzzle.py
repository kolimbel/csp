import numpy as np

# class EinsteinsPuzzleSolutions:
#     def __init__(self):
#         self.matrix = []
#
#     def insert_solution(self, einsteins_puzzle):
#         self.matrix.append(einsteins_puzzle)
#
#     def print_solutions(self):
#         for i in range(len(self.matrix)):
#             self.matrix[i].print_solution()
#
#
#     # def backtracking_search(self, temp_ep):
#     #     return recursive_backtracking(temp_ep)
#
#     def recursive_backtracking(self, temp_ep):
#         if not(99 in temp_ep):
#             self.insert_solution(temp_ep)
#             self.print_solutions()
#
#
#     def find_solution(self, row, col, temp_ep):
#         counter_value = 0
#         len_domain = 5
#         while counter_value < len_domain:
#             if col == 0:
#                 temp_value = temp_ep.nationality[counter_value]
#                 len_domain = len(temp_ep.nationality)
#             elif col == 1:
#                 temp_value = temp_ep.colour[counter_value]
#                 len_domain = len(temp_ep.colour)
#             elif col == 2:
#                 temp_value = temp_ep.drink[counter_value]
#                 len_domain = len(temp_ep.drink)
#             elif col == 3:
#                 temp_value = temp_ep.tobacco[counter_value]
#                 len_domain = len(temp_ep.tobacco)
#             elif col == 4:
#                 temp_value = temp_ep.animals[counter_value]
#                 len_domain = len(temp_ep.animals)
#             else:
#                 raise Exception('brak kolumny')
#
#             temp_ep.set_matrix_value(row, col, temp_value)
#             if temp_ep.verification() is True:
#                 temp_ep.remove_value_from_domain(col, temp_value)
#                 len_domain -= 1
#                 if col == 4:
#                     if self.find_solution(row + 1, 0, temp_ep) is False:
#
#
#                 else:
#                     if self.find_solution(row, col + 1, temp_ep) is False:
#                 if col == 4 and row == 4:
#                     if temp_ep.verification() is True:
#                         self.insert_solution(temp_ep)
#                         return True
#             else:
#                 temp_ep.default_matrix_value(row, col)
#                 counter_value += 1
#
#



# class EinsteinsPuzzle:
# def __init__(self):
#     n = m = 5
#     # self.matrix = [[0 for i in range(n)] for j in range(m)]
#     # self.matrix = [[None] * n for _ in range(m)]
#     self.matrix = np.full((n, m), fill_value=99, dtype=int)
#     self.nationality = list(range(0, 5))
#     self.colour = list(range(0, 5))
#     self.drink = list(range(0, 5))
#     self.tobacco = list(range(0, 5))
#     self.animals = list(range(0, 5))
#
# def set_matrix_value(self, row, col, value):
#     self.matrix[row, col] = value
#     # if col == 0:  # nationality
#     #     self.nationality.remove(value)
#     # elif col == 1:  # colour
#     #     self.colour.remove(value)
#     # elif col == 2:  # drink
#     #     self.drink.remove(value)
#     # elif col == 3:  # tobacco
#     #     self.tobacco.remove(value)
#     # elif col == 4:  #animals
#     #     self.animals.remove(value)
#     # else:
#     #     raise Exception('bledna wartosc [row, col, value] {}'.format([row, col, value]))
#
# def default_matrix_value(self, row, col):
#     self.matrix[row, col] = 99
#     # if col == 0:  # nationality
#     #     self.nationality.insert(-1, value)
#     # elif col == 1:  # colour
#     #     self.colour.insert(-1, value)
#     # elif col == 2:  # drink
#     #     self.drink.insert(-1, value)
#     # elif col == 3:  # tobacco
#     #     self.tobacco.insert(-1, value)
#     # elif col == 4:  # animals
#     #     self.animals.insert(-1, value)
#     # else:
#     #     raise Exception('bledna wartosc [row, col, value] {}'.format([row, col, value]))
#
# def remove_value_from_domain(self, col, value):
#     if col == 0:  # nationality
#         self.nationality.remove(value)
#     elif col == 1:  # colour
#         self.colour.remove(value)
#     elif col == 2:  # drink
#         self.drink.remove(value)
#     elif col == 3:  # tobacco
#         self.tobacco.remove(value)
#     elif col == 4:  #animals
#         self.animals.remove(value)
#     else:
#         raise Exception('bledna wartosc  [col, value]: {}'.format([col, value]))
#
# def print_solution(self):
#     # n = m = 5
#     # np.zeros(n, m)
#     n = self.matrix.shape[0]
#     m = self.matrix.shape[1]
#     print_matrix = np.empty((n, m), dtype='object')
#     print(self.matrix)
#     # for col in range(m):
#     #     if col == 0:  # nationality
#     #         for i in range(n):
#     #             if self.matrix[i, col] == 0:
#     #                 print_matrix[i, col] = 'anglik'
#     #             elif self.matrix[i, col] == 1:
#     #                 print_matrix[i, col] = 'dunczyk'
#     #             elif self.matrix[i, col] == 2:
#     #                 print_matrix[i, col] = 'niemiec'
#     #             elif self.matrix[i, col] == 3:
#     #                 print_matrix[i, col] = 'norweg'
#     #             elif self.matrix[i, col] == 4:
#     #                 print_matrix[i, col] = 'szwed'
#     #             else:
#     #                 raise Exception('bledna wartosc {}'.format(self.matrix[i, col]))
#     #     elif col == 1:  # colour
#     #         for i in range(n):
#     #             if self.matrix[i, col] == 0:
#     #                 print_matrix[i, col] = 'bialy'
#     #             elif self.matrix[i, col] == 1:
#     #                 print_matrix[i, col] = 'czerwony'
#     #             elif self.matrix[i, col] == 2:
#     #                 print_matrix[i, col] = 'niebieski'
#     #             elif self.matrix[i, col] == 3:
#     #                 print_matrix[i, col] = 'zielony'
#     #             elif self.matrix[i, col] == 4:
#     #                 print_matrix[i, col] = 'zolty'
#     #             else:
#     #                 raise Exception('bledna wartosc {}'.format(self.matrix[i, col]))
#     #     elif col == 2:  # drink
#     #         for i in range(n):
#     #             if self.matrix[i, col] == 0:
#     #                 print_matrix[i, col] = 'herbata'
#     #             elif self.matrix[i, col] == 1:
#     #                 print_matrix[i, col] = 'kawa'
#     #             elif self.matrix[i, col] == 2:
#     #                 print_matrix[i, col] = 'mleko'
#     #             elif self.matrix[i, col] == 3:
#     #                 print_matrix[i, col] = 'piwo'
#     #             elif self.matrix[i, col] == 4:
#     #                 print_matrix[i, col] = 'woda'
#     #             else:
#     #                 raise Exception('bledna wartosc {}'.format(self.matrix[i, col]))
#     #     elif col == 3:  # tobacco
#     #         for i in range(n):
#     #             if self.matrix[i, col] == 0:
#     #                 print_matrix[i, col] = 'cyagara'
#     #             elif self.matrix[i, col] == 1:
#     #                 print_matrix[i, col] = 'fajka'
#     #             elif self.matrix[i, col] == 2:
#     #                 print_matrix[i, col] = 'p. bez filtra'
#     #             elif self.matrix[i, col] == 3:
#     #                 print_matrix[i, col] = 'p. light'
#     #             elif self.matrix[i, col] == 4:
#     #                 print_matrix[i, col] = 'p. mentol'
#     #             else:
#     #                 raise Exception('bledna wartosc {}'.format(self.matrix[i, col]))
#     #     elif col == 4:  # animals
#     #         for i in range(n):
#     #             if self.matrix[i, col] == 0:
#     #                 print_matrix[i, col] = 'konie'
#     #             elif self.matrix[i, col] == 1:
#     #                 print_matrix[i, col] = 'koty'
#     #             elif self.matrix[i, col] == 2:
#     #                 print_matrix[i, col] = 'psy'
#     #             elif self.matrix[i, col] == 3:
#     #                 print_matrix[i, col] = 'ptaki'
#     #             elif self.matrix[i, col] == 4:
#     #                 print_matrix[i, col] = 'rybki'
#     #             else:
#     #                 raise Exception('bledna wartosc {}'.format(self.matrix[i, col]))
#     #     else:
#     #         raise Exception('bledny rozmiar macierzy')
#     # print(print_matrix)
#
# def verification(self):
#     result_verification = True
#     matrix = self.matrix # = einsteins_puzzle.matrix
#     n = matrix.shape[0]
#     m = matrix.shape[1]
#
#
#
#     # 1. Norweg zamieszkuje pierwszy dom
#     m00 = matrix[0, 0]
#     if not(m00 == 3 or m00 == 99):
#         result_verification = False
#
#     if result_verification is False:
#         return result_verification
#
#     # 2. Anglik mieszka w czerwonym domu.
#     for i in range(n):
#         if matrix[i, 0] == 0:
#             mi1 = matrix[i, 1]
#             if not(mi1 == 1 or mi1 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 3. Zielony dom znajduje się bezpośrednio po lewej stronie domu białego. (+ zielony nie moze byc ostatni, biały nie moze byc pierwszy)
#     if matrix[0, 1] == 0:
#         result_verification = False
#     if matrix[4, 1] == 3:
#         result_verification = False
#
#     for i in range(n):
#         if matrix[i, 1] == 3:
#             if not(matrix[i + 1, 1] == 0 or matrix[i + 1, 1] == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 4. Duńczyk pija herbatkę.
#     for i in range(n):
#         if matrix[i, 2] == 0:
#             mi0 = matrix[i, 0]
#             if not(mi0 == 1 or mi0 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 5. Palacz papierosów light mieszka obok hodowcy kotów.
#     for i in range(n):
#         if matrix[i, 3] == 3:
#             if i == 0:
#                 if not(matrix[i + 1, 4] == 1 or matrix[i + 1, 4] == 99):
#                     result_verification = False
#             elif i == 4:
#                 if not(matrix[i - 1, 4] == 1 or matrix[i - 1, 4] == 99):
#                     result_verification = False
#             else:
#                 if not(matrix[i + 1, 4] == 1 or matrix[i + 1, 4] == 99):
#                     result_verification = False
#                 elif not(matrix[i - 1, 4] == 1 or matrix[i - 1, 4] == 99):
#                     result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 6. Mieszkaniec żółtego domu pali cygara.
#     for i in range(n):
#         if matrix[i, 1] == 4:
#             mi3 = matrix[i, 3]
#             if not(mi3 == 0 or mi3 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 7. Niemiec pali fajkę.
#     for i in range(n):
#         if matrix[i, 0] == 2:
#             mi3 = matrix[i, 3]
#             if not(mi3 == 1 or mi3 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 8. Mieszkaniec środkowego domu pija mleko.
#     if not(matrix[3, 2] == 2 or matrix[3, 2] == 99):
#         result_verification = False
#
#     if result_verification is False:
#         return result_verification
#
#     # 9. Palacz papierosów light ma sąsiada, który pija wodę.
#     for i in range(n):
#         if matrix[i, 3] == 3:
#             if i == 0:
#                 if not(matrix[i + 1, 2] == 4 or matrix[i + 1, 2] == 99):
#                     result_verification = False
#             elif i == 4:
#                 if not(matrix[i - 1, 2] == 4 or matrix[i - 1, 2] == 99):
#                     result_verification = False
#             else:
#                 if not(matrix[i + 1, 2] == 4 or matrix[i + 1, 2] == 99):
#                     result_verification = False
#                 elif not(matrix[i - 1, 2] == 4 or matrix[i - 1, 2] == 99):
#                     result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 10. Palacz papierosów bez filtra hoduje ptaki.
#     for i in range(n):
#         if matrix[i, 3] == 2:
#             mi4 = matrix[i, 4]
#             if not(mi4 == 3 or mi4 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 11. Szwed hoduje psy.
#     for i in range(n):
#         if matrix[i, 0] == 4:
#             mi4 = matrix[i, 4]
#             if not(mi4 == 2 or mi4 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 12. Norweg mieszka obok niebieskiego domu.
#     if not(matrix[2, 1] == 2 or matrix[2, 1] == 99):
#         result_verification = False
#
#     if result_verification is False:
#         return result_verification
#
#     # 13. Hodowca koni mieszka obok żółtego domu.
#     for i in range(n):
#         if matrix[i, 4] == 0:
#             if i == 0:
#                 if not(matrix[i + 1, 1] == 4 or matrix[i + 1, 1] == 99):
#                     result_verification = False
#             elif i == 4:
#                 if not(matrix[i - 1, 1] == 4 or matrix[i - 1, 1] == 99):
#                     result_verification = False
#             else:
#                 if not(matrix[i + 1, 1] == 4 or matrix[i + 1, 1] == 99):
#                     result_verification = False
#                 elif not(matrix[i - 1, 1] == 4 or matrix[i - 1, 1] == 99):
#                     result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 14. Palacz mentolowych pija piwo.
#     for i in range(n):
#         if matrix[i, 3] == 4:
#             mi2 = matrix[i, 2]
#             if not(mi2 == 3 or mi2 == 99):
#                 result_verification = False
#             break
#
#     if result_verification is False:
#         return result_verification
#
#     # 15. W zielonym domu pija się kawę.
#     for i in range(n):
#         if matrix[i, 1] == 3:
#             mi2 = matrix[i, 2]
#             if not(mi2 == 2 or mi2 == 99):
#                 result_verification = False
#             break
#
#     return result_verification


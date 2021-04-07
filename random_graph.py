import copy
import random
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = []


class Graph:
    def __init__(self, size_x, size_y, number_of_points):
        self.size_x = size_x
        self.size_y = size_y
        self.number_of_points = number_of_points
        self.points = []
        self.strgraph = ''

        if self.number_of_points > self.size_x * self.size_y:
            raise Exception('nie ma az tylu punktow na siatce [size_x, size_y, number_of_points] {}'.format([self.size_x, self.size_y, self.number_of_points]) + '; maksymalnie możesz wziac caly rozmiar siatki, czyli {} punktów'.format(self.size_x * self.size_y))

        # self.points.append(Point(6,6))
        # self.points.append(Point(8,1))
        # self.points.append(Point(6,2))
        # self.points.append(Point(8,4))
        temp_points = []
        for a in range(self.size_x):
            for b in range(self.size_y):
                temp_points.append(Point(a, b))

        random.shuffle(temp_points)

        i = 0
        while i < self.number_of_points:
            self.points.append(temp_points[i])
            i += 1

        counter_cannot_connect = 0

        def check_todo_connection():
            do_connection = False
            for point in self.points:
                if len(point.connections) == 0:
                    do_connection = True
            return do_connection

        points_to_connection = list(range(len(self.points)))

        while len(points_to_connection) > 1: #check_todo_connection(): # and counter_cannot_connect < self.number_of_points * 1000 * np.sqrt(self.size_x**2 * self.size_y**2):
        # while counter_cannot_connect < (self.size_x * self.size_y):
            random_point_idx = random.sample(points_to_connection, 1)[0]
            random_point = self.points[random_point_idx]
            x1, y1 = random_point.x, random_point.y
            distances = []
            set_dif = set(self.points) - {random_point}
            for p in set_dif:
                dist = np.sqrt((x1-p.x)**2 + (y1-p.y)**2)
                distances.append((p, dist))

            # nearest_point = min(distances, key=lambda t: t[1])[0]
            nearest_points = sorted(distances, key=lambda t: t[1])
            nearest_point = nearest_points[0][0]

            for npoint in nearest_points:
                if npoint[0] in random_point.connections:
                    pass
                else:
                    cross = False
                    for p in self.points:
                        for con in p.connections:
                            if intersect(p, con, random_point, npoint[0]): # if doIntersect(p, con, random_point, nearest_point):
                                cross = True
                    if not cross:
                        # self.points[self.points.index(random_point)].connections.append(npoint[0])
                        # self.points[self.points.index(npoint[0])].connections.append(random_point)
                        random_point.connections.append(npoint[0])
                        npoint[0].connections.append(random_point)
            if random_point_idx in points_to_connection:
                points_to_connection.remove(random_point_idx)
                    # else:
                    #     counter_cannot_connect += 1

            # counter_exist_connect = 0
            # while nearest_point in random_point.connections:
            #     counter_exist_connect += 1
            #     if counter_exist_connect >= len(nearest_points):
            #         break
            #     else:
            #         nearest_point = nearest_points[counter_exist_connect][0]
            #
            # if nearest_point in random_point.connections:
            #     counter_cannot_connect += 1
            # else:
            #     cross = False
            #     for p in self.points:
            #         for con in p.connections:
            #             if intersect(p, con, random_point, nearest_point): # if doIntersect(p, con, random_point, nearest_point):
            #                 cross = True
            #     if not cross:
            #         self.points[self.points.index(random_point)].connections.append(nearest_point)
            #         self.points[self.points.index(nearest_point)].connections.append(random_point)
            #     else:
            #         counter_cannot_connect += 1

        for point in self.points:
            self.strgraph += str(point.x) + '.' + str(point.y) + ': '
            for con in point.connections:
                self.strgraph += str(con.x) + '.' + str(con.y) + ' '
            self.strgraph += ';'

        self.strgraph = self.strgraph[:-1]

        print('random_graph: done')

    def get_tuples(self):
        tuples = []
        for point in self.points:
            for con in point.connections:
                tuples.append((str(point.x) + '.' + str(point.y), (str(con.x) + '.' + str(con.y))))
        return tuples

    def get_nodes(self):
        nodes = []
        positions = []
        for point in self.points:
            nodes.append(str(point.x) + '.' + str(point.y))
            positions.append((point.x, point.y))
        return nodes, positions



def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


# def onSegment(p, q, r):
#     if ((q.x < max(p.x, r.x)) and (q.x > min(p.x, r.x)) and
#             (q.y < max(p.y, r.y)) and (q.y > min(p.y, r.y))):
#         return True
#     return False
#
#
# def orientation(p, q, r):
#     # to find the orientation of an ordered triplet (p,q,r)
#     # function returns the following values:
#     # 0 : Colinear points
#     # 1 : Clockwise points
#     # 2 : Counterclockwise
#
#     # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
#     # for details of below formula.
#
#     val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
#     if (val > 0):
#
#         # Clockwise orientation
#         return 1
#     elif (val < 0):
#
#         # Counterclockwise orientation
#         return 2
#     else:
#
#         # Colinear orientation
#         return 0
#
#
# # The main function that returns true if
# # the line segment 'p1q1' and 'p2q2' intersect.
# def doIntersect(p1, q1, p2, q2):
#     # Find the 4 orientations required for
#     # the general and special cases
#     o1 = orientation(p1, q1, p2)
#     o2 = orientation(p1, q1, q2)
#     o3 = orientation(p2, q2, p1)
#     o4 = orientation(p2, q2, q1)
#
#     # General case
#     if ((o1 != o2) and (o3 != o4)):
#         return True
#
#     # Special Cases
#
#     # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
#     if ((o1 == 0) and onSegment(p1, p2, q1)):
#         return True
#
#     # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
#     if ((o2 == 0) and onSegment(p1, q2, q1)):
#         return True
#
#     # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
#     if ((o3 == 0) and onSegment(p2, p1, q2)):
#         return True
#
#     # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
#     if ((o4 == 0) and onSegment(p2, q1, q2)):
#         return True
#
#     # If none of the cases
#     return False
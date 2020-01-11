# %%
import json
import math # contains sqrt, exp, pow, etc.
import random
import time
from collections import deque
from TSP.helpers import *
import itertools
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

# %%
def dist(xy1, xy2):
    """ Calculate the distance between two points.

    You may choose to use Euclidean distance, Manhattan distance, or some
    other metric
    """
    # TODO: Implement this function!
    # raise NotImplementedError
    distance = ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** (1 / 2)
    return distance

# %%
class TravelingSalesmanProblem:
    """ Representation of a traveling salesman optimization problem.

    An instance of this class represents a complete circuit of the cities
    in the `path` attribute.


    Parameters
    ----------
    cities : iterable
        An iterable sequence of cities; each element of the sequence must be
        a tuple (name, (x, y)) containing the name and coordinates of a city
        on a rectangular grid. e.g., ("Atlanta", (585.6, 376.8))

    shuffle : bool
        If True, then the order of the input cities (and therefore the starting
        city) is randomized.

    Attributes
    ----------
    names : sequence
        An iterable sequence (list by default) containing only the names from
        the cities in the order they appear in the current TSP path

    coords : sequence
        An iterable sequence (list by default) containing only the coordinates
        from the cities in the order they appear in the current TSP path

    path : tuple
        A path between cities as specified by the order of the city
        tuples in the list.
    """

    def __init__(self, cities, shuffle=False):
        ##### YOU DO NOT NEED TO MODIFY THIS FUNCTION #####
        if shuffle:
            cities = list(cities)
            random.shuffle(cities)
        self.path = tuple(cities)  # using a tuple makes the path sequence immutable
        self.__utility = None  # access this attribute through the .utility property

    def copy(self, shuffle=False):
        ##### YOU DO NOT NEED TO MODIFY THIS FUNCTION #####
        cities = list(self.path)
        if shuffle: random.shuffle(cities)
        return TravelingSalesmanProblem(cities)

    @property
    def names(self):
        """Strip and return only the city name from each element of the
        path list. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> ["Atlanta", ...]
        """
        ##### YOU DO NOT NEED TO MODIFY THIS FUNCTION #####
        names, _ = zip(*self.path)
        return names

    @property
    def coords(self):
        """ Strip the city name from each element of the path list and
        return a list of tuples containing only pairs of xy coordinates
        for the cities. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
        """
        ##### YOU DO NOT NEED TO MODIFY THIS FUNCTION #####
        _, coords = zip(*self.path)
        return coords

    @property
    def utility(self):
        """ Calculate and cache the total distance of the path in the
        current state.
        """
        ##### YOU DO NOT NEED TO MODIFY THIS FUNCTION #####
        if self.__utility is None:
            self.__utility = self.__get_value()
        return self.__utility

    def successors(self):
        """ Return a list of states in the neighborhood of the current state.

        You may define the neighborhood in many different ways; although some
        will perform better than others. One method that usually performs well
        for TSP is to generate neighbors of the current path by selecting a
        starting point and an ending point in the current path and reversing
        the order of the nodes between those boundaries.

        For example, if the current list of cities (i.e., the path) is [A, B, C, D]
        then the neighbors will include [B, A, C, D], [C, B, A, D], and [A, C, B, D].
        (The order of successors does not matter.)

        Returns
        -------
        iterable<Problem>
            A list of TravelingSalesmanProblem instances initialized with their list
            of cities set to one of the neighboring permutations of cities in the
            present state
        """
        # TODO: Implement this function!
        # raise NotImplementedError
        permuta = itertools.permutations(list(self.path))
        for p in permuta:
            yield TravelingSalesmanProblem(p)

    def get_successor(self):
        """ Return a random state from the neighborhood of the current state.

        You may define the neighborhood in many different ways; although some
        will perform better than others. One method that usually performs well
        for TSP is to generate neighbors of the current path by selecting a
        starting point and an ending point in the current path and reversing
        the order of the nodes between those boundaries.

        For example, if the current list of cities (i.e., the path) is [A, B, C, D]
        then the neighbors will include [B, A, C, D], [C, B, A, D], and [A, C, B, D].
        (The order of successors does not matter.)

        Returns
        -------
        list<Problem>
            A list of TravelingSalesmanProblem instances initialized with their list
            of cities set to one of the neighboring permutations of cities in the
            present state
        """
        # TODO: Implement this function!
        # raise NotImplementedError
        return list(self.path)

    def __get_value(self):
        """ Calculate the total length of the closed-circuit path of the current
        state by summing the distance between every pair of cities in the path
        sequence.

        For example, if the current path is (A, B, C, D) then the total path length is:

            dist = DIST(A, B) + DIST(B, C) + DIST(C, D) + DIST(D, A)

        You may use any distance metric that obeys the triangle inequality (e.g.,
        Manhattan distance or Euclidean distance) for the DIST() function.

        Since the goal of our optimizers is to maximize the value of the objective
        function, multiply the total distance by -1 so that short path lengths
        are larger numbers than long path lengths.

        Returns
        -------
        float
            A floating point value with the total cost of the path given by visiting
            the cities in the order according to the self.cities list

        Notes
        -----
            (1) Remember to include the edge from the last city back to the first city

            (2) Remember to multiply the path length by -1 so that short paths have
                higher value relative to long paths
        """
        # TODO: Implement this function!
        # raise NotImplementedError
        # self.path = self.get_successor()
        dist_agg = 0
        for i in range(len(self.coords)):
            if i == len(self.coords) - 1:
                # print(i,0)
                dist_agg += dist(self.coords[i], self.coords[0])
            else:
                # print(i,i+1)
                dist_agg += dist(self.coords[i], self.coords[i + 1])
        return -1 * dist_agg

# %%
test_cities = [('DC', (11, 1)), ('SF', (0, 0)), ('PHX', (2, -3)), ('LA', (0, -4))]
# %%
tsp = TravelingSalesmanProblem(test_cities)
print(tsp.utility)
# Construct an instance of the TravelingSalesmanProblem and test `.__get_value()`
test_cities = [('DC', (11, 1)), ('SF', (0, 0)), ('PHX', (2, -3)), ('LA', (0, -4))]
tsp = TravelingSalesmanProblem(test_cities)
assert round(-tsp.utility, 2) == 28.97, \
    "There was a problem with the utility value returned by your TSP class."
print("Looks good!")
# %%
# Test the successors() method
successor_paths = set([x.path for x in tsp.successors()])
expected_paths = [
    (('SF', (0, 0)), ('DC', (11, 1)), ('PHX', (2, -3)), ('LA', (0, -4))),
    (('DC', (11, 1)), ('LA', (0, -4)), ('SF', (0, 0)), ('PHX', (2, -3))),
    (('LA', (0, -4)), ('PHX', (2, -3)), ('DC', (11, 1)), ('SF', (0, 0)))
]
assert all(contains(successor_paths, x) for x in expected_paths), \
    "It looks like your successors list does not implement the suggested neighborhood function."
print("Looks good!")
# %%
# Create the problem instance and plot the initial state
num_cities = 10
shuffle = False

capitals_tsp = TravelingSalesmanProblem(capitals_list[:num_cities], shuffle=shuffle)
starting_city = capitals_tsp.path[0]
print("Initial path value: {:.2f}".format(-capitals_tsp.utility))
print(capitals_tsp.path)  # The start/end point is indicated with a yellow star
show_path(capitals_tsp.coords, starting_city)
# %%


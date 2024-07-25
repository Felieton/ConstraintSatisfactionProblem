from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import random as rand
from constraint_map import ConstraintMap

GRID_SIDE_LENGTH = 7


def generate_instance(points_amount):
    random_points = generate_random_points(points_amount)
    tri, random_points_list = triangulate(random_points)
    # plot_instance(tri, random_points_list)
    neighbourhood = get_points_neighbourhood(tri, random_points_list)
    return neighbourhood, tri, random_points_list


def generate_random_points(amount):
    random_points = []
    for i in range(amount):
        random_point = [rand.randint(0, GRID_SIDE_LENGTH), rand.randint(0, GRID_SIDE_LENGTH)]
        while random_point in random_points:
            random_point = [rand.randint(0, GRID_SIDE_LENGTH), rand.randint(0, GRID_SIDE_LENGTH)]
        random_points.append(random_point)

    return random_points


def triangulate(random_points):
    points = np.array(random_points)
    tri = Delaunay(points)

    return tri, points


def plot_instance(tri, points):
    plt.triplot(points[:, 0], points[:, 1], tri.simplices)
    plt.plot(points[:, 0], points[:, 1], 'o')
    plt.show()


def find_neighbours(tri):
    neighbours = defaultdict(set)

    for simplex in tri.simplices:
        for idx in simplex:
            other = set(simplex)
            other.remove(idx)
            neighbours[idx] = neighbours[idx].union(other)

    return neighbours


def get_points_neighbourhood(tri, points_list):
    neighbour_dict = find_neighbours(tri)
    neighbourhood = {}

    for point, neighbours in neighbour_dict.items():
        act_point = (points_list[point][0], points_list[point][1])
        neighbourhood[act_point] = []
        for neighbour in neighbours:
            neighbourhood[act_point].append((points_list[neighbour][0], points_list[neighbour][1]))

    return neighbourhood


def get_constraints(neighbourhood):
    constraints = []
    for point, neighbours in neighbourhood.items():
        for neighbour in neighbours:
            constraints.append([point, neighbour])

    constraints_optimized = []
    for constraint in constraints:
        if [constraint[0], constraint[1]] not in constraints_optimized and \
                [constraint[1], constraint[0]] not in constraints_optimized:
            constraints_optimized.append(ConstraintMap(constraint[0], constraint[1]))

    return constraints_optimized


def get_variables(neighbourhood):
    variables = []
    for key, value in neighbourhood.items():
        variables.append(key)

    return variables

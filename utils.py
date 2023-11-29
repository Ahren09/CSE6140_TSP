# Adjusted parsing function to skip header lines
import math
from typing import Tuple

import numpy as np
import pandas as pd


def parse_tsp_data(data) -> pd.DataFrame:
    """
    Parse TSP data into a pd.DataFrame
    :param data:
    :return: pd.DataFrame. Each line represents a city, with the first column being the city ID and the second and third columns being the x and y coordinates, respectively.
    """

    lines = data.strip().split('\n')
    coords = {}
    parsing_coordinates = False
    for line in lines:
        if line.startswith('EOF'):
            break
        if line.startswith('NODE_COORD_SECTION'):
            parsing_coordinates = True
            continue
        if parsing_coordinates:
            parts = line.split()
            coords[int(parts[0])] = (float(parts[1]), float(parts[2]))

    coords = pd.DataFrame(coords).T
    return coords


def euclidean_distance(point1: Tuple[int, int], point2: Tuple[int, int]):
    """
    Calculate Euclidean distance between two points

    :param point1:
    :param point2:
    :return:
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def create_distance_matrix(data):
    """Create a distance matrix from city coordinates."""
    cities = list(data.keys())
    n = len(cities)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = euclidean_distance(data[cities[i]], data[cities[j]])
    return distance_matrix
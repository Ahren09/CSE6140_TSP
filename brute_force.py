
import itertools
import math
import time

from utils import parse_tsp_data


def euclidean_distance(point1: int, point2: int):
    """
    Calculate Euclidean distance between two points

    :param point1:
    :param point2:
    :return:
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def brute_force_tsp(coords, time_limit):
    """
    Brute-force TSP solution with time cut-off
    :param coords:
    :param time_limit:
    :return:
    """

    start_time = time.time()
    min_path = None
    min_distance = float('inf')

    for path in itertools.permutations(coords.keys()):
        # Check time limit
        if time.time() - start_time > time_limit:
            break

        # Calculate the total distance of the path
        total_distance = sum(euclidean_distance(coords[path[i]], coords[path[i + 1]]) for i in range(len(path) - 1))
        if total_distance < min_distance:
            min_distance = total_distance
            min_path = path

    return min_path, min_distance



tsp_data = open("data/Atlanta.tsp", "r").read()

coords = parse_tsp_data(tsp_data)

# Set the time limit (in seconds)
time_limit = 300


brute_force_tsp(coords, time_limit)
import numpy as np
import pandas as pd
import random
import math
import time
import argparse
import os

from utils import get_tsp_filename


class SimulatedAnnealing:
    def __init__(self, coordinates, temp, cooling_rate=0.9999):
        """
        Initialize the Simulated Annealing (Local Search method)  with the given coordinates and parameters.
        """
        self.coordinates = coordinates
        self.temperature = temp
        self.cooling_rate = cooling_rate
        self.best_path = list(range(len(coordinates)))
        self.best_distance = self.calculate_total_distance(self.best_path)
        self.trace = []

    def calculate_total_distance(self, path):
        """
        Calculate the total Euclidean distance of the path.
        """
        total_dist = 0
        for i in range(len(path)):
            start, end = path[i], path[(i + 1) % len(path)]
             # Calculate the Euclidean distance between the current node and the next node
            total_dist += np.linalg.norm(np.array(self.coordinates[start]) - np.array(self.coordinates[end]))
        return total_dist

    def optimize(self, time_limit):
        """
        Run the Simulated Annealing optimization process within the given time limit.
        """
        start_time = time.time()
        # loop untill cooled down to the minimum temperature
        while self.temperature > 1e-3 and time.time() - start_time < time_limit:
            self.try_new_path(start_time)
            self.temperature *= self.cooling_rate

    def try_new_path(self, start_time):
        """
        Try a new path and accept it if it improves the distance or meets the acceptance probability.
        """

        # Select two indices and create a new path by reversing them.
        i, j = sorted(random.sample(range(len(self.best_path)), 2))
        new_path = self.best_path[:i] + list(reversed(self.best_path[i:j + 1])) + self.best_path[j + 1:]
        new_distance = self.calculate_total_distance(new_path)

        # decision to accept new path in simulated annealing
        if new_distance < self.best_distance or math.exp((self.best_distance - new_distance) / self.temperature) > random.random():
            # accept the new path if it's shorter
            self.best_path, self.best_distance = new_path, new_distance
             # record the time and distance of the new best path
            self.trace.append((time.time() - start_time, self.best_distance))


def read_coordinates(file_path):
    """
    Read the TSP file and extract the coordinates.
     """
    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')
        coords_start = lines.index('NODE_COORD_SECTION') + 1
        coords_end = lines.index('EOF', coords_start)
        coords = [tuple(map(float, line.split()[1:])) for line in lines[coords_start:coords_end]]
    return coords

def get_localsearch_result(best_sol, output_file):
    """
    Write the solution to an output file.
    """
    with open(output_file, "w") as f:
        f.write(f"{int(round(best_sol.best_distance))}\n")
        f.write(','.join(str(vertex) for vertex in best_sol.best_path) + '\n')

def run_localsearch(inst, time_limit, seed):
    coordinates = read_coordinates(get_tsp_filename(inst))
    random.seed(seed)

    # intizlize algo and optize it
    sa = SimulatedAnnealing(coordinates, temp=10000)
    sa.optimize(time_limit)
    return sa

"""
if __name__ == '__main__':
    start_time = time.time() 
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', required=True)
    parser.add_argument('-time', required=True, type=int)
    parser.add_argument('-seed', type=int, default=0)
    args = parser.parse_args()

    # run algo and save result
    solution = main(args.inst, args.time, args.seed)
    output_filename = f"{os.path.splitext(os.path.basename(args.inst))[0]}_LS_{args.time}_{args.seed}.sol"
    get_result(solution, output_filename)
    end_time = time.time()
    run_time = end_time - start_time
    print(f"Running time: {run_time:.4f} seconds")
"""

# python localSearch.py -inst data/Atlanta.tsp -time 60 -seed 42

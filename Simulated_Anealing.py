import numpy as np
import pandas as pd
import random
import math
import time
import argparse
import os

class SimulatedAnnealing:
    def __init__(self, path, coordinates, temp, cooling_rate=0.99):
        self.path = path
        self.coordinates = coordinates
        self.temperature = temp
        self.cooling_rate = cooling_rate
        self.best_path = path
        self.best_distance = self.calculate_total_distance(path)
        self.trace = []

    def calculate_total_distance(self, path):
        total_dist = 0
        for i in range(len(path)):
            start, end = path[i], path[(i + 1) % len(path)]
            total_dist += np.linalg.norm(np.array(self.coordinates[start]) - np.array(self.coordinates[end]))
        return total_dist

    def optimize(self, time_limit):
        start_time = time.time()
        while self.temperature > 1:
            i, j = sorted(random.sample(range(len(self.path)), 2))
            new_path = self.path[:i] + list(reversed(self.path[i:j + 1])) + self.path[j + 1:]
            new_distance = self.calculate_total_distance(new_path)
            if math.exp((self.best_distance - new_distance) / self.temperature) > random.random():
                self.path = new_path
                if new_distance < self.best_distance:
                    self.best_path, self.best_distance = new_path, new_distance
                    self.trace.append([time.time() - start_time, self.best_distance])
            self.temperature *= self.cooling_rate
            if time.time() - start_time > time_limit:
                break

def main(file, seed, time_limit):
    data = pd.read_csv(file, skiprows=4, header=None, sep=',')
    coordinates = data.iloc[:, 1:3].values.tolist()
    random.seed(seed)
    initial_path = random.sample(range(len(coordinates)), len(coordinates))
    sa = SimulatedAnnealing(initial_path, coordinates, 1000)
    sa.optimize(time_limit)
    return sa

def write_output(best_sol, path):
    with open(path, "w") as f:
        f.write(str(round(best_sol.best_distance)) + "\n")
        f.write(','.join(str(vertex) for vertex in best_sol.best_path) + '\n')


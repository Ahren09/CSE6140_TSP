# MST Approximation Algorithm for the Traveling Salesman Problem (TSP)
#
# This implementation defines a class MSTApprox that represents a 2-approximation algorithm
# for solving the TSP based on the Minimum Spanning Tree (MST) of the given graph.
#
# The algorithm works as follows:
# 1. Constructs an MST using a heuristic approach.
# 2. Performs a preorder traversal of the MST starting from a specified seed node.
# 3. Constructs a tour by connecting consecutive nodes in the traversal order.
# 4. Outputs the constructed tour, including the order of visited nodes and the corresponding distances.
#
# The resulting tour is guaranteed to be within a factor of 2 of the optimal TSP solution.
#
# Example Usage:
# tsp_instance_name = "city_name"
# random_seed_value = 1
# cutoff_time_value = 300
# mst_approx_instance = MSTApprox(tsp_instance_name, random_seed_value, cutoff_time_value)
# graph_data = mst_approx_instance.read_tsp_data()
# mst_approx_instance.generate_tour(graph_data)

import numpy as np
import math
import timeit as tt

class MSTApprox:

    def __init__(self, city_instance, random_seed, cutoff_time=600):
        self.city = city_instance
        self.random_seed = random_seed
        self.cutoff_time = cutoff_time
        self.inf = float("inf")
        self.path = []
        self.total_distance = 0.0

    def minimum_spanning_tree(self, graph):
        num_nodes = len(graph)
        adjacency_matrix = np.array(graph)

        edges = []
        visited_nodes = [self.random_seed]

        while len(visited_nodes) < num_nodes:
            row = adjacency_matrix[visited_nodes[-1]].copy()  # Make a copy to avoid modifying the original matrix
            row[visited_nodes] = self.inf  # Set visited nodes to infinity
            min_edge = np.argmin(row)
            new_node = min_edge
            
            visited_nodes.append(new_node)
            edges.append((visited_nodes[-2], new_node))

        # Duplicate edges to form an undirected graph
        edges.extend([(y, x) for (x, y) in edges])

        return edges

    def preorder_traversal(self, edges, parent):
        if parent not in self.path:
            self.path.append(parent)
            children = [x[1] for x in edges if x[0] == parent]
            if children:
                for node in children:
                    self.preorder_traversal(edges, node)

    def generate_tour(self, graph):
        start_time = tt.default_timer()
        self.total_distance = 0.0
        self.path = []

        mst_edges = self.minimum_spanning_tree(graph)
        self.preorder_traversal(mst_edges, self.random_seed)

        tour_edges = []
        for i in range(len(self.path) - 1):
            distance = graph[self.path[i]][self.path[i + 1]]
            tour_edges.append((self.path[i], self.path[i + 1], distance))
            self.total_distance += distance

        # Closing the loop
        last_node = self.path[-1]
        first_node = self.path[0]
        tour_edges.append((last_node, first_node, graph[last_node][first_node]))
        self.total_distance += graph[last_node][first_node]

        stop_time = tt.default_timer()

        self.write_trace(stop_time - start_time, int(self.total_distance))
        self.write_data(tour_edges, self.total_distance)

    def read_tsp_data(self):
        tsp_data = []
        with open(f'./DATA/{self.city}.tsp') as file:
            next(file)  # Skip the first five lines
            next(file)
            next(file)
            next(file)
            next(file)
            for line in file:
                if line == 'EOF\n':
                    break
                data = line[:-1].split(' ')
                tsp_data.append({'x': float(data[1]), 'y': float(data[2])})

        num_nodes = len(tsp_data)
        graph = np.zeros((num_nodes, num_nodes))

        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j:
                    graph[i][j] = int(round(math.sqrt((tsp_data[i]['x'] - tsp_data[j]['x']) ** 2 +
                                                     (tsp_data[i]['y'] - tsp_data[j]['y']) ** 2)))

        return graph

    def write_data(self, output, total_distance):
        total_distance = str(int(total_distance))
        file_name = f'{self.city}_MSTApprox_{self.cutoff_time}_{self.random_seed}.sol'
        with open(file_name, 'w') as file:
            file.write(total_distance + '\n')
            for edge in output:
                file.write(f"{edge[0]} {edge[1]} {int(edge[2])}\n")

    def write_trace(self, elapsed_time, total_distance):
        file_name = f'{self.city}_MSTApprox_{self.cutoff_time}_{self.random_seed}.trace'
        with open(file_name, 'w') as file:
            file.write('{:.2f} {}\n'.format(elapsed_time, total_distance))

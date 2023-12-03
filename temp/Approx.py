import numpy as np
import math
import timeit as tt

class MSTApprox:
    """ This class provides an approximate solution to the TSP
    using a Minimum Spanning Tree approach. """

    INFINITY = float("inf")

    def __init__(self, city_instance, random_seed, cutoff_time=600):
        """ Initializes the MSTApprox method with the given city instance, random seed, and cutoff time. """
        self.city = city_instance
        self.random_seed = random_seed
        self.cutoff_time = cutoff_time
        self.path = []
        self.total_distance = 0.0

    def MST_algo(self, graph):
        """ 
        Implement the minimum spanning tree algorithm for the given graph.
        """
        num_nodes = len(graph)
        # convert to NumPy array for easy manipulation
        adjacency_matrix = np.array(graph)
        edges = []
        visited_nodes = [self.random_seed]

        while len(visited_nodes) < num_nodes:
            current_node = visited_nodes[-1]# to get the last visited node
            distances_to_unvisited = adjacency_matrix[current_node].copy()
            # set distances to visited nodes as infinity to avoid revisiting
            distances_to_unvisited[visited_nodes] = self.INFINITY
            new_node = np.argmin(distances_to_unvisited)
            
            visited_nodes.append(new_node)
            edges.append((current_node, new_node))

        # since the original graph is undirected, add reverse edges to ensure undirectedness
        undirected_edges = edges + [(y, x) for (x, y) in edges]

        return undirected_edges

    def generate_path(self, edges, node):
        """ 
        Performs a preorder traversal on the tree to generate the TSP path. 
        """
        if node not in self.path:
            self.path.append(node)
            # find all children of the current node 
            children = [target for source, target in edges if source == node]
            for child in children:
                self.generate_path(edges, child)

    def generate_tour(self, graph):
        """ 
        Generates a TSP tour based on the Minimum Spanning Tree (MST) and calculates the total distance of the tour.
        """
        start_time = tt.default_timer()

        # generate MST and create a TSP path from the MST
        self.path = []
        mst_edges = self.MST_algo(graph)
        self.generate_path(mst_edges, self.random_seed)

        # calculate the total distance of the TSP path
        self.total_distance = sum(graph[self.path[i]][self.path[i + 1]] for i in range(len(self.path) - 1))
        self.total_distance += graph[self.path[-1]][self.path[0]]  # Closing the loop to complete the tour

        # get result
        stop_time = tt.default_timer()
        self.get_result(self.path, self.total_distance)

    def read_tsp_data(self):
        """ 
        Reads TSP data from a file and generates a graph represented by a distance matrix. 
        """
        # open tsp file and read 
        with open(f'./DATA/{self.city}.tsp') as file:
            lines = file.readlines()
            coordinates = [line.strip().split(' ') for line in lines if line.strip() and line[0].isdigit()]
            coordinates = [(float(x), float(y)) for _, x, y in coordinates]

        num_nodes = len(coordinates)
        graph = np.zeros((num_nodes, num_nodes))

        # calculate the distance between each pair of nodes
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):  # Avoid computing distance twice
                graph[i][j] = graph[j][i] = int(round(math.hypot(coordinates[i][0] - coordinates[j][0],
                                                                  coordinates[i][1] - coordinates[j][1])))

        return graph

    def get_result(self, path, total_distance):
        """ Writes the TSP tour and total distance to a solution file. """
        file_name = f'{self.city}_MSTApprox_{self.cutoff_time}_{self.random_seed}.sol'
        with open(file_name, 'w') as file:
            file.write(f'{int(total_distance)}\n')
            file.write(','.join(map(str, path)))

# Usage example:
tsp_instance_name = "Atlanta"
random_seed_value = 1
cutoff_time_value = 300
mst_approx_instance = MSTApprox(tsp_instance_name, random_seed_value, cutoff_time_value)
graph_data = mst_approx_instance.read_tsp_data()
mst_approx_instance.generate_tour(graph_data)

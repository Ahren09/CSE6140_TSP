import itertools
import time

from utils import euclidean_distance


def brute_force_tsp(shared_data, stop_event, coords):
    """
    Brute-force TSP solution with time cut-off
    :param coords:
    :param time_limit:
    :return:
    """

    start_time = time.time()
    shared_data['min_path'] = None
    shared_data['min_distance'] = float('inf')

    nodes = [int(n) for n in coords.index.values]
    coords = coords.values.tolist()

    N = len(coords)

    # all_node_indices ranges from 0 to N-1
    # N is the number of nodes (cities / locations)
    all_node_indices = list(range(N))

    for node_indices_of_path in itertools.permutations(all_node_indices):
        if stop_event.is_set():
            print("Time limit reached, stopping calculation.")
            return

        # Calculate the total distance of the path
        total_distance = sum(euclidean_distance(coords[node_indices_of_path[i]], coords[node_indices_of_path[i + 1]])
                             for i in
                             range(N - 1))
        if total_distance < shared_data['min_distance']:
            # Update the best path and distance
            
            shared_data['min_distance'] = total_distance
            path = [str(nodes[i]) for i in node_indices_of_path]

            shared_data['min_path'] = path

            # print(f"New best distance: {shared_data['min_distance']}")
            # print(f"New best path: {shared_data['min_path']}")
    
    end_time = time.time()
    run_time = end_time - start_time
    print(f"Running time: {run_time:.2f} seconds")

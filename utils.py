# Adjusted parsing function to skip header lines
import pandas as pd


def parse_tsp_data(data):
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




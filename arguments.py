import argparse


def parse_args():

    parser = argparse.ArgumentParser(description="Dynamic Graph Embedding Trajectory.")
    parser.add_argument('--dataset_name', type=str, required=True,
                        help="Name of the dataset.")

    args = parser.parse_args()

    return args






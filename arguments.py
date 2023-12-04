import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="TSP")
    parser.add_argument('-inst', dest='inst', type=str)
    parser.add_argument('-alg', choices=["BF", "Approx", "LS"], dest='alg', type=str)
    parser.add_argument('-time', dest='time_limit', type=int)
    parser.add_argument('-seed', dest='seed', type=int, default=0)

    args = parser.parse_args()

    return args

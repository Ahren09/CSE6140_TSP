import os
import os.path as osp

from Simulated_Anealing import main, write_output
from arguments import parse_args
from brute_force import brute_force_tsp
from timeout import TimeoutException, function_with_timeout
from utils import parse_tsp_data

if __name__ == "__main__":
    args = parse_args()

    if args.alg == "BF":

        results = {'best_result': None}
        tsp_data = open(osp.join("data", args.file), "r").read()
        coords = parse_tsp_data(tsp_data)

        try:
            results = function_with_timeout(args.time_limit, brute_force_tsp, coords)  # Should timeout and return
            print(results)

        except TimeoutException as e:
            print(f"Timeout at {args.time_limit} seconds")

        output_file = os.path.basename(args.file)[: -4] + '_' + args.alg + '_' + str(args.time_limit) + ".sol"

        # Open a file in write mode ('w' or 'wt' for text files)
        with open(output_file, 'w') as file:
            # Write lines to the file
            file.write(str(results['min_distance']) + "\n")
            file.write(','.join(results['min_path']))

        exit(0)





    elif args.alg == 'Approx':
        sa = main(args.inst, args.seed, args.time_limit)
        output_file = os.path.basename(args.file)[: -4] + '_' + args.alg + '_' + str(args.time_limit) + "_" + str(
            args.seed) + ".sol"
        write_output(sa, output_file)

    else:
        print("Unsupported algorithm specified.")


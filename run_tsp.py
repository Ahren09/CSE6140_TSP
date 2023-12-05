import os
import os.path as osp
import time

from Approx import run_mst_approx
from bak_Simulated_Anealing import main, write_output
from arguments import parse_args
from brute_force import brute_force_tsp
from localSearch import run_localsearch, get_localsearch_result
from timeout import TimeoutException, function_with_timeout
from utils import parse_tsp_data, get_tsp_filename

if __name__ == "__main__":
    args = parse_args()

    t0 = time.time()

    # Sanity-check for the instance name

    original_inst = args.inst

    if ".tsp" in args.inst:
        if args.inst.lower().startswith("data/") or args.inst.lower().endswith(".tsp"):
            # Format: "Data/Atlanta.tsp"
            args.inst = args.inst.split('/')[-1].split(".tsp")[0]

    print(f"{original_inst} -> {args.inst}")





    if args.alg == "BF":

        results = {'best_result': None}
        tsp_data = open(get_tsp_filename(args.inst), "r").read()
        coords = parse_tsp_data(tsp_data)

        try:
            results = function_with_timeout(args.time_limit, brute_force_tsp, coords)  # Should timeout and return
            print(results)

        except TimeoutException as e:
            print(f"Timeout at {args.time_limit} seconds")

        output_file = os.path.basename(args.inst)[: -4] + '_' + args.alg + '_' + str(args.time_limit) + ".sol"

        # Open a file in write mode ('w' or 'wt' for text files)
        with open(output_file, 'w') as file:
            # Write lines to the file
            file.write(str(results['min_distance']) + "\n")
            file.write(','.join(results['min_path']))

    elif args.alg == 'LS':
        solution = run_localsearch(args.inst, args.time_limit, args.seed)
        output_filename = f"{os.path.splitext(os.path.basename(args.inst))[0].lower()}_LS_{args.time_limit}_{args.seed}.sol"
        get_localsearch_result(solution, output_filename)


    elif args.alg == 'Approx':
        run_mst_approx(args.inst, args.seed, args.time_limit)

        # sa = main(args.inst, args.seed, args.time_limit)
        output_file = os.path.basename(args.inst)[: -4].lower() + '_' + args.alg + '_' + str(args.time_limit) + "_" + str(
            args.seed) + ".sol"
        # write_output(sa, output_file)

    else:
        print("Unsupported algorithm specified.")

    print(f"Running time: {time.time() - t0:.4f} seconds")


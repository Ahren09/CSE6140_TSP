## CSE6140 Group Project

### Getting Started

Download `DATA.zip` from Canvas and extract all files to the `data/` directory.

Run the program using the following script to 

```bash
python run_tsp.py -inst <filename> -alg [BF | Approx | LS] -time <cutoff_in_seconds> -seed <random_seed>
```

For example:

* Run `python run_tsp.py -inst Atlanta.tsp -alg BF -time 600 -seed 0`: run the brute force algorithm on the `Atlanta` graph in the `data/` directory.

### Requirements

python >= 3.6




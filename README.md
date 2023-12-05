## CSE6140 Group Project

### Getting Started

Download `DATA.zip` from Canvas and extract all files to the `data/` directory.

Run the program using the following script 

```bash
python run_tsp.py -inst <filename> -alg [BF | Approx | LS] -time <cutoff_in_seconds> -seed <random_seed>
```

For example, to run brute force:

* `python run_tsp.py -inst Atlanta.tsp -alg BF -time 600 -seed 0`: run the brute force algorithm on the `Atlanta` graph in the `data/` directory.


To run local search:

* `python run_tsp.py -inst Atlanta.tsp -alg LS -time 600 -seed 0`

To run approximation:

* `python run_tsp.py -inst Atlanta.tsp -alg Approx -time 600 -seed 0`

  
### Requirements

python >= 3.6


### Notes

#### Generating an executable from our Python file

We will need PyInstaller.

1. **Install PyInstaller:**
   PyInstaller can be installed using pip. Open your terminal and run:
   
2. ```bash
   pip install pyinstaller
   ```

2. **Create the Executable:**
   Navigate to the project directory `CSE6140_TSP` run the following command:
   
3. **Generate the executable**
   ```bash
   pyinstaller --onefile run_tsp.py
   ```
   The `--onefile` option tells PyInstaller to package everything into a single executable file.

3. Generate the executable
   
   ```bash
   pyinstaller --onefile run_tsp.py
   ```


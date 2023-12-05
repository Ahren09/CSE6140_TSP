import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

inst = "Atlanta"
alg = "BF"

solution_qualities = {}

time_limits = np.array(list(range(10, 110, 10)))

cities = ["Atlanta", "NYC", "Berlin", "Toronto", "Denver"]

# for inst in ["Atlanta", "NYC", "Philadelphia"]:
for inst in cities:

    for time_limit in time_limits:
        filename = f"output/{inst}_{alg}_{time_limit}.sol"

        # Open the file in read mode ('r')
        with open(filename, 'r') as file:
            # Read the first line
            first_line = file.readline().strip()
            solution_quality = float(first_line)

            if inst in solution_qualities:
                solution_qualities[inst] += [solution_quality]
            else:
                solution_qualities[inst] = [solution_quality]

df = pd.DataFrame(solution_qualities)

df['time'] = time_limits
# Set Seaborn style
sns.set(style="whitegrid")


for inst in cities:
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df, x='time', y=inst, label=inst)
    # Adding labels and a legend
    plt.xlabel('Time')
    plt.ylabel('Solution Quality')
    plt.title('Solution Quality vs. Time')
    plt.legend()
    plt.tight_layout()

    # plt.show()
    os.makedirs("visualization", exist_ok=True)
    plt.savefig(f"visualization/{inst}_{alg}.png")


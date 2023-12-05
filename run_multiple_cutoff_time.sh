#!/bin/bash

# Initialize TIME at 10
# TIME=10
TIME=10
# cities=("Atlanta" "NYC" "Philadephia")
cities=("Denver")

# Iterate over the list
for city in "${cities[@]}"
do
  # Loop until TIME reaches 100
  while [ $TIME -le 100 ]
  do
      # Run the Python script with the current value of TIME
      python run_tsp.py -inst $city -alg BF -time $TIME -seed 0
      TIME=$((TIME + 10))
  done
done

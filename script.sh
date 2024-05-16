#!/bin/bash

output_file="random_test.txt"

for i in {1..100}
do
    echo "GAME ${i}: $(python -m referee random-agent random-agent -v 0)" | tee -a "$output_file"
done
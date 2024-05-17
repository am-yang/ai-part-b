#!/bin/bash

output_file="out/new_ver_tests/agent_test5.txt"

for i in {1..100}
do
    echo "GAME ${i}: $(python -m referee minimax random-agent -v 0)" | tee -a "$output_file"
done
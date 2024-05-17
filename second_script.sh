#!/bin/bash

output_file="out/old_ver_tests/agent_test7.txt"

for i in {1..100}
do
    echo "GAME ${i}: $(python -m referee random-agent minimax -v 0)" | tee -a "$output_file"
done
#!/usr/bin/env bash

set -e

output_file="primo_ciclica.out"
output_dir="../out/"
run_dir="../"

processes=(1 2 4 6)

: > "$output_dir$output_file"

for process_count in "${processes[@]}"; do
    {
        echo "===== Processes: $process_count ====="
        mpiexec -n "$process_count" python "$run_dir"problema6_ciclica.py
        echo
    } >> "$output_dir$output_file" 2>&1
done

echo "Results saved to $output_dir$output_file"

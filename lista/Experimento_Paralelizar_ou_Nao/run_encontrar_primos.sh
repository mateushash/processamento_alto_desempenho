#!/usr/bin/env bash

set -e

output_file="encontrar_primos.out"
processes=(1 2 4 6)
numbers=(1000 10000 100000 1000000 10000000)

: > "$output_file"

for process_count in "${processes[@]}"; do
    {
        echo "===== Processes: $process_count ====="
        for number in "${numbers[@]}"; do
          {
            echo "Finding primes up to $number"
            mpiexec -n "$process_count" python encontrar_primos.py "$number"
            echo
          }
        done
    } >> "$output_file" 2>&1
done

echo "Results saved to $output_file"

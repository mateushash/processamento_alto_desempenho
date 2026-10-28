import sys

import numpy as np

import benchmarks as bch
from stencil2D import stencil2D as ste
from ui import show_analyssis_options, show_benchmarks_options, show_stride_options, show_stride_analyssis_options


if __name__ == "__main__":
    print("benchmarks: 1")
    print("analysis: 2")
    print("stride: 3")
    print("stride analysis: 4")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input()

    match (choice):
        case "1":
            choice = None
            if len(sys.argv) > 2:
                choice = sys.argv[2]
            show_benchmarks_options(choice)
        case "2":
            show_analyssis_options()
        case "3":
            show_stride_options()
        case "4": 
            show_stride_analyssis_options()

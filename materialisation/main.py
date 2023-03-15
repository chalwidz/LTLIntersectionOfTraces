from dataset import DataSet
from program import Program
from materialisation import *
from time import time


if_continues = True
while if_continues:
    program_file_name = input("Name of the file with the program: ").lower().strip()
    dataset_file_name = input("Name of the file with the dataset: ").lower().strip()
    program_path = "programs/" + program_file_name
    dataset_path = "datasets/" + dataset_file_name

    try:
        program = Program(program_path)
        trace = DataSet(dataset_path).trace
    except:
        print("Invalid program and/or dataset file name.")
    else:
        materialise(trace, program)
    wants_to_continue = input("\nDo you want to continue? [y/n] ").lower().strip()
    if wants_to_continue == "n":
        if_continues = False

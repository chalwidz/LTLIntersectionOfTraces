from random import *


def dataset_generator(num_of_variables, max_num_of_occur, max_timepoint, dataset_number):
    for proposition in range(num_of_variables):
        for _ in range(0, randint(0, max_num_of_occur)):
            timepoint = randint(0, max_timepoint)
            with open(f"datasets/data{dataset_number}.txt", "a") as d:
                d.write(f"p{proposition}@{timepoint}\n")


def program_generator(num_of_variables, max_num_of_rules, program_number):
    for _ in range(randint(int(max_num_of_rules/2), max_num_of_rules)):
        rule_type = randint(1, 5)
        if rule_type == 1:
            head = f"Xp{randint(0, num_of_variables - 1)}"
            body = f"p{randint(0, num_of_variables - 1)}"
        elif rule_type == 2:
            head = f"p{randint(0, num_of_variables - 1)}"
            body = f"Xp{randint(0, num_of_variables - 1)}"
        elif rule_type == 3:
            head = f"Gp{randint(0, num_of_variables - 1)}"
            body = f"p{randint(0, num_of_variables - 1)}"
        elif rule_type == 2:
            head = f"p{randint(0, num_of_variables - 1)}"
            body = f"Gp{randint(0, num_of_variables - 1)}"
        else:
            head_index = randint(0, num_of_variables - 1)
            body_1_index = choice([index for index in range(num_of_variables) if index != head_index])
            body_2_index = choice([index for index in range(num_of_variables) if index != head_index])
            head = f"p{head_index}"
            body = f"p{body_1_index}, p{body_2_index}"
        rule = f"{head} :- {body}"
        with open(f"programs/program{program_number}.txt", "a") as p:
            p.write(f"{rule}\n")

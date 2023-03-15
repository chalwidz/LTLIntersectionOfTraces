def dataset_to_ltl(path):
    output_dataset_formula = ""
    with open(path) as d:
        list_of_facts = d.read().strip().split("\n")
    for fact_index in range(len(list_of_facts)):
        fact_split = list_of_facts[fact_index].strip().split("@")
        timepoint = int(fact_split[1])
        proposition = fact_split[0]
        fact_parsed = ""
        for _ in range(timepoint):
            fact_parsed += "X"
        fact_parsed += proposition
        if fact_index < len(list_of_facts) - 1:
            output_dataset_formula += f"{fact_parsed} & "
        else:
            output_dataset_formula += fact_parsed
    return output_dataset_formula


def program_to_ltl(path):
    output_program_formula = ""
    with open(path) as p:
        list_of_rules = p.read().strip().split("\n")
    for rule_index in range(len(list_of_rules)):
        rule_split = list_of_rules[rule_index].strip().split(":-")
        head = rule_split[0].strip()
        body_atoms = rule_split[1].strip().split(",")
        if len(body_atoms) == 2:
            body = f"({body_atoms[0].strip()} & {body_atoms[1].strip()})"
        else:
            body = body_atoms[0].strip()
        rule = f"G({body} -> {head})"
        if rule_index < len(list_of_rules) - 1:
            output_program_formula += f"{rule} & "
        else:
            output_program_formula += rule
    return output_program_formula


def dataset_and_program_to_ltl(path_1, path_2):
    dataset = dataset_to_ltl(path_1)
    program = program_to_ltl(path_2)
    return f"{dataset} & {program}\n"

def clean_trace(trace):
    for timepoint in trace:
        trace[timepoint] = list(set(trace[timepoint]))
        trace[timepoint].sort()
        trace = dict(sorted(trace.items()))
    # empty_timepoints = []
    # for timepoint in trace:
    #     if not trace[timepoint]:
    #         empty_timepoints.append(timepoint)
    # for timepoint in empty_timepoints:
    #     del trace[timepoint]
    return trace


def adjust_trace(trace):
    trace = adjust_x(trace)
    trace = adjust_g(trace)
    trace = clean_trace(trace)
    return trace


def adjust_g(trace):
    for timepoint_1 in trace:
        for atom in trace[timepoint_1]:
            if "G" in atom:
                if atom.strip("G") in trace[timepoint_1]:
                    trace[timepoint_1].remove(atom.strip("G"))
                for timepoint_2 in trace:
                    if timepoint_2 > timepoint_1 and \
                            (atom in trace[timepoint_2] or atom.strip("G") in trace[timepoint_2]):
                        if atom in trace[timepoint_2]:
                            trace[timepoint_2].remove(atom)
                        if atom.strip("G") in trace[timepoint_2]:
                            trace[timepoint_2].remove(atom.strip("G"))
    for timepoint_1 in reversed(sorted(trace.keys())):
        for atom in trace[timepoint_1]:
            if "G" in atom:
                for timepoint_2 in trace:
                    if timepoint_2 == timepoint_1 - 1 and atom.strip("G") in trace[timepoint_2]:
                        trace[timepoint_1].remove(atom)
                        trace[timepoint_2].remove(atom.strip("G"))
                        trace[timepoint_2].append(atom)
    return trace


def adjust_x(trace):
    aux_trace = {}
    for timepoint_1 in trace:
        for atom in trace[timepoint_1]:
            if "X" in atom:
                trace[timepoint_1].remove(atom)
                if timepoint_1 + 1 in trace:
                    trace[timepoint_1 + 1].append(atom.strip("X"))
                elif timepoint_1 + 1 in aux_trace:
                    aux_trace[timepoint_1 + 1].append(atom.strip("X"))
                else:
                    aux_trace[timepoint_1 + 1] = [atom.strip("X")]
    for timepoint in aux_trace:
        trace[timepoint] = aux_trace[timepoint]
    return trace


def apply_rules(program, trace):
    aux_trace = {}
    aux_trace = apply_rules_type_1(program, trace, aux_trace)
    aux_trace = apply_rules_type_2(program, trace, aux_trace)
    aux_trace = apply_rules_type_3(program, trace, aux_trace)
    aux_trace = apply_rules_type_4(program, trace, aux_trace)
    aux_trace = apply_rules_type_5(program, trace, aux_trace)
    trace = merge_traces(trace, aux_trace)
    trace = adjust_trace(trace)
    return trace


def apply_rules_type_1(program, trace, aux_trace):
    for rule in program.rules_type_1:
        for timepoint in trace:
            if rule["b"][0] in trace[timepoint]:
                aux_trace = augment_trace(aux_trace, timepoint + 1, rule["h"].strip("X"))
            if "G" + rule["b"][0] in trace[timepoint]:
                aux_trace = augment_trace(aux_trace, timepoint + 1, "G" + rule["h"].strip("X"))
                break
    return aux_trace


def apply_rules_type_2(program, trace, aux_trace):
    for rule in program.rules_type_2:
        for timepoint in trace:
            if rule["b"][0].strip("X") in trace[timepoint] and timepoint > 0:
                aux_trace = augment_trace(aux_trace, timepoint - 1, rule["h"])
            if "G" + rule["b"][0].strip("X") in trace[timepoint] and timepoint > 0:
                aux_trace = augment_trace(aux_trace, timepoint - 1, "G" + rule["h"])
                break
    return aux_trace


def apply_rules_type_3(program, trace, aux_trace):
    for rule in program.rules_type_3:
        for timepoint in trace:
            if rule["b"][0] in trace[timepoint] or "G" + rule["b"][0] in trace[timepoint]:
                aux_trace = augment_trace(aux_trace, timepoint, rule["h"])
                break
    return aux_trace


def apply_rules_type_4(program, trace, aux_trace):
    for rule in program.rules_type_4:
        for timepoint in trace:
            if rule["b"][0] in trace[timepoint]:
                aux_trace = augment_trace(aux_trace, timepoint, "G" + rule["h"])
                break
    return aux_trace


def apply_rules_type_5(program, trace, aux_trace):
    for rule in program.rules_type_5:
        atom_1 = False
        atom_2 = False
        for timepoint in trace:
            if "G" + rule["b"][0] in trace[timepoint]:
                atom_1 = True
            if "G" + rule["b"][1] in trace[timepoint]:
                atom_2 = True
            if (rule["b"][0] in trace[timepoint] and rule["b"][1] in trace[timepoint]) or (atom_1 and rule["b"][1] in trace[timepoint]) or (rule["b"][0] in trace[timepoint] and atom_2):
                aux_trace = augment_trace(aux_trace, timepoint, rule["h"])
            if atom_1 and atom_2:
                aux_trace = augment_trace(aux_trace, timepoint, "G" + rule["h"])
                break
    return aux_trace


def merge_traces(trace_1, trace_2):
    for timepoint in trace_2:
        if timepoint in trace_1:
            trace_1[timepoint] += trace_2[timepoint]
        else:
            trace_1[timepoint] = trace_2[timepoint]
    return trace_1


def augment_trace(trace, timepoint, atom):
    if timepoint in trace:
        trace[timepoint].append(atom)
    else:
        trace[timepoint] = [atom]
    return trace


def amend_trace(program, trace, minimum, maximum):
    g_atoms = []
    trace_aux = {}
    for timepoint in range(minimum + 1, maximum + 3):
        if timepoint not in trace:
            trace_aux[timepoint] = []
    for timepoint in trace:
        for atom in trace[timepoint]:
            if "G" in atom:
                g_atoms.append(atom)
                trace[timepoint].append(atom.strip("G"))
                for timepoint_aux in trace_aux:
                    if timepoint_aux > timepoint:
                        trace_aux[timepoint_aux].append(atom)
                        trace_aux[timepoint_aux].append(atom.strip("G"))
        for atom in g_atoms:
            if atom not in trace[timepoint]:
                trace[timepoint].append(atom)
            if atom.strip("G") not in trace[timepoint]:
                trace[timepoint].append(atom.strip("G"))
        if minimum + 1 < timepoint <= maximum + 2:
            for atom in trace[timepoint]:
                if "X" + atom in program.program_atoms:
                    if timepoint - 1 in trace_aux:
                        trace_aux[timepoint - 1].append("X" + atom)
                    else:
                        trace_aux[timepoint - 1] = ["X" + atom]
    return merge_traces(trace, trace_aux)

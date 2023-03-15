from copy import deepcopy
from trace import *
from time import time


def materialise(my_trace, my_program):
    start_time = time()
    i_max = max([timepoint for timepoint in my_trace])
    trace_1 = my_trace
    trace_2 = deepcopy(trace_1)
    print(f"Dataset: {trace_1}")
    counter = 0
    while True:
        counter += 1
        trace_2 = apply_rules(my_program, trace_2)
        print(f"ApplyRules^{counter}: {trace_2}")
        common_interval = compare_traces(trace_1, trace_2)
        if is_equal(trace_1, trace_2):
            trace_2 = extend_trace(trace_2)
        if find_period(my_program, trace_2, i_max, common_interval):
            period = find_period(my_program, trace_2, i_max, common_interval)
            if unfold_period(trace_2, period):
                for atom in unfold_period(trace_2, period):
                    trace_2[period[1] + 1].append("G" + atom)
                trace_2 = adjust_trace(trace_2)
                i_max = period[1] + 1
                print(f"Partial unfolding: {trace_2}")
                counter = 0
            else:
                optimization_factor = optimize_period(trace_2, period)
                period = [period[0] - optimization_factor, period[1] - optimization_factor]
                print(f"Shortest representation of the IAT: {shortest_representation(trace_2, period)}")
                end_time = time()
                print(f"Runtime: {end_time - start_time}s")
                return [shortest_representation(trace_2, period), end_time - start_time]
        trace_1 = deepcopy(trace_2)


def compare_traces(trace_1, trace_2):
    timeline_1 = [timepoint for timepoint in trace_1]
    timeline_2 = [timepoint for timepoint in trace_2]
    min_different_timepoint = min(set(timeline_1).symmetric_difference(set(timeline_2)), default=max(timeline_1) + 1)
    common_timeline = [timepoint for timepoint in timeline_1 if timepoint < min_different_timepoint]
    for timepoint in common_timeline:
        if trace_1[timepoint] != trace_2[timepoint]:
            timepoint -= 1
            return timepoint
    return max(common_timeline, default=-1)


def is_equal(trace_1, trace_2):
    timeline_1 = [timepoint for timepoint in trace_1]
    timeline_2 = [timepoint for timepoint in trace_2]
    if timeline_1 != timeline_2:
        return False
    else:
        for timepoint in timeline_1:
            if trace_1[timepoint] != trace_2[timepoint]:
                return False
    return True


def extend_trace(trace):
    max_timepoint = max([timepoint for timepoint in trace])
    trace[max_timepoint + 1] = []
    return trace


def find_period(my_program, my_trace, my_min, my_max):
    my_trace_aux = deepcopy(my_trace)
    my_trace_aux = amend_trace(my_program, my_trace_aux, my_min, my_max)
    for timepoint_2 in range(my_min + 2, my_max + 2):
        for timepoint_1 in range(my_min + 1, timepoint_2):
            if set(my_trace_aux[timepoint_1]) == set(my_trace_aux[timepoint_2]):
                return [timepoint_1, timepoint_2 - 1]
    return None


def unfold_period(my_trace, my_period):
    unfolded_atoms = [atom for atom in my_trace[my_period[0]] if "G" not in atom]
    for timepoint in my_period:
        if timepoint in my_trace:
            unfolded_atoms = [atom for atom in unfolded_atoms if atom in my_trace[timepoint]]
        else:
            unfolded_atoms = []
            break
    return unfolded_atoms


def optimize_period(my_trace, my_period):
    optimization_factor = 0
    for decrement in range(1, my_period[0] + 1):
        if my_period[0] - decrement not in my_trace and my_period[1] + 1 - decrement not in my_trace:
            optimization_factor = decrement
        elif my_period[0] - decrement in my_trace and my_period[1] + 1 - decrement in my_trace:
            prop_atoms = [atom for atom in my_trace[my_period[0] - decrement] if "G" not in atom]
            g_atoms = [atom for atom in my_trace[my_period[0] - decrement] if "G" in atom]
            if set(prop_atoms) == set(my_trace[my_period[1] + 1 - decrement]):
                optimization_factor = decrement
            if g_atoms:
                break
        else:
            break
    return optimization_factor


def shortest_representation(my_trace, my_period):
    representation = {timepoint: [] for timepoint in range(my_period[1] + 1)}
    g_list = []
    for timepoint in representation:
        if timepoint in my_trace:
            for atom in my_trace[timepoint]:
                if "G" not in atom:
                    representation[timepoint].append(atom)
                else:
                    representation[timepoint].append(atom.strip("G"))
                    g_list.append(atom)
            for atom in g_list:
                if atom.strip("G") not in representation[timepoint]:
                    representation[timepoint].append(atom.strip("G"))
    offset = {timepoint: representation[timepoint] for timepoint in representation if timepoint < my_period[0]}
    period = {timepoint: representation[timepoint] for timepoint in representation if timepoint >= my_period[0]}
    return {"offset": offset, "period": period}

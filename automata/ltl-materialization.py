import spot
import buddy
from IPython.display import display
from spot.jupyter import display_inline
import multiprocessing
import time
import csv

TIMEOUT = 10
HORN_BENCHMARKS = "benchmarks/LTLbenchmarks.csv"
HORN_RESULTS = "benchmarks/automata_results.csv"
LTL_BENCHMARKS = "benchmarks/ltl-{}.ltl"
LTL_RESULTS = "ltl-{}-results.csv"
LTL_LENGTHS = "ltl-{}-lengths.csv"

# Takes an automaton as input and returns array indicating whether language at given state is non-empty
def non_empty_states(a):
    s_init = a.get_init_state_number();
    nes = [False] * a.num_states()
    
    for s in range(0, a.num_states()):
        a.set_init_state(s)
        if not a.is_empty():
            nes[s] = True

    a.set_init_state(s_init)

    return nes


# Takes an automaton, a list indicating non-emptiness and a set of states as input and returns the set of all successor states that have non-empty language and a BDD representing the intersection of all labels leading to those successor states
def compute_successors(a, nes, ss):
    ssn = set()

    cond = buddy.bddtrue
    count = 0
    
    for e in [e for e in a.edges() if e.src in ss and nes[e.dst]]:
        count = count + 1
        ssn.add(e.dst)
        cond = buddy.bdd_and(cond, e.cond)

    if cond == buddy.bddtrue:
        cond = buddy.bddfalse

    return (frozenset(ssn), cond)


# Computes the materialization of the language of a Buchi automaton
def materialize_ba(a):
    cntr = 0
    ss = frozenset(set([a.get_init_state_number()]))
    s_dict = { ss : cntr }
    nes = non_empty_states(a)
    trace = []

    while True:
        (ssn, cond) = compute_successors(a, nes, ss)
        trace.append(cond)
        
        if not(ssn in s_dict):
            cntr = cntr + 1
            s_dict[ssn] = cntr
            ss = ssn
        else:
            return (trace[:s_dict[ssn]], trace[s_dict[ssn]:])

# Prints the ultimately periodic word            
def print_segments(i_segment, p_segment):
    si_segment = list(spot.bdd_format_formula(a.get_dict(), cond)\
                      for cond in i_segment)
    sp_segment = list(spot.bdd_format_formula(a.get_dict(), cond)\
                          for cond in p_segment)     
    print ("u = ", end="")
    print (*si_segment, sep=" ", end="  ")
    print ("w = ", end="")
    print (*sp_segment, sep=" ")


# Takes an LTL formula as input and computes its materialization
# If LTL formula is unsatisfiable no computation is performed
def materialize_ltl(ltl_formula):
    a = spot.translate(ltl_formula, 'Buchi', 'state-based', 'complete')
    if not(a.is_empty()):
        (i_segment, p_segment) = materialize_ba(a)

# Takes LTL benchmark file as input and returns array containing all LTL formulas
def load_ltl_benchmark(filename):
    my_file = open(filename, 'r')
    formulas = [s.strip() for s in  my_file.readlines()]
    indices = list(range(1, len(formulas)+1))
    return dict(zip(indices,formulas))

# Loads a Horn benchmark CSV file
def load_horn_benchmark(filename):
    formulas = {}
    sizes = {}

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)

        cntr = 0
        for row in reader:
            if cntr == 0:
                cntr = 1
                continue
            formulas[row[0]] = row[1]
            sizes[row[0]] = row[2]

    return (formulas, sizes)


# Benchmarking subroutine
def perform_benchmarks(formulas):
    times = {}

    for key in formulas:
        print(key)
        benchmark = formulas[key]
        p = multiprocessing.Process(target=materialize_ltl, args=(benchmark,))
        p.start()
        p.join(TIMEOUT)
        if p.is_alive():
            p.kill()
            times[key] = "timeout"
        else:
            start_time = time.perf_counter()
            for i in range(10):
                materialize_ltl(benchmark)
            end_time = time.perf_counter()
            times[key] = (end_time - start_time) / 10

    return times

# Returns a dictionary of the lengths of benchmark formulas
def compute_lengths(benchmarks):
    sizes = {}
    for key in benchmarks:
        sizes[key] = len(benchmarks[key])
    return sizes

def write_csv(fname, benchmarks):
    with open("benchmarks/{}".format(fname), "w") as result_file:
        for key in benchmarks:
            result_file.write("{},{}\n".format(key, benchmarks[key]))

spot.setup()


####### Run Horn benchmarks ########
(formulas, sizes) = load_horn_benchmark(HORN_BENCHMARKS)
horn_benchmarks = perform_benchmarks(formulas)
with open(HORN_RESULTS, "w") as result_file:
    for key in horn_benchmarks:
        result_file.write("{},{}\n".format(key,horn_benchmarks[key]))

        
####### Run LTL benchmarks ########
for i in range(1,6):
    benchmarks = load_ltl_benchmark(LTL_BENCHMARKS.format(i))
    write_csv(LTL_BENCHMARKS.format(i), perform_benchmarks(benchmarks))
    write_csv(LTL_LENGTHS.format(i), compute_lengths(benchmarks))

    
#materialize_ltl('(G(p -> XXXXp) | G(p -> XXXXXXXp)) & XXXXp')

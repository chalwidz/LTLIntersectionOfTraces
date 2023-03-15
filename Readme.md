# Materialisation-based generation of the intersection of all traces for an LTL Horn formula

This folder contains an implementation of a materialisation-based algorithm calculating the shortest representation of the intersection of all traces satisfying a given Horn formula of linear temporal logic (LTL).

## Running the program
The folder is self-contained and does not require pre-installing any packages. In order to run the algorithm, the user needs to type:

    FOLDER_PATH>python main.py
After starting the program, the user will be asked to provide the names of files containing a program and a dataset for which they want to sythesise the intersection of all traces:

    Name of the file with the program:
	Name of the file with the dataset:
These names should refer to *.txt* files stored in the folders *programs* and *datasets*, respectively. When given the file names, the program outputs the shortest representation of the intersection of all traces alongside all intermediate steps of materialisation and unfolding. For example, with the following input:

    Name of the file with the program: program3.txt
	Name of the file with the dataset: data3.txt
the program will produce the following output:

    Dataset: {0: ['p']}
	ApplyRules^1: {0: ['p'], 1: ['p']}
	ApplyRules^2: {0: ['p'], 1: ['p'], 2: ['p']}
	ApplyRules^3: {0: ['p'], 1: ['p'], 2: ['p'], 3: ['p']}
	Partial unfolding: {0: ['Gp'], 1: [], 2: [], 3: []}
	ApplyRules^1: {0: ['Gp', 'Gq'], 1: [], 2: [], 3: []}
	ApplyRules^2: {0: ['Gp', 'Gq', 'Gs'], 1: [], 2: [], 3: []}
	ApplyRules^3: {0: ['Gp', 'Gq', 'Gs', 'Gt'], 1: [], 2: [], 3: []}
	ApplyRules^4: {0: ['Gp', 'Gq', 'Gs', 'Gt', 'Gu'], 1: [], 2: [], 3: []}
	ApplyRules^5: {0: ['Gp', 'Gq', 'Gs', 'Gt', 'Gu'], 1: [], 2: [], 3: []}
	ApplyRules^6: {0: ['Gp', 'Gq', 'Gs', 'Gt', 'Gu'], 1: [], 2: [], 3: [], 4: []}
	Shortest representation of the IAT: {'offset': {}, 'period': {0: ['p', 'q', 's', 't', 'u']}}
	Runtime: 0.003988027572631836s
where *program3.txt* contains:

    Xp :- p  
	q :- Gp  
	s :- p, q  
	Xs :- s  
	t :- s, s  
	u :- t, s
and the content of *data3.txt* is:

    p@0
Currently the folders *programs* and *datasets* contain 100 files each.
## Inputting new programs and datasets   
The materialisation-based algorithm for generating the (shortest representation of the) intersection of all traces works for LTL-Horn formulas in *normal form* which mention only $\mathsf{X}$ and $\mathsf{G}$ among temporal operators, that is, formulas being conjunctions of *facts* of the form:
$$\mathsf{X}^k p$$
and *rules* which can be of one of the following forms:
$$\mathsf{G}(p\to\mathsf{X}q)\qquad\mathsf{G}(\mathsf{X}p\to q)\qquad\mathsf{G}(p\to\mathsf{G}q)\qquad\mathsf{G}(\mathsf{G}p\to q)\qquad\mathsf{G}((p\land q)\to r),$$
where $k\in\mathbb{N}$ and $p,q,r$ are propositional atoms.
All the facts occurring in an LTL-Horn formulas are called a *dataset* and all the rules are called a *program*.

If the user wants to propose their own program and/or dataset to test, they need to create a *.txt* file in the folder *programs* and/or *datasets* and then input its name when prompted. Program files should contain rules put in separate lines. Each rule should be of one of the forms:

    Xq :- p
    q :- Xp
    Gq :- p
    q :- Gp
    r :- p, r
X and G are the *next* and *going to* operator, respectively, and p, q, r are propositional atoms. A rule that does not follow any of the above patterns will be ignored by the program. Propositional atom can be represented by any string of symbols excluding 'X', 'G', ',' and blank space.
Dataset files should contain facts put in separate lines. Each fact should be of the form

    p@n
where p is a propositional atom and n is a non-negative interger indicating the time point at which the propositional atom holds. For instance, the following facts are well formed:

    p@0
    r4@29
    q0@17

whereas the syntax of the following ones is invalid:

    p@-2
    q 5@10


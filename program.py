class Program:
    def __init__(self, path):
        self.path = path
        self.program = self.read_input()
        self.rules_type_1 = []
        self.rules_type_2 = []
        self.rules_type_3 = []
        self.rules_type_4 = []
        self.rules_type_5 = []
        self.program_atoms = []
        self.extract_program()

    def read_input(self):
        with open(self.path) as i:
            program = i.read().strip().split("\n")
        return program

    def extract_program(self):
        program_parsed = []
        for rule in self.program:
            program_parsed.append({"h": rule.split(":-")[0].strip(),
                                   "b": [atom.strip() for atom in rule.split(":-")[1].split(",")]})
        for rule in program_parsed:
            if rule["h"].count("X") == 1 and rule["h"].count("G") == 0 and rule["h"].count(" ") == 0 and len(rule["b"]) == 1 and rule["b"][0].count("X") == 0 and rule["b"][0].count("G") == 0 and rule["b"][0].count(" ") == 0 and rule not in self.rules_type_1:
                self.rules_type_1.append(rule)
            elif rule["h"].count("X") == 0 and rule["h"].count("G") == 0 and rule["h"].count(" ") == 0 and len(rule["b"]) == 1 and rule["b"][0].count("X") == 1 and rule["b"][0].count("G") == 0 and rule["b"][0].count(" ") == 0 and rule not in self.rules_type_2:
                self.rules_type_2.append(rule)
            elif rule["h"].count("X") == 0 and rule["h"].count("G") == 1 and rule["h"].count(" ") == 0 and len(rule["b"]) == 1 and rule["b"][0].count("X") == 0 and rule["b"][0].count("G") == 0 and rule["b"][0].count(" ") == 0 and rule not in self.rules_type_3:
                self.rules_type_3.append(rule)
            elif rule["h"].count("X") == 0 and rule["h"].count("G") == 0 and rule["h"].count(" ") == 0 and len(rule["b"]) == 1 and rule["b"][0].count("X") == 0 and rule["b"][0].count("G") == 1 and rule["b"][0].count(" ") == 0 and rule not in self.rules_type_4:
                self.rules_type_4.append(rule)
            elif len(rule["b"]) == 2 and rule["h"].count("X") == 0 and rule["h"].count("G") == 0 and rule["h"].count(" ") == 0 and rule["b"][0].count("X") == 0 and rule["b"][0].count("G") == 0 and rule["b"][0].count(" ") == 0 and rule["b"][1].count("X") == 0 and rule["b"][1].count("G") == 0 and rule["b"][1].count(" ") == 0 and rule not in self.rules_type_5:
                self.rules_type_5.append(rule)
            if rule["h"] not in self.program_atoms:
                self.program_atoms.append(rule["h"])
            for atom in rule["b"]:
                if atom not in self.program_atoms:
                    self.program_atoms.append(atom)
        self.program_atoms.sort()

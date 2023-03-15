from trace import *


class DataSet:
    def __init__(self, path):
        self.path = path
        self.data = self.read_input()
        self.trace = self.extract_trace()

    def read_input(self):
        with open(self.path) as i:
            data = i.read().strip().split("\n")
        return data

    def extract_trace(self):
        timeline = list(set([int(fact.split("@")[1].strip()) for fact in self.data]))
        trace = {timepoint: [] for timepoint in timeline}
        for timepoint in trace:
            for fact in self.data:
                if int(fact.split("@")[1].strip()) == timepoint:
                    trace[timepoint].append(fact.split("@")[0].strip())
        trace = clean_trace(trace)
        return trace

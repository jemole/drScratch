"""This module provides plugins with clasic Sw Engineering metrics"""
import math
from collections import Counter
from hairball.plugins import HairballPlugin


class CyclomaticComplexity(HairballPlugin):

    """Plugin that calculates the Cyclomatic Complexity of a project."""

    def __init__(self):
        super(CyclomaticComplexity, self).__init__()
        self.cc = []
        self.total = 0

    def finalize(self):
        """
            Output the Cyclomatic Complexity results.
            CC = number of conditions + 1
        """
        print("Total Cyclomatic Complexity: %i" % self.total)
        #average =  float (self.total) / len(self.cc)
        #print ("Average Cyclomatic Complexity: %.2f" % average)
        #print ("Cyclomatic Complexity by script:")
        #print self.cc

    def analyze(self, scratch):
        """Run and return the results from the CyclomaticComplexity plugin."""
        conditionals = (['if %s then%s', 'repeat until %s%s',
            'wait until %s', '%s and %s', '%s or %s'])
        for script in self.iter_scripts(scratch):
            conditions = 0
            for name, _, _ in self.iter_blocks(script.blocks):
                if name in conditionals:
                    conditions += 1
                elif name == 'if %s then%selse%s':
                    conditions +=2
            self.cc.append(conditions + 1)
            self.total += conditions +1

class Halstead(HairballPlugin):

    """Plugin that calculates the Halstead complexity measures of a project."""

    def __init__(self):
        super(Halstead, self).__init__()
        self.operators = Counter()
        self.operands = Counter()
        self.n = 0
        self.N = 0
        self.V = 0
        self.D = 0
        self.E = 0
        self.T = 0

    def finalize(self):
        """Output the Halstead complexity measures results."""
        print ("Program vocabulary: %i" % self.n)
        print ("Program length: %i" % self.N)
        print ("Volume: %.2f" % self.V)
        print ("Difficulty: %.2f" % self.D)
        print ("Effort: %.2f" % self.E)
        print ("Time required to program: %.2f seconds = %.2f minutes"  %
            (self.T, self.T / float (60)))



    def analyze(self, scratch):
        """Run and return the results from the Halstead plugin."""
        file_operators = Counter()
        file_operands = Counter()
        for script in self.iter_scripts(scratch):
            for name, _, arguments in self.iter_blocks(script.blocks):
                file_operators[name] += 1
                for arg in arguments.args:
                    if (not (type (arg) is list) and
                        'kurt' not in str(type(arg))):
                        file_operands[arg] += 1
        N1 = sum(file_operators.values())
        N2 = sum(file_operands.values())
        n1 = len(file_operators.values())
        n2 = len(file_operands.values())
        self.n = n1 + n2
        self.N = N1 + N2
        self.V = float(self.N) * math.log(self.n, 2)
        self.D = n1/ float (2) * (N2/float (n2))
        self.E = float (self.V * self.D)
        self.T = float (self.E / 18)

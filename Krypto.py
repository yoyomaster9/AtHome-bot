import itertools

###############################################################
#
# Outline
# =======
# 1- Input numbers and target
# 2- Permute numbers, set all permutations to list
# 3- Permute operations, set all permutations to list
# 4- For each permutations of number & operations, generate list
#    of expressions under 14 paranthesis permutations
# 5- Run eval() over each string generated in previous step
# 6- Check if any of the eval() functions returned target card
# 7- Output solution string
#
# NOTE:
# Based on the Catalan number, C_4, there are 14 different ways to
# have paranthesis on an expression with 5 terms
#
# SOURCE:
# https://www.johndcook.com/blog/2013/10/03/parenthesize-expression-catalan/
#
###############################################################



class Q:
    def __init__(self, n, d = 1):
        self.n = n
        self.d = d
        self.reduce()

    def __add__(self, other):
        n = (self.n * other.d) + (self.d * other.n)
        d = self.d * other.d
        return Q(n, d)

    def __sub__(self, other):
        other.n = -other.n
        return self + other

    def __mul__(self, other):
        n = self.n * other.n
        d = self.d * other.d
        return Q(n, d)

    def __truediv__(self, other):
        other.n, other.d = other.d, other.n
        return self * other

    def reduce(self):
        a = max(self.n, self.d)
        b = min(self.n, self.d)
        while b:
            a, b = b, a % b
        a = abs(a)
        self.n = self.n // a
        self.d = self.d // a

    def __str__(self):
        if self.d == 1:
            return 'Q({})'.format(self.n)
        else:
            return 'Q({}, {})'.format(self.n, self.d)

    def __eq__(self, other):
        if self.n == other.n and self.d == other.d:
            return True
        else:
            return False

    def print(self):
        if self.d == 1:
            return '{}'.format(self.n)
        else:
            return '{}/{}'.format(self.n, self.d)



# Generate list of possible expressions
def GenerateExpressions(n, op):
    Expressions = [
    "{} {} ( {} {} ( {} {} ( {} {} {} )))".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "{} {} ( {} {} (( {} {} {} ) {} {} ))".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "{} {} (( {} {} {} ) {} ( {} {} {} ))".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "{} {} (( {} {} ( {} {} {} )) {} {} )".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "{} {} ((( {} {} {} ) {} {} ) {} {} )".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "( {} {} {} ) {} ( {} {} ( {} {} {} ))".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "( {} {} {} ) {} (( {} {} {} ) {} {} )".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "( {} {} ( {} {} {} )) {} ( {} {} {} )".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "( {} {} ( {} {} ( {} {} {} ))) {} {}".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "( {} {} (( {} {} {} ) {} {} )) {} {}".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "(( {} {} {} ) {} {} ) {} ( {} {} {} )".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "(( {} {} {} ) {} ( {} {} {} )) {} {}".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "(( {} {} ( {} {} {} )) {} {} ) {} {}".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4]),
    "((( {} {} {} ) {} {} ) {} {} ) {} {}".format(n[0], op[0], n[1], op[1], n[2], op[2], n[3], op[3], n[4])
    ]
    return Expressions



# Evaluate each expression
def Solver(NUMBERS, TARGET, StopAfterSolution = True):
    trial = 0
    Solutions = [] # list containing all solutions

    # Permute operations
    OPERATIONS = list(itertools.product(['+', '-', '*', '/'], repeat = 4))
    # OPERATSIONS is the list of all permutations of operations

    for n in NUMBERS:
        for op in OPERATIONS:
                Expressions = GenerateExpressions(n, op)
                for exp in Expressions:
                    trial += 1
                    try:
                        x = eval(exp)
                    except ZeroDivisionError:
                        x = -1
                    if x == TARGET:
                        Solutions.append({'trial': trial, 'exp': exp})
                        if StopAfterSolution:
                            return Solutions
    return Solutions

def StrToQ(s):
    s = s.split('/')
    if len(s) == 1:
        return Q(int(s[0]))
    else:
        return Q( int(s[0]) , int(s[1]))

def InterpretSolution(s):
    s = s.replace('/', '÷')
    for i in range(s.count('Q')): # Fix to # of Q's in string
        start = s.index('Q')
        end = s.index(')', start)
        sub = s[start:end+1]
        x = eval(sub).print()
        s = s.replace(sub, x, 1)
    return s

def Main(s): # s will be string of 5 numbers followed by the solution
    s = s.replace(' ', '')
    NUMBERS = []
    for x in s.split(','):
        NUMBERS.append(StrToQ(x))

    TARGET = NUMBERS.pop()

    # Permute numbers
    NUMBERS = list(itertools.permutations(NUMBERS))
    # NUMBERS is the list of all permutations of NUMBERS

    StopAfterSolution = True
    try:
        Solutions = Solver(NUMBERS, TARGET, StopAfterSolution)
        Solution = '{} = {}'.format(Solutions[0]['exp'], TARGET)
        return InterpretSolution(Solution)
    except:
        return False

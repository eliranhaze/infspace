from itertools import product

from formula import *

class Expressions(object):

    FIRST_VAR = 'p'

    def __init__(self, size=2):
        self.size = size
        self.variables = self._get_vars()
        self.all_assignments = self._get_assignments()
        self._init_expressions()

    def _init_expressions(self):
        values = list(_truth_values(self.size))
        supervalues = list(_truth_values(len(values)))
        known = self._get_known()
        exp = {}
        self.expressions = []
        for superval in supervalues:
            known_e = known.get(superval)
            if known_e:
                exp[superval] = known_e
                continue
            disjuncts = []
            for i, is_true in enumerate(superval):
                atoms = []
                if is_true:
                    for j, var in enumerate(self.variables):
                        if values[i][j]:
                            atom = var
                        else:
                            atom = '~'+var
                        atoms.append(atom)
                    disjuncts.append('(%s)' % '&'.join(atoms))
            expression = 'v'.join(disjuncts) if disjuncts else self.FIRST_VAR+'&~'+self.FIRST_VAR
            exp[superval] = expression

        expset = set()
        been = set()
        for superval, e in exp.iteritems():
            if e in been:
                continue
            opp = tuple(not v for v in superval)
            chosen = min(e, exp[opp], key=lambda x: len(x))
            expset.add(chosen)
            been.add(e)
            been.add(exp[opp])
        self.expressions = list(expset)
    def _get_known(self):
        combs = self._get_var_combinations()
        exp = []
        for comb in combs:
            exp.append('&'.join(comb))
            exp.append('v'.join(comb))
            exp.append('='.join(comb))
            if len(comb) > 2:
                exp.append('='.join(['&'.join(comb[:2])]+list(comb[2:])))
                exp.append('='.join(['v'.join(comb[:2])]+list(comb[2:])))
                exp.append('&'.join(['v'.join(comb[:2])]+list(comb[2:])))
                exp.append('&'.join(['='.join(comb[:2])]+list(comb[2:])))
                exp.append('v'.join(['&'.join(comb[:2])]+list(comb[2:])))
                exp.append('v'.join(['='.join(comb[:2])]+list(comb[2:])))
#        more = set()
#        for e in exp:
#            if len(e) == 1:
#                continue
#            for e in exp:
#                if len(e) == 1:
#                    continue
#                for c in ('&', 'v', '='):
#                    more.add('(%s)%s(%s)' % (e, c, e))
#        exp += list(more)
        known = {}
        for e in exp:
            result = self._get_tt_result(e)
            prev_e = known.get(result)
            if not prev_e or len(e) < len(prev_e):
                known[result] = e
        return known

    def _get_var_combinations(self):
        atoms = [x+y for x, y in product(['','~'], self.variables)]
        return set(tuple(set(v)) for v in product(*((atoms,) * self.size)))

    def _get_tt_result(self, e):
        tt = TruthTable(Formula('p'))
        tt.variables = self.variables
        tt.values = tt._values(self.variables)
        return tuple(tt.result(assign_func=lambda a: evaluate(e, a)))

    def _get_vars(self):
        return [chr(ord(self.FIRST_VAR)+i) for i in xrange(self.size)]

    def _get_assignments(self):
        vals = _truth_values(self.size)
        a = []
        for val_row in vals:
            a.append({var: v for var, v in zip(self.variables, val_row)})
        return a

    def closer_to_than(self, x, y, dest):
        for a in self.all_assignments:
            for b1 in self.all_assignments:
                if evaluate(x, b1) == evaluate(x, a):
                    found = any((evaluate(y, a) == evaluate(y, b2)) and (evaluate(dest, b1) == evaluate(dest, b2)) for b2 in self.all_assignments)
                    if not found:
                        return False
        return True

def _truth_values(size):
    return product(*(((True, False),) * size))

def evaluate(f, assignment):
    """ only works with dnf """
    if 'v' in f:
        fs = f.split('v')
        return any(evaluate(f, assignment) for f in fs) 
    if '&' in f:
        fs = f.replace('(','').replace(')','').split('&')
        return all(evaluate(f, assignment) for f in fs)
    if '=' in f:
        fs = f.replace('(','').replace(')','').split('=')
        evs = [evaluate(f, assignment) for f in fs]
        return all(evs) or not any(evs)
    if f.startswith('~'):
        return not assignment[f[1]]
    return assignment[f]

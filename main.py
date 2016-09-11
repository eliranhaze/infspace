from itertools import product

import argparse
import sys

import expressions

def make_relations(expressions, e, relation):
    mapping = {}
    equivs = []
    i = 0
    for e1 in expressions:
        i += 1
        print '(%d/%d) %s' % (i, len(expressions), e1)
        for e2 in expressions:
            if e1 != e2 and not is_trans(e1, e2, mapping):
                if relation(e1, e2, e):
                    other_direction = relation(e2, e1, e)
                    if other_direction:
                        found = False
                        for eq in equivs:
                            if e1 in eq or e2 in eq:
                                eq.add(e1)
                                eq.add(e2)
                                found = True
                                break
                        if not found:
                            equivs.append({e1, e2})
                    else:
                        eset = mapping.setdefault(e1, set())
                        eset.add(e2)
#    equivs = []
#    for e1 in expressions:
#        for e2 in expressions:
#            if e1 != e2 and relation(e1, e2, e) and relation(e2, e1, e):
#                if {e1, e2} not in equivs:
#                    equivs.append({e1,e2})
    return mapping, equivs

def is_trans(e1, e2, mapping, indirect=False):
    if not e1 in mapping:
        return False
    if not indirect and e2 in mapping[e1]:
        return True
    return any(is_trans(e1_, e2, mapping) for e1_ in mapping[e1]) 

###################################################################################################
def main():
    print 'starting'

    args = get_args()

    size = args.size
    e = args.exp
    outfile = args.out if args.out else 'out/exp_%s_size%d.out' % (e, size)

    exp = expressions.Expressions(size)
    all_exps = exp.expressions

    print 'mapping'
    mapping, equivs = make_relations(all_exps, e, relation=exp.closer_to_than)
    print 'equivs', equivs

    print 'filtering'
    for f, f_list in mapping.iteritems():
        mapping[f] = [f_l for f_l in f_list if not is_trans(f, f_l, mapping, indirect=True)]

    print 'writing output:', outfile
    # PASTE OUTPUT TO: http://www.webgraphviz.com/
    with open(outfile, 'w') as out:
        out.write('digraph G {\n')
        out.write('  rankdir=BT;\n')
        out.write('  size="100,100";\n')
        out.write('  node [shape = box];\n')
        for i, equiv in enumerate(equivs):
            out.write('  subgraph cluster_%d {\n' % i)
            out.write('    color=blue;\n')
            for eq in equiv:
                out.write('    "%s";\n' % eq)
            out.write('  }\n')
        for f, f_list in mapping.iteritems():
          for f_l in f_list:
            out.write('  "%s" -> "%s"\n' % (f, f_l))
        out.write('}\n')

    print 'done'

###################################################################################################

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', dest='out')
    parser.add_argument('--size', type=int, dest='size', required=True)
    parser.add_argument('--exp', dest='exp', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()

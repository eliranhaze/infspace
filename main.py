from itertools import product
import sys

import expressions

def main():
  #################################################
  # EXPRESSIONS:
  e1 = '~p&~q'
  e2 = 'pvq'
  e  = 'p'
  #################################################
  
  print '==============================='
  print 'RESULT:', closer_to_than(e1, e2, e)
  print '==============================='

###################################################################################################
def main2(outfile):
  print 'outfile:', outfile
  print 'starting'
  size = 3
  exp = expressions.Expressions(size)
  fs = exp.expressions
  e = 'p&q&r'
  if not outfile:
      outfile = 'exp_%s_size%d.out' % (e, size)
  print 'outfile:', outfile
  print 'got expressions'
  def lvls2():
    cmps = {}
    i = 0
    for f1 in fs:
      i += 1
      print 'check (%d/%d) %s' % (i, len(fs), f1)
      for f2 in fs:
        if f1 != f2 and not is_trans(f1, f2, cmps):
          if exp.closer_to_than(f1, f2, e) and not exp.closer_to_than(f2, f1, e):
            fset = cmps.setdefault(f1, set())
            fset.add(f2)
    return cmps
  def is_trans(f1, f2, cmps, indirect=False):
      if not f1 in cmps:
          return False
      if not indirect and f2 in cmps[f1]:
          return True
      return any(is_trans(f1_, f2, cmps) for f1_ in cmps[f1]) 
  cmps = lvls2()
  print 'filtering'
  for f, f_list in cmps.iteritems():
      cmps[f] = [f_l for f_l in f_list if not is_trans(f, f_l, cmps, indirect=True)]
  print 'writing output'
  # PASTE OUTPUT TO: http://www.webgraphviz.com/
  with open(outfile, 'w') as out:
      out.write("digraph G {\n")
      out.write("rankdir=BT;\n")
      out.write("size=\"100,100\";\n")
      out.write("node [shape = box];\n")
      for f, f_list in cmps.iteritems():
        for f_l in f_list:
          out.write('"%s" -> "%s"\n' % (f, f_l))
      out.write("}\n")
  print 'done'
###################################################################################################

if __name__ == '__main__':
    main2(outfile=sys.argv[1] if len(sys.argv) > 1 else None)

import json
import os
import datetime

from equivalenceclasses import *

logStartTime = None
logPrefix = 'jail2Audrey'
printMessagesToConsole = True
logFileName = "*WHATEVER*"

def createLogFile():
  global logFileName
  global logStartTime
  if not os.path.exists("logs"):
    os.mkdir("logs")
  logStartTime = datetime.datetime.utcnow()
  startTimeString = logStartTime.strftime("%Y-%m-%d-%H-%M-%S")    
  logFileName = "logs/" + logPrefix + '-' + startTimeString


def logwrite (msg):
  global logFileName
  with open (logFileName, 'a') as logFile:
    # [2018/07/12, audrey] add conversion of logStartTime to a datetime.timedelta bc
    # otherwise python actually complains
    timeElapsed = datetime.datetime.utcnow() - logStartTime
    timedMsg = str(timeElapsed) + ': ' + str(msg)
    if printMessagesToConsole:
      print(timedMsg) 
    logFile.write(timedMsg + "\n")
# [2018/07/13] If a block is a math_compare, then it returns
# the mathematical symbol for what its operation is.
def compareOp(b):
  op = b['OP']
  if op == 'GT':
    return '>'
  elif op == 'LT':
    return '<'
  return op

# [2018/07/13] Gets the component type of a block. It also accounts for
# the few cases where screens are called "Form" instead.
def getComponentType(b):
  if 'component_type' in b:
    if b['component_type'] == 'Form':
      return 'Screen'
    return b['component_type']
  return ""

# [2018/07/16] helper function for determining whether
# a block is a math type or not.
# [2018/07/18] added a check for whether it's even a
# block or not
def isMathType(block):
  if isinstance(block, dict):
    if '*type' in block:
      return block['*type'].startswith('math')
  return False

# [2018/07/16] helper function for determining whether
# a block of type math is a function that is commutative
def isCommutative(mathBlock):
  if isMathType(mathBlock):
    commutatives = ['math_multiply', 'math_add']
    return mathBlock['*type'] in commutatives
  return False


def prettyPrint(obj):
  return json.dumps(obj, indent=2, separators=(',', ': '))

# [2018/07/13] Tests whether two blocks are equivalent.
def equivalent(a, b, depth=0):
  ''' a:       the first of the two blocks to be tested
      b:       the second of the two blocks to be tested
      depth:   optional, an argument for how nested the blocks
               that are being tested are. This is more useful for
               debugging this function.
  '''
  childBlocksKey = '~bodyStm'
  argsKey = '~args'
  branchesKey = '~branches'
  elseKey = '~branchofelse'
  expKey = '~bodyExp'
  #print depth, ":", getName(a) + "|" + getName(b)
  if not (isinstance(a, dict) and isinstance(b,dict)):
    return False
  if a['*type'] == b['*type']:
    #if a['*type'] == 'logic_boolean':
    #    if a['BOOL'] != b['BOOL']:
    #        print a['BOOL'], b['BOOL']
    t = True
    if expKey in a and expKey in b:
        return equivalent(a[expKey], b[expKey], depth + 1)
    # Check if a/b are if statements, and if they have branches
    if branchesKey in a and branchesKey in b:
      if len(a[branchesKey]) == len(b[branchesKey]):
        for i in range(len(a[branchesKey])):
          tmp = equivalent(a[branchesKey][i]['test'], b[branchesKey][i]['test'], depth)
          if not tmp:
            return False
          aThen = a[branchesKey][i]['then']
          bThen = b[branchesKey][i]['then']
          if len(aThen) == len(bThen):
            for j in range(len(aThen)):
              tmp = tmp and equivalent(aThen[j], bThen[j], depth + 1)
              if not tmp:
                return False
          else:
            return False
          t = t and tmp
      else:
        return False
    if elseKey in a and elseKey in b:
      if len(a[elseKey]) == len(b[elseKey]):
        for i in range(len(a[elseKey])):
          tmp = equivalent(a[elseKey][i], b[elseKey][i], depth + 1)
          if not tmp:
            return False
      else:
        return False
    elif elseKey in a or elseKey in b:
        # there's an else in only one of them, because the last if's test
        # failed
        return False
    # Check that the args of a and b are similar
    if argsKey in a and argsKey in b:
      if isCommutative(a):
        # then b is a commutative math type also because they have the same type
        if a['items'] != b['items']:
          return False
        aSorted = sorted(a[argsKey])
        bSorted = sorted(b[argsKey])
        for i in range(len(a[argsKey])):
          if not equivalent(a[argsKey][i], b[argsKey][i]):
            return False
        return True
      else:
          #print "hey"
          if len(a[argsKey]) == len(b[argsKey]):
            for i in range(len(a[argsKey])):
              #print a[argsKey][i]
              #print b[argsKey][i]
              tmp = equivalent(a[argsKey][i], b[argsKey][i], depth+1)
              if not tmp:
                return False
              t = t and tmp
          else:
            return False
    # Check that a and b have similar blocks contained within them
    if childBlocksKey in a and childBlocksKey in b:
      if len(a[childBlocksKey]) == len(b[childBlocksKey]):
        for i in range(len(a[childBlocksKey])):
          tmp = equivalent(a[childBlocksKey][i],b[childBlocksKey][i], depth+1)
          if not tmp:
            return False
          t = t and tmp
      else:
        return False
    elif childBlocksKey not in a and childBlocksKey not in b:
      #print depth, " leaf:", getName(a) + "|" +  getName(b)
      # Can just return true because if it got here without returning false, then
      # its args or whatever should be fine and this is a leaf
      return True
    return t
  return False


# [2018/07/13] Specifically renders the names for getName(of a block)
# when the block is some kind of math element. This is because many
# math elements have exactly two arguments, and have specific symbols
# for demonstrating what kind of operation is being done, so math
# gets its own function for displaying a block's name.
# [2018/07/18] Accounted for case where a string is somehow passed as
# a block.
def renderMathNames(b, depth=0):
  ''' b:     a block in the form of a Python dictionary/object
      depth: optional integer, used more specifically by the function's
             recursive nature to render parentheses around math
             expressions
  '''
  if isMathType(b):
    #print type(b), "\"" + str(b) + "\""
    t = b['*type']
    argsKey = '~args'
    args0 = ""
    args1 = ""
    begin = "" if depth < 1 else "("
    end = "" if depth < 1 else ")"
    if argsKey in b:
      if len(b[argsKey]) == 2:
        args0 = b[argsKey][0]
        args1 = b[argsKey][1]
    if t == 'math_multiply':
      return begin + renderMathNames(args0, depth + 1) + " x " + renderMathNames(args1, depth + 1) + end
    elif t == 'math_number':
      return b['NUM']
    elif t == 'math_subtract':
      return begin + renderMathNames(args0, depth + 1) + " - " + renderMathNames(args1, depth + 1) + end
    elif t == 'math_compare':
      return begin + renderMathNames(args0, depth + 1) + " " + compareOp(b) + " " + renderMathNames(args1, depth + 1) + end
    elif t == 'math_add':
      return begin + renderMathNames(args0, depth + 1) + " + " + renderMathNames(args1, depth + 1) + end
    return t
  return getName(b)

# [2018/07/13] Renders the name of a block in a format
# similar to that generated by ai2summarizer2.py. This is
# so that it is familiar to people who are familiar with the
# summarizer.
# This is the most useful for simply the printed output,
# because it renders the name nicely.
def getName(b):
  if isinstance(b, dict):
    t = b['*type']
    if 'NAME' in b:
      return b['NAME']
    elif t == 'component_event':
      return getComponentType(b) + "$" + b['instance_name'] + "." + b['event_name']
    elif t == 'component_set' or t == 'component_get':
      name = b['set_or_get'].capitalize() + " " + getComponentType(b)
      if 'instance_name' in b:
        return name + "$" + b['instance_name'] + "." + b['PROP']
      elif b['is_generic'] == 'true':
        return "Generic" + name + "." + b['PROP']
    elif t == 'logic_boolean':
      return "bool(" + b['BOOL'] + ")"
    elif t == 'text':
      if b['TEXT'] == None:
        return "text()"
      return "text(" + b['TEXT'].encode('utf-8') + ")"
    elif t == 'controls_if':
      return "if " + renderMathNames(b['~branches'][0]['test'])
    elif t.startswith('math'):
      logwrite("getName: {}".format(t))
      return renderMathNames(b)
    return t
  return b.encode('utf-8')

''' Wrapper function for testing whether different top blocks contain similar handlers.
'''
def compareBlocks(blks, num1, num2):
  return equivalent(blks[num1], blks[num2])


# [2018/07/12] Checks to see if at a minimum, blocks are not
# exact duplicates of each other.
def allAreUnique(c):
  for i in range(len(c)):
    for j in range(i+1, len(c)):
      if c[i] == c[j] and i != j:
        print i, j, c[i] == c[j]
#    #return True


# [2018/07/13] Tries to remove the IDs, as well as other random
# info that you may/may not want, from a block. This acts on the
# block itself. This includes the various tags from the body
# statements of a handler or other top block.
# [2018/07/16] Added support for handling the internal
# statements of an if, as well as its else branch, in addition to
# the args.
def removeIDs(thing, depth=0):
  childBlockKey = '~bodyStm'
  argsKey = '~args'
  branchesKey = "~branches"
  elseKey = '~branchofelse'
  if 'id' in thing:
    #print depth, thing.pop('id', 0)
    thing.pop('id', 0)
  if 'instance_name' in thing:
    thing.pop('instance_name', 0)
  if 'x' in thing and 'y' in thing:
    thing.pop('x', 0)
    thing.pop('y', 0)
  if childBlockKey in thing:
    #removeIDs(thing['params'], depth+1)
    for p in thing[childBlockKey]:
      # print p
      removeIDs(p, depth + 1)
  if argsKey in thing:
    for a in thing[argsKey]:
      removeIDs(a, depth + 1)
  if branchesKey in thing:
    for b in thing[branchesKey]:
      removeIDs(b['test'], depth + 1)
      for t in b['then']:
        removeIDs(t, depth + 1)
  if elseKey in thing:
    for e in thing[elseKey]:
      removeIDs(e, depth + 1)


#removeIDs(blocks[0], 0)


def size(b):
  childBlocksKey = "~bodyStm"
  total = 1
  if childBlocksKey in b:
    for child in b[childBlocksKey]:
      total += size(child)
  return total


# [2018/07/13] comparse all of the blocks against each other, while
# also accounting for never comparing the same pair twice.
def compareAllBlocks(blocks):
  #seen = []
  ecs = {}
  global diffDirectory
  diffDirectory = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")
  def checkNotIn(a, b):
    if a in ecs:
      return b not in ecs[a]
    elif b in ecs:
      return a not in ecs[b]
    return True

  for i in range(len(blocks)):
    for j in range(len(blocks)):
      if equivalent(blocks[i], blocks[j]) and i != j and checkNotIn(i, j):
        #seen.append((i,j))
        #seen.append((j,i))
        if i in ecs:
          #for k in ecs[i]:
          #    ecs[k].append(j)
          ecs[i].append(j)
        else:
          ecs[i] = [j]
        if j in ecs:
          #for 
          ecs[j].append(i)
        else:
          ecs[j] = [i]
        #print i, j, ":", getName(blocks[i]), getName(blocks[j]) #size(blocks[i]), size(blocks[j])
      elif checkNotIn(i, j) and not equivalent(blocks[i], blocks[j]):
        #seen.append((j,i))
        #seen.append((i,j))
        createDiff(blocks[i], blocks[j])
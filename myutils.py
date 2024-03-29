# 2019/07/19: Lyn made changes for today's B&B 2019 genericization deadline
# See [2019/07/19, lyn] notes below
import json
import os
import datetime

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Apparently this import line was just sitting here doing noTHING
#from equivalenceclasses import *

logStartTime = None
logPrefix = 'jail2Audrey'
printMessagesToConsole = True
logFileName = "*WHATEVER*"

actualColors = {
  "color_blue": "#0000ff",
  "color_white": "#ffffff",
  "color_red": "#ff0000",
  "color_green": "#00ff00",
  "color_pink": "#ffafaf",
  "color_cyan": "#00ffff",
  "color_magenta": "#ff00ff",
  "color_light_gray": "#cccccc",
  "color_gray": "#888888",
  "color_dark_gray": "#444444",
  "color_yellow": "#ffff00",
  "color_black": "#000000"
}

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
  mymsg = ""
  if not (isinstance(msg, str) or isinstance(msg, unicode)):
    print type(msg)
    mymsg = str(msg)
  else:
    mymsg = msg.encode("utf-8")
  with open (logFileName, 'a') as logFile:
    # [2018/07/12, audrey] add conversion of logStartTime to a datetime.timedelta bc
    # otherwise python actually complains
    timeElapsed = datetime.datetime.utcnow() - logStartTime
    timedMsg = str(timeElapsed) + ': ' + mymsg
    if printMessagesToConsole:
      print(timedMsg) 
    logFile.write(timedMsg + "\n")
    logFile.flush()

# [2019/01/14] Originally in abstraction.py, moved here since
# it's useful for the majority of analyses.
# It originally took a relative path or an absolute path, but
# it seems neither really mattered after all.
def getJail(jailLocation):
  #dirName = os.path.dirname
  # Upon further inspection, it appears that this line of code was not used at all?!?!?!
  #path = jailLocation if os.path.isabs(jailLocation) else os.path.join(dirName, jailLocation)
    jail = ""
    with open(jailLocation, "r") as f:
        jail = json.load(f)
    return jail

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
def isBoolean(block):
  if isADictionary(block):
    if getTypeKey() in block:
      tipe = block[getTypeKey()]
      return tipe == "logic_boolean" or tipe == "logic_false"
  return False
def isLogicType(block):
  typeKey = getTypeKey()
  if isADictionary(block) and typeKey in block:
    tipe = block[typeKey]
    return tipe.startswith('logic')
  return False
def isColorType(block):
  typeKey = getTypeKey()
  if isADictionary(block) and typeKey in block:
    return block[typeKey].startswith('color')
  return False
def isColorLiteral(block):
  typeKey = getTypeKey()
  if isADictionary(block) and typeKey in block:
    tipe = block[typeKey]
    return tipe != "color_make_color" and tipe != "color_split_color"
  return False
# [2018/07/16] helper function for determining whether
# a block of type math is a function that is commutative
def isCommutative(mathBlock):
  if isMathType(mathBlock):
    commutatives = ['math_multiply', 'math_add']
    return mathBlock['*type'] in commutatives
  return False

# [2019/07/19, lyn] New helper function:
def isProcedureCallType(block):
  typeKey = getTypeKey()
  if isADictionary(block) and typeKey in block:
    tipe = block[typeKey]
    return tipe in ['procedures_callnoreturn', 'procedures_callreturn']
  else :
    return False

# [2019/07/19, lyn] New helper function:
def isLexicaVariableType(block):
  typeKey = getTypeKey()
  if isADictionary(block) and typeKey in block:
    tipe = block[typeKey]
    return tipe in ['lexical_variable_get', 'lexical_variable_set']
  else:
    return False

# [2019/07/19, lyn] New helper function:
def isLocalDeclarationType(block):
  typeKey = getTypeKey()
  if isADictionary(block) and typeKey in block:
    tipe = block[typeKey]
    return tipe in ['local_declaration_statement','local_declaration_expression']
  else:
    return False

def isComponentBlock(block):
  if isinstance(block, dict):
    if '*type' in block:
      return block['*type'].startswith("component")
  return False

def isComponentEvent(block):
  if isADictionary(block):
    if hasTypeKey(block):
      return block[getTypeKey()] == "component_event"
  return False

# [2019/03/27] Essentially for convenience, so that I don't have to
#              remember what the type key actually is, just that it
#              exists.
def getTypeKey():
  return "*type"

def hasTypeKey(block):
  if isADictionary(block):
    return '*type' in block

def isGlobalDeclaration(block):
  if isADictionary(block):
    if hasTypeKey(block):
      return block['*type'] == "global_declaration"
  return False

def getBlockListKeys():
  return ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']

def getTagsToCheck():
  return ['test', '~bodyExp']

#[2019/09/07, audrey] moved this above, not sure how much order of functions
# matters in python but might as well, since this is used later
def getComponentBlockNameKeys():
  # Returns the keys that hold the name of the particular component block
  return ["instance_name", "COMPONENT_SELECTOR", "component_selector"] # [2019/07/19, lyn] lyn capitalized 2nd entry (don't know if really necessary)

"""Used for finding a comprehensive list of all of the component
   blocks' names used in a given block.

   Used in EquivalenceClass.isGenericifiable

   Returns a set.
"""
def findCompBlocks(blk):
  comps = set()
  # componentNameKeys = ["instance_name", "component_selector"]
  #componentNameKeys = ["instance_name", "COMPONENT_SELECTOR", "component_selector"] # [2019/07/19, lyn] lyn capitalized 2nd entry (don't know if really necessary)
  componentNameKeys = getComponentBlockNameKeys()
  
  if isComponentBlock(blk):
    for name in componentNameKeys:
      if name in blk:
        comps.add(blk[name])
        break
  for tag in getTagsToCheck():
    if tag in blk:
      # Take the union of comps and the additional comps
      comps.update(findCompBlocks(blk[tag]))
  for key in getBlockListKeys():
    if key in blk:
      for i in range(len(blk[key])):
        # Take the union of comps and the additional comps
        comps.update(findCompBlocks(blk[key][i]))
  return comps



def numCompBlocksInCommon(blockA, blockB):
  blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']
  tagsToCheck = ['test', '~bodyExp']
  count = 0
  
  if isComponentBlock(blockA) and isComponentBlock(blockB):
    # nameKeys = ["instance_name", "component_selector"]
    nameKeys = getComponentBlockNameKeys() #["instance_name", "COMPONENT_SELECTOR", "component_selector"] # [2019/07/19, lyn] lyn capitalized 2nd entry (don't know if really necessary) #[2019/09/07, audrey] just replaced with call to helper function....since I had the helper function anyway
    i = 0
    while count == 0 and i < len(nameKeys):
      name = nameKeys[i]
      if name in blockA and name in blockB and blockA[name] == blockB[name]:
        count += 1
      i += 1
  for tag in tagsToCheck:
    if tag in blockA and tag in blockB:
      count += numCompBlocksInCommon(blockA[tag], blockB[tag])
  for key in blockListKeys:
    if key in blockA and key in blockB and len(blockA[key]) == len(blockB[key]):
      for i in range(len(blockA[key])):
        count += numCompBlocksInCommon(blockA[key][i], blockB[key][i])
  return count

def smallDifference(setA, setB):
  diffAB = setA.difference(setB)
  diffBA = setB.difference(setA)
  return len(diffAB) <= 1 and len(diffBA) <= 1

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
  # [audrey, 2019/03/29] should actually check that these two
  # blocks have equivalent types, including the particular property
  # these two set, if they're a component_set kind of block.
  if checkTypeEquivalent(a, b):
    #if a['*type'] == b['*type']:
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
      if len(a[argsKey]) == len(b[argsKey]):
        if isCommutative(a):
          # then b is a commutative math type also because they have the same type
          if 'items' in a and 'items' in b:
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
          #if len(a[argsKey]) == len(b[argsKey]):
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
    try:
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
        return begin + renderMathNames(args0, depth + 1).encode("utf-8") + " " + compareOp(b) + " " + renderMathNames(args1, depth + 1).encode("utf-8") + end
      elif t == 'math_add':
        return begin + renderMathNames(args0, depth + 1) + " + " + renderMathNames(args1, depth + 1) + end
      return t
    except UnicodeDecodeError as e:
      print "UnicodeDecodeError happened!"
      print e
      print b
      return "??????"
  return getName(b)

def isColorBlock(b):
  if isADictionary(b):
    typeKey = "*type"
    if typeKey in b:
      t = b[typeKey]

      return t.startswith("color")
  return False

# [2019/01/16] Very related to renderColorNames
def getActualColorType(b):
  colorKey = 'COLOR'
  typeKey = '*type'
  if typeKey in b:
    if colorKey in b:
      t = b[typeKey]
      c = b[colorKey]

      if t in actualColors:

        # [2019/01/20] Switched around so that we just care if it's
        # a color or not.
        return "color_value"
        '''
        if c == actualColors[t]:
          return t
        elif c in actualColors.values():
          return actualColors.keys()[actualColors.values().index(c)]
        # [2019/01/20] Used to be "custom_color", but then it would
        # look like not a color type block to my function for
        # finding color-type blocks. It was also inconsistent with
        # the renderColorNames function below.
        return "color_custom"
        '''
      return t
    if isColorBlock(b):
      return b[typeKey]
  return "myutils::getActualColorType: no type key in block!"


# [2019/01/16] Renders the name of a color block correctly,
# since the type of a color block doesn't always indicate its
# actual color.
def renderColorNames(b):
  colorKey = 'COLOR'
  typeKey = '*type'
  
  if typeKey in b:
    if colorKey in b:
      t = b[typeKey]
      c = b[colorKey]
      if t in actualColors:
        # [2019/01/20] Just changed it to simply changing this to
        # "color_value" type instead of a specific color
        return "color_value"
        '''
        val = actualColors[t]
        if c == val:
          return t
        elif c in actualColors.values():
          return actualColors.keys()[actualColors.values().index(c)]
        else:
          return "color_custom:" + c
        '''
      else:
        return t
  return "myutils::renderColorNames: no type key in block!"

def isGeneric(b):
  if isComponentBlock(b):
    if "is_generic" in b:
      return b["is_generic"] == "true"
  return False


# [audrey, 2019/03/29] Entirely for ensuring that the
# equivalence checking function actually does what
# I think it does, and doesn't accidentally consider
# two types to be equal when they aren't.
def checkTypeEquivalent(blockA, blockB):
  return getBlockType(blockA) == getBlockType(blockB)

# [audrey, 2019/03/30] Created for the purposes of better differentiating different math types.
def getMathType(b):
  # All of the types that are grouped under "singles"
  singles = ["math_single", "math_abs", "math_neg", "math_round", "math_ceiling", "math_floor"]
  trig = ["math_trig", "math_cos", "math_tan"]
  # All of the other math operations that we alo want to differentiate further
  otherMathOperations = ["math_compare", "math_is_a_number", "math_on_list", "math_bitwise", "math_convert_angles", "math_convert_number", "math_divide"]
  # Gives the appropriate math prefix to prepend onto the lowercased op given.
  # Note: these all result in made-up types, that only exist to differentiate
  # between types that we couldn't differentiate between before.
  mathPrefix = {
    "math_is_a_number": "math_is_",
    "math_bitwise": "math_bitwise_",
    "math_convert_number": "math_convert_",
    "math_convert_angles": "math_convert_"
  }
  # Converts the names of these things to something that's a little bit more readable.
  # It's necessary to go by the operation in this case, since the type is uncertain and
  # could be any number of things.
  opToSingle = {
    "NEG": "math_neg",
    "ABS": "math_abs",
    "ROOT": "math_square_root", # [audrey, 2019/03/30] I made this up because otherwise there's no way to differentiate
    "CEILING": "math_ceiling",
    "FLOOR": "math_floor",
    "LN": "math_natural_log", # [audrey, 2019/03/30] also made up this one, also it's misleading that it's the natural log according to this but the function is just called log??? hmmm?????
    "EXP": "math_power_of_e", # [audrey, 2019/03/30] and this one
    "ROUND": "math_round"
  }
  # get the plain type
  tipe = getType(b)
  if tipe: #if it's not None
    if tipe in singles:
      if "OP" in b:
        return opToSingle[b["OP"]]
      raise RuntimeError("myutils.py::getMathType(): no 'OP' key in math_single block! {}".format(b))
    elif tipe in otherMathOperations or tipe in trig:
      if "OP" in b:
        # Use the generic prefix if there isn't a special one defined, else use the special one
        return ("math_" if tipe not in mathPrefix else mathPrefix[tipe]) + b["OP"].lower()
      # It appears that sometimes they don't have ops, which may be due to old versions of App Inventor.
      return tipe
      #raise RuntimeError("myutils.py::getMathType(): no 'OP' key in block, for other math_ op! {}".format(b))
    # The type is OK to go as is
    return tipe
  return "<NO TYPE FOUND!>"
# [audrey, 2019/03/30] Created for the purpose of properly differentiating logic block types.
def getLogicType(b):
  if isBoolean(b):
    # Fold "logic_boolean" and "logic_false" into the same thing
    return "logic_boolean"
  else:
    tipe = getType(b)
    if tipe: # if type is not None
      if tipe == "logic_operation":
        if "OP" in b:
          return "logic_operation_" + b["OP"].lower()
        raise RuntimeError("myutils.py::getLogicType(): no 'OP' key in block, for logic_operation! {}".format(b))
      elif tipe == "logic_compare":
        if "OP" in b:
          return "logic_compare_" + b["OP"].lower()
        raise RuntimeError("myutils.py::getLogicType(): no 'OP' key in block, for logic_compare! {}".format(b))
      # If it's none of these messed up options, then we should be good to go!
      return tipe
    raise RuntimeError("myutils.py::getLogicType(): NO TYPE FOUND! {}\ntype key in b?: {}".format(b, getTypeKey() in b))




# [audrey, 2019/03/29]
# Gets the actual type of the block, as a human might expect
# it to be, i.e. where a less than "<" is not equivalent to
# either a "<=" or a ">=" or an "="
# 
# [2019/07/19, lyn] previous version was too lenient on certain types of nodes. 
def getBlockType(b):
  if isComponentBlock(b):
    return getComponentBlockType(b)
  elif isLogicType(b):
    return getLogicType(b)
  elif isColorType(b):
    if isColorLiteral(b):
      return "color_literal"
  elif isMathType(b):
    return getMathType(b)
    #tipe = getType(b)
    #if tipe:
    #  if tipe == "math_compare" or tipe == "math_on_list" or tipe == "math_bitwise":
    #    if "OP" in  b:
    #      return "math_" + b["OP"].lower()
    #    return tipe
  # [2019/07/19, lyn] for equivalence purposes, only consider procedure calls to be 
  # the same for the same proc name!
  elif isProcedureCallType(b):
    tipe = getType(b) 
    if isADictionary(b) and "PROCNAME" in b:
      return tipe + "_" + b["PROCNAME"]
    else:
      return tipe
  # [2019/07/19, lyn] for equivalence purposes, only consider lexical var ops to be 
  # the same for the same var name!
  elif isLexicaVariableType(b):
    tipe = getType(b) 
    if isADictionary(b) and "VAR" in b:
      varName = b["VAR"]
      if varName.startswith('global'): 
        # Treat globals specially, else empirically we lose many opportunities for 
        # proceduralization and genericization. 
        return tipe + "_global" # <== Treat globals specially; all globals considered "the same"
        # return tipe + '_' + '_'.join(varName.split()) # [2019/08/01, lyn] This version does *not* treat globals specially
      else:
        return tipe + "_" + varName
    else:
      return tipe
  # [2019/07/19, lyn] for equivalence purposes, only consider local decls to 
  # be the same if they declare the same names in the same order!
  elif isLocalDeclarationType(b):
    tipe = getType(b) 
    if isADictionary(b) and "params" in b:
      params = b["params"]
      if len(params) > 0: 
        return tipe + '_' + '_'.join(params)
      else:
        return tipe
    else:
      return tipe
  else:
    return getType(b)

def getType(b):
  typeKey = "*type"
  if typeKey in b:
    return b[typeKey] # [2019/09/07, audrey] just realized that "*type" was literally in here, as a string literal
  return None

# [2019/07/19, lyn] previous version didn't handle component_component_block correctly
def getComponentBlockType(b):
  typeKey = '*type'
  if typeKey in b:
    t = b['*type']
    if isComponentBlock(b):
      if t.endswith("event"):
        compType = getComponentType(b) + "." # [2019/07/19, lyn] moved this line down.
        return compType + b['event_name']
      elif "set_or_get" in b:
        name = b['set_or_get'].capitalize() + " " + getComponentType(b)
        if isGeneric(b):
          name = "Generic " + name
        return name + "." + b['PROP']
      elif "method_name" in b:
        name = getComponentType(b)
        method = b['method_name']
        if isGeneric(b):
          name = "Generic " + name
        return name + "." + method
      elif t == "component_component_block": # [2019/07/19, lyn] added by lyn 
        return t                             # [2019/07/19, lyn] added by lyn 
  print "***ERROR: shouldn't happen in getComponentBlockType", b
  return "myutils::getComponentBlockType: not a component block?!"

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
      # [2019/01/15] This is the old way of doing this
      # return b['NAME']
      # [2019/01/15] Since it's usually not very informative to
      # just have the name of the thing, and not the type, changed
      # it to this
      return (t.replace("_", " ") + ":" + b['NAME'].encode("utf-8")).encode("utf-8")
    elif t == 'component_event':
      if 'instance_name' in b:
        if 'event_name' in b:
          return getComponentType(b) + "$" + b['instance_name'] + "." + b['event_name']
        return getComponentType(b) + "$" + b['instance_name'] + ".<UNKNOWN_EVENT_NAME>"
      return getComponentType(b) + "$<UNKNOWN_INSTANCE_NAME>.<UNKNOWN_EVENT_NAME>"
    elif t == 'component_set' or t == 'component_get':
      name = b['set_or_get'].capitalize() + " " + getComponentType(b)
      if 'instance_name' in b:
        if 'PROP' in b:
          return name + "$" + b['instance_name'] + "." + b['PROP']
        return name + "$" + b['instance_name'] + ".<UNKNOWN_PROP_NAME>"
      elif b['is_generic'] == 'true':
        if 'PROP' in b:
          return "Generic" + name + "." + b['PROP']
        return "Generic" + name
    elif t == 'component_method':
      name = getComponentType(b)
      method = b["method_name"]
      if 'instance name' in b:
        return name + '$' + b['instance_name'] + "." + method
      elif isGeneric(b):
        return "Generic" + name + "." + method
    elif t == 'logic_boolean':
      return "bool(" + b['BOOL'] + ")"
    elif t == 'text':
      if 'TEXT' in b:
        if b['TEXT'] == None:
          return "text()"
        return "text(" + (b['TEXT'] if len(b['TEXT']) < 20 else "...").encode('utf-8') + ")"
      return "text"
    elif t == 'controls_if':
      return "if " + renderMathNames(b['~branches'][0]['test'])
    elif t.startswith('math'):
      mathName = renderMathNames(b)
      #logwrite("getName: {} to {}".format(t, mathName))
      return mathName
    elif isColorBlock(b):
      colorName = renderColorNames(b)
      #logwrite("getName: {} to {}".format(t, colorName))
      return colorName
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


# [2018/07/13] compares all of the blocks against each other, while
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


def countSomething(block, func):
  if not isinstance(block, dict):
    return 0
  if isDisabled(block):
    return 0
  typeKey = '*type'
  tagsToCheck = ['test', '~bodyExp']

  for tag in tagsToCheck:
    if tag in block:
      countSomething(block[tag], func)

  if typeKey in block:
    # it's a block
    func(block)
  blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']

  for key in blockListKeys:
    if key in block:
      for b in block[key]:
        countSomething(b, func)

def isADictionary(thing):
  return isinstance(thing, dict)

# [2019/01/14] Wanted to be able to count things more simply
def countAndRecord(block, func, records):
  ''' block: some kind of object containing jail
      func: a function that takes a block and a dictionary
      records: some kind of dictionary/object that will containing the resulting data
  '''
  if not isADictionary(block):
    return
  if isDisabled(block):
    return
  typeKey = '*type'
  tagsToCheck = ['test', '~bodyExp']

  for tag in tagsToCheck:
    if tag in block:
      countAndRecord(block[tag], func, records)

  if typeKey in block:
    # it's a block
    func(block, records)
  blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']

  for key in blockListKeys:
    if key in block:
      for b in block[key]:
        countAndRecord(b, func, records)

def countAndRecordWithDepth(block, func, records, depth=0):
  if not isADictionary(block):
    return
  if isDisabled(block):
    return
  typeKey = '*type'
  tagsToCheck = ['test', '~bodyExp']

  for tag in tagsToCheck:
    if tag in block:
      countAndRecordWithDepth(block[tag], func, records, float(depth) + 0.5)

  if typeKey in block:
    func(block, records, depth)

  blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']
  

  for key in blockListKeys:
    if key in block:
      newDepth = depth + 1
      if key == "~args":
        newDepth = float(newDepth) - 0.5
      for b in block[key]:
        countAndRecordWithDepth(b, func, records, newDepth)
        
def countGenerics(block):
  mydict = {"total": 0}
  def countFunction(blk):
    if "is_generic" in blk:
      if blk["is_generic"] == "true":
        mydict["total"] += 1
  countSomething(block, countFunction)
  return mydict["total"]

def isDisabled(block):
  if "disabled" in block:
    return block["disabled"] == "true"
  return False

def countBlocksInside(block):
  count = countAllBlocks(block)
  return count - 1 if count > 0 else 0

# Finds the total number of blocks
def countAllBlocks(block):
  global tagsSeen
  if not isinstance(block, dict):
    return 0
  if isDisabled(block):
    #logwrite("countAllBlocks:: block " + getName(block) + " is disabled.")
    return 0
  count = 0
  typeKey = '*type'
  tagsToCheck = ['test', '~bodyExp']

  #for tag in block:
  #    if tag not in tagsSeen:
  #        tagsSeen[tag] = []
  #    if isinstance(block[tag]) not in tagsSeen[tag]:
  #        tagsSeen[tag].append(block[tag])

  for tag in tagsToCheck:
    if tag in block:
      count += countAllBlocks(block[tag])

  if typeKey in block:
    count += 1
  #if 'test' in block:
  #    count += countAllBlocks(block['test'])
  blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']

  for key in blockListKeys:
    if key in block:
      for b in block[key]:
        count += countAllBlocks(b)
  return count

def countComponents(blocks):
  if not isinstance(blocks, dict):
    return 0, 0
  if isDisabled(blocks):
    #logwrite("countComponents:: block " + getName(blocks) + " is disabled.")
    return 0, 0
  count = 0
  genericCount = 0
  typeKey = '*type'
  tagsToCheck = ['test', '~bodyExp']
  blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']
  if typeKey in blocks:
    if blocks[typeKey].startswith("component"):
      count += 1
      if "is_generic" in blocks:
        if blocks['is_generic'] == "true":
          genericCount += 1
  #if 'test' in blocks:
  #    c, gc = countComponents(blocks['test'])
  #    count += c
  #    genericCount += gc

  for tag in tagsToCheck:
    if tag in blocks:
      #logwrite("countComponents: " + prettyPrint(blocks))
      c, gc = countComponents(blocks[tag])
      count += c
      genericCount += gc

  for key in blockListKeys:
    if key in blocks:
      for b in blocks[key]:
        c, gc = countComponents(b)
        count += c
        genericCount += gc

  return count, genericCount

def iterateOverProjectSets(ps, func):
  for eq in ps:
    for codeset in eq:
      for equivClass in codeset:
        if equivClass.size() > 0:
          for blk in equivClass:
            func(eq, blk)

# This is really bad, but I'm not exactly sure why I made this function.
# It was probably because I pass it to a different function so that it
# can act on it, and this other function wants to put in two parameters:
#     eq: equivalence class, probably
#     blk: block.
def countAllBlocksWrapper(eq, blk):
  countAllBlocks(blk)


def makeCSVLines(columns, data):
  '''
  columns: a list of the names of the columns for the csv
  data: a list of Python objects/dictionaries that contain keys that are
        identical to names found in columns
  '''
  strdata = [{colTag:str(d) for colTag,d in datum.iteritems()} for datum in data]
  return "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in columns])) for d in strdata])

def maxPairs(pair1, pair2):
  a1, b1 = pair1
  a2, b2 = pair2
  return ( max(a1, a2), max(b1, b2) )

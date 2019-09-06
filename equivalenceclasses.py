# 2019/07/19: Lyn made changes for today's B&B 2019 genericization deadline
# See [2019/07/19, lyn] notes below
import myutils as mus

#from myutils import *

def equivalenceClassify(blocks, screenName=None):
  size = len(blocks)
  blockset = CodeSet(screenName)

  for i in range(size-1):
    for j in range(i + 1, size):
      if mus.equivalent(blocks[i], blocks[j]):
        #print i, j
        blockset.addPair(blocks[i], blocks[j])
  return blockset

def projectEquivClasses(projectScreenCode, screenNames=None):
  if screenNames == None:
    return [equivalenceClassify(code) for code in projectScreenCode]
  projClasses = []
  for i in range(len(screenNames)):
    projClasses.append(equivalenceClassify(projectScreenCode[i], screenNames[i]))
  return projClasses


class EquivalenceClass:
  ''' A data structure that records relationships between different
      projects in a ProjectSet, specifically ones that are all equivalent. '''
  def __init__(self, a, b, screen=None):
    ''' a: an object equivalent to b
        b: an object equivalent to a
    '''
    self.members = [a, b]
    self.screen = screen or ""
    self.corrmatrix = []
  
  def inClass(self, a, b):
    ''' a: an object where a is deemed equivalent to the other object b
        b: an object where b is deemed equivalent to the other object a
    '''
    return a in self.members or b in self.members

  def isAMember(self, a):
    return a in self.members
  
  def add(self, newObject):
    if newObject not in self.members:
      self.members.append(newObject)

  def addPair(self, a, b):
    if not self.isAMember(a):
      self.add(a)
    elif not self.isAMember(b):
      self.add(b)
  def getBlock(self, index=0):
    if index < self.size():
      return self.members[index]
    return None

  def head(self):
    return self.getBlock(index=0)
  
  def getName(self, index=0):
    if index < self.size():
      return self.screen + "|" + mus.getName(self.members[index])
    return ""
  def numBlocks(self):
    if self.size() > 0:
      return mus.countAllBlocks(self.members[0])
    return 0
  
  def size(self):
    return len(self.members)

  def numBlocks(self):
    if self.size() == 0:
      return 0
    return mus.countAllBlocks(self.members[0])

  def largeEnough(self):
    # [2019/07/09, lyn] this was reasonable for proceduralization,
    # but not for removing duplicate handlers in the context of generic handlers.
    # return self.numBlocks() > 5
    return True
  
  def hasOverlap(self, other):
    for obj in self.members:
      if other.isAMember(obj):
        return True
    return False
    
  def isCombinable(self, other):
    ''' other: another Equivalence Class
    '''
    if self.size() > other.size():
      return other.hasOverlap(self)
    return self.hasOverlap(other)

  def combine(self, other):
    if self.isCombinable(other):
      self.members.extend(other.members)

  def __str__(self):
    return "{" + ", ".join(map(lambda x: mus.getName(x), self.members)) + "}"

  def dump(self):
    return mus.prettyPrint(self.members)

  def findComponentCorrespondence(self):
    if len(self.corrmatrix) != self.size(): # [2019/08/01, lyn] Added this check; either it hasn't been calculated yet,
                                            # or it was calculated before one or more new members
                                            # were added to equivalence class
      self.corrmatrix = []
      for i in range(self.size()):
        self.corrmatrix.append([])
        for j in range(i):
          self.corrmatrix[i].append(0)
        for j in range(i, self.size()):
          self.corrmatrix[i].append(mus.numCompBlocksInCommon(self.members[i], self.members[j]))

  def showCorrespondence(self):
    # print "showCorrespondence for", self.getName() # [2019/07/19, lyn] for debugging
    for i in range(len(self.corrmatrix)):
      print " ".join(map(lambda x: str(x).ljust(4), self.corrmatrix[i]))

  def needsGenerics(self):
    # print "needsGenerics" # [2019/07/19, lyn] for debugging
    # if self.corrmatrix == []:
    #  self.findComponentCorrespondence()
    # [2019/08/01, lyn] replaced the above two lines by the following,
    # since changed findComponentCorrespondence itself to do memoization
    self.findComponentCorrespondence()
    # self.showCorrespondence() # [2019/07/19, lyn] for debugging
    allZero = True
    for i in range(self.size()):
      allZero = allZero and self.corrmatrix[i][i] == 0
    if allZero:
      # print "needsGenerics returns False from allZero" # [2019/07/19, lyn] for debugging
      return False
    for i in range(self.size()-1):
      item = self.corrmatrix[i][i]
      for j in range(i + 1, self.size()):
        if item - 1 > self.corrmatrix[i][j]:
          # print "needsGenerics returns True early" # [2019/07/19, lyn] for debugging
          return True
    # print "needsGenerics returns False late" # [2019/07/19, lyn] for debugging
    return False

  # [audrey, 2019-03-27] added for the VLHCC paper
  def isGenericifiable(self):
    compBlockSets = [mus.findCompBlocks(blk) for blk in self]

    for i in range(len(compBlockSets)-1):
      for j in range(i, len(compBlockSets)):
        diffA = compBlockSets[i].difference(compBlockSets[j])
        diffB = compBlockSets[j].difference(compBlockSets[i])
        if len(diffA) > 1:
          return False
        if len(diffB) > 1:
          return False
    return True
  def getType(self):
    first = self.head()
    if first:
      if mus.getTypeKey() in first:
        return first[mus.getTypeKey()]
    return "<NO TYPE KEY FOUND IN {}>".format(first)
  def __iter__(self):
    self.index = -1
    return self

  # [2019/08/01, lyn] Added this 
  def isSingleProcedureCall(self):
    if self.size() < 2: # [2019/08/01, lyn] Should never be true!
      return False
    else:
      handler = self.members[0]
      if (not isinstance(handler, dict) 
          or '*type' not in handler 
          or handler['*type'] != 'component_event'
          or '~bodyStm' not in handler):
        print "***ERROR: handler not expected dict in isSingleProcedureCall"
        return False
      else: 
        body = handler['~bodyStm']
        if len(body) != 1 or '*type' not in body[0]:
          return False
        else:
          stm = body[0]
          return stm['*type'] == "procedures_callnoreturn"

  def next(self):
    if self.index == self.size() - 1:
      raise StopIteration
    self.index += 1
    return self.members[self.index]

  def everyPair(self):
    return iter([(a, b) for a in self for b in self if a != b])
  
class CodeSet:
  """Contains all of the equivalence classes
     associated with a particular
     screen."""
  def __init__(self, screenName=None):
    self.classes = []
    self.codeDict = {}
    self.screenName = "" if screenName == None else screenName
    
  def numClasses(self):
    return len(self.classes)

  def numClassesLargeEnough(self):
    return len(self.sizes(True))
  
  def sizes(self, useLargeEnough=False):
    if useLargeEnough:
      return [x.size() for x in self.classes if x.largeEnough()]
    return [x.size() for x in self.classes]

  def avgNumBlocks(self, useLargeEnough=False):
    if useLargeEnough:
      if self.numClassesLargeEnough() == 0:
        return 0
      total = 0
      for clss in self.classes:
        if clss.largeEnough():
          total += clss.numBlocks()
      return total / float(self.numClassesLargeEnough())
    if self.numClasses() == 0:
      return 0
    return reduce((lambda x, y: x + y.numBlocks()), self.classes) / float(self.numClasses)
  def hasKey(self, code):
    if isinstance(code, str):
      return code in self.codeDict
    name = mus.getName(code)
    return name in self.codeDict

  def getIndex(self, code):
    if isinstance(code, str):
      return self.codeDict[code]
    name = mus.getName(code)
    if self.hasKey(name):
      return self.codeDict[name]
    return -1

  def setIndex(self, code, other):
    name = ""
    if isinstance(code, str):
      name = code
    else:
      name = mus.getName(code)
    if isinstance(other, int):
      self.codeDict[name] = other
    elif self.getIndex(other) != -1:
      self.codeDict[name] = self.getIndex(other)
    
  def addPair(self, codeA, codeB):
    nameA = mus.getName(codeA)
    nameB = mus.getName(codeB)
    
    if not (self.hasKey(codeA) or self.hasKey(codeB)):
      self.classes.append(EquivalenceClass(codeA, codeB, self.screenName))
      ind = self.numClasses() - 1
      self.codeDict[nameA] = ind
      self.codeDict[nameB] = ind
    elif self.hasKey(codeA) != self.hasKey(codeB):
      if self.hasKey(nameA):
        self.setIndex(nameB, nameA)
      else:
        self.setIndex(nameA, nameB)
      ind = self.getIndex(nameA)
      self.classes[ind].addPair(codeA, codeB)

  def __str__(self):
    return "[" + ", ".join(map(lambda x: str(x), self.classes)) + "]"

  def __iter__(self):
    self.index = -1
    return self

  def next(self):
    if self.index == self.numClasses() - 1:
      raise StopIteration
    self.index += 1
    return self.classes[self.index]

  # [2019/08/01, lyn] Added this. 
  # Returns a pair of (1) maximum equiv class size and (2) maximum equiv class num blocks
  def maxes(self): 
    maxPair = (0, 0)
    for equivClass in self: 
      maxPair = mus.maxPairs(maxPair, (equivClass.size(), equivClass.numBlocks()))
    return maxPair

class ProjectSet:
  def __init__(self, blocks, screenNames=None, name=None, programmer=None):
    self.screenClasses = projectEquivClasses(blocks, screenNames)
    self.screenNames = screenNames or []
    self.projectName = "" if name == None else name
    self.programmerName = "" if programmer == None else programmer
        
  def numScreens(self):
    return len(self.screenClasses)

  def __inRange(self, screenNumber):
    return not (screenNumber < 0 or screenNumber >= self.numScreens)

  def numClasses(self, screenNumber):
    if screenNumber < 0:
      return -1
    if screenNumber >= self.numScreens():
      return -2
    return self.screenClasses[screenNumber].numClasses()

  def classSizes(self, screenNumber):
    if self.__inRange(screenNumber):
      return "{" + ", ".join(map(str, self.screenClasses[screenNumber].sizes())) + "}"

  def __iter__(self):
    self.index = -1
    return self

  def next(self):
    if self.index == self.numScreens() - 1:
      raise StopIteration
    self.index += 1
    return self.screenClasses[self.index]

  def getScreenEquivBlockItems(self):
    return iter([(screen, ec, blk) for screen in self for ec in screen for blk in ec])
  def getScreenEquivItems(self):
    return iter([(screen, ec) for screen in self for ec in screen])
  def identity(self):
    return self.programmerName + ":" + self.projectName + ("" if len(self.screenNames) == 0 else "(" + ",".join(self.screenNames) + ")")

  # [2019/08/01, lyn] Added this. 
  # Returns a pair of (1) maximum equiv class size and (2) maximum equiv class num blocks
  def maxes(self): 
    maxPair = (0, 0)
    for codeSet in self: 
      maxPair = mus.maxPairs(maxPair, codeSet.maxes())
    return maxPair


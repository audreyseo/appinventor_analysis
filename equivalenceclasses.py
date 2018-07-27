from myutils import *

def equivalenceClassify(blocks):
    size = len(blocks)
    blockset = CodeSet()

    for i in range(size-1):
        for j in range(i + 1, size):
            if equivalent(blocks[i], blocks[j]):
                #print i, j
                blockset.addPair(blocks[i], blocks[j])
    return blockset

def projectEquivClasses(projectScreenCode, screenNames=None):
    if screenNames == None:
        return [equivalenceClassify(code) for code in projectScreenCode]
    projClasses = {}
    for i in range(len(screenNames)):
        projClasses[screenNames[i]] = equivalenceClassify(projectScreenCode[i])
    return projClasses


class EquivalenceClass:
  ''' A data structure that records relationships between different
      projects in a ProjectSet, specifically ones that are all equivalent. '''
  def __init__(self, a, b):
    ''' a: an object equivalent to b
        b: an object equivalent to a
    '''
    self.members = [a, b]

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
    
  def size(self):
    return len(self.members)

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
    return "{" + ", ".join(map(lambda x: getName(x), self.members)) + "}"

  def dump(self):
    return prettyPrint(self.members)

  def __iter__(self):
    self.index = -1
    return self
  
  def next(self):
    if self.index == self.size() - 1:
      raise StopIteration
    self.index += 1
    return self.members[self.index]
  
class CodeSet:
  def __init__(self):
    self.classes = []
    self.codeDict = {}

  def numClasses(self):
    return len(self.classes)
  
  def sizes(self):
    return [x.size() for x in self.classes]
    
  def hasKey(self, code):
    if isinstance(code, str):
      return code in self.codeDict
    name = getName(code)
    return name in self.codeDict

  def getIndex(self, code):
    if isinstance(code, str):
      return self.codeDict[code]
    name = getName(code)
    if self.hasKey(name):
      return self.codeDict[name]
    return -1

  def setIndex(self, code, other):
    name = ""
    if isinstance(code, str):
      name = code
    else:
      name = getName(code)
    if isinstance(other, int):
      self.codeDict[name] = other
    elif self.getIndex(other) != -1:
      self.codeDict[name] = self.getIndex(other)
    
  def addPair(self, codeA, codeB):
    nameA = getName(codeA)
    nameB = getName(codeB)
    
    if not (self.hasKey(codeA) or self.hasKey(codeB)):
      self.classes.append(EquivalenceClass(codeA, codeB))
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


class ProjectSet:
  def __init__(self, blocks, screenNames=None, name=None, programmer=None):
    self.screenClasses = projectEquivClasses(blocks)
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

import equivalenceclasses as ecs

import myutils as mus

def checkIfGenericizable(equiv):
  '''equiv: an equivalence class, full of blocks
            that are supposedly equivalent.
  '''
  if equiv.isGenericifiable():
    # isGenericifiable is just a basic check on whether we
    # could make it generic
    # Now we want to see if there is actually basically an
    # isomorphism between the two
    for blkA, blkB in equiv.everyPair():
      if not isGenericEquivalent(blkA, blkB):
        return False

  return False

def isGenericEquivalent(blockA, blockB):
  '''Tests if when at most one component is switched out, if blockA is equivalent to blockB
  '''
  
  setA = mus.findCompBlocks(blockA)
  setB = mus.findCompBlocks(blockB)
  if len(setA) == len(setB):
    if mus.smallDifference(setA, setB):
      if len(setA.difference(setB)) == 1:
        if len(setB.difference(setA)) == 1:
          switcher = {
            setA.difference(setB)[0]: setA.difference(setB)[0],
            setB.difference(setA)[0]: setA.difference(setB)[0]
          }
          for a in setA:
            if a not in switcher:
              switcher[a] = a
          for b in setB:
            if b not in switcher:
              

def testSwitch(switchDict, blockA, blockB):
  blockListKeys = mus.getBlockListKeys()
  tagsToCheck = mus.getTagsToCheck()
  theSame = True
  if mus.isComponentBlock(blockA) and mus.isComponentBlock(blockB):
    nameKeys = mus.getComponentBlockNameKeys()
    for n in nameKeys:
      if n in blockA and n in blockB:
        theSame = theSame and blockA[n] == blockB[n]
        if not theSame:
          return theSame
  for tag in tagsToCheck:
    if tag in blockA and tag in blockB:
      theSame = theSame and testSwitch(switchDict, blockA, blockB)

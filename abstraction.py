''' abstraction.py
    Created on 2018/07/12 by Audrey Seo

    Parses a jail file and then allows you to compare how similar each of the handlers are.

    Most of the history can be read in the comments throughout, or in the commit messages.
'''

import json
import os
import copy
# [2018/07/13] Use difflib to generate output
import difflib

import datetime

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

class CodeSet:
    def __init__(self):
        self.classes = []
        self.codeDict = {}

    def numClasses(self):
        return len(self.classes)

    def hasKey(self, code):
        if isinstance(code, str):
            return code in self.codeDict
        name = getName(code)
        return name in self.codeDict

    def getIndex(self, code):
        if isinstance(code, str):
            return self.codeDict[str]
        name = getName(code)
        return self.codeDict[name]

    def setIndex(self, code, other):
        name = ""
        if isinstance(code, str):
            name = code
        else:
            name = getName(code)
        if isinstance(other, int):
            self.codeDict[name] = other
        else:
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
    
diffDirectory = ""
dirName = os.path.dirname(os.path.realpath(__file__))

def getJail(jailLocation):
    global dirName
    jail = ""
    with open(os.path.join(dirName, jailLocation), "r") as f:
        jail = json.load(f)
    return jail

# [2018/07/12] Checks to see if at a minimum, blocks are not
# exact duplicates of each other.
def allAreUnique(c):
    for i in range(len(c)):
        for j in range(i+1, len(c)):
            if c[i] == c[j] and i != j:
                print i, j, c[i] == c[j]
#    #return True

def fuzzify(blk, depth=0):
    childBlockKey = '~bodyStm'
    argsKey = '~args'
    branchesKey = "~branches"
    elseKey = '~branchofelse'

    tagsToRemove = ['id', 'instance_name', 'COMPONENT_SELECTOR', 'x', 'y']
    genericTags = {'text': ('TEXT', '*generic_text*'),
                   'logic_boolean': ('BOOL', '*generic_boolean*')}#,
    #               'math_number': ('NUM', '*generic_number*')}
    blockListKeys = ['~bodyStm', '~args', '~branches', '~branchofelse', 'then']

    # [2018/07/18] standardize ordering of arguments
    if isCommutative(blk):
        if argsKey in blk:
            arg1 = copy.deepcopy(blk[argsKey][0])
            arg2 = copy.deepcopy(blk[argsKey][1])
            name1 = getName(arg1)
            name2 = getName(arg2)
            if len(name1) > len(name2):
                blk[argsKey][0] = arg2
                blk[argsKey][1] = arg1
    
    #if 'then' in blk:
    #    for t in blk['then']:
    #        fuzzify(t, depth+1)
    if 'test' in blk:
        fuzzify(blk['test'], depth + 1)

    
    for tag in tagsToRemove:
        if tag in blk:
            blk.pop(tag, 0)
    for key in blockListKeys:
        if key in blk:
            for child in blk[key]:
                fuzzify(child, depth + 1)
    for k,v in genericTags.iteritems():
        if "*type" in blk:
            if blk['*type'] == k:
                a = v[0]
                b = v[1]
                blk[a] = b

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
    #print depth, ":", getName(a) + "|" + getName(b)
    if a['*type'] == b['*type']:
        #if a['*type'] == 'logic_boolean':
        #    if a['BOOL'] != b['BOOL']:
        #        print a['BOOL'], b['BOOL']
        t = True

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
                a0 = a[argsKey][0]
                a1 = a[argsKey][1]
                b0 = b[argsKey][0]
                b1 = b[argsKey][1]
                if equivalent(a0, b0, depth+1):
                    return equivalent(a1, b1, depth+1)
                elif equivalent(a0, b1, depth+1):
                    return equivalent(a1, b0, depth+1)
                return False
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
#removeIDs(blocks[0], 0)

# [2018/07/13] Gets the component type of a block. It also accounts for
# the few cases where screens are called "Form" instead.
def getComponentType(b):
    if 'component_type' in b:
        if b['component_type'] == 'Form':
            return 'Screen'
        return b['component_type']
    return ""

# [2018/07/13] If a block is a math_compare, then it returns
# the mathematical symbol for what its operation is.
def compareOp(b):
    op = b['OP']
    if op == 'GT':
        return '>'
    elif op == 'LT':
        return '<'
    return op

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
            return b['set_or_get'].capitalize() + " " + getComponentType(b) + "$" + b['instance_name'] + "." + b['PROP']
        elif t == 'logic_boolean':
            return "bool(" + b['BOOL'] + ")"
        elif t == 'text':
            return "text(" + b['TEXT'] + ")"
        elif t == 'controls_if':
            return "if " + renderMathNames(b['~branches'][0]['test'])
        elif t.startswith('math'):
            return renderMathNames(b)
        return t
    return str(b)

def size(b):
    childBlocksKey = "~bodyStm"
    total = 1
    if childBlocksKey in b:
        for child in b[childBlocksKey]:
            total += size(child)
    return total
        
#equivalent(blocks[16], blocks[15])
#block = blocks[0]

# [2018/07/16] formats a block specifically for the purposes of using
# the output with difflib. It returns an array of strings, the lines
# of the json pretty-printed output.
def formatBlock(block):
    blockCopy = copy.deepcopy(block)
    removeIDs(blockCopy)
    return json.dumps(blockCopy, indent=2, separators=(',', ': ')).split('\n')

# [2018/07/16] determines if nonsimilar blocks should have a diff outputed
# for them, and creates and outputs that diff.
def createDiff(blockA, blockB, nameA=None, nameB=None):
    if nameA == None:
        if 'instance_name' in blockA:
            nameA = getName(blockA)
    else:
        nameA = str(nameA)
    if nameB == None:
        if  'instance_name' in blockB:
            nameB = getName(blockB)
    else:
        nameB = str(nameB)
    stri = formatBlock(blockA)
    strj = formatBlock(blockB)
    if len(stri) != 0 and len(strj) != 0:
        ratio = float(len(stri)) / float(len(strj))
    if ratio > 0.9 and ratio < 1.1:
        global diffDirectory
        path = "diff"
        if diffDirectory == "":
            diffDirectory = datetime.datetime.now().strftime("%Y-%m-%d::%H:%M:%S")
            path = os.path.join("diffs", diffDirectory)
            if not os.path.exists(path):
                os.makedirs(os.path.join("diffs", diffDirectory))
            with open(os.path.join(path,  nameA + "-" + nameB + ".html"), "w") as f:
                f.write(difflib.HtmlDiff().make_file(stri, strj, nameA, nameB))
                f.flush()

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
                print i, j, ":", getName(blocks[i]), getName(blocks[j]) #size(blocks[i]), size(blocks[j])
            elif checkNotIn(i, j) and not equivalent(blocks[i], blocks[j]):
                #seen.append((j,i))
                #seen.append((i,j))
                createDiff(blocks[i], blocks[j])
                


''' Wrapper function for testing whether different top blocks contain similar handlers.
'''
def compareBlocks(blks, num1, num2):
    return equivalent(blks[num1], blks[num2])

#print compareBlocks(blocks, 17, 18)

#compareAllBlocks(blocks)

def equivalenceClassify(blocks):
    size = len(blocks)
    blockset = CodeSet()

    for i in range(size-1):
        for j in range(i + 1, size):
            if equivalent(blocks[i], blocks[j]):
                print i, j
                blockset.addPair(blocks[i], blocks[j])
    return blockset

def projectEquivClasses(projectScreenCode, screenNames=None):
    if screenNames != None:
        return [equivalenceClassify(code) for code in projectScreenCode]
    projClasses = {}
    for i in range(len(screenNames)):
        projClasses[screenNames[i]] = equivalenceClassify(projectScreenCode[i])
    return projClasses

potenciaJailFile = "myjails/p024_023_potencia_4.jail"
bakeJailFile = "10kjails/09/09265/p019_019_bake.jail"

potenJail = getJail(potenciaJailFile)
screens = potenJail["*Names of Screens"]

bakeJail = getJail(bakeJailFile)
bakeScreens = bakeJail["*Names of Screens"]
bakeScreens.sort()
print len(bakeScreens)
print bakeScreens
screen1Names = [bakeScreens[1], bakeScreens[2], bakeScreens[4]]
screen2Names = [bakeScreens[3], bakeScreens[5]]

bakeCode = [bakeJail['screens'][s]['bky']['topBlocks'] for s in bakeScreens]

screen1s = [bakeJail['screens'][s]['bky']['topBlocks'] for s in screen1Names]
screen2s = [bakeJail['screens'][s]['bky']['topBlocks'] for s in screen2Names]

def fuzzifyScreens(screens):
    for blks in screens:
        for b in blks:
            fuzzify(b)
#

#print(screen1s[0])

#fuzzifyScreens(screen1s)
#fuzzifyScreens(screen2s)

'''for i in range(len(screen1s)-1):
    for j in range(i+1, len(screen1s)):
        tmp = False
        minScreens = min(len(screen1s[i]), len(screen1s[j]))
        #if len(screen1s[i]) == len(screen1s[j]):
        for k in range(minScreens):
            tmp = tmp or equivalent(screen1s[i][k], screen1s[j][k])
        #else:
        if len(screen1s[i]) != len(screen1s[j]):
            print "Not same size", minScreens
            #tmp = False
        print i, j, tmp #equivalent(screen1s[i], screen1s[j]) #screen1s[i] == screen1s[j]'''
#print 0, 1, equivalent(screen2s[0], screen2s[1]) #screen2s[0] == screen2s[1]

#print screens

s = screens[0]

code = potenJail['screens'][s]['bky']['topBlocks']
blocks = copy.deepcopy(code)

#for b in blocks:
#    fuzzify(b)

#allAreUnique(blocks)


#print compareBlocks(blocks, 15, 16)

#createDiff(blocks[15], blocks[16], 15, 16)

ec = equivalenceClassify(blocks)

bakeECs = [equivalenceClassify(c) for c in bakeCode]

print ec
i = 0
for equiv in bakeECs:
    print bakeScreens[i], equiv
    i += 1

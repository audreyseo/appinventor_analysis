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

dirName = os.path.dirname(os.path.realpath(__file__))

jail = ""
with open(os.path.join(dirName, "myjails/p024_023_potencia_4.jail"), "r") as f:
    jail = json.load(f)

screens = jail["*Names of Screens"]

#print screens

s = screens[0]

code = jail['screens'][s]['bky']['topBlocks']
blocks = copy.deepcopy(code)


# [2018/07/12] Checks to see if at a minimum, blocks are not
# exact duplicates of each other.
def allAreUnique(c):
    for i in range(len(c)):
        for j in range(len(c)):
            print i, j, c[i] == c[j]
            if c[i] == c[j] and i != j:
                return False
    return True

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
def isMathType(block):
    return block['*type'].startswith('math')

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
removeIDs(blocks[0], 0)

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
def renderMathNames(b, depth=0):
    ''' b:     a block in the form of a Python dictionary/object
        depth: optional integer, used more specifically by the function's
               recursive nature to render parentheses around math
               expressions
    '''
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

def size(b):
    childBlocksKey = "~bodyStm"
    total = 1
    if childBlocksKey in b:
        for child in b[childBlocksKey]:
            total += size(child)
    return total
        
equivalent(blocks[16], blocks[15])
block = blocks[0]

# [2018/07/16] formats a block specifically for the purposes of using
# the output with difflib. It returns an array of strings, the lines
# of the json pretty-printed output.
def formatBlock(block):
    blockCopy = copy.deepcopy(block)
    removeIDs(blockCopy)
    return json.dumps(blockCopy, indent=2, separators=(',', ': ')).split('\n')

# [2018/07/16] determines if nonsimilar blocks should have a diff outputed
# for them, and creates and outputs that diff.
def createDiff(blockA, blockB):
    if 'instance_name' in blockA and 'instance_name' in blockB:
        nameA = getName(blockA)
        nameB = getName(blockB)
        stri = formatBlock(blockA)
        strj = formatBlock(blockB)
        if len(stri) != 0 and len(strj) != 0:
            ratio = float(len(stri)) / float(len(strj))
            if ratio > 0.9 and ratio < 1.1:
                with open("diffs/" + nameA + "-" + nameB + ".html", "w") as f:
                    f.write(difflib.HtmlDiff().make_file(stri, strj, nameA, nameB))
                    f.flush()

# [2018/07/13] comparse all of the blocks against each other, while
# also accounting for never comparing the same pair twice.
def compareAllBlocks(blocks):
    #seen = []
    ecs = {}
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
                

compareAllBlocks(blocks)

''' Wrapper function for testing whether different top blocks contain similar handlers.
'''
def compareBlocks(blks, num1, num2):
    return equivalent(blks[num1], blks[num2])

#print compareBlocks(blocks, 17, 18)

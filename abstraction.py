''' abstraction.py
    Created on 2018/07/12 by Audrey Seo

    Parses a jail file and then allows you to compare how similar each of the handlers are.
'''

import json
import os
import copy
# Use difflib!!
import difflib

dirName = os.path.dirname(os.path.realpath(__file__))

jail = ""
with open(os.path.join(dirName, "myjails/p024_023_potencia_4.jail"), "r") as f:
    jail = json.load(f)

screens = jail["*Names of Screens"]

#print screens

s = screens[0]

code = jail['screens'][s]['bky']['topBlocks']


def allAreUnique(c):
    for i in range(len(c)):
        for j in range(len(c)):
            print i, j, c[i] == c[j]
            if c[i] == c[j] and i != j:
                return False
    return True


blocks = copy.deepcopy(code)

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


def equivalent(a, b, depth=0):
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

def getComponentType(b):
    if 'component_type' in b:
        if b['component_type'] == 'Form':
            return 'Screen'
        return b['component_type']
    return ""

def compareOp(b):
    op = b['OP']
    if op == 'GT':
        return '>'
    elif op == 'LT':
        return '<'
    return op

def renderMathNames(b, depth=0):
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
    else:
        return getName(b)

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

def formatBlock(block):
    blockCopy = copy.deepcopy(block)
    removeIDs(blockCopy)
    return json.dumps(blockCopy, indent=2, separators=(',', ': ')).split('\n')

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

def compareAllBlocks(blocks):
    seen = []
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            if equivalent(blocks[i], blocks[j]) and i != j and (i,j) not in seen and (j,i) not in seen:
                seen.append((i,j))
                seen.append((j,i))
                print i, j, ":", getName(blocks[i]), getName(blocks[j]) #size(blocks[i]), size(blocks[j])
            elif (i,j) not in seen and (j,i) not in seen and not equivalent(blocks[i], blocks[j]):
                seen.append((j,i))
                seen.append((i,j))
                createDiff(blocks[i], blocks[j])
                

compareAllBlocks(blocks)

''' Wrapper function for testing whether different top blocks contain similar handlers.
'''
def compareBlocks(blks, num1, num2):
    return equivalent(blks[num1], blks[num2])

#print compareBlocks(blocks, 17, 18)

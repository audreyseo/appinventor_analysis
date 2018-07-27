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

from equivalenceclasses import *
from myutils import *
from findmissing import *


diffDirectory = ""
dirName = os.path.dirname(os.path.realpath(__file__))


def getJail(jailLocation):
    global dirName
    path = jailLocation if os.path.isabs(jailLocation) else os.path.join(dirName, jailLocation)
    jail = ""
    with open(jailLocation, "r") as f:
        jail = json.load(f)
    return jail


def fuzzify(blk, depth=0):
    childBlockKey = '~bodyStm'
    argsKey = '~args'
    branchesKey = "~branches"
    elseKey = '~branchofelse'

    tagsToRemove = ['id', 'instance_name', 'COMPONENT_SELECTOR', 'x', 'y']
    tagsToCheck = ['test', '~bodyExp']
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
    for tag in tagsToCheck:
        if tag in blk:
            fuzzify(blk[tag], depth + 1)
    #if 'test' in blk:
    #    fuzzify(blk['test'], depth + 1)

    
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

def fuzzifyScreens(screens):
    for blks in screens:
        for b in blks:
            fuzzify(b)




        
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

                



#print compareBlocks(blocks, 17, 18)

#compareAllBlocks(blocks)


def jailToEquivs(jailLocation):
    printMessagesEverySoOften = 10000
    bigDirs = getDirectories(jailLocation)
    equivs = []
    num = 0
    for bigdir in bigDirs:
        littledirs = getDirectories(os.path.join(jailLocation, bigdir))
        for littledir in littledirs:
            files = getFileNames(os.path.join(jailLocation, bigdir, littledir))
            for f in files:
                jail = getJail(os.path.join(jailLocation, bigdir, littledir, f))
                screens = jail['*Names of Screens']
                code = []
                for s in screens:
                    if isinstance(jail['screens'][s]['bky'], dict):
                        code.append(jail['screens'][s]['bky']['topBlocks'])
                equivs.append(ProjectSet(code, f, littledir))
                num += 1
                if num % printMessagesEverySoOften == 0:
                    logwrite(str(num) + " " + str(equivs[num-1].numScreens()))
    return equivs

'''potenciaJailFile = "myjails/p024_023_potencia_4.jail"
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
'''

def countSomething(block, func):
    if not isinstance(block, dict):
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
    
def countAllBlocks(block):
    if not isinstance(block, dict):
        return 0
    count = 0
    typeKey = '*type'
    tagsToCheck = ['test', '~bodyExp']

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

if __name__=='__main__':
    createLogFile()
    equivs = jailToEquivs("10kjails")

    allCount = 0
    compCount = 0
    topBlocksWithNoComps = 0
    totalBlocks = 0
    ind = 0

    nonComponentBlockTypes = {}
    kindsDict = {}
    numBlocksWithKind = 0
    numBlocksWithoutKind = 0
    nonComponentBlockTypesKinds = {}
    
    totalNumBlocksBesidesGlobalDecls = 0
    totalNumCompBlocksWOGlobalDecls = 0
    
    declTypeKinds = {}
    
    procedureReturns = []

    for eq in equivs:
        for codeset in eq:
            for equivClass in codeset:
                if equivClass.size() > 0:
                    for blk in equivClass:
                        totalBlocks += 1
                        ind += 1
                        tmpAll = countAllBlocks(blk)
                        tmpComp, tmpGeneric = countComponents(blk)
                        allCount += tmpAll
                        compCount += tmpComp
                        if 'kind' in blk:
                            numBlocksWithKind += 1
                            k = blk['kind']
                            tipe = blk['*type']
                            if tipe == "procedures_defreturn":
                                procedureReturns.append(eq.projectName + "-" + eq.programmerName)
                            if k in kindsDict:
                                kindsDict[k] += 1
                            else:
                                kindsDict[k] = 1
                            if k == "declaration":
                                totalNumBlocksBesidesGlobalDecls += tmpAll
                                totalNumCompBlocksWOGlobalDecls += tmpComp
                                if k in declTypeKinds:
                                    if tipe in declTypeKinds[k]:
                                        declTypeKinds[k][tipe]['num'] += 1
                                        declTypeKinds[k][tipe]['all'] += tmpAll
                                        declTypeKinds[k][tipe]['comp'] += tmpComp
                                        declTypeKinds[k][tipe]['generic'] += tmpGeneric
                                    else:
                                        declTypeKinds[k][tipe] = {}
                                        declTypeKinds[k][tipe]['num'] = 1
                                        declTypeKinds[k][tipe]['all'] = tmpAll
                                        declTypeKinds[k][tipe]['comp'] = tmpComp
                                        declTypeKinds[k][tipe]['generic'] = tmpGeneric
                                else:
                                    declTypeKinds[k] = {}
                                    declTypeKinds[k][tipe] = {}
                                    declTypeKinds[k][tipe]['num'] = 1
                                    declTypeKinds[k][tipe]['all'] = tmpAll
                                    declTypeKinds[k][tipe]['comp'] = tmpComp
                                    declTypeKinds[k][tipe]['generic'] = tmpGeneric
                        else:
                            numComponentBlocksWithoutKind+=1

                        tipe = blk['*type']
                        if (tmpComp == 0 and tmpAll != 0) or (tipe == "component_event" and tmpComp == 1):
                            k = blk['kind']
                        
                            if tipe not in nonComponentBlockTypes:
                                nonComponentBlockTypes[tipe] = 1
                            else:
                                nonComponentBlockTypes[tipe] += 1
                            if k in nonComponentBlockTypesKinds:
                                if tipe in nonComponentBlockTypesKinds[k]:
                                    nonComponentBlockTypesKinds[k][tipe] += 1
                                else:
                                    nonComponentBlockTypesKinds[k][tipe] = 1
                            else:
                                nonComponentBlockTypesKinds[k] = {}
                                nonComponentBlockTypesKinds[k][tipe] = 1
                                topBlocksWithNoComps += 1
                                #print "Project " + eq.projectName + " by " + eq.programmerName + " has no component blocks"
                        if ind % 1000 == 0:
                            print allCount, compCount

    print compCount, allCount, topBlocksWithNoComps, totalBlocks, numBlocksWithKind
    print totalNumBlocksBesidesGlobalDecls, totalNumCompBlocksWOGlobalDecls

    print prettyPrint(nonComponentBlockTypes)
    print prettyPrint(kindsDict)
    print prettyPrint(nonComponentBlockTypesKinds)

    with open("declarationtypesdict.txt", "w") as f:
        f.write(prettyPrint(declTypeKinds))
        f.flush()

    with open("procedurenames.txt", "w") as f:
        f.write('\n'.join(procedureReturns))
        f.flush()

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
'''
s = screens[0]

code = potenJail['screens'][s]['bky']['topBlocks']
blocks = copy.deepcopy(code)

#for b in blocks:
#    fuzzify(b)

#allAreUnique(blocks)


#print compareBlocks(blocks, 15, 16)

#createDiff(blocks[15], blocks[16], 15, 16)

ec = equivalenceClassify(blocks)

bakeproj = ProjectSet(bakeCode)

print bakeproj.classSizes(3)

#bakeECs = [equivalenceClassify(c) for c in bakeCode]

print ec
i = 0
#for equiv in bakeECs:
#    print bakeScreens[i], equiv
#    i += 1


'''

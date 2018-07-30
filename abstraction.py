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

import zipUtils as zu

diffDirectory = ""
dirName = os.path.dirname(os.path.realpath(__file__))

tagsSeen = {}

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
    
    for tag in tagsToCheck:
        if tag in blk:
            fuzzify(blk[tag], depth + 1)
     
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

def jailToEquivs(jailLocation):
    printMessagesEverySoOften = 10000
    bigDirs = getDirectories(jailLocation)
    equivs = []
    class MyNum:
        num = 0
    #num = 0

    def unarchivedFiles(usersDir, userID, projName):
        jail = getJail(os.path.join(jailLocation, usersDir, userID, projName))
        equivify(jail, usersDir, userID, projName)

    def archivedFiles(fileName, fileArchive):
        jail = json.load(fileArchive)
        splits = fileName.split("/")
        equivify(jail, "", splits[0], splits[1])
        
    def equivify(jail, usersDir, userID, projName):
        screenNames = jail['*Names of Screens']
        onlyUsedNames = []
        code = []
        for name in screenNames:
            screenCode = jail['screens'][name]['bky']
            if isinstance(screenCode, dict):
                blks = screenCode['topBlocks']
                blks = [b for b in blks if 'kind' in b and b['kind'] == 'declaration']
                if len(blks) != 0:
                    code.append(blks)
                    onlyUsedNames.append(name)
        #             screen names --> vvvvvvvvvvvvv
        equivs.append(ProjectSet(code, onlyUsedNames, projName, userID))
        #                                     the user's id --> ^^^^^^^
        MyNum.num += 1
        if MyNum.num % printMessagesEverySoOften == 0:
            logwrite("equivify() in jailToEquivs()::" + str(MyNum.num) + ": " + os.path.join(usersDir, userID, projName))
    if len(bigDirs) == 0:
        files = getFileNames(jailLocation)
        for f in files:
            zu.withUnzippedFiles(os.path.join(jailLocation, f), archivedFiles)
    else:
        for bigdir in bigDirs:
            littledirs = getDirectories(os.path.join(jailLocation, bigdir))
            for littledir in littledirs:
                files = getFileNames(os.path.join(jailLocation, bigdir, littledir))
                for f in files:
                    unarchivedFiles(bigdir, littledir, f)
                    '''jail = getJail(os.path.join(jailLocation, bigdir, littledir, f))
                    screens = jail['*Names of Screens']
                    code = []
                    for s in screens:
                        if isinstance(jail['screens'][s]['bky'], dict):
                            code.append(jail['screens'][s]['bky']['topBlocks'])
                    equivs.append(ProjectSet(code, f, littledir))
                    num += 1
                    if num % printMessagesEverySoOften == 0:
                        logwrite(str(num) + " " + str(equivs[num-1].numScreens()))'''
    return equivs


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

def isDisabled(block):
    if "disabled" in block:
        return block["disabled"] == "true"
    return False
                    
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

def countAllBlocksWrapper(eq, blk):
    countAllBlocks(blk)
                        
#def zipFileProcessFunction(archFileName, archFile):
#    logwrite(archFileName)

#def getEquivsFromZips(location):
#    zipFileNames = getFileNames(location)
#    for zf in zipFileNames:
#        zu.withUnzippedFiles(os.path.join("46kjailzips", zf), zipFileProcessor)                    
if __name__=='__main__':
    createLogFile()
    loc10k = "10kjails"
    loc46k = "46kjailzips"

    #jailToEquivs(loc46k)
    equivs = jailToEquivs(loc10k)

    iterateOverProjectSets(equivs, countAllBlocksWrapper)

    for k,v in tagsSeen.iteritems():
        logwrite(k + ": " + ", ".join(v))
    #equivs = jailToEquivs("10kjails")

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

    decls = []

    for eq in equivs:
        for codeset in eq:
            for equivClass in codeset:
                equivClass.findComponentCorrespondence()
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
                                decls.append({"type": tipe,
                                              "kind": k,
                                              "name": getName(blk),
                                              "screen": codeset.screenName,
                                              "programmer": eq.programmerName,
                                              "project": eq.projectName,
                                              "numBlocks": str(tmpAll),
                                              "numCompBlocks": str(tmpComp),
                                              "numDupes": equivClass.size()
                                })
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
                            logwrite("all, comp: " + str(allCount) + ", " + str(compCount))
                            equivClass.showCorrespondence()
                            

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

    cols = ["type", "kind", "name", "screen", "programmer", "project", "numBlocks", "numCompBlocks", "numDupes"]
    with open("declfacts.csv", "w") as f:
        declCSVLines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in decls])
        f.write(",".join(cols))
        f.write(declCSVLines)
        f.flush()

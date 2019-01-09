''' abstraction.py
    Created on 2018/07/12 by Audrey Seo

    Parses a jail file and then allows you to compare how similar each of the handlers are.

    Most of the history can be read in the comments throughout, or in the commit messages.
'''

import json
import os
import copy
# [2018/07/13] Use difflib to generate diff output
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


totalGenerics = 0
totalHandlerBlocks = 0
totalComponents = 0
def jailToEquivs(jailLocation):
    printMessagesEverySoOften = 10000
    bigDirs = getDirectories(jailLocation)
    equivs = []
    global totalGenerics
    global totalHandlerBlocks
    global totalComponents
    class MyNum:
        num = 0
        totalGenerics = 0
        totalHandlerBlocks = 0
    #num = 0

    def getStatsOnGenerics(jail):
        global totalGenerics
        global totalHandlerBlocks
        global totalComponents
        screenNames = jail["*Names of Screens"]
        for screen in screenNames:
            code = jail["screens"][screen]["bky"]
            if isinstance(code, dict):
                blocks = code["topBlocks"]
                blocks = [b for b in blocks if '*type' in b and b['*type'] == "component_event"]
                #blocks = [b for b in blocks if 'kind' in b and b['kind'] == "declaration" and "*type" in b and b["*type"] != "global_declaration"]
                for blk in blocks:
                    totalGenerics += countGenerics(blk)
                    totalHandlerBlocks += countBlocksInside(blk)
                    comp, gen = countComponents(blk)
                    totalComponents += comp

    def unarchivedFiles(usersDir, userID, projName):
        jail = getJail(os.path.join(jailLocation, usersDir, userID, projName))
        equivify(jail, usersDir, userID, projName)

    def archivedFiles(fileName, fileArchive):
        jail = json.load(fileArchive)
        splits = fileName.split("/")
        equivify(jail, "", splits[0], splits[1])
        
    def equivify(jail, usersDir, userID, projName):
        #getStatsOnGenerics(jail)
        screenNames = jail['*Names of Screens']
        onlyUsedNames = []
        code = []
        for name in screenNames:
            screenCode = jail['screens'][name]['bky']
            if isinstance(screenCode, dict):
                blks = screenCode['topBlocks']
                blks = [b for b in blks if '*type' in b and b['*type'] == "component_event"]
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
    logwrite("jailToEquivs():: Number of generics: " + str(totalGenerics))
    logwrite("jailToEquivs():: Total number of blocks in handlers: " + str(totalHandlerBlocks))
    logwrite("jailToEquivs():: Total number of component blocks: " + str(totalComponents))
    return equivs


def dupesByEquivsObject(project, projectSet, equivClass):
    return {
        "programmer": project.programmerName,
        "project": "\"" + project.projectName + "\"",
        "screen": projectSet.screenName,
        "name": "" if equivClass.size() == 0 else "\"" + getName(equivClass.members[0]) + "\"",
        "type": "" if equivClass.size() == 0 else equivClass.members[0]["*type"],
        "kind": "" if equivClass.size() == 0 else equivClass.members[0]["kind"],
        "size": "0" if equivClass.size() == 0 else str(countAllBlocks(equivClass.members[0])),
        "requiresGenerics": str(equivClass.needsGenerics())
    }

                        
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
    logEvery = 1000
    analysisType = "10k"
    equivs = []
    csvDirectory = "testCSVs"
    txtDirectory = "testTXTs"
    if analysisType == "46k":
        logEvery = 50000
        equivs = jailToEquivs(loc46k)
    else:
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

    duplicationsByScreen = []

    dupesByEC = []

    # Why is going through this stuff always a pain sigh.
    # I want to make this look better, i.e. cleaner but is it always just going to be this mess.
    for eq in equivs:
        for codeset in eq:
            greaterThanFive = False
            for equivClass in codeset:
                dupesByEC.append(dupesByEquivsObject(eq, codeset, equivClass))
                equivClass.findComponentCorrespondence()
                if equivClass.size() > 0:
                    for blk in equivClass:
                        ind += 1
                        tmpAll = countAllBlocks(blk)
                        tmpComp, tmpGeneric = countComponents(blk)
                        if tmpAll > 5:
                            totalBlocks += 1
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
                                if tipe != "global_declaration" and k == "declaration":
                                    decls.append({"type": tipe,
                                                  "kind": k,
                                                  "name": "\"" + getName(blk) + "\"",
                                                  "screen": codeset.screenName,
                                                  "programmer": eq.programmerName,
                                                  "project":  "\"" + eq.projectName + "\"",
                                                  "numBlocks": str(tmpAll),
                                                  "numCompBlocks": str(tmpComp),
                                                  "numDupes": str(equivClass.size())
                                    })
                                    totalNumBlocksBesidesGlobalDecls += tmpAll
                                    totalNumCompBlocksWOGlobalDecls += tmpComp
                                    if k not in declTypeKinds:
                                        declTypeKinds[k] = {}
                                    if tipe not in declTypeKinds[k]:
                                        declTypeKinds[k][tipe] = {}
                                    #if k in declTypeKinds:
                                    #    if tipe not in declTypeKinds[k]:
                                    #        declTypeKinds[k][tipe] = {}
                                    #else:
                                    #    declTypeKinds[k] = {}
                                    #    declTypeKinds[k][tipe] = {}
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
                                
                            if ind % logEvery == 0:
                                logwrite(eq.identity() + "::" + equivClass.getName() +  ":: all, comp: " + str(allCount) + ", " + str(compCount))
                                equivClass.showCorrespondence()
            #if greaterThanFive:
            scrn = codeset.screenName
            basics = {"programmer": eq.programmerName,
                      "project": "\"" + eq.projectName + "\"",
                      "screen": codeset.screenName,
                      "numEquivClasses": str(codeset.numClasses()),
                      "totalDuplicatedHandlers": str(0) if codeset.numClassesLargeEnough() == 0 else str(reduce((lambda x, y: x + y), codeset.sizes(useLargeEnough=True))),
                      "avgNumBlocks": str(codeset.avgNumBlocks(True))
            }
            duplicationsByScreen.append(basics)                

    print compCount, allCount, topBlocksWithNoComps, totalBlocks, numBlocksWithKind
    print totalNumBlocksBesidesGlobalDecls, totalNumCompBlocksWOGlobalDecls

    print prettyPrint(nonComponentBlockTypes)
    print prettyPrint(kindsDict)
    print prettyPrint(nonComponentBlockTypesKinds)

    declarationTypesDictLoc = os.path.join(txtDirectory, analysisType + "declarationtypesdict.txt")
    procedureNamesLoc = os.path.join(txtDirectory, analysisType + "procedurenames.txt")

    with open(declarationTypesDictLoc, "w") as f:
        f.write(prettyPrint(declTypeKinds))
        f.flush()

    with open(procedureNamesLoc, "w") as f:
        f.write('\n'.join(procedureReturns))
        f.flush()


    declarationFactsLoc = os.path.join(csvDirectory, analysisType + "declfacts.csv")
    dupesLoc = os.path.join(csvDirectory, analysisType + "-dupes.csv")
    equivclassDupesLoc = os.path.join(csvDirectory, analysisType + "-ec_dupes.csv")
    with open(declarationFactsLoc, "w") as f:
        cols = ["type", "kind", "name", "screen", "programmer", "project", "numBlocks", "numCompBlocks", "numDupes"]
        declCSVLines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in decls])
        f.write(",".join(cols) + "\n")
        f.write(declCSVLines)
        f.flush()

    with open(dupesLoc, "w") as f:
        cols = ["programmer", "project", "screen", "numEquivClasses", "totalDuplicatedHandlers", "avgNumBlocks"]
        csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in duplicationsByScreen])
        f.write(",".join(cols) + "\n")
        f.write(csvlines)
        f.flush()

    with open(equivclassDupesLoc, "w") as f:
        cols = ["programmer", "project", "screen", "type", "kind", "name", "size", "requiresGenerics"]
        csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in dupesByEC])
        f.write(",".join(cols) + "\n")
        f.write(csvlines)
        f.flush()

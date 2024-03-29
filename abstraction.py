# Lyn's version 
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
import argparse

# [2019/01/11] The "libraries" that I made of helper functions for this
# from equivalenceclasses import *
import equivalenceclasses as eclasses
import myutils as mus
#from myutils import *
import findmissing as fm
#from findmissing import *

import zipUtils as zu

diffDirectory = ""
dirName = os.path.dirname(os.path.realpath(__file__))

tagsSeen = {}



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
    if mus.isCommutative(blk):
        if argsKey in blk:
            arg1 = copy.deepcopy(blk[argsKey][0])
            arg2 = copy.deepcopy(blk[argsKey][1])
            name1 = getName(arg1)
            name2 = mus.getName(arg2)
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
    mus.removeIDs(blockCopy)
    return json.dumps(blockCopy, indent=2, separators=(',', ': ')).split('\n')

# [2018/07/16] determines if nonsimilar blocks should have a diff outputed
# for them, and creates and outputs that diff.
def createDiff(blockA, blockB, nameA=None, nameB=None):
    if nameA == None:
        if 'instance_name' in blockA:
            nameA = mus.getName(blockA)
    else:
        nameA = str(nameA)
    if nameB == None:
        if  'instance_name' in blockB:
            nameB = mus.getName(blockB)
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
userMaxes = {} # [2019/08/01, lyn] track max equivClassSize and equivClassNumBlocks for each user

def jailToEquivs(jailLocation):
    printMessagesEverySoOften = 10000
    bigDirs = fm.getDirectories(jailLocation)
    equivs = []
    global totalGenerics
    global totalHandlerBlocks
    global totalComponents

    class MyNum:
        num = 0
        totalGenerics = 0
        totalHandlerBlocks = 0
    #num = 0

    # Only used once in commented-out code, so this is technically obsolete
    """
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
    """
    def unarchivedFiles(usersDir, userID, projName):
        jail = mus.getJail(os.path.join(jailLocation, usersDir, userID, projName))
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
                blks = [b for b in blks if '*type' in b and b['*type'] == "component_event"
                        and not mus.isDisabled(b) # [2019/08/01, lyn] Added this since previous version
                                                  # was including some disabled event handlers here
                                                  # and they caused problems later. Disabled is effectively
                                                  # commented out, so treat them like not there. 
                        ]
                if len(blks) != 0:
                    code.append(blks)
                    onlyUsedNames.append(name)
        #             screen names --> vvvvvvvvvvvvv

        # [2019/08/01] Changed the following four lines, adding userMaxes stuff
        projSet = eclasses.ProjectSet(code, onlyUsedNames, projName, userID)
        equivs.append(projSet)
        oldMaxEquivClassSize, oldMaxEquivClassNumBlocks = (0, 0) if userID not in userMaxes else userMaxes[userID]
        projMaxEquivClassSize, projMaxNumBlocks = projSet.maxes()
        userMaxes[userID] = ( max(oldMaxEquivClassSize, projMaxEquivClassSize), 
                              max(oldMaxEquivClassNumBlocks, projMaxNumBlocks)
                            )
        MyNum.num += 1
        if MyNum.num % printMessagesEverySoOften == 0:
            mus.logwrite("equivify() in jailToEquivs()::" + str(MyNum.num) + ": " + os.path.join(usersDir, userID, projName))
    if len(bigDirs) == 0:
        files = fm.getFileNames(jailLocation)
        for f in files:
            zu.withUnzippedFiles(os.path.join(jailLocation, f), archivedFiles)
    else:
        for bigdir in bigDirs:
            littledirs = fm.getDirectories(os.path.join(jailLocation, bigdir))
            for littledir in littledirs:
                files = fm.getFileNames(os.path.join(jailLocation, bigdir, littledir))
                for f in files:
                    unarchivedFiles(bigdir, littledir, f)
                    '''jail = mus.getJail(os.path.join(jailLocation, bigdir, littledir, f))
                    screens = jail['*Names of Screens']
                    code = []
                    for s in screens:
                        if isinstance(jail['screens'][s]['bky'], dict):
                            code.append(jail['screens'][s]['bky']['topBlocks'])
                    equivs.append(eclasses.ProjectSet(code, f, littledir))
                    num += 1
                    if num % printMessagesEverySoOften == 0:
                        mus.logwrite(str(num) + " " + str(equivs[num-1].numScreens()))'''
    mus.logwrite("jailToEquivs():: Number of generics: " + str(totalGenerics))
    mus.logwrite("jailToEquivs():: Total number of blocks in handlers: " + str(totalHandlerBlocks))
    mus.logwrite("jailToEquivs():: Total number of component blocks: " + str(totalComponents))
    return equivs


def dupesByEquivsObject(project, projectSet, equivClass):
    return {
        "programmer": project.programmerName,
        "project": "\"" + project.projectName + "\"",
        "screen": projectSet.screenName,
        "name": "" if equivClass.size() == 0 else "\"" + mus.getName(equivClass.members[0]) + "\"",

        # [2019/08/01, lyn] All types are component_event, so punt
        # "type": "" if equivClass.size() == 0 else equivClass.members[0]["*type"],

        # [2019/08/01, lyn] All kinds are declaration, so punt
        # "kind": "" if equivClass.size() == 0 else equivClass.members[0]["kind"],

        # [2019/08/01, lyn] Add this field from ec_sizes (so don't need ec_sizes anymore)
        "numberDuplicatedHandlers": str(equivClass.size()),

        # [2019/08/01, lyn] Change size to numBlocks, and use equiv class numBlocks method
        # "size": "0" if equivClass.size() == 0 else str(mus.countAllBlocks(equivClass.members[0])),
        "numBlocks": "0" if equivClass.size() == 0 else str(equivClass.numBlocks()), 

        "requiresGenerics": str(equivClass.needsGenerics()), 

        # [2019/08/01, lyn] Added this
        "isSingleProcedureCall": str(equivClass.isSingleProcedureCall())
    }

                        
#def zipFileProcessFunction(archFileName, archFile):
#    mus.logwrite(archFileName)

#def getEquivsFromZips(location):
#    zipFileNames = fm.getFileNames(location)
#    for zf in zipFileNames:
#        zu.withUnzippedFiles(os.path.join("46kjailzips", zf), zipFileProcessor)                    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Run loop analysis")

    parser.add_argument("--kind", action="store", type=int, choices=[10, 46], default=10, help="Choose which dataset to run analysis on, either 10 or 46. Defaults to 10.")

    parser.add_argument("-s", "--start", action="store", type=int, default=-1, help="Which batch of users to start from (inclusive). Defaults to 0, values range from 0-46 for 46k. Only applies to the 46k dataset.")

    parser.add_argument("-e", "--end", action="store", type=int, default=-1, help="Which batch of users to end with (exclusive). Defaults to 5, values range from 0-47 for 46k. Only applies to the 46k dataset.")

    args = parser.parse_args()
    print(args)
    mus.createLogFile()
    loc10k = "10kjails"
    loc46k = "46kjailzips"
    # loc46k = "../../data/ai2_46K_prolific_users_deidentified_jails_00_00000"
    logEvery = 1000
    analysisType = "10k" if args.kind == 10 else "46k"
    equivs = []
    csvDirectory = "testCSVs"
    txtDirectory = "testTXTs"
    if analysisType == "46k":
        logEvery = 50000
        equivs = jailToEquivs(loc46k)
    else:
        equivs = jailToEquivs(loc10k)

    # [2019/08/01] As far as lyn can determine, the following 4 lines have no effect b/c
    #   (1) mus.countAllBlocksWrapper (really mus.countAllBlocks) returns a number, but doesn't have a side effect
    #   (2) tagsSeen is no longer updated by mus.countAllBlocksWrapper (really mus.countAllBlocks)
    # mus.iterateOverProjectSets(equivs, mus.countAllBlocksWrapper)
    # 
    # for k,v in tagsSeen.iteritems():
    #    mus.logwrite(k + ": " + ", ".join(v))

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
    # equivalence class size, for generating frequency
    ecSizes = []
    procedureReturns = []

    decls = []

    duplicationsByScreen = []

    dupesByEC = []

    shouldPrint = True

    # Why is going through this stuff always a pain sigh.
    # I want to make this look better, i.e. cleaner but is it always just going to be this mess.
    for eq in equivs:
        for codeset in eq:
            greaterThanFive = False # [2019/08/01, lyn] I set this to False, but it is never used!
            for equivClass in codeset:
                dupesByEC.append(dupesByEquivsObject(eq, codeset, equivClass))
                # equivClass.findComponentCorrespondence() # [2019/08/01, lyn] I think this is unnecessary, 
                                                           # since dupesByEquivsObject calls equivClass.needsGenerics()
                                                           # which calls self.findComponentCorrespondence() if 
                                                           # self.corrmatrix == [].
                                                           # In any case, this test shoud be moved into 
                                                           # self.findComponentCorrespondence() itself to memoize result.

# [2019/08/01, lyn] Commented out all of the following
#                 ecSizes.append({
#                     "screen": codeset.screenName,
#                     "programmer": eq.programmerName,
#                     "project": eq.projectName,
#                     "numberDuplicatedHandlers": str(equivClass.size()),
#                     "blockName": equivClass.getName()
#                 })
#                 if equivClass.size() > 0: # [2019/08/01, lyn] This is always true, so why test? 
#                     for blk in equivClass:
                        
#                         ind += 1
#                         tmpAll = mus.countAllBlocks(blk) # ***==> [2019/08/01, lyn]
#                                                          # should really make this an operation on equivClass so:
#                                                          # (1) Calculate it for only one member of equiv class
#                                                          # (2) Store it in equiv class so it never needs to be calcualted again.
#                         tmpComp, tmpGeneric = mus.countComponents(blk) # ***==> [2019/08/01, lyn] Similar remarks to previous comment
#                         # [2019/08/01, lyn] the next two lines are hacky; should be done above in dictionary added to ecSizes
#                         if "numBlocks" not in ecSizes[len(ecSizes)-1]: 
#                             ecSizes[len(ecSizes) - 1]["numBlocks"] = str(tmpAll)
#                         if shouldPrint and tmpAll > 30: # [2019/08/01, lyn] For debugging? 
#                             print mus.prettyPrint(blk)
#                             shouldPrint = False
#                         if tmpAll > 5: # ***==> [2019/08/01, lyn] WHOAH, THIS IS HARDWIRED CHECK FOR NUM BLOCKS > 5.
#                                        # WHAT EFFECT DOES THIS HAVE ON RESULTS? 
#                             totalBlocks += 1
#                             allCount += tmpAll
#                             compCount += tmpComp
#                             if 'kind' in blk:
#                                 numBlocksWithKind += 1
#                                 k = blk['kind']
#                                 tipe = blk['*type']
#                                 if tipe == "procedures_defreturn":
#                                     procedureReturns.append(eq.projectName + "-" + eq.programmerName)
#                                 if k in kindsDict:
#                                     kindsDict[k] += 1
#                                 else:
#                                     kindsDict[k] = 1
#                                 if tipe != "global_declaration" and k == "declaration":
#                                     decls.append({"type": tipe,
#                                                   "kind": k,
#                                                   "name": "\"" + mus.getName(blk) + "\"",
#                                                   "screen": codeset.screenName,
#                                                   "programmer": eq.programmerName,
#                                                   "project":  "\"" + eq.projectName + "\"",
#                                                   "numBlocks": str(tmpAll),
#                                                   "numCompBlocks": str(tmpComp),
#                                                   "numDupes": str(equivClass.size())
#                                     })
#                                     totalNumBlocksBesidesGlobalDecls += tmpAll
#                                     totalNumCompBlocksWOGlobalDecls += tmpComp
#                                     if k not in declTypeKinds:
#                                         declTypeKinds[k] = {}
#                                     if tipe not in declTypeKinds[k]:
#                                         declTypeKinds[k][tipe] = {}
                                    
#                                     declTypeKinds[k][tipe]['num'] = 1
#                                     declTypeKinds[k][tipe]['all'] = tmpAll
#                                     declTypeKinds[k][tipe]['comp'] = tmpComp
#                                     declTypeKinds[k][tipe]['generic'] = tmpGeneric
#                             else:
#                                 numComponentBlocksWithoutKind+=1

#                             tipe = blk['*type']
#                             if (tmpComp == 0 and tmpAll != 0) or (tipe == "component_event" and tmpComp == 1):
#                                 k = blk['kind']

#                                 if tipe not in nonComponentBlockTypes:
#                                     nonComponentBlockTypes[tipe] = 1
#                                 else:
#                                     nonComponentBlockTypes[tipe] += 1

#                                 if k not in nonComponentBlockTypesKinds:
#                                     nonComponentBlockTypesKinds[k] = {}

#                                 if tipe not in nonComponentBlockTypesKinds[k]:
#                                     nonComponentBlockTypesKinds[k][tipe] = 1
#                                 else:
#                                     nonComponentBlockTypesKinds[k][tipe] += 1
                                
#                                 topBlocksWithNoComps += 1
                                
#                             if ind % logEvery == 0:
#                                 mus.logwrite(eq.identity() + "::" + equivClass.getName() +  ":: all, comp: " + str(allCount) + ", " + str(compCount))
#                                 equivClass.showCorrespondence()
#             #if greaterThanFive:
#             scrn = codeset.screenName
#             basics = {"programmer": eq.programmerName,
#                       "project": "\"" + eq.projectName + "\"",
#                       "screen": codeset.screenName,
#                       "numEquivClasses": str(codeset.numClasses()),
#                       "totalDuplicatedHandlers": str(0) if codeset.numClassesLargeEnough() == 0 else str(reduce((lambda x, y: x + y), codeset.sizes(useLargeEnough=True))),
#                       "avgNumBlocks": str(codeset.avgNumBlocks(True))
#             }
#             duplicationsByScreen.append(basics)                

#     print compCount, allCount, topBlocksWithNoComps, totalBlocks, numBlocksWithKind
#     print totalNumBlocksBesidesGlobalDecls, totalNumCompBlocksWOGlobalDecls

#     print mus.prettyPrint(nonComponentBlockTypes)
#     print mus.prettyPrint(kindsDict)
#     print mus.prettyPrint(nonComponentBlockTypesKinds)

#     declarationTypesDictLoc = os.path.join(txtDirectory, analysisType + "declarationtypesdict.txt")
#     procedureNamesLoc = os.path.join(txtDirectory, analysisType + "procedurenames.txt")

#     with open(declarationTypesDictLoc, "w") as f:
#         f.write(mus.prettyPrint(declTypeKinds))
#         f.flush()

#     with open(procedureNamesLoc, "w") as f:
#         f.write('\n'.join(procedureReturns))
#         f.flush()


#   declarationFactsLoc = os.path.join(csvDirectory, analysisType + "declfacts.csv")
#   dupesLoc = os.path.join(csvDirectory, analysisType + "-dupes.csv")
    equivclassDupesLoc = os.path.join(csvDirectory, analysisType + "-ec_dupes.csv")
    userMaxesLoc = os.path.join(csvDirectory, analysisType + "-user_maxes.csv")
#   ecSizesLoc = os.path.join(csvDirectory, analysisType + "-ec_sizes.csv")

#   print declarationFactsLoc, dupesLoc, equivclassDupesLoc
    print equivclassDupesLoc, userMaxesLoc
    
#     with open(declarationFactsLoc, "w") as f:
#         cols = ["type", "kind", "name", "screen", "programmer", "project", "numBlocks", "numCompBlocks", "numDupes"]
#         declCSVLines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in decls])
#         f.write(",".join(cols) + "\n")
#         f.write(declCSVLines)
#         f.flush()

#     with open(dupesLoc, "w") as f:
#         cols = ["programmer", "project", "screen", "numEquivClasses", "totalDuplicatedHandlers", "avgNumBlocks"]
#         csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in duplicationsByScreen])
#         f.write(",".join(cols) + "\n")
#         f.write(csvlines)
#         f.flush()

    with open(equivclassDupesLoc, "w") as f:
        # cols = ["programmer", "project", "screen", "type", "kind", "name", "size", "requiresGenerics"]
        # [2019/08/01, lyn] changed columns
        cols = ["programmer", "project", "screen", "name", 
                "numberDuplicatedHandlers", "numBlocks" , "requiresGenerics", "isSingleProcedureCall"]
        csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in dupesByEC])
        f.write(",".join(cols) + "\n")
        f.write(csvlines)
        f.flush()

#     with open(ecSizesLoc, "w") as f:
#         cols = ["programmer", "project", "screen", "blockName", "numberDuplicatedHandlers", "numBlocks"]
#         csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in cols])) for d in ecSizes])
#         f.write(",".join(cols) + "\n")
#         f.write(csvlines)
#         f.flush()

    def userMaxesLines(userMaxesDict):
        sortedUsers = sorted(userMaxesDict.keys())
        return [userMaxesLine(user, userMaxesDict) for user in sortedUsers]

    def userMaxesLine(user, userMaxesDict):
        if user in userMaxesDict:
            max1, max2 = userMaxesDict[user]
        else:
            max1, max2 = (0, 0)
        return [user, str(max1), str(max2)]

    # [2019/08/01, lyn] New cvs file for tracking user maxes.
    with open(userMaxesLoc, "w") as f:
        cols = ["programmer", "maxEquivClassSize", "maxEquivClassNumBlocks"]
        csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), line))
                              for line in userMaxesLines(userMaxes)])
        f.write(",".join(cols) + "\n")
        f.write(csvlines)
        f.flush()

        

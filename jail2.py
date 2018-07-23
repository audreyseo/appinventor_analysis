# Represent App Inventor project file as JAIL = JSON App Inventor Language
#
# Authors: Lyn Turbak, with contributions by Audrey Seo, Maja Svanberg, and Benjie Xie
# 
# History: 
# * Initially created by Lyn in summer 2015? 
# * Maja adapted code to her ai2_summarizer for tutorial finding. 
#   This incorporated some code by Benji and was heavily edited by Lyn 
# * 2016-11-19: As part of writing FLAIRS paper with Eni & Maja, lyn
#   adapted most current state of ai2_summarizer to do full JAIL again
# * 2018-07-11: Audrey brought in more code from ai2summarizer2, and
#   actually got jail working (mostly) completely.
#
# TODO:
# As of 2016-11-19:
# * Can we just use AI1_v134a_component_specs instead of componentDict from simple_components.json?

''' History (reverse chronological, comments through 2016/08/13 for ai2_summarizer.py, not jail.py)
-------------------------------------------------------------------------------
2018/07/23 (Audrey):
====================
* Stopped it from raising an error whenever the formName doesn't match the screenName

-------------------------------------------------------------------------------
2018/07/21 (Audrey):
====================
I wanted to get the jail files for at least all of the 10k projects, so I
commented out all of the print statements so that it would hopefully print out
in a somewhat timely manner.

I also needed to test it on a wider range of .aia files so that I could be sure
that it was actually fixed. There seems to be some exceptions regarding

* whether currentScreenName is defined
* the presence of yacodeblocks in the bky.

I think I will need to write a short script so that I can figure out which of
the files are missing because exceptions occurred during processing.

Updates:

* Added currentScreenName (useful for debugging anyway)
* Fixed logwrite and logStartTime so that it shows you the actual difference in
  time, because before it was just showing you today's date/time which was nice
  but not what I was looking for
* If variable names overlapped with the names of python's builtin functions,
  I changed the name given to something shortened or otherwise changed, i.e.
  type => tipe, property => prop, etc.
* Added support for mangled types
* Added dummy yacode for when yacodeblocks is missing from the XML


Noted problems:

* Claims to not recognize type TinyDB1_StoreValue -- which is shouldn't anyway,
  because that isn't a type in the first place, as well as other types
* screen names do not match form names
* Unknown method name for some method called DoQuery for FusionTablesControl
* Unrecognized block type Ball1_setproperty
* blockTypeToKind: unrecognized mangled component_set_get

-------------------------------------------------------------------------------
018/07/12 (Audrey):
====================
jail2 brings as many parts of ai2summarizer2 as is possible to adapt in just two days.
The functions that I've added include

* componentTypeToBlockName
* componentTypeToBlockType
* formToScreen
* upgradeNameFormat
* upgradeTypeFormat
* warningIgnoringMalformedBlock

I've also added in the globals

* logPrefix
* logStartTime
* printMessagesToConsole

for various logging reasons, which was for debugging. jail2.py should work completely
now, and it needs the support file dictionaries.py. I made the most changes to
blockToJAIL in order to get rid of the bugs.

-------------------------------------------------------------------------------
2016/11/19 (Lyn):
====================
Adapated most recent ai2summarizer.py to do JAIL rep for components and blocks
rather than summaries. Some notes: 

* rename bkyToSummary to bkyToJAIl and similarly for other functions. 
* have these functions record all details of blocks, not just summaries  
* Removed functions like processRawBlockList, sortListToDict, findBlockInfo
* Reinstall the used of componentDict, which reads simple_components.json. 
  Not clear if this is necessary, or we could just use AI1_v134a_component_specs instead

-------------------------------------------------------------------------------
2016/08/12-13 (Maja):
====================
* Modified bkyToSummary to only add the block to list of top level blocks
        if it isDeclarationType. 
* Moved declaration of temporary variables (directories etc, top flag etc) inside
    if __name__ == __main__ statement to enable functions to be resused in other
    contexts

-------------------------------------------------------------------------------
2016/08/12-13 (Lyn):
====================

* Modified findProjectDirs so that:
  + it does not assume dirName argument is a list of user directories, 
    each of which contains a list of projects. It handles any directory structure
    whose leaves are .aia/.zip files or Benji-like project directories
  + It will ignore project directory XYZ if XYZ.zip already exisits; otherwise,
    it will create XYZ.zip.
  + It now displays relative file name with project number to give better sense of progress.

* Modified allProjectsToJSONFile so that:
  + It doesn't delete .zip files anymore. (if .zip files are created, as for Benji user data, 
    they're cached and the original project directories from which they're created are ignored 
    by findProjectDirs.)
  + It now displays relative file name with project number to give better sense of progress.

* Fixed bug in not correctly handling output directory structure for long-term dataset. 
  Before, put 00000, ..., 00999,... 01000, ..., 01999, ..., 02000 all in the same output directory.
  Now it puts them in 00/00000, ..., 00/00999, ..., 01/01000, ..., 01/01999, ... 02/02000, ...

* Fixed bug in findCreatedModifiedTimes for handling METADATA file in Benji-style projects 
  (didn't work before).

* Modified error/exception and warning messages to include details of project and file names.

* Replaced several instances of the pattern list += subList by list.extend(subList);
  the later is more efficient since it doesn't copy initial prefix of list. 

-------------------------------------------------------------------------------
2016/08/07 (Maja):
================

MAJOR CHANGES:
-------------
* Incorporated ai2topsummarizer.py
    + added global variable topSummary as a flag
    + Remade processRawBlockList (fka formatLists) with a check to be able to format the two kinds.
    + bkyToSummary does not add blocks to top if topSummary is true. Enabled 
    two different return statements. Appending lists of blocks instead of adding
    them, allowing us to find the top block of each group. 
    + Added check to projectToJSONProjectFileName to write different named summaries
        + XYZ_summary_top.json and XYZ_summary.json
    
MINOR CHANGES
-------------
* Changed names of functions for clarity
    + formatLists -> processRawBlockList
    + sortToDict -> sortListToDict
* An exception thrown used variable projectPath that no longer exists. 
    + Changed this to refer to relProjectPath
    
-------------------------------------------------------------------------------
2016/08/05 (Lyn):
================

MAJOR CHANGES
-------------
* Modified findProjectDirs to return a list of *relative* project paths, not *absolute* project paths.
  (This simplifies writing summary files to destination directory other than user directory.)
* Modified allProjectsToJSONFiles so that:
  + 2nd arg = numUsers has default value None, which returns projects of all users 
  + has new 3rd arg outputDir with default value None
    - A non-None value specifies (possibly new) target directory for summary .json files
    - A None value writes XYZ_summary.json file to same directory as .aia/.zip file
* Modified findProjectDirs so that numUsers has default value None, which returns projects of all users 
* Modified projectToJSONFile so that 1st arg is pathname relative to new 2nd arg and new 3rd argument 
  is outputDir with with default value None.
  + A non-None value specifies (possibly newly created) target directory for summary .json files
  + A None value writes XYZ_summary.json file to same directory as .aia/.zip file
* Modified scmToComponents to process components recursively, fixing bug in previous versions,
  which didn't correct process subcomponents of HorizontalArrangement, VerticalArrangement, and Canvas
* Defined isDeclarationType(generalType, specificType), which fixes several bugs in determining whether
  a block is a top-level declaration block. 
  + lexical_variable_get and lexical_variable_set used to be incorrectly treated as top-level declarations.
  + any "old-style" block, like 'DrawingCanvas_Clicked', 'DrawingCanvas_DrawCircle', or 'Button_SetText'
    was previously treated as a top-level declaration, but only the first is. Handling this correctly
    required introducing the dictionary AI1_v134a_component_specs from the AI1 to AI2 converter. 
* For old-style projects, replaced findComponentType/searchComponents by a mechanism that creates 
  (only once for each old-style screen) a dictionary mapping component names (like 'DrawingCanvas') 
  to component types (like 'Canvas').
* Modified blockType and upgradeFormat to handle generic methods and generic getters/setters.
  Name of generic blocks were not handled before, but now end in 'Generic'.
  E.g. Button.SetText is the non-generic setter, but Button.SetTextGeneric is the generic setter
* Modified scmToComponents to distinguish "Number of Component Types" from "Number of Components"
* Modified bkyToSummary to distinguish "*Number of Block Types" from "Number of Blocks"
* Fixed bug in findBlockInfo in categorizing global vs. local variable getters/setters

MINOR CHANGES
-------------
* Add new function projectToJSONProjectFileNamed that handles cases where projectPath contains dot
  in position other than extension
* Cleaned up use of global variables. It's generally considered bad style to pass parameters by global variable, 
  so passing information by explicit parameters is preferred. One exception is where a parameter would need
  to be passed down a long chain of calls to the point where it is used. 
  + Renamed global var projectPath to currentProjectPath, and declare it globally. 
    This is helpful for including projectPath in exception messages. 
  + Removed global var zippedFile. 
    Modified findName, findCreatedModifiedTimes, and friends to take explict zippedFile argument.
  + Removed global var screen and changed screenToJSON to take explicit screenName argument.
  + Removed global var scmFileName and changed scmToComponents to take explicit scmFileName argument.
  + Removed global name bkyFileName and changed bkyToSummary to take explicit arg
  + Added global currentScmJSONContents = to track contents of .scm file for currentScreen
* Modified findCreatedModifiedTimes to handle both META and METADATA files and projects without these
* Commented out dummyMeta, which is superseded by modified findCreatedModifiedTimes
* Simplified the collection of media in scmToComponents and findMedia. Made the findMedia function
  local to scmToComponents. 
* Added missing entries to blocklyTypeDict: 
  + 'text_split_at_spaces'
  + 'obfuscated_text', 
  + 'obsufcated_text' (early misspelling of 'obfuscated_text')

OTHER NOTES
-----------
* Use processTutorials() to create summaries for all tutorials.
  But you'll need to first set the global vars tutorialsInputDir and tutorialsOutputDir

-------------------------------------------------------------------------------
2015/08/03 (Maja)
================
* Fixed bug where no old-style format blocks were named "active blocks"
* Incorporated Eni's changes and instead of declaring an empty project to 
    have "NO BLOCKS", instead the empty dictionary structure is returned. 
    
-------------------------------------------------------------------------------
2015/08/02 (Maja)
================
* In an effort to speed up the code, passing down some parameters as global variables instead 
    of explicit. Later removed by Lyn.
    
-------------------------------------------------------------------------------
2015/07/22 (Lyn)
================
* Enabled summarizer to run on larger dataset, includes nextIndex functions
    to enable code to be run on separate occasions. 

-------------------------------------------------------------------------------
2015/07/15 (Maja)
================
* Fixed bug that caused old-style block not recognized by the upgrader to be handled
properly instead of returning "None.ACTION"
* Added commenting to parts of the code

-------------------------------------------------------------------------------
2015/07/12 (Maja)
================
* Fixed bug in old-style formatting upgrade, get_set is now handled properly. 

-------------------------------------------------------------------------------
2015/05 and 2015/06 (Maja)
================

Editing history forgone, all changes not recorded were made by Maja. 

-------------------------------------------------------------------------------
2015/04/23 (Benji)
================
* added error handling for missing SCM files, validation for screen 
    names startin with letter, timing execution
* added error handling for JSON loading
    
-------------------------------------------------------------------------------
2015/03/24 (Benji)
================
* handled issues relating to missing project.properties file and 
    improper case for scm and bky files
* added created and modified times to summary, handling cases for missing 
    META file, counting # of missing properties, META, case mismatches
    
-------------------------------------------------------------------------------
2015/01/19 (Maja)
================
* fixed bug of findComponentType requesting nonexisting keys
  
-------------------------------------------------------------------------------
2015/01/17 (Benji)
================
* fixed bug of trying to access zip file that did not exist in allProjectsToJSONFiles

-------------------------------------------------------------------------------
2015/01/15 (Maja)
================
* Cleaned up formatting of bkyToSummary(), following note Lyn made.

-------------------------------------------------------------------------------
2015/12/27 (Maja)
================
* Fixed bug in findMedia()

-------------------------------------------------------------------------------
2015/11/15 (Maja)
================
* Enabled upgrade of Old-Style blocks, added functions upgradeFormat() and findComponentType()

-------------------------------------------------------------------------------
2015/11/11 (Lyn):
================
* replace component_event, component_method, component_set_get by component-specific details. E.g.
  + not component_event, but Canvas.Draggged, ListPicker.AfterPicking, etc.  
  + not component_method, but Canvas.DrawLine
  + not component_set_get, but Label.GetText, Label.SetText

-------------------------------------------------------------------------------
2015/10 (Maja)
================
* Document created by Maja
     + Run by using allProjectsToJSONFiles()
     + Creates JSON sumaries of all .aia, .zip and directories representing 
     ai2 projects. 


'''

import os
import os.path
import json
import zipfile
import xml.etree.ElementTree as ET
import datetime
import sys # [2016/08/06, lyn] New, for sys.exc_info()

from dictionaries import * # [2018/07/11, audrey] Gets all of the same dictionaries that ai2summarizer2 uses

# for dummy project.properties and meta files 
DUMMY_PROJECT_NAME = '<<dummy_project_name>>'
DUMMY_USER_NAME = '<<dummy_user_name>>'
DUMMY_CREATED_TIME = -2
DUMMY_MODIFIED_TIME = -1
DUMMY_VERSION = -1
DUMMY_SCREEN_NAME = '<<dummy_screen_name>>'

num_missing_properties = 0
num_missing_meta = 0
num_missing_scm = 0
num_case_mismatches = 0

# *** Added by lyn 
# print_every = 100
# print_every = 1
print_every = 1000

# *** Removed by lyn
'''
# meta_filename = 'METADATA' # 'METADATA' for old files, 'META' for new files
meta_filename = 'META' # 'METADATA' for old files, 'META' for new files
'''

# *** Added by lyn 
currentProjectPath = None # Global variable that tracks current project path being processed
currentScmJSONContents = None # Global variable that tracks contents of .scm file for currentScreen
currentComponentDictionary = {} # Global variable that contains dictionary mapping component names to component types for current screen

# *** Added by audrey
currentScreenName = None

def allProjectsToJAILFiles(inputDir, numToKeep=None, outputDir=None):
    '''assumes cwd contains dir, that contains projects (in .aia, .zip, or as dir).
      + 2nd arg = numUsers has default value None, which returns projects of all users 
      + has new 3rd arg outputDir with default value None
        - A non-None value specifies (possibly new) target directory for summary .json files
        - A None value writes XYZ_summary.json file to same directory as .aia/.zip file.'''
    logwrite('allProjectsToJAILFiles({}, {}, {})'.format(inputDir, numToKeep, outputDir))
    logwrite('Finding projects (zipping as necessary) ...')
    listOfAllProjects = findProjectDirs(inputDir, numToKeep)
    logwrite("Done finding projects...")
    # *** Added by lyn 
    logwrite("Number of projects to process: " + str(len(listOfAllProjects)))
    # *** Added by lyn 
    num_projects_processed = 0
    for relProjectPath in listOfAllProjects:
        absProjectPath = os.path.join(inputDir, relProjectPath)
        if os.path.exists(absProjectPath):
            projectToJAILFile(relProjectPath, inputDir, outputDir)
            # [2016/08/12] Don't delete .zip file anymore! (Leave it in case we want to reprocess!)
            # if os.path.exists(absProjectPath.split('.')[0]) and absProjectPath.split('.')[1] == 'zip':
            #    # *** Note from Lyn: should only remove if it's not the main representation of the project!
            #    os.remove(absProjectPath)
        # *** Added by lyn 
        num_projects_processed += 1
        if num_projects_processed % print_every == 0: 
            logwrite(str(num_projects_processed) + ": " + relProjectPath)

# [2016/08/06, lyn] Modified this to return list of paths *relative* to dirName, rather than
#  *absolute* paths including dirName. This simplifies  This simplifies writing summary files 
# to a destination directory other than dirName.
def findProjectDirs(dirName, numToKeep=None):
    """
    given path to directory containing users (dirName) and number of users(numUsers),
    zip user directories and return list of PATHS RELATIVE TO DIRNAME to zipped project directories.
    If numUsers is None, return projects of all users; else return projects of
    first numUser users. 
    """
    relProjectPaths = []
    num_projects_processed = [0] # Listify to solve scoping issues
    def processFileOrDir(relPrefix, fileOrDir): # Recursively process directories until get to projects. 
        foundProject = False
        relPath = os.path.join(relPrefix, fileOrDir)
        absPath = os.path.join(dirName, relPath)
        if relPath.endswith('.aia') or relPath.endswith('.zip'):
            # Assume this is a project file
            relProjectPaths.append(relPath)
            foundProject = relPath
        elif os.path.isdir(absPath): 
            if isProjectDir(absPath):
                if not os.path.exists(absPath + '.zip'):
                    # Only zip project directory into .zip file if it hasn't been zipped already
                    zipdir(absPath, absPath + '.zip')
                    relZipFile = relPath + '.zip'
                    relProjectPaths.append(relZipFile)
                    foundProject = relZipFile
                # else do nothing!
            else: # Not a project directory; process contents recursively
                for fod in os.listdir(absPath):
                    processFileOrDir(relPath, fod)
        else: 
            # Ignore other files 
            pass
        if foundProject: 
            num_projects_processed[0] += 1
            if num_projects_processed[0] % print_every == 0: 
                logwrite(str(num_projects_processed[0]) + ": " + foundProject)

    # *** Added by lyn 
    filesOrDirs = os.listdir(dirName)
    if numToKeep != None:
        filesOrDirs = filesOrDirs[:numToKeep]
    for fileOrDir in filesOrDirs:
        processFileOrDir('', fileOrDir)
    return relProjectPaths

# [2016/08/12] Returns True iff absDirPath is an AI2 project directory like one
# in Benji's data. I.e., it contains only files and has at least a .scm or .bky file. 
def isProjectDir(absDirPath):
    filesOrDirs = os.listdir(absDirPath)
    for fileOrDir in filesOrDirs:
        if os.path.isdir(os.path.join(absDirPath, fileOrDir)):
            return False # Project file has no subdirs
        if fileOrDir.endswith('.scm') or fileOrDir.endswith('.bky'):
            return True
        # Otherwise try next fileOrDir
    return False # Return false if find no evidence it's project dir

def zipdir(path, ziph):
    """
    Given directory to path (path) and path to outputted zipped file (ziph),
    zip directory and return ziph
    """
    zf = zipfile.ZipFile(ziph, "w")
    for root, dirs, files in os.walk(path):
        for file in files:
            zf.write(os.path.join(root, file))
    zf.close()
    return ziph

# [2016/08/06, lyn] Modified this so that 1st arg is *relative* pathname to new 2nd arg, 
# and new 3rd arg (if non-None) specifies outputDir different from userDir. 
def projectToJAILFile(relProjectPath, userDir, outputDir=None):
    """
    Given path to zipped project (relProjectPath) relative to userDir, 
    create summary file and write to disk. 
    If outputDir is None, writes XYZ_summary.json file to same directory as .aia/.zip file
    If outputDir is non-None, writes XYZ_summary.json file (possibly newly created) outputDir.
    """
    if not relProjectPath.endswith('.zip') and not relProjectPath.endswith('.aia'):
        raise Exception("project " + relProjectPath +" is not .aia or  .zip") 
        #[2016-08-07 Maja] changed projectPath to relProjectPath

    global currentProjectPath
    currentProjectPath = os.path.join(userDir, relProjectPath) # Remember this absolute path as global for error handling
                                                               # Lyn sez: could avoid this by using try/except here instead
    try: 
        jsonProject = projectToJAIL(currentProjectPath)
        if outputDir == None:
            # Write summary file to same directory as input file 
            jsonProjectFileName = projectToJAILProjectFileName(currentProjectPath)
        else:
            jsonProjectFileName = projectToJAILProjectFileName(os.path.join(outputDir, relProjectPath))
            (dirPath, basefile) = os.path.split(jsonProjectFileName) # Split jsonProjectFileName into directory path and base filename
            # Debugging:
            # print "***os.path.split***", (dirPath, basefile)
            # print "jsonProjectFileName", jsonProjectFileName
            if not os.path.exists(dirPath):
                os.makedirs(dirPath) # Make all intermediate directories that don't yet exist
                # Debugging:
                # print "dirPath", dirPath, os.path.exists(dirPath)
                # print "jsonProject", str(jsonProject)

            with open (jsonProjectFileName, 'w') as outFile:
                outFile.write(json.dumps(jsonProject,
                                         sort_keys=True,
                                         indent=2, separators=(',', ':')))
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except:
        packet = sys.exc_info()[:2]
        if currentScreenName != None:
            logwrite('***EXCEPTION' + " " + str(packet[0]) + " " + str(packet[1]) + ",\n possibly in screen " + currentScreenName + " of project " + currentProjectPath)
        elif currentProjectPath != None:
            logwrite("***Exception" + " " + str(packet[0]) + " " + str(packet[1]) + " in project " + currentProjectPath)
        else:
            logwrite("***EXCEPTION" + " " + str(packet[0]) + " " + str(packet[1]))

# Introduced by Lyn. projectPath name might contain a dot, so 
# 
#   projectPath.split('.')[0] + '_summary.json'
# 
# won't always work.  Even though project name is guaranteed not to have dots, other components
# of projectPath might have dots.  E.g., suppose projectPath is 
# /Users/fturbak/ai2.users.long.term.randomized/03/03017/p001_002_AlexTalkToMe.aia
def projectToJAILProjectFileName(projectPath):
    parts = projectPath.split('.')
    allButExtension = '.'.join(parts[:-1])
    return allButExtension + '.jail'

def projectToJAIL(projectPath):
    """
    Given path to zipped project (projectPath), return JAIL = JSON representation of project
    """
    jailRep = {}
    with zipfile.ZipFile(projectPath, 'r') as zippedFile:
        jailRep['**Project Name'] = findName(zippedFile)
        jailRep['**created'], jailRep['**modified'] = findCreatedModifiedTimes(zippedFile)
        screenNames = findScreenNames(zippedFile)
        jailRep['*Names of Screens'] = screenNames
        jailRep['*Number of Screens'] = len(screenNames)
        jailRep['screens'] = { screenName: screenToJAIL(zippedFile, screenName) for screenName in screenNames }
    return jailRep

'''Given a Python zip file and a pathless filename (no slashes), extract the lines from filename,             
   regardless of path. E.g., Screen1.bky should work if archive name is Screen1.bky                                                                                  or src/appinventor/ai_fturbak/PROMOTO_IncreaseButton/Screen1.bky. 
   it also strips the file from '&'s and '>'  '''
def linesFromZippedFile(zippedFile, pathlessFilename):
    if "/" in pathlessFilename:
        raise RuntimeError("linesFromZippedFile -- filename should not contain slash: " + pathlessFilename 
                           + " in project " + currentProjectPath)
    names = zippedFile.namelist()
    if pathlessFilename in names:
        fullFilename = pathlessFilename
    else:
        matches = filter(lambda name: name.endswith("/" + pathlessFilename), names)
        if len(matches) == 1:
            fullFilename = matches[0]
        elif len(matches) == 0:
            if pathlessFilename == 'project.properties': # use dummy properties file if missing
                return dummyProperties()
            elif pathlessFilename == 'META': #use dummy META file if missing
                # return dummyMeta() 
                raise Exception("Should not look for META in zipped file {}; should be handled by findCreatedModifiedTimes".format(currentProjectPath)) # Lyn
            matches_alt = filter(lambda name: str.lower(name.split('/')[-1]) == str.lower(pathlessFilename), names) #considering case issues
            if len(matches_alt) == 1:
                global num_case_mismatches
                num_case_mismatches += 1
                fullFilename = matches_alt[0]
            else:
                suffix = pathlessFilename.split('.')[-1]
                if suffix == 'scm':
                    return dummyScm()
                elif suffix == 'bky':
                    if u'$Components' not in currentScmJSONContents[u'Properties']:
                        # .scm says empty .bky file is OK
                        logwrite("NOTE (*not* an error): Pretending there's an empty .bky file {} in project {} to match .scm file with no components".format(pathlessFilename, currentProjectPath))
                        return emptyBkyLines()
                    else:
                        raise RuntimeError("linesFromZippedFile -- no match for nonempty .bky file named: " + pathlessFilename
                                           + " in project " + currentProjectPath)
                else:
                    raise RuntimeError("linesFromZippedFile -- no match for file named: " + pathlessFilename
                                       + " in project " + currentProjectPath)
        else:
            raise RuntimeError("linesFromZippedFile -- multiple matches for file named: "
                         + pathlessFilename
                         + "[" + ",".join(matches) + "] -- in project" + currentProjectPath)
    return zippedFile.open(fullFilename).readlines()

def findName(zippedFile):
    """
    given zipfile of a project (zippedFile), return name of project 
    """
    pp = linesFromZippedFile(zippedFile, 'project.properties')
    if pp:
        return  pp[1][:-1].split('=')[1]
    return ""

'''2016/08/05: Modified by Lyn to handle both META and METADATA files and supersede dummyMeta()'''
def findCreatedModifiedTimes(zippedFile):
    """
    given a zipfile of a project (zippedFile), return tuple of created and modified times
    """
    names = zippedFile.namelist()
    if 'META' in names: 
        # Zipped file has metadata with one line that is JSON that looks like: 
        # {"name": "TALKTOME", "modified": 1438782081076, "created": 1438008239454}
        lines = linesFromZippedFile(zippedFile, 'META')
        if len(lines) != 1:
            raise Exception("project " + currentProjectPath + " has malformed META file with " + str(len(lines)) + " lines")
        else: 
            meta = json.loads(lines[0])
            return meta['created'], meta['modified']
    else: 
        # [2016/08/12, lyn] Fixed bug in handling of METADATA file 
        metadataFilenames = [name for name in names if name.endswith('METADATA')]
        if len(metadataFilenames) == 1:
            # Zipped file has metadata file with two lines that looks like: 
            # dateCreated = 1396713895474
            # dateModified = 1396714632270
            lines = linesFromZippedFile(zippedFile, 'METADATA')
            if len(lines) != 2:
                raise Exception("project " + currentProjectPath + " has malformed METADATA file with " + str(len(lines)) + " lines")
            else: 
                meta = map(lambda x: int(x.split(" = ")[1]), lines)
                return meta[0], meta[1]
        else: # supersede dummyMeta
            global num_missing_meta
            num_missing_meta += 1
            return str(DUMMY_CREATED_TIME), str(DUMMY_MODIFIED_TIME)

# [2016/08/05, lyn] modified to include names ending in either .bky or .scm'
def findScreenNames(zippedFile): 
    names = zippedFile.namelist()
    screens = []
    for file in names:
        name = str(file.split('/')[-1])
        extension = name[-4:]
        if (extension == '.scm' or extension == '.bky') and name[0].isalpha():
            # Lyn asks: what is name[0].isalpha() for? 
            screens.append(name[:-4])
    return list(set(screens)) # list(set(...)) removes duplicates 

# [2018/07/23, audrey] modified to not raise exception and just make a note
# whenever form name and screen name don't match
def screenToJAIL(zippedFile, screenName):
    # [2018/07/21, audrey] Set currentScreenName properly
    global currentScreenName
    currentScreenName = screenName
    # logwrite("Current screen name: {}".format(currentScreenName))
    scmFileName = screenName + '.scm'
    componentsJAIL = scmToJAIL(zippedFile, scmFileName)
    bkyFileName = screenName + '.bky'
    bkyJAIL = bkyToJAIL(zippedFile, bkyFileName)
    # Verify that screenName matches name of Form (screen)
    formName = componentsJAIL['Properties']['$Name']

    # [2018/07/23, audrey] prevent it from killing everything if they don't match
    # because I want to be able to compare the screens of one project, 09265's bake
    if screenName != formName:
      logwrite("WARNING (not an error): screenToJail: screen name  \"{}\" does not match formName \"{}\"".format(screenName, formName))
    
    #if screenName == formName: 
    return {"*components": componentsJAIL, "bky":bkyJAIL} # Use *components so it comes first alphabetically
    #else: 
    #  raise RuntimeError("screenToJAIL: screenName (" + screenName 
    #                     + ") does not match formName (" + formName + ")")

# [2016/08/05, lyn] Introduced this helper function that returns JSON contents of .scm file
def scmJSONContents(zippedFile, scmFileName):
    scmLines = linesFromZippedFile(zippedFile, scmFileName)
    if (len(scmLines) == 4
        and scmLines[0].strip() == '#|'
        and scmLines[1].strip() == '$JSON'
        and scmLines[3].strip() == '|#'):
        try:
            contents= json.loads(scmLines[2])
        except:
            e = sys.exc_info()[0]
            contents = {u'Properties':{}}
            logwrite("Malformed scm file {} in project {}. Error: {}".format(scmFileName, currentProjectPath, e)) # [2016/08/06, lyn] modified 
    else:
        try:
            contents = json.loads(scmLines)
        except:
            e = sys.exc_info()[0]
            contents = {u'Properties':{}}
            logwrite("Malformed scm file {} in project {}. Error: {}".format(scmFileName, currentProjectPath, e)) # [2016/08/06, lyn] modified 
    global currentScmJSONContents
    currentScmJSONContents = contents # Tracks contents of .scm file for currentScreen.
                                      # Used by upgradeFormat below to upgrade block types for old projects. 
    global currentComponentDictionary
    currentComponentDictionary = {} # Reset this to empty dict, and populate it only if we need to upgrade old-style components
    return contents

# [2016/08/06, lyn] Modified to distinguish number of components and number of different component types
def scmToJAIL(zippedFile, scmFileName):
  return scmJSONContents(zippedFile, scmFileName)

def elementTreeFromLines(lines):
    """ This function is designed to handle the following bad case: <xml xmlns="http://www.w3.org/1999/xhtml">
    for each file parse the xml to have a tree to run the stats collection on
    assumes if a namespace exists that it's only affecting the xml tag which is assumed to be the first tag"""
    # lines = open(filename, "r").readlines()                                     
    try:
        firstline = lines[0] #we are assuming that firstline looks like: <xml...>... we would like it to be: <xml>...                                                             
        if firstline[0:4] != "<xml":
            return ET.fromstringlist(['<xml></xml>'])
        else:
            closeindex = firstline.find(">")
            firstline = "<xml>" + firstline[closeindex + 1:]
            lines[0] = firstline
            #Invariant: lines[0] == "<xml>..." there should be no need to deal with namespace issues now
            return ET.fromstringlist(lines)
    except (IndexError, ET.ParseError):
        return ET.fromstringlist(['<MALFORMED></MALFORMED>'])

def bkyToJAIL(zippedFile, bkyFileName):
  bkyLines = linesFromZippedFile(zippedFile, bkyFileName)
  rootElt = elementTreeFromLines(bkyLines)
  if rootElt.tag == 'MALFORMED':
      logwrite("***Project " + currentProjectPath + " has malformed .bky file " + bkyFileName)
      return 'MALFORMED BKYFILE'
  elif not rootElt.tag == 'xml':
      raise RuntimeError('bkyToJAIL: Root of bky file is not xml but ' + rootElt.tag 
                         + " in project " + currentProjectPath)
  else:
    topBlocks = [] 
    yacodeblocks = None
    for child in rootElt: 
      if child.tag == 'block': 
        topBlocks.append(blockToJAIL(child))
      elif child.tag == 'yacodeblocks': 
        if yacodeblocks: # Has already been defined
          raise RuntimeError('bkyToJAIL: More than one yacodeblocks')
        else:
          #logwrite("bkyToJAIL yacodeblocks: " + str(child.attrib))
          yacodeblocks = child.attrib
      else:
        raise RuntimeError('bkyToJAIL: unrecognized tag ' + child.tag)
    if not yacodeblocks:
      # [2018/07/21, audrey] raising the error was unproductive so I added a dummy version.
      yacodeblocks = {'ya-version': str(DUMMY_VERSION), 'language-version': str(DUMMY_VERSION)}
      #raise RuntimeError('bkyToJAIL: no yacodeblocks!')
    
    yaVersion = ""
    languageVersion = ""
    if 'ya-version' in yacodeblocks: 
      yaVersion = yacodeblocks['ya-version']
    else: 
      raise RuntimeError('bkyToJAIL: no ya-version')
    if 'language-version' in yacodeblocks: 
      languageVersion = yacodeblocks['language-version']
    else: 
      raise RuntimeError('bkyToJAIL: no language-version')
    return {'topBlocks': topBlocks, 'ya-version': yaVersion, 'language-version': languageVersion}

# Only called on XML with tag = 'block'
# Return a dictionary with all info of block
# [2018/07/12, audrey] clean up logic/variable names to get rid of bug
# [2018/07/21, audrey] change variable names to names not taken by python built-ins
def blockToJAIL(xmlBlock):
  blockDict = {}
  statements = {} # Map statement names to list of statement blocks
  values = {} # Map value names to list of statement blocks
  for prop in xmlBlock.attrib: # [2018/07/21, audrey] rename property to prop, somewhat for proper highlighting
    if prop == 'type': 
      # rename 'type' to '*type' so type appears at top of blockDict when keys are sorted
      # (makes output easier to read)
      generalType = xmlBlock.attrib[prop]
      blockDict['*type'] = generalType
      specificType = blockType(xmlBlock) # [2015/11/11, lyn] Specially handle component_event, component_method, component_set_get
                                         # E.g., for generalType component_event, might have Button.Click;
                                         #       for generalType component_method, might have Canvas.DrawCircle
                                         #       for generalType component_set_get, might have Button.GetText or Button.SetText
                                         # Now also handles "old style" types. E.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
      if isDeclarationType(generalType, specificType): # declaration = top-level/root block 
        blockDict['kind'] = 'declaration'
      #else:
      #  logwrite("blockToJAIL: non declaration type {} of specific type {}".format(generalType, specificType))
      if blockDict['*type'] not in blockTypeDict:
        if specificType in AI2_component_specs_nb155:
          if 'kind' in AI2_component_specs_nb155[specificType]:
            blockDict['kind'] = AI2_component_specs_nb155[specificType]['kind']
          else:
            blockDict['kind'] = 'declaration'
            #raise RuntimeError("blockToJAIL: type {} does not have key \"kind\"".format(specificType))
    else:
      blockDict[prop] = xmlBlock.attrib[prop]
  # [2018/07/12, audrey] add blkType because apparently this function
  # was looking for some variable "type" that was never actually
  # defined, instantiated, or anything???? So it was actually comparing
  # the block type strings to a function lmao.
  # So I took this cue from addBlockInfo in ai2summarizer2.py.
  blkType = blockType(xmlBlock)
  #logwrite("blockToJAIL: " + blkType)
  if '*type' not in blockDict: 
    raise RuntimeError('blockToJAIL: block has no type!')
  counter = 0
  for child in xmlBlock:
    counter += 1
    if child.tag == 'mutation':
      # Add each mutation attribute to block blockDict
      for property in child.attrib:
        blockDict[property] = child.attrib[property]
      #logwrite("blockToJAIL: " + str(child))
      if (blkType == 'procedures_defnoreturn' or blkType == 'procedures_defreturn' 
          or blkType == 'procedures_callnoreturn' or blkType == 'procedures_callreturn'):
        # For procedure declarations and calls, collect argument names in params property
        # (params is a better name than args)
        params = [] 
        for param in child:
          if param.tag == 'arg':
            params.append(param.attrib['name']) # Name of parameter (so-called 'arg' in XML)
          else: 
            raise RuntimeError('blockToJAIL: unexpected tag in procedure block mutation -- ' + param.tag)
        # [2018/07/12, audrey] decided this wasn't an error because it was being set off by procedures that simply don't have arguments lmao
        #if 'params' not in blockDict:
          # [2018/07/12, audrey] add str( ) around blockDict
          #  raise RuntimeError('blockToJAIL: params unexpectedly missing from blockDict -- ' + str(blockDict))
        blockDict['params'] = params
      elif blkType == 'local_declaration_statement' or blkType == 'local_declaration_expression':
        # For local variable declarations, collect local variable names in params property
        # (named consistently with other bound variables)
        params = [] 
        for param in child:
          if param.tag == 'localname': 
            params.append(param.attrib['name']) # Name of parameter (so-called 'arg' in XML)
          else: 
            raise RuntimeError('blockToJAIL: unexpected tag in local variable declaration block mutation -- ' + param.tag)
        blockDict['params'] = params
      else:
        # Sanity check: verify that other mutation elements don't have children
        # (other than 'eventparam', which is used for translating event parameters)
        mutationChildren = list(child)
        # [2018/07/12, audrey] added list( ) around the call to filter because filter returns an
        # iterator, not a list itself, and you cannot take the len( ) of an iterator.
        unexpectedTags = list(map(lambda mchild: mchild.tag, list(filter(lambda mchild: mchild.tag != 'eventparam', mutationChildren))))
        if len(unexpectedTags) != 0:
          raise RuntimeError('blockToJAIL: unexpected mutation children with tags ' + 
                             ",".join(unexpectedTags))
    elif child.tag == 'field' or child.tag == 'title': # TITLE is old name for FIELD
      blockDict[child.attrib['name']] = child.text
    elif child.tag == 'comment':
      blockDict['comment'] = commentToJAIL(child)
    elif child.tag == 'value':
      values[child.attrib['name']] = valueToJAIL(child)
    elif child.tag == 'statement':
      statements[child.attrib['name']] = statementToJAIL(child)
    elif child.tag == 'next':
      kind = determineKind(blockDict)
      if kind != 'statement':
        logwrite("blockToJail: kind -- " + kind)
        raise RuntimeError('blockToJail: next tag found in nonstatement ' + str(getBlockInfo(xmlBlock)))
      else: 
        blockDict['next'] = nextToJAIL(child)
    else: 
      raise RuntimeError('blockToJAIL: unexpected child tag -- ' + child.tag)
  determineKind(blockDict)
  addSubBlocks(blockDict['*type'], blockDict, statements, values)
  return blockDict


def getBlockInfo(xmlBlock):
    '''return a dict string of id, x, y (if available)'''
    attribs = xmlBlock.attrib
    return {'id': attribs.get('id', 'NO id'), 
            'x': attribs.get('x', 'NO x'), 
            'y': attribs.get('y', 'NO y')}

declarationTypes = ['component_event', 'global_declaration', 'procedures_defnoreturn', 
                    'procedures_defreturn', 'procedures_callnoreturn', 'procedures_callreturn']

nonDeclarationTypes = ['component_method', 'component_set_get']

# [2016/08/06, lyn] This is new, and correctly handles several cases not handled correctly before:
# * lexical_variable_get and lexical_variable_set used to be incorrectly treated as top-level declarations.
# * any "old-style" block, like 'DrawingCanvas_Clicked', 'DrawingCanvas_DrawCircle', or 'StartButton_SetText'
#   was previously treated as a top-level declaration, but only the first is.
# [2018/07/21, audrey] Removed by Audrey; apparently this got duplicated somehow.
'''def isDeclarationType(generalType, specificType):
    if generalType in declarationTypes: 
        return True
    elif generalType in nonDeclarationTypes:
        return False
    elif generalType in blockTypeDict: # e.g, math_add, lists_append_lists
        return False
    # If get here, generalType must be "old-style" type like 'DrawingCanvas_Clicked' 
    # and specificType must be upgraded type, like 'Canvas.Clicked'
    elif specificType in AI1_v134a_component_specs: # handles old-style component_event and component_method
        return AI1_v134a_component_specs[specificType]['type'] == 'component_event'
    else: 
        return False # Handles old-style component getters and setters. E.g. 'StartButton_GetText'
                     # as well as generic methods, E.g. Canvas.DrawCircleGeneric
'''
# From the block type, determine the kind for blockDict 
# ('expression', 'statement', or 'declaration'), 
# set the 'kind' property to this value, and return it. 
# Assumes type and mutation have already been processed
# 
# Handle the block type component_set_get specially
# based on the property 'set_or_get' from the mutator, 
# and in this case also refine the '*type' property to be
# either 'component_get' or 'component_set'.
#
# Handle the block type component_method specially
# based on the entry in componentMethodDict, 
# and in this case also refine the '*type' property to be
# either 'component_method_call_expression' or 'component_method_call_statement'
def determineKind(blockDict):
  if blockDict['*type'] in mangledBlockTypesDict:
      tipe = blockDict['*type']
      tipe = mangledBlockTypesDict[tipe]
      blockDict['*type'] = tipe
  if 'kind' in blockDict:
    # Do nothing; already processed. 
    pass
  # For kind, handle component_set_get specially
  elif blockDict['*type'] == 'component_set_get': 
    if 'set_or_get' not in blockDict: 
      raise RuntimeError('getKind: no set_or_get for component_set_get')
    else: 
      setGet = blockDict['set_or_get']
      if setGet == 'get': 
        blockDict['kind'] = 'expression'
        blockDict['*type'] = 'component_get' # Create new type for JAIL
      elif setGet == 'set': 
        blockDict['kind'] = 'statement'
        blockDict['*type'] = 'component_set' # Create new type for JAIL
      else:
        raise RuntimeError('blockToJAIL: unexpected set_or_get value -- ' + setGet)
  # For kind, handle component_method (component method calls) specially
  elif blockDict['*type'] == 'component_method': 
    (kind, numArgs) = lookupMethod(blockDict['component_type'], blockDict['method_name'])
    if kind == 'statement':
      blockDict['kind'] = 'statement'
      blockDict['*type'] = 'component_method_call_statement'
    else: 
      blockDict['kind'] = 'expresssion'
      blockDict['*type'] = 'component_method_call_expression'
  else: 
    blockDict['kind'] = blockTypeToKind(blockDict['*type'])
  return blockDict['kind']

def commentToJAIL(xmlComment): 
  dict = {} 
  for property in xmlComment.attrib:
    dict[property] = xmlComment.attrib[property]
  dict['text'] = xmlComment.text
  return dict

def valueToJAIL(xmlValue):
  children = list(xmlValue) # returns a list of all children of node
  if len(children) != 1:
    raise RuntimeError('valueToJail: unexpected number of children ' + str(children))
  elif children[0].tag != 'block':
    raise RuntimeError('valueToJail: non-block child ' + children[0].tag)
  else:
    return blockToJAIL(children[0])

def statementToJAIL(xmlStatement):
  children = list(xmlStatement) # returns a list of all children of node
  if len(children) != 1:
    raise RuntimeError('statementToJail: unexpected number of children ' + str(children))
  elif children[0].tag != 'block':
    raise RuntimeError('statementToJail: non-block child ' + children[0].tag)
  else:
    return blockToJAIL(children[0])

def nextToJAIL(xmlNext):
  children = list(xmlNext) # returns a list of all children of node
  if len(children) != 1:
    raise RuntimeError('nextToJail: unexpected number of children ' + str(children))
  elif children[0].tag != 'block':
    raise RuntimeError('nextToJail: non-block child ' + children[0].tag)
  else:
    return blockToJAIL(children[0])

def addSubBlocks(type, blockDict, statements, values):
  if type == 'component_event': 
    if len(values) != 0:
      raise RuntimeError('addSubBlocks: component_event has values ' + str(values))
    else: 
      componentType = blockDict['component_type']
      eventName = blockDict['event_name']
      blockDict['params'] = lookupEventParams(componentType, eventName)
      blockDict['~bodyStm'] = getStatementListNamed('DO', statements) # *** Is this always right? 
  elif type == 'controls_if':
    elseifNum = 0
    elseNum = 0
    if 'elseif' in blockDict:
      elseifNum = int(blockDict['elseif'])
    if 'else' in blockDict:
      elseNum = int(blockDict['else'])
    # Make branches of form {'test': <exp>, 'then': <statementList>}
    branches = []
    # print('elseifNum', blockDict['elseif'], elseifNum)
    for index in range(0, elseifNum + 1):
      branches.append({'test': getValueBlockNamed('IF' + str(index), values), # IF0, IF1, ...
                       'then': getStatementListNamed('DO' + str(index), statements) # DO0, DO1, ...
                       })
    blockDict['~branches'] = branches # use ~branches rather than branches, so is at end of block dict when sorted alphabetically
    # print('elseNum', blockDict['else'], elseNum)
    if elseNum == 1: 
      # ~branchofelse if alphabetically after ~branches, for readability
      blockDict['~branchofelse'] = getStatementListNamed('ELSE', statements)
  elif type == 'controls_forEach' or type == 'controls_forRange' or type == 'controls_while': 
    argNames = blockDictToArgNames(blockDict)
    blockDict['~argNames'] = argNames
    blockDict['~args'] = map(lambda name: getValueBlockNamed(name, values), argNames) 
    blockDict['~bodyStm'] = getStatementListNamed('DO', statements) 
  elif type == 'controls_do_then_return': 
    blockDict['statement'] = getStatementListNamed('STM', statements)
    blockDict['value'] = getStatementListNamed('VALUE', values)
  elif type == 'procedures_defnoreturn': 
    blockDict['~bodyStm'] = getStatementListNamed('STACK', statements) 
  elif type == 'procedures_defreturn': 
    blockDict['~bodyExp'] = getValueBlockNamed('RETURN', values)
  elif type == 'local_declaration_statement': 
    # print 'local_declaration_statement', "before len(blockDict['params'])" #****
    numDecls = len(blockDict['params'])
    # print 'local_declaration_statement', "after len(blockDict['params'])" #****
    declNames = map(lambda index: 'DECL' + str(index), range(0, numDecls))
    blockDict['~*decls'] = map(lambda name: getValueBlockNamed(name, values), declNames) # Use ~*decls so precedes ~body alphabetically
    blockDict['~bodyStm'] = getStatementListNamed('STACK', statements) 
  elif type == 'local_declaration_expression': 
    # print 'local_declaration_expression', "before len(blockDict['params'])" #****
    numDecls = len(blockDict['params'])
    # print 'local_declaration_expression', "before len(blockDict['params'])" #****
    declNames = map(lambda index: 'DECL' + str(index), range(0, numDecls))
    blockDict['~*decls'] = map(lambda name: getValueBlockNamed(name, values), declNames) # Use ~*decls so precedes ~body alphabetically
    blockDict['~bodyExp'] = getStatementListNamed('RETURN', values) 
  else:
    if len(statements) != 0:
      raise RuntimeError('addSubBlocks: block has unexpected substatements ' + type + "; " + str(statements))
    argNames = blockDictToArgNames(blockDict)
    if len(argNames) > 0: # Don't include these fields if they're empty lists. 
      # Use ~ in next two names to put fields at bottom when sorted. 
      blockDict['~argNames'] = argNames
      blockDict['~args'] = map(lambda name: getValueBlockNamed(name, values), argNames) 

def getValueBlockNamed(name, valuesDict):
  if name in valuesDict:
    return valuesDict[name]
  else: 
    return emptySocket()

# A pseudo-block dict that "fills" an empty socket
def emptySocket():
  return {'*type': 'empty_socket'}

# Return a list of block dicts corresponding to the named statement.
# Create a list from a single statement block dict by following 'next' subBlocks.
def getStatementListNamed(name, statementsDict):
  if name not in statementsDict:
    return [] 
  else: 
    result = statementsDict[name]
    if type(result) == list: 
      # if already calculated and cached, return cached result;
      # not clear this is used, but I want to be safe. 
      return result
    else: 
      # Must be a block dict for a single statement instead
      stmBlockDict = result
      # Turn this into a list by processing 'next' sub blocks
      stmList = [stmBlockDict]
      current = stmBlockDict
      while 'next' in current: 
        nextBlockDict = current['next']
        del current['next'] # Clean up current
        stmList.append(nextBlockDict)
        current = nextBlockDict
    statementsDict[name] = stmList # cache the result for later
    return stmList

# Handles (1) parameters of events and (2) parameters and return/noreturn of method calls
def componentJSONToComponentDict(jsonFilename): 
  componentDict = {} # Dict of dicts, first keyed by component name, then method name
  with open (jsonFilename, 'r') as inFile:  
    cmpJson = json.loads(inFile.read())
    for componentDescription in cmpJson: 
      componentName = componentDescription['name']
      eventDict = {}
      methodDict = {}
      for eventDescription in componentDescription['events']:
        eventName = eventDescription['name']
        # print "before eventDescription['params']"
        eventParamNames = map(lambda paramDescription: paramDescription['name'], eventDescription['params'])
        # print "after eventDescription['params']"
        eventDict[eventName] = eventParamNames # only thing we care about for events
      for methodDescription in componentDescription['methods']:
        methodName = methodDescription['name']
        if 'returnType' in methodDescription:
          methodKind = 'expression'
        else: 
          methodKind = 'statement'
        # print "before methodDescription['params']"
        methodParamNames = map(lambda paramDescription: paramDescription['name'], methodDescription['params'])
        # print "after methodDescription['params']"
        methodDict[methodName] = {'kind': methodKind, 'params': methodParamNames}
      componentDict[componentName] = {'events': eventDict, 'methods': methodDict}
  return componentDict

# [2018/07/11, audrey] comment out in process of adapting for AI2_component_specs_nb155
#componentDict =  #componentJSONToComponentDicto('simple_components.json')

# [2018/06/21, audrey] Added to standardize a lot of the logs and generally make code cleaner.
# [2018/07/12, audrey] Taken from ai2summarizer2, because used in componentTypeToBlockType
def warningIgnoringMalformedBlock(callingFunctionName, hasMutation, tipe, xmlBlock):
    global currentScreenName
    logwrite('*WARNING*: {} is ignoring malformed block{} with type {} in screen {} of project {} (block info: {})'.format(callingFunctionName, "" if hasMutation else " (no mutation)", tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))

# [2017/03/29, lyn] Factored out this helper function to call it recursively for mangled types
# [2018/07/12, audrey] Taken from ai2summarizer2 to bring jail up to speed
def componentTypeToBlockType(xmlBlock, tipe):
    # Debugging:
    #logwrite("componentTypeToBlockType")
    # print "***blockType", xmlBlock, tipe
    if tipe == '*IGNORE*': # Special string meaning something is wrong with block and it should be ignored
        return '*IGNORE*'

    elif tipe == 'component_event':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return formToScreen(child.attrib['component_type']) + "." + child.attrib['event_name']
        warningIgnoringMalformedBlock("blockType", False, tipe, xmlBlock) #logwrite('*WARNING*: blockType is ignoring malformed block (no mutation) with type {} in screen {} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*IGNORE*' # Special string to indicate something is wrong with this block
    elif tipe == 'component_method':
        for child in xmlBlock:
            if child.tag == 'mutation':
                methodName = formToScreen(child.attrib['component_type']) + "." + child.attrib['method_name']
                if child.attrib['is_generic'] == 'true':
                    methodName += 'Generic'
                return methodName
        warningIgnoringMalformedBlock("blockType", False, tipe, xmlBlock) #logwrite('*WARNING*: blockType is ignoring malformed block (no mutation) with type {} in screen {} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*IGNORE*' # Special string to indicate something is wrong with this block
    elif tipe == 'component_set_get':
        for child in xmlBlock:
            if child.tag == 'mutation':
                getterSetterName = (formToScreen(child.attrib['component_type'])
                                    + "." 
                                    + child.attrib['set_or_get'].capitalize() 
                                    + child.attrib['property_name'])
                if child.attrib['is_generic'] == 'true':
                    getterSetterName += 'Generic'
                return getterSetterName
        warningIgnoringMalformedBlock("blockType", False, tipe, xmlBlock)
        #logwrite('*WARNING*: blockType is ignoring malformed block (no mutation) with type {} in screen {} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*IGNORE*' # Special string to indicate something is wrong with this block
    elif tipe == 'component_component_block':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return formToScreen(child.attrib['component_type']) + ".ComponentGeneric"
        warningIgnoringMalformedBlock("blockType", False, tipe, xmlBlock) #logwrite('*WARNING*: blockType is ignoring malformed block (no mutation) with type {} in screen {} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
    elif tipe not in blockTypeDict:
        if tipe in mangledBlockTypesDict:
            unmangledType = mangledBlockTypesDict[tipe] # [2017/03/29, lyn] Handle mangled types
            logwrite('*WARNING*: automatically transforming mangled block type {} to {} in screen {} of project {} (block info: {})'.format(tipe,unmangledType, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
            return componentTypeToBlockType(xmlBlock, unmangledType)

        # E.g., 'DrawingCanvas_Clicked'
        
        # handles component_set_get in the old format [Maja 2016-07-12]
        elif tipe.endswith('etproperty'):
            
            oldTipe = tipe 
            #establish set or get [Maja 2016-07-12]
            if tipe.endswith('getproperty'):
                set_or_get = "Get"
            else:
                set_or_get = "Set"
                
            # find action taken [Maja 2016-07-12]
            for child in xmlBlock:
                if child.tag == 'title' or child.tag == 'field':
                    tipe = tipe.split("_")[0] + "_" + set_or_get + child.text

            if oldTipe != tipe: 
                logwrite("*NOTE*: blockType transformed block type {} into {} in screen {} of project {} (block info {})".format(oldTipe, tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        # [Maja, 2015/11/15] handles the old style formatting 
        # e.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
       
        return upgradeTypeFormat(tipe)
    else:
        #logwrite("componentTypeToBlockType: Exit")
        return tipe


# [2018/07/12, audrey] taken from ai2summarizer2.py to bring jail up to speed
def formToScreen(comp):
    '''Change all occurrences of component Form to Screen'''
    if comp == 'Form':
        return 'Screen'
    else:
        return comp

# [2018/07/12, audrey] taken from ai2summarizer2.py to bring jail up to speed
def componentTypeToBlockName(xmlBlock, tipe):
    # Debugging:
    # if currentProjectNumber == 70:
    #    print "***blockType", xmlBlock, tipe
    if tipe == '*IGNORE*': # Special string meaning something is wrong with block and it should be ignored
                           # This shouldn't happen!
        return '*UNKNOWN-BLOCK-NAME*'
    elif 'id' in xmlBlock.attrib:
        blockID = '#' + xmlBlock.attrib['id']
    elif 'x' in xmlBlock.attrib and 'y' in xmlBlock.attrib: # use x,y coords as psuedoID
        blockID = '#x=' + xmlBlock.attrib['x'] + ',y=' + xmlBlock.attrib['y']
    else:
        blockID = '#NoID'
    if 'disabled' in xmlBlock.attrib and xmlBlock.attrib['disabled'] == 'true':
        blockID = blockID + '!disabled'
    if tipe == 'component_event':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return (child.attrib['component_type'] + '$' # Just in case instance name doesn't indicate component type
                        + child.attrib['instance_name'] + "." + child.attrib['event_name'] 
                        + blockID)
        warningIgnoringMalformedBlock("componentTypeToBlockName", True, tipe, xmlBlock) #logwrite('*WARNING*: componentTypeToBlockName is ignoring malformed block with type {} in screen{} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*UNKNOWN-BLOCK-NAME*' # Special string to indicate something is wrong with this block
    elif tipe == 'component_method':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return (child.attrib['component_type']\
                            if child.attrib['is_generic']\
                            else child.attrib['component_type'] + '$' + child.attrib['instance_name'] # Just in case instance name doesn't indicate component type
                        + "." + child.attrib['method_name'] 
                        + 'Generic' if child.attrib['is_generic'] else ''
                        + blockID)
        warningIgnoringMalformedBlock("componentTypeToBlockName", True, tipe, xmlBlock) #logwrite('*WARNING*: componentTypeToBlockName is ignoring malformed block with type {} in screen {}  of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*UNKNOWN-BLOCK-NAME*' # Special string to indicate something is wrong with this block
    elif tipe == 'component_set_get':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return (child.attrib['component_type']\
                            if child.attrib['is_generic']\
                            else child.attrib['component_type'] + '$' + child.attrib['instance_name'] # Just in case instance name doesn't indicate component type
                        + "." 
                        + child.attrib['set_or_get'].capitalize() 
                        + child.attrib['property_name']
                        + 'Generic' if child.attrib['is_generic'] else ''
                        + blockID)
        warningIgnoringMalformedBlock("componentTypeToBlockName", True, tipe, xmlBlock) #logwrite('*WARNING*: componentTypeToBlockName is ignoring malformed block with type {} in screen {} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*UNKNOWN-BLOCK-NAME*' # Special string to indicate something is wrong with this block
    elif tipe == 'component_component_block':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return (child.attrib['component_type'] + '$' # Just in case instance name doesn't indicate component type
                        + child.attrib['instance_name'] 
                        + blockID)
            elif child.tag == 'title' or child.tag == 'field':
                if child.attrib['name'] == 'COMPONENT_SELECTOR':
                    return child.text + blockID
        warningIgnoringMalformedBlock("componentTypeToBlockName", True, tipe, xmlBlock) #logwrite('*WARNING*: componentTypeToBlockName is ignoring malformed block with type {} in screen {} of project {} (block info: {})'.format(tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        return '*UNKNOWN-BLOCK-NAME*' # Special string to indicate something is wrong with this block
        
    elif tipe == 'procedures_defnoreturn' or tipe == 'procedures_defreturn':
        procName, procParams = procDeclNameAndParams(xmlBlock)
        return 'to_' + procName + blockID
    elif tipe == 'global_declaration':
        return 'global_' + globalDeclName(xmlBlock) + blockID
    elif tipe not in blockTypeDict.keys():
        # E.g., 'DrawingCanvas_Clicked'

        if tipe in mangledBlockTypesDict:
            unmangledType = mangledBlockTypesDict[tipe] # [2017/03/29, lyn] Handle mangled types
            logwrite('*WARNING*: automatically transforming mangled block type {} to {} in screen {} of project {} (block info: {})'.format(tipe,unmangledType, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
            return componentTypeToBlockName(xmlBlock, unmangledType)
        
        # handles component_set_get in the old format [Maja 2016-07-12]
        if tipe.endswith('etproperty'):
            
            oldTipe = tipe 
            #establish set or get [Maja 2016-07-12]
            if tipe.endswith('getproperty'):
                set_or_get = "Get"
            else:
                set_or_get = "Set"
                
            # find action taken [Maja 2016-07-12]
            for child in xmlBlock:
                if child.tag == 'title':
                    tipe = tipe.split("_")[0] + "_" + set_or_get + child.text

            if oldTipe != tipe: 
                logwrite("*NOTE*: blockName transformed block type {} into {} in screen {} project {} (block info: {})".format(oldTipe, tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))
        # [Maja, 2015/11/15] handles the old style formatting 
        # e.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
        return upgradeNameFormat(tipe) + blockID
    else:
        return tipe + blockID

# [2017/03/26, lyn] Added
# [2018/07/12, audrey] taken from ai2summarizer2.py to bring jail up to speed
def upgradeNameFormat(tipe):
    logwrite("upgradeNameFormat: about to split")
    action = tipe.split('_')[-1]
    logwrite("upgradeNameFormat: about to join and split")
    compName = '_'.join(tipe.split('_')[:-1]) # Fixed by lyn
    compType = findComponentType(compName)
    if compType == None:
        upgradedName = '*UNKNOWN-BLOCK-NAME*'
    else:
        upgradedName = compName + '.' + action
        if compType == compName:
            upgradedName += 'Generic' # Handle generic types for old-style projects
        # Debugging:
        # print "***upgradeFormat***", tipe, upgradedType, currentProjectPath
    logwrite("*NOTE*: upgradeNameFormat transformed old-style name {} into {} in screen {} of project {}".format(tipe, upgradedName, currentScreenName, currentProjectPath))
    return upgradedName


# Returns a tuple (kind, numParams) (currently uses only number of params, not their names)
# [2018/07/11, audrey] Change to be compatible with AI2_component_specs_nb155
def lookupMethod(componentName, methodName):
  componentName = formToScreen(componentName)
  if componentName not in AI2_component_names: 
    raise RuntimeError("lookupMethod: unknown component name " + componentName)
  handler = componentName + "." + methodName
  if handler not in AI2_component_specs_nb155:
    raise RuntimeError("lookupMethod: unknown method name " + methodName + " for component " + componentName)
  methodEntry = AI2_component_specs_nb155[handler]
  #print "before methodEntry['paramNames'] for " + handler
  #print methodEntry['paramNames']
  return (methodEntry['kind'], len(methodEntry['paramNames']))

# Returns parameter names for event
def lookupEventParams(componentName, eventName):
  componentName = formToScreen(componentName)
  if componentName not in AI2_component_names:
    # [2018/07/11, audrey] correct name of method shown in error (used to be lookupMethod)
    raise RuntimeError("lookupEventParams: unknown component name " + componentName)
  #componentEntry = [componentName]
  eventHandler = componentName + "." + eventName
  #eventDict = componentEntry['events']
  if eventHandler not in AI2_component_specs_nb155:
    # [2018/07/11, audrey] correct name of method shown in the error raised (used to be lookupMethod instead)
    raise RuntimeError("lookupEventParams: unknown event name " + eventName + " for component " + componentName)
  return AI2_component_specs_nb155[eventHandler]["paramNames"] # Event entry *is* param list

# [2018/07/12, audrey] taken from ai2summarizer2.py to bring jail up to speed,
# though I have to admit that this may be slightly redundant given the above function.
def eventParams(blkType):
    if blkType in AI2_component_specs_nb155:
        return AI2_component_specs_nb155[blkType]['paramNames']
    else: 
        logwrite('***eventParams not found for event {} in {}'.format(blkType, currentProjectPath))
        return []

# [2018/07/21, audrey] change the parameter from "type" to "tipe"
def blockTypeToKind(tipe):
  #tipe = blockDict['*type']
  #tipe = blockType(blockDict)
  if tipe in mangledBlockTypesDict:
    tipe = mangledBlockTypesDict[tipe]
  if tipe in blockTypeDict: 
    return blockTypeDict[tipe]['kind']
  else:
    logwrite("blockTypeToKind: Unrecognized block type " + tipe)
    return blockTypeToKind(upgradeTypeFormat(tipe))
    #    raise RuntimeError('blockTypeToKind: unrecognized type -- ' + tipe)

'''The arg names of a block depends on several factors, including whether it
   has expandable arg names, whether it's a component method call or procedure call,
   and whether it's a generic component method call or component property getter/setter.
   Note that this is only used for value sockets and not for statement sockets, 
   and is not used for "special" blocks like if, loops, etc.'''
def blockDictToArgNames(blockDict):
  tipe = blockDict['*type']
  if tipe in mangledBlockTypesDict:
      tipe = mangledBlockTypesDict[tipe]
      blockDict['*type'] = tipe
  oldTipe = tipe
  try:
      specificType = upgradeTypeFormat(tipe)
      blockDict['*type'] = AI2_component_specs_nb155[specificType]['type']
      tipe = blockDict['*type']
      logwrite("blockDictToArgNames:\n\tspecificType: {}\n\tblockType: {}\n\toldType: {}".format(specificType, tipe, oldTipe))
  except:
      tipe = oldTipe
  #if oldTipe != tipe:
  #    blockDict['*type'] = tipe
  if tipe == 'component_method_call_expression' or tipe == 'component_method_call_statement':
    (kind, numArgs) = lookupMethod(blockDict['component_type'], blockDict['method_name'])
    argNames = map(lambda index: 'ARG' + str(index), range(0, numArgs))
    if 'is_generic' in blockDict and blockDict['is_generic'] == 'true': 
      argNames.insert(0, 'COMPONENT') # Generic calls have extra COMPONENT ARG
  elif tipe == 'component_method': # [2018/07/21, audrey] added to handle this
    params = AI2_component_specs_nb155[blockDict['component_type'] + "." + blockDict['method_name']]['paramNames']
    argNames = map(lambda index: 'ARG' + str(index), range(0, len(params)))
    if 'is_generic' in blockDict and blockDict['is_generic'] == 'true':
      argNames.insert(0, 'COMPONENT')
    #logwrite("component method: " + str(json.dumps(blockDict, indent=2, separators=(',', ': '))))
  elif tipe == 'component_get' or tipe == 'component_set':
    argNames = blockTypeDict[tipe]['argNames'][:] # Need to copy via [:] since may mutate and don't want to change original!
    # print('blockDictToArgNames', 'type=', type, 'argNames=', argNames, 
    #      'is_generic in blockDict=', 'is_generic' in blockDict, 
    #      'blockDict[is_generic]=', blockDict['is_generic'],
    #      "blockDict[is_generic] == 'true'", blockDict['is_generic'] == 'true')
    if 'is_generic' in blockDict and blockDict['is_generic'] == 'true': 
      argNames.insert(0, 'COMPONENT') # Generic calls have extra COMPONENT ARG
  elif tipe == 'procedures_callnoreturn' or tipe == 'procedures_callreturn': # procedure calls
    # print "procedures", "before len(blockDict['params'])" #****
    # print blockDict
    numParams = 0
    if 'params' in blockDict:
        numParams = len(blockDict['params'])
    # print "procedures", "after len(blockDict['params'])" #****
    argNames = map(lambda index: 'ARG' + str(index), range(0, numParams))
  elif tipe in blockTypeDict: 
    entry = blockTypeDict[tipe]
    if 'argNames' in entry:
      argNames = entry['argNames'][:] # Need to copy via [:] since may mutate and don't want to change original!
    else:
      argNames = []
    if 'expandableArgName' in entry:
      expandableName = entry['expandableArgName']
      if 'items' in blockDict:
        numItems = int(blockDict['items'])
        argNames.extend(map(lambda index: expandableName + str(index), range(0, numItems)))
      else:
        raise RuntimeError('blockDictToArgNames: no items for expandable arg ' 
                           + expandableName + " in block of type " + tipe)
  else: 
    raise RuntimeError('blockDictToArgNames: unrecognized type -- ' + tipe)
  return argNames

declarationTypes = ['component_event', 'global_declaration', 'procedures_defnoreturn', 
                    'procedures_defreturn']
# [2018/07/12, audrey] These were in the "declarationTypes" dict but don't seem to be declaration types
# themselves??? Also these aren't in the corresponding declarationTypes list in ai2summarizer2.py.
# So just trying to make it more consistent.
#, 'procedures_callnoreturn', 'procedures_callreturn']

nonDeclarationTypes = ['component_method', 'component_set_get']

# [2016/08/06, lyn] This is new, and correctly handles several cases not handled correctly before:
# * lexical_variable_get and lexical_variable_set used to be incorrectly treated as top-level declarations.
# * any "old-style" block, like 'DrawingCanvas_Clicked', 'DrawingCanvas_DrawCircle', or 'StartButton_SetText'
#   was previously treated as a top-level declaration, but only the first is. 
def isDeclarationType(generalType, specificType):
    if generalType in declarationTypes: 
        return True
    elif generalType in nonDeclarationTypes:
        return False
    elif generalType in blockTypeDict: # e.g, math_add, lists_append_lists
        return False
    # If get here, generalType must be "old-style" type like 'DrawingCanvas_Clicked' 
    # and specificType must be upgraded type, like 'Canvas.Clicked'
    elif specificType in AI2_component_specs_nb155: # handles old-style component_event and component_method
        return AI2_component_specs_nb155[specificType]['type'] == 'component_event'
    else: 
        return False # Handles old-style component getters and setters. E.g. 'StartButton_GetText'
                     # as well as generic methods, E.g. Canvas.DrawCircleGeneric

# [2016/08/06, lyn] Modified to handle generic methods and generic getters/setters
def blockType(xmlBlock):    
    ''' [2015/11/11, lyn] Specially handle component_event, component_method, component_set_get
         E.g., for generalType component_event, might have Button.Click;
               for generalType component_method, might have Canvas.DrawCircle
               for generalType component_set_get, might have Button.GetText or Button.SetText
         Now also handles "old style" types. E.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked' 
         Now also handles generic methods and getters/setters: 
             e.g. Canvas.DrawCircleGeneric and Button.GetTextGeneric
    '''
    # [2018/07/11, audrey] Make consistent with changes to same function in ai2summarizer2.py
    return componentTypeToBlockType(xmlBlock, xmlBlock.attrib['type'])
    '''tipe = xmlBlock.attrib['type']    
    # Debugging:
    # print "***blockType", xmlBlock, tipe
    if tipe == 'component_event':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return child.attrib['component_type'] + "." + child.attrib['event_name']
    elif tipe == 'component_method':
        for child in xmlBlock:
            if child.tag == 'mutation':
                methodName = child.attrib['component_type'] + "." + child.attrib['method_name']
                if child.attrib['is_generic'] == 'true':
                    methodName += 'Generic'
                return methodName
    elif tipe == 'component_set_get':
        for child in xmlBlock:
            if child.tag == 'mutation':
                getterSetterName = (child.attrib['component_type'] 
                                    + "." 
                                    + child.attrib['set_or_get'].capitalize() 
                                    + child.attrib['property_name'])
                if child.attrib['is_generic'] == 'true':
                    getterSetterName += 'Generic'
                return getterSetterName
    elif tipe not in blockTypeDict.keys():
        
        # handles component_set_get in the old format [Maja 2016-07-12]
        if tipe.endswith('etproperty'):
            
            #establish set or get [Maja 2016-07-12]
            if tipe.endswith('getproperty'):
                set_or_get = "Get"
            else:
                set_or_get = "Set"
                
            # find action taken [Maja 2016-07-12]
            for child in xmlBlock:
                if child.tag == 'title':
                    tipe = tipe.split("_")[0] + "_" + set_or_get + child.text
        # [Maja, 2015/11/15] handles the old style formatting 
        # e.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
        # [2018/07/12] update to reflect removal of upgradeFormat
        return upgradeTypeFormat(tipe)
    else:
        return tipe'''


# [Maja, 2015/11/15] Create
# [2016/08/06, lyn] Modified to handle generic types
# [2017/03/29, lyn] Modified to handle nonworking cases
def upgradeTypeFormat(tipe):
    if tipe in blockTypeDict:
        #logwrite('upgradeTypeFormat: found normal type {}'.format(tipe))
        return tipe
    #logwrite("upgradeTypeFormat")
    action = tipe.split('_')[-1]
    #logwrite("upgradeTypeFormat: about to attempt to join")
    compName = '_'.join(tipe.split('_')[:-1]) # Fixed by lyn
    #logwrite("upgradeTypeFormat: after join")
    if compName not in blockTypeDict:
        compType = findComponentType(compName)
    else:
        return tipe
    if compType == None:
        upgradedType = '*IGNORE*'
    else:
        upgradedType = compType + '.' + action
        if compType == compName:
            upgradedType += 'Generic' # Handle generic types for old-style projects
        # Debugging:
        # print "***upgradeFormat***", tipe, upgradedType, currentProjectPath

    logwrite("*NOTE*: upgradeTypeFormat transformed old-style block type {} into {} in screen {} of project {}".format(tipe, upgradedType, currentScreenName, currentProjectPath))
    return upgradedType


# [2018/07/12, audrey] Commented out the following because upgradeTypeFormat replaces it
# in the ai2summarizer2
'''
# [Maja, 2015/11/15] Create
# [2016/08/06] Modified to handle generic types
def upgradeFormat(tipe):
    action = tipe.split('_')[-1]
    compName = '_'.join(tipe.split('_')[:-1]) # Fixed by lyn
    compType = findComponentType(compName)
    upgradedType = str(compType) + '.' + str(action)
    if compType == compName:
        upgradedType += 'Generic' # Handle generic types for old-style projects
    # Debugging:
    # print "***upgradeFormat***", tipe, upgradedType, currentProjectPath
    return upgradedType
'''

# [2018/07/21, audrey] Fix to check for mangled types
def findComponentType(compName): 
    if currentComponentDictionary == {}: 
        populateCurrentComponentDictionary() # Populate dictionary if not already populated. 
    if compName in currentComponentDictionary:
        return currentComponentDictionary[compName] # Return answer from populated dictionary.
    elif compName in AI2_component_names:
        return compName
    elif compName in mangledBlockTypesDict:
        return mangledBlockTypes[compName]
    else:
        raise Exception("findComponentType: Unable to find component name " + compName 
                        + " for old-style project " + currentProjectPath)


def populateCurrentComponentDictionary():
    '''Assume that currentComponentDictionary is currently {}. 
       Process the components in the currentScmJSONContents to populate currentComponentDictionary
       with mappings of component names (like 'DrawingCanvas') to component types (like 'Canvas').'''
    def recursivelyProcessComponents(componentDict):
        # Debugging: 
        # print componentDict[u'$Name'], "=>", componentDict[u'$Type']
        currentComponentDictionary[componentDict[u'$Name']] = componentDict[u'$Type']
        if u'$Components' in componentDict:
            for component in componentDict[u'$Components']:
                recursivelyProcessComponents(component)
    # Debugging: 
    # print("populating dictionary for " + currentProjectPath)
    recursivelyProcessComponents(currentScmJSONContents[u'Properties'])

# Lyn sez: the above code supersedes the following
"""
def findComponentType(compName): 
    ''' takes the component name, opens the .scm file, and finds the type of component '''
    scmLines = linesFromZippedFile(currentScmFileName)
    if (len(scmLines) == 4
        and scmLines[0].strip() == '#|'
        and scmLines[1].strip() == '$JSON'
        and scmLines[3].strip() == '|#'):
        data = json.loads(scmLines[2])
        
        # Makes sure all names are found and included [Maja 2016-07-12] 
    if u'$Components' in data[u'Properties'].keys():
        
        return searchComponents(compName[0], data[u'Properties'])

def searchComponents(name, components): #[Maja 2016-07-12]
    '''Takes a name and the value of a $Components (a dictionary) and
    returns the type of the component with the $Name name'''
    
    if '$Name' in components.keys() and components['$Name'].encode('utf-8') == name or \
    '$Type' in components.keys() and components['$Type'].encode('utf-8') == name:

        return components[u'$Type']

    elif "$Components" in components.keys():
        dlist = components["$Components"]
        
        for dyct in dlist:
            result = searchComponents(name, dyct)
        
            if result != None:
                return result
"""




def dummyProperties():
    """
    Return a list representing a dummy project properties file
    equivalent to output of linesFromZippedFile(myZip, 'project.properties')
    """
    global num_missing_properties
    num_missing_properties += 1   
    return ['main=appinventor.' + DUMMY_USER_NAME + '.' + DUMMY_PROJECT_NAME + '.Screen1\n',
     'name=' + DUMMY_PROJECT_NAME + '\n',
     'assets=../assets\n',
     'source=../src\n',
     'build=../build\n',
     'versioncode=1\n',
     'versionname=1.0\n',
     'useslocation=False\n',
     'aname=' + DUMMY_PROJECT_NAME + '\n']

# Removed by Lyn
'''
def dummyMeta():
    """
    Return dummy meta file for projects without META files
    """
    global num_missing_meta
    num_missing_meta += 1
    return ['{"name": "' + DUMMY_PROJECT_NAME + '", "modified": ' + str(DUMMY_MODIFIED_TIME) + ', "created": ' + str(DUMMY_CREATED_TIME) + '}']
'''

def dummyScm():
    """
    Return dummy SCM file for projects with missing SCM files
    """
    global num_missing_scm
    num_missing_scm += 1
    return '{"YaVersion":"' + str(DUMMY_VERSION) + '","Source":"Form","Properties":{"$Name":"' + str(DUMMY_SCREEN_NAME) + '","$Type":"Form","$Version":"' + str(DUMMY_VERSION) + '","AppName":"' + str(DUMMY_PROJECT_NAME) + '","Title":"' + str(DUMMY_SCREEN_NAME) + '","Uuid":"0"}}\n'

def emptyBkyLines():
    return ['<xml>', '</xml>']
    
"""
Given the path to a directory that contains users (dirName) and a file extension (fileType),
remove all files in the project directory that end with that file extension
"""
def cleanup(dirName, fileType):
    for user in os.listdir(dirName):
        user = os.path.join(dirName, user)
        if os.path.isdir(user):
          for project in os.listdir(user):
              projectPath = os.path.join(user, project)
              if projectPath.endswith(fileType):
                  os.remove(projectPath)

# Deleted a bunch of dictionaries from here because they should be in dictionary.py

# -------------------------------------------------------------------------------
# [2018/07/12, audrey] Updated logging using functions from ai2summarizer2,
# to make it more consistent. Also the time logging feature is very helpful.

logStartTime = None
logPrefix = 'jail2Audrey'
printMessagesToConsole = True

def createLogFile():
    global logFileName
    global logStartTime
    if not os.path.exists("logs"):
        os.mkdir("logs")
    logStartTime = datetime.datetime.utcnow()
    startTimeString = logStartTime.strftime("%Y-%m-%d-%H-%M-%S")    
    logFileName = "logs/" + logPrefix + '-' + startTimeString

def logwrite (msg): 
    with open (logFileName, 'a') as logFile:
        # [2018/07/12, audrey] add conversion of logStartTime to a datetime.timedelta bc
        # otherwise python actually complains
        timeElapsed = datetime.datetime.utcnow() - logStartTime
        timedMsg = str(timeElapsed) + ': ' + msg
        if printMessagesToConsole:
            print(timedMsg) 
        logFile.write(timedMsg + "\n")


# [2016/08/12, lyn] No longer needed 
'''
def padWithZeroes(num, digits):
  s = str(num)
  digitsToGo = digits - len(s)
  if digitsToGo > 0:
    return ('0' * digitsToGo) + s
  else: 
    return s
'''

def readLastDirectoryProcessed(): 
    if not os.path.exists(lastDirectoryProcessedFilename):
        return None
    else:
        with open(lastDirectoryProcessedFilename, 'r') as inFile:
            return inFile.readline().strip()

def writeLastDirectoryProcessed(dirName): 
    with open(lastDirectoryProcessedFilename, 'w') as outFile:
        outFile.write(dirName)

def readLastTopDir(): 
    if not os.path.exists(lastTopDirFilename):
        return None
    else: 
        with open(lastTopDirFilename, 'r') as inFile:
            return inFile.readline().strip()

def writeLastTopDir(dirName): 
    with open(lastTopDirFilename, 'w') as outFile:
        outFile.write(dirName)

def processNext(): 
    if topDir != readLastTopDir():
        fromBeginning = True
        if os.path.exists(lastDirectoryProcessedFilename):
            os.remove(lastDirectoryProcessedFilename)
    elif os.path.exists(lastDirectoryProcessedFilename):
        # We have a choice: to continue with file after last one completely process, or do start fresh.
        lastDirectory = readLastDirectoryProcessed()
        logwrite("You have already processed directories through " + lastDirectory + ".")
        logwrite("To continue processing with the next directory, enter any input *other* than B or b.")
        logwrite("To process all directories again from the beginning, enter B or b.")
        answer = raw_input("> ").strip().lower()
        logwrite(answer)
        fromBeginning = (answer == 'b')
        if fromBeginning:
            os.remove(lastDirectoryProcessedFilename)
    else:
        fromBeginning = True
    writeLastTopDir(topDir)
    createLogFile()
    if isDirectoryOfUserDirectories(topDir): # Is topDir a directory of users? 
        # If so, process directly with processDir
        processDir('') # I.e., only use topDir
    else: # Otherwise, process subdirs of topDir with processDir
        allFiles = os.listdir(topDir)
        allDirs = [file for file in allFiles if os.path.isdir(os.path.join(topDir, file))]
        allDirsSorted = sorted(allDirs)
        lastIndex = len(allDirsSorted) - 1
        if fromBeginning:
            nextIndex = 0
        else: 
            nextIndex = allDirsSorted.index(lastDirectory) + 1
        while nextIndex <= lastIndex:
            nextDir = allDirsSorted[nextIndex]
            processDir(nextDir)
            writeLastDirectoryProcessed(nextDir)
            nextIndex += 1        

def processDir(dir): 
    global num_missing_properties, num_missing_meta, num_missing_scm, num_case_mismatches
    num_missing_properties = 0
    num_missing_meta = 0 
    num_missing_scm = 0
    num_case_mismatches = 0
    start = datetime.datetime.now()
    logwrite('*** Start processing directory {} with topSummary={} at {}'.format(dir, str(topSummary), str(start)))
    allProjectsToJSONFiles(os.path.join(topDir, dir), None, os.path.join(summaryDir, dir))
    end = datetime.datetime.now()
    logwrite('*** Done processing directory {} with topSummary={} at {}'.format(dir, str(topSummary), str(end)))
    logwrite("ran in {}".format(end-start))
    logwrite("Num missing project.properties: {}. Num missing META: {}. Num missing SCM: {}. Num case mismatches: {}".format(num_missing_properties, num_missing_meta, num_missing_scm, num_case_mismatches))


# Returns True if first subdir of dir is a directory of containing projects
# If there are no subdirs, return False
def isDirectoryOfUserDirectories(dir):
    for fileOrDir in os.listdir(dir):
        absPath = os.path.join(dir, fileOrDir)
        if os.path.isdir(absPath):
            return isUserDirectory(absPath)
    return False

# Returns True if directory contains a .aia or .zip project or directories that are ProjectDirectory
# Returns false otherwise. 
def isUserDirectory(dir):
    for fileOrDir in os.listdir(dir):
        absPath = os.path.join(dir, fileOrDir)
        if absPath.endswith('.aia') or absPath.endswith('.zip'): # Ignore other regular files
            return True
        elif os.path.isdir(absPath):
            return isProjectDir(absPath)
    return False



def processTutorials():
    allProjectsToJSONFiles(tutorialsInputDir, None, tutorialsOutputDir)
    


'''
if __name__=='__main__':  
    logFileName = '*unopenedFilename*'
    logPrefix = 'ai2ToJailLyn'
    printMessagesToConsole = True
    # print sys.argv
    # userDir = 'aia-files'
    # outputDir = 'jail-files'
    # projectToJAILFile(sys.argv[1], userDir, outputDir)
    userDir = '/Users/fturbak/Projects/AppInventor2Stats/code/ai2_tutorialfinder/TutorialsMore'
    outputDir = '/Users/fturbak/Projects/AppInventor2Stats/code/ai2_tutorialfinder/TutorialsMoreJAIL'
    allProjectsToJAILFiles(userDir, numToKeep=None, outputDir=outputDir)
''' 
'''    
    logFileName = '*unopenedFilename*'
    logPrefix = 'ai2summarizerLyn'
    printMessagesToConsole = True
        
    # [2016/08/12, lyn] indexedDir is no longer used; it is superseded by topDir (see below)
    #indexedDir = '/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized'
    #summaryDir = '/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized_2016_08_06_test1'
    #indexedDir = '/Users/Maja/Documents/AI/biggerprojects/ai2_users_long_term_randomized'
    #summaryDir = '/Users/Maja/Documents/AI/biggerprojects/ai2_users_long_term_randomized_2016_08_07_test1'
    
    topDir = '/Users/Maja/Documents/AI/biggerprojects/ai2_users_long_term_randomized'
    summaryDir = '/Users/Maja/Documents/AI/biggerprojects/ai2_users_long_term_randomized_2016_11_13_nontop_final'
    #topDir = '/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random'
    #summaryDir = '/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random_2016_08_13_nontop_final'
    
    # [2016/08/12, lyn] The following code is modified to handle more general input directory structure for data 
    lastDirectoryProcessedFilename = 'lastDirectoryProcessed.txt'
    lastTopDirFilename = 'lastTopDir.txt'

    #tutorialsInputDir = '/Users/fturbak/Projects/AppInventor2Stats/code/ai2_tutorialfinder/Tutorials'
    #tutorialsOutputDir = '/Users/fturbak/Projects/AppInventor2Stats/data/tutorial_summaries_top_2016_08_19'
    #
    #tutorialsInputDir = '/Users/Maja/Documents/AI/ihaveadream'
    #tutorialsOutputDir = '/Users/Maja/Documents/AI/ihaveadream/sum'
    
    tutorialsInputDir = '/Users/Maja/Documents/AI/git/Tutorials'
    tutorialsOutputDir = '/Users/Maja/Documents/AI/git/TutorialSummaries/tutorial_summaries_nontop'
    
    # *** Added by Maja [2016-08-07]
    #topSummary = True # Global variable as flag for which kind of summary we are trying to produce
    topSummary = False
    
    
    processNext()
    #processTutorials()
    # allProjectsToJSONFiles('/Users/Maja/Documents/AI/Tutorials', 100000)
'''

# print 'running...'
# start = datetime.datetime.now()

# Maja's tests
#cleanup('/Users/Maja/Documents/AI/Tutorials', '.json')
#projectToJSONFile('/Users/Maja/Documents/AI/Tutorials/AI_website/PicCall.zip')
#allProjectsToJSONFiles('/Users/Maja/Documents/AI/Tutorials', 100000)
# findComponentType('hey', '/Users/Maja/Documents/AI/PaintPot2Old.zip', 'Screen1.scm')
#print upgradeFormat('Canvas_Clicked', '/Users/Maja/Documents/AI/PaintPot2Old.zip', 'Screen1.scm')


# Lyn's testsx
# cleanup('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random', '.zip')
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random', 10)
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random', 10003
# projectToJSONFile('/Users/fturbak/Projects/AppInventor2Stats/data/MIT-tutorials/HelloPurr.aia')

# This doesn't work because of splitting on dots!
# allProjectsToJSONFiles('../../../data/ai2_users_long_term_randomized/00', 1000

# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random_copy', 10000)
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized/00', 1000)
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized/01', 1000)


# Benji's Tests
# dir_small = "/Users/bxie/Documents/ai2_users_long_term_15k" 
# N = 15000
# cleanup(dir_small, 'summary.json')
# print 'cleanup done...'
# allProjectsToJSONFiles(dir_small, N)

# end = datetime.datetime.now()
# print 'done!'
# print "ran in {}".format(end-start)
# print "Num missing project.properties: {}. Num missing META: {}. Num missing SCM: {}. Num case mismatches: {}".format(num_missing_properties, num_missing_meta, num_missing_scm, num_case_mismatches)

#methodDict = AI2_component_specs_nb155['methods']
if __name__=='__main__':
    logFileName = '*unopenedFilename*'
    logPrefix = 'ai2ToJail2Audrey'
    printMessagesToConsole = True
    createLogFile()
    #allProjectsToJAILFiles('/Users/audrey/Personal/School/College/Work/summer2018/ai2_tutorialfinder/myprojects', numToKeep=None, outputDir="myjails")
    allProjectsToJAILFiles('/Users/audrey/Downloads/ai2_10k_random_users_deidentified_aias', numToKeep=None, outputDir="10kjails")

# Lyn Turbak, Benji Xie, Maja Svanberg, Audrey Seo
# AI2 summarizer, 2nd version 
# Code adapted from jail.py

''' History (reverse chronological)
2018/06/29 (Audrey):
-------------------------------------------------------------------------------
* Find disabled blocks
* Keep track of the numbers of various block types that are "disabled" versus
  "active" and leave dictionary entries like *Number of Blocks as "total"
  values.
* Also records the number of each block type that is disabled
* Records a list of the screens' names under "*Screen Names"
* Keep track of the names of components, by their types, so it adds a dictionary
  where the key is the type of the component and the value is a list of names
  given to components of this particular type.
* Handle disabled procedure calls differently from enabled ones

2018/06/21 (Audrey):
-------------------------------------------------------------------------------
* Refactor some logging that was identical across several instances
* Move the long dictionaries to a different file

2018/06/14 (Audrey):
-------------------------------------------------------------------------------
* Fix typo in *UnknownGlobalVarName*

2017/07/26 (Lyn): 
-------------------------------------------------------------------------------
* Remove rogue double quote in millisToDatetime '"NoDateTime'

2017/07/12 (Lyn): 
-------------------------------------------------------------------------------
* In userToJSONFiles, add guard os.path.exists(os.path.join(outputDir, relUserPath))
  outside call to os.makedirs(os.path.join(outputDir, relUserPath))
* Move the following from processDir to be globals: topSummary, logPrefix, printMessagesToConsole

2017/07/10 (Lyn): 
-------------------------------------------------------------------------------
* Modify blockType to changed component_component_block to form like Ball.ComponentGeneric
* Added Media to each screen.

2017/07/02 (Lyn): 
-------------------------------------------------------------------------------
* Fix bug in reporting total number of users processed at end
* Track currentScreenName for errors and warnings
* Print id,x,y for malformed blocks 
* Print more details in *EXCEPTION case (encountered only one in 46K dataset)

2017/06/28 (Lyn): 
-------------------------------------------------------------------------------
* Fixed bug where createdMills datetime was also being reported for modifiedMillis datetime
* Remove numer-of-project argument (no longer used)
* Focus on user directories rather than user projects, so directories empty summaries can be produced

2017/06/22 (Lyn): 
-------------------------------------------------------------------------------
* Fixed major bug in addBlockInfo, where it was failing to traverse:
  + arg and next block of lexical set
  + next block of loops and lexical decl stm
* Added **creaated/modifiedDatetime, and renamed **created/modified to **created/modifiedMillis

2017/03/27-28 (Lyn): 
-------------------------------------------------------------------------------

* Overhauld findBlockInfo/processRawBlocksList to fix bugs and calculate extra 
  summary information for DMSVLSS2017 paper. New combined fundtion is named
  'addBlockInfo' and uses lots of new helper functions. 
  + Previous version would use both proc and param names for procedure name; fixed
  + No longer track list of Local names and Procedure Names (not useful);
    Instead track:
    - Name Summary (number of sets and gets) for each kind of name:
      globals, event params, proc params, loop vars, local decl names, unbounds
    - Distinguish nonglobal bound names by their "source". E.g.
      startX|Canvas1.Flung#125, long2|distanceBetweenLatLon#27, 
      rowList|controls_forEach#46, listOfLists|local_declaration_statement#57
    - Procedure Summary: name, fruitfulness, params, numcalls for each procedure
  + Also track block summary information for (1) each top block and (2) each orphan root. 
* Renamed upgradeFormat to upgradeTypeFormat

     
2016/11/19 (Lyn): 
-------------------------------------------------------------------------------

* Fixed indentation bug in projectTOJSONFile 

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
import utils
from dictionaries import * # [2018/06/21, audrey] New, holds dictionaries pertaining to blocks and components

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
# shouldPrintFoundProjectDirs = True
shouldPrintFoundProjectDirs = False
print_every = 1000

# Added by audrey because I just wanted to get all of the function/variable names defined
# and leaving logFileName as an undefined global won't allow me to use dir(modulename) to get
# all of the functions/variables
logFileName = "*undefinedfilename*"

# *** Removed by lyn
'''
# meta_filename = 'METADATA' # 'METADATA' for old files, 'META' for new files
meta_filename = 'META' # 'METADATA' for old files, 'META' for new files
'''

# *** Added by lyn 
currentProjectPath = None # Global variable that tracks current project path being processed
currentProjectNumber = 0 # Global variable that tracks current project path being processed
currentUserNumber = 0 # Global variable that tracks current user being processed
currentScreenName = None # Global variable that tracks name of current screen being processed
currentScmJSONContents = None # Global variable that tracks contents of .scm file for currentScreen
currentComponentDictionary = {} # Global variable that contains dictionary mapping component names to component types for current screen

def allProjectsToJSONFiles(inputDir, outputDir=None):
    '''assumes inputDir is path to directory tree that somewhere contains user directories
       that contains projects (in .aia, .zip, or as dir).
      + has 2nd arg outputDir with default value None
        - A non-None value specifies (possibly new) target directory for summary .json files
        - A None value writes XYZ_summary.json file to same directory as .aia/.zip file.
      [lyn, 2017/06/28] removed numToKeep argument'''
    logwrite('allProjectsToJSONFiles({}, {})'.format(inputDir, outputDir))
    # logwrite('Finding users (zipping as necessary) ...'
    logwrite('Finding users ...')
    listOfAllUsers = findUserDirs(inputDir)
    logwrite("Done finding users...")
    # *** Added by lyn 
    logwrite("Number of users to process: " + str(len(listOfAllUsers)))
    # *** Added by lyn 
    global currentUserNumber, currentProjectNumber
    currentUserNumber = 0 # Helps in debugging particular projects
    currentProjectNumber = 0 # Helps in debugging particular projects
    for relUserPath in listOfAllUsers:
        userToJSONFiles(relUserPath, inputDir, outputDir)
    logwrite('Done processing all {} users. Total number of projects processed: {}'.format(currentUserNumber, currentProjectNumber))

def userToJSONFiles(relUserPath, inputDir, outputDir=None):
    if outputDir != None and not os.path.exists(os.path.join(outputDir, relUserPath)):
        os.makedirs(os.path.join(outputDir, relUserPath))
    absUserPath = os.path.join(inputDir, relUserPath)
    projectFilenames = [filename for filename in os.listdir(absUserPath)
                        if filename.endswith('.aia') or filename.endswith('.zip')]
    for projectFilename in projectFilenames: 
        relProjectPath = os.path.join(relUserPath, projectFilename)
        absProjectPath = os.path.join(inputDir, relProjectPath)
        # Print right *before* we process a project 
        global currentUserNumber, currentProjectNumber
        if currentProjectNumber % print_every == 0: 
            logwrite(str(currentProjectNumber) + ": " + relProjectPath)
        if os.path.exists(absProjectPath):
            projectToJSONFile(relProjectPath, inputDir, outputDir)
            # [2016/08/12] Don't delete .zip file anymore! (Leave it in case we want to reprocess!)
            # if os.path.exists(absProjectPath.split('.')[0]) and absProjectPath.split('.')[1] == 'zip':
            #    # *** Note from Lyn: should only remove if it's not the main representation of the project!
            #    os.remove(absProjectPath)
        # *** Added by lyn 
        currentProjectNumber += 1
    currentUserNumber += 1


def findUserDirs(dirName):
    """
    given path to directory tree (dirName) that somewhere contains user directories
    return list of PATHS RELATIVE TO DIRNAME of user directories containing projects.
    """
    relUserPaths = []
    num_users_processed = [0] # Listify to solve scoping issues
    def processFileOrDir(relPrefix, fileOrDir): # Recursively process directories until get to projects. 
        relPath = os.path.join(relPrefix, fileOrDir)
        absPath = os.path.join(dirName, relPath)
        if isUserDir(absPath):
            relUserPaths.append(relPath)
            num_users_processed[0] += 1
            if shouldPrintFoundProjectDirs and num_users_processed[0] % print_every == 0: 
                logwrite(str(num_users_processed[0]) + ": " + relPath)
        elif os.path.isdir(absPath): 
            for fod in os.listdir(absPath):
                processFileOrDir(relPath, fod)
        else: 
            # Ignore other files 
            pass
    filesOrDirs = os.listdir(dirName)
    for fileOrDir in filesOrDirs:
        processFileOrDir('', fileOrDir)
    return relUserPaths

'''
# [2017/06/28, lyn] No longer use this, changing it to findUserDirs. But keep for historical record.

# [2016/08/06, lyn] Modified this to return list of paths *relative* to dirName, rather than
#  *absolute* paths including dirName. This simplifies writing summary files 
# to a destination directory other than dirName.
def findProjectDirs(dirName, numToKeep=None):
    """
    given (1) path to directory tree (dirName) that somewhere contains user directories
    and (2) number of users(numUsers), return list of PATHS RELATIVE TO DIRNAME of 
    .aia project files or zipped project directories.
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
            if shouldPrintFoundProjectDirs and num_projects_processed[0] % print_every == 0: 
                logwrite(str(num_projects_processed[0]) + ": " + foundProject)

    # *** Added by lyn 
    filesOrDirs = os.listdir(dirName)
    if numToKeep != None:
        filesOrDirs = filesOrDirs[:numToKeep]
    for fileOrDir in filesOrDirs:
        processFileOrDir('', fileOrDir)
    return relProjectPaths
'''

# [2016/06/28] Returns True iff absDirPath is an AI2 user directory. 
# I.e., it's an empty dir or contains a .zip, .aia, or projectDir
def isUserDir(absPath):
    if not os.path.isdir(absPath):
        return False # [lyn, 2017/06/28] added
    else:
        filesOrDirs = [filename for filename in os.listdir(absPath) if filename != '.DS_Store']
        return filesOrDirs == [] or utils.exists(lambda filename: filename.endswith('.aia')\
                                                                  or filename.endswith('.zip')\
                                                                  or isProjectDir(os.path.join(absPath, filename)),
                                                 filesOrDirs)


# [2016/08/12] Returns True iff absDirPath is an AI2 project directory like one
# in Benji's data. I.e., it contains only files and has at least a .scm or .bky file. 
def isProjectDir(absPath):
    if not os.path.isdir(absPath):
        return False # [lyn, 2017/06/28] added
    else: 
        filesOrDirs = os.listdir(absPath)
        for fileOrDir in filesOrDirs:
            if os.path.isdir(os.path.join(absPath, fileOrDir)):
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
def projectToJSONFile(relProjectPath, userDir, outputDir=None):
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
        jsonProject = projectToJSON(currentProjectPath)
        if outputDir == None:
            # Write summary file to same directory as input file 
            jsonProjectFileName = projectToJSONProjectFileName(currentProjectPath)
        else:
            jsonProjectFileName = projectToJSONProjectFileName(os.path.join(outputDir, relProjectPath))
        (dirPath, basefile) = os.path.split(jsonProjectFileName) # Split jsonProjectFileName into directory path and base filename
        # [lyn, 2016/11/19] Fixed indentation bug on this block by de-indenting it
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
    except:
        packet = sys.exc_info()[:2]
        logwrite('***EXCEPTION while processing project {} (and possibly screen {}): {}; {}'.format(
                currentProjectPath, currentScreenName, packet[0], packet[1]))

# Introduced by Lyn. projectPath name might contain a dot, so 
# 
#   projectPath.split('.')[0] + '_summary.json'
# 
# won't always work.  Even though project name is guaranteed not to have dots, other components
# of projectPath might have dots.  E.g., suppose projectPath is 
# /Users/fturbak/ai2.users.long.term.randomized/03/03017/p001_002_AlexTalkToMe.aia
def projectToJSONProjectFileName(projectPath):
    parts = projectPath.split('.')
    allButExtension = '.'.join(parts[:-1])
    # [2016-08-07, Maja] adding check to enable different kinds of summaries
    if topSummary:
        return allButExtension + '_summary_top2.json'
    return allButExtension + '_summary2.json' # [lyn, 2017/03/28] Change name to _summary2.json to emphasize differences. 

def projectToJSON(projectPath):
    """
    Given path to zipped project (projectPath), return JSON summary of project
    """
    #***debugging: print projectPath
    summary = {}
    with zipfile.ZipFile(projectPath, 'r') as zippedFile:
        summary['**Project Name'] = findName(zippedFile)
        summary['**createdMillis'], summary['**modifiedMillis'] = findCreatedModifiedTimes(zippedFile)
        summary['**createdDatetime'] = millisToDatetime(summary['**createdMillis'])
        summary['**modifiedDatetime'] = millisToDatetime(summary['**modifiedMillis'])
        listOfScreens = findScreenNames(zippedFile)
        summary['*Number of Screens'] = len(listOfScreens)
        summary['*Screen Names'] = [] # [audrey, 2018/06/29] Add a list of screen names
        media = []
        for screenName in listOfScreens:
            global currentScreenName
            currentScreenName = screenName
            summary['*Screen Names'].append(screenName) # [audrey, 2018/06/29] Append this screen's name to the list of screen names
            screenInfo = screenToJSON(zippedFile, screenName)
            summary[str(screenName)] = screenInfo[0]
            media.extend(screenInfo[1]) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
        summary['*Media Assets'] = list(set(media)) # list(set(...)) removes duplicates
    return summary

def millisToDatetime(millis):
    #***debugging: print "millisToDatetime", type(millis), millis
    if isinstance(millis, int) and millis > 0: 
        return str(datetime.datetime.utcfromtimestamp(millis/1000.0))
    else:
        return 'NoDatetime'
    

'''GIVEN a Python zip file and a pathless filename (no slashes), extract the lines from filename,             
   regardless of path. E.g., Screen1.bky should work if archive name is Screen1.bky
   or src/appinventor/ai_fturbak/PROMOTO_IncreaseButton/Screen1.bky. 
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
                        logwrite("*NOTE* (*not* an error): Pretending there's an empty .bky file {} to match .scm file with **NO** components in project {}".format(pathlessFilename, currentProjectPath))
                        return emptyBkyLines()
                    else:
                        logwrite("*WARNING* (*might* be considered an error): Pretending there's an empty .bky file {} to match .scm file with **SOME** components in project {}".format(pathlessFilename, currentProjectPath))
                        return emptyBkyLines()
#                        raise RuntimeError("linesFromZippedFile -- no match for nonempty .bky file named: " + pathlessFilename
#                                           + " in project " + currentProjectPath)
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

def screenToJSON(zippedFile, screenName):
    scmFileName = screenName + '.scm'
    components = scmToComponents(zippedFile, scmFileName)
    bkyFileName = screenName + '.bky'
    bky = bkyToSummary(zippedFile, bkyFileName)
    return {'Components': components[0], 'Blocks': bky, 'Media': components[1]}, components[1] # components[1] is list of all media
    # [2017/07/10, lyn] Added Media to each screen.

# [2016/08/05, lyn] Introduced this helper function that returns JSON contents of .scm filex
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
# [audrey, 2018/06/29] Added component names by type to the resulting dictionary
def scmToComponents(zippedFile, scmFileName):
    numComponents = [0] # Listify to solve scope problem; does not count Screen itself
    components = {}
    strings = []
    namesByType = {}
    media = []
    def recursivelyProcessComponents(componentDict):
       '''[2016/08/06, lyn] This function fixes bug in previous versions that processed only top-level components
          and did not descend into container components like HorizontalArrangement, VerticalArrangement, and Canvas.'''
       if u'$Components' in componentDict:
           # This is a container component -- i.e., Screen/Form, HorizontalArrangement, 
           # VerticalArrangement, or Canvas.
           for component in componentDict[u'$Components']:
               numComponents[0] += 1
               if u'$Name' in component: # [audrey, 2018/06/29] add to keep track of component names
                   if component[u'$Type'] in namesByType:
                       namesByType[component[u'$Type']].append(component[u'$Name'])
                   else:
                       namesByType[component[u'$Type']] = [component[u'$Name']]
               if component[u'$Type'] in components:
                   components[component['$Type']] += 1
               else: 
                   components[component['$Type']] = 1
               if u'Text' in component:
                   strings.append(component[u'Text'])
               findMedia(component)
               # Recursively process any subcomponents (of HorizontalArrangement, VerticalArrangement, or Canvas).
               recursivelyProcessComponents(component)
    # [2016/08/06] Lyn made this a local function to modify local media list directly
    def findMedia(component):
        # [2016/08/06] Lyn reorganized this: 
        for (key,value) in component.items():
            if (key == 'Picture' or \
                    key == 'Image' or \
                    key == 'Source' or \
                    key == 'BackgroundImage' or \
                    key == 'ResponseFileName'): # [2015/12/27, maja] these were the only keys I found in any of the tutorials that had files as values. 
                media.append(value) # Lyn sez: don't worry about dups here, nor whether value is string with dot. 
             # [2016/08/06] No need to specially process values that are lists (e.g., subcomponents)
             #   because that will be handled by recursive calls to recursivelyProcessComponents.
    contents = scmJSONContents(zippedFile, scmFileName)
    recursivelyProcessComponents(contents[u'Properties'])
    return ({'Number of Components': numComponents[0],        # [2016/08/06, lyn] Distinguish number of components
             'Number of Component Types': len(components), # and number of different component types!
             'Component Names by Type': namesByType, # [audrey, 2018/06/29] add list of components' names to components dict
             'Type and Frequency': components, 
             'Strings': strings
             }, list(set(media)) # Remove dups in media
            )

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


# **********************************************************************
# BEGIN 2017/03/27-28 CODE
# [lyn, 2017/03/27] new 
# [audrey, 2018/06/29] add entries to dictionaries for disabled blocks,
#   including number of disabled blocks/active blocks, number of
#   disabled blocks types/active block types, and a dictionary for
#   containing the number of various disabled block types.
def makeAllBlockSummaryDict(): 
  return {'Types': {},
          'Disabled Types': {},
          '*Number of Blocks': 0,
          '*Number of Block Types': 0,
          '*Number of Disabled Blocks': 0,
          '*Number of Disabled Block Types': 0,
          '*Number of Active Blocks': 0,
          '*Number of Active Block Types': 0,
          'Strings': [], 
          'Procedure Summary': {},
          'Name Summary': {'globals': {},
                           'event params': {},
                           'proc params': {},
                           'loop vars': {},
                           'local vars': {},
                           'unbounds': {}}
          }
# [audrey, 2018/06/29] similar changes to the above on the same date
def makeRootBlockSummaryDict(): 
  return {'Types': {},
          'Disabled Types': {},
          '*Number of Blocks': 0,
          '*Number of Block Types': 0,
          '*Number of Disabled Blocks': 0,
          '*Number of Disabled Block Types': 0,
          '*Number of Active Blocks': 0,
          '*Number of Active Block Types': 0
          }

def addEventDecl(params, blkName, allSummaryDict):
    paramDict = allSummaryDict['Name Summary']['event params']
    for param in params:
        key = makeComposedName(param, blkName) # Can't use tuple b/c want to turn into JSON
        paramDict[key] = {'gets': 0, 'sets':  0}

def addGlobalDecl(globalName, allSummaryDict):
    globalDict = allSummaryDict['Name Summary']['globals']
    if globalName not in globalDict:
        globalDict[globalName] = {'gets': 0, 'sets':  0}
    # Otherwise already there. 

def addLoopDecl(loopVar, loopDeclName, allSummaryDict):
    loopDict = allSummaryDict['Name Summary']['loop vars']
    key = makeComposedName(loopVar, loopDeclName) # Can't use tuple b/c want to turn into JSON
    if key not in loopDict:
        loopDict[key] = {'gets': 0, 'sets':  0}
    # Otherwise already there. 

def addLocalDecls(localNames, localDeclName, allSummaryDict):
    localDict = allSummaryDict['Name Summary']['local vars']
    for localName in localNames: 
        key = makeComposedName(localName, localDeclName) # Can't use tuple b/c want to turn into JSON
        localDict[key] = {'gets': 0, 'sets':  0}

def addProcDecl(procName, params, blkName, blkType, allSummaryDict):
    # Lyn experimented with using blkName, just in case (in error) multiple procs with the same name are defined.
    # But addProcCalls won't know the block name, so this issue is moot. 
    procDict = allSummaryDict['Procedure Summary']
    #***debugging: print "addProcDecl start:", [procName, params, blkName, blkType, procDict, allSummaryDict]
    if procName not in procDict:
        procDict[procName] = {'numcalls': 0}
    procDict[procName]['params'] = params
    procDict[procName]['fruitful?'] = (blkType == 'procedures_defreturn')

    paramDict = allSummaryDict['Name Summary']['proc params']
    for param in params:
        key = makeComposedName(param, procName) # Can't use tuple b/c want to turn into JSON
        paramDict[key] = {'gets': 0, 'sets':  0}

    #***debugging: print "addProcDecl finish:", procDict, paramDict

# [audrey, 2018/06/29] Added handling for when the procedure call has been disabled
def addProcCall(procName, allSummaryDict, isDisabled=False):
    #***debugging: print "addProcCall start", [procName, allSummaryDict]
    procDict = allSummaryDict['Procedure Summary']
    if isDisabled:
        if procName not in procDict:
            procDict[procName] = {'numcalls': 0, 'numDisabledCalls': 1}
        elif 'numDisabledCalls' not in procDict[procName]:
            procDict[procName]['numDisabledCalls'] = 1
        else:
            procDict[procName]['numDisabledCalls'] += 1
    else:
        if procName not in procDict:
            procDict[procName] = {'numcalls': 1, 'numDisabledCalls': 0}
        else:
            procDict[procName]['numcalls'] += 1
    #***debugging: print "addProcCall finish", procDict

declTypeToNameSummaryDict = {
    'component_event': 'event params', 
    'controls_forEach': 'loop vars',
    'controls_forRange': 'loop vars',
    'global_declaration': 'globals', 
    'local_declaration_statement': 'local vars', 
    'local_declaration_expression': 'local vars',
    'procedures_defnoreturn': 'proc params', 
    'procedures_defreturn': 'proc params', 
    'unbound': 'unbounds'
}

lexTypeToGetSetKeyDict = {
    'lexical_variable_get': 'gets',
    'lexical_variable_set': 'sets',
}

def addNameRef(lexName, lexType, declName, declType, allSummaryDict):
    nameSummaryType = declTypeToNameSummaryDict[declType]
    nameDict = allSummaryDict['Name Summary'][nameSummaryType]
    getSetKey = lexTypeToGetSetKeyDict[lexType]
    if nameSummaryType in ['globals', 'unbounds']:
        lexKey = lexName
    else:
        lexKey = makeComposedName(lexName, declName)
    if lexKey in nameDict:
        nameDict[lexKey][getSetKey] += 1 # Add 1 to getters or setters
    elif getSetKey == 'gets':
        nameDict[lexKey] = {'gets': 1, 'sets': 0}
    else: # getSetKey == 'sets':
        nameDict[lexKey] = {'gets': 0, 'sets': 1}

def addString(string, allSummaryDict):
    allSummaryDict['Strings'].append(string)

def makeComposedName(varName, declName):
    return varName + '|' + declName

def makeEmptyEnv():
  return {}

def envExtend(env, names, declName, declType):
    newEnv = env.copy()
    for name in names:
        newEnv[name] = {'declName': declName, 'declType': declType}
    return newEnv

def bkyToSummary(zippedFile, bkyFileName):
  #***debugging: print "bkyToSummary", bkyFileName
  bkyLines = linesFromZippedFile(zippedFile, bkyFileName)
  rootElt = elementTreeFromLines(bkyLines)
  if rootElt.tag == 'MALFORMED':
      logwrite("***Project " + currentProjectPath + " has malformed .bky file " + bkyFileName)
      return 'MALFORMED BKYFILE'
  elif not rootElt.tag == 'xml':
      raise RuntimeError('bkyToSummary: Root of bky file is not xml but ' + rootElt.tag 
                         + " in project " + currentProjectPath)
  else:
      # [lyn, 2017/03/27] modified the following from collecting lists of dicionaries and the postprocessing them
      # to instead mutate result dictionaries

      activeBlocksDict = makeAllBlockSummaryDict()
      orphanBlocksDict = makeAllBlockSummaryDict()

      # topSummaryDict maps the name of each top block to the list of blocks it contains
      # This allows the summarizer to know what blocks are in the stack for each top block. 
      topSummaryDict = {}
      # orphanSummaryDict maps the name of the root of each orphan block to info on the stack rooted there.
      orphanSummaryDict = {}
      top  = []

      #if len(rootElt) < 1:
      #    return {'Active Blocks': {}, 'Orphan Blocks': {}}
      for child in rootElt: 
          if child.tag == 'block': # block children of root are top blocks
              generalType = child.attrib['type']
              specificType = blockType(child) # [2015/11/11, lyn] Specially handle component_event, component_method, component_set_get
                                              # E.g., for generalType component_event, might have Button.Click;
                                              #       for generalType component_method, might have Canvas.DrawCircle
                                              #       for generalType component_set_get, might have Button.GetText or Button.SetText
                                              # Now also handles "old style" types. E.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
              if specificType == '*IGNORE*': # Special string meaning something's malformed about block
                  continue # ignore this block and try next one
              blkName = blockName(child) # [2017/03/27] Used as key on topBlockDict
              # [2016/08/07, Maja] add topSummary check if we need to append top or not
              # appending subblocks to list instead of adding them enables us recognize the first element as top block
              if isDeclarationType(generalType, specificType): # declaration = top-level/root block 
                  if not topSummary: # moved inside isDeclarationType statement [Maja, 2016/11/13]
                    top.append(specificType) 
                  topBlockDict = makeRootBlockSummaryDict()
                  topSummaryDict[blkName] = topBlockDict
                  addBlockInfo(child, makeEmptyEnv(), activeBlocksDict, topBlockDict)
              else:
                  orphanBlockDict = makeRootBlockSummaryDict()
                  orphanSummaryDict[blkName] = orphanBlockDict
                  addBlockInfo(child, makeEmptyEnv(), orphanBlocksDict, orphanBlockDict)
      # blocks = processRawBlockList(listOfBlocks)
      # orphans = processRawBlockList(listOfOrphans)
    # [2016/08/07, Maja] Return formatting suitable for findClosest running on toplevelsummaries.
      if topSummary:
          logwrite("***WARNING***; topSummary not working after 2017/03/26 overhaul")
          return {'Active Blocks': activeBlocksDict, 'Orphan Blocks': orphanBlocksDict}
      else:
          return {'*Top Level Blocks': sortListToDict(top), 
                  'Active Blocks': activeBlocksDict, 
                  'Orphan Blocks': orphanBlocksDict,
                  'Active Details': topSummaryDict,
                  'Orphan Details': orphanSummaryDict}

declarationTypes = ['component_event', 'global_declaration', 'procedures_defnoreturn', 'procedures_defreturn']

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
    elif generalType in blockTypeDict: # e.g, math_add, lists_append_lists,  procedures_callnoreturn,  procedures_callreturn
        return False
    # If get here, generalType must be "old-style" type like 'DrawingCanvas_Clicked' 
    # and specificType must be upgraded type, like 'Canvas.Clicked'
    elif specificType in AI1_v134a_component_specs: # handles old-style component_event and component_method
        return AI1_v134a_component_specs[specificType]['type'] == 'component_event'
    else: 
        return False # Handles old-style component getters and setters. E.g. 'StartButton_GetText'
                     # as well as generic methods, E.g. Canvas.DrawCircleGeneric

# [lyn, 2017/03/17] Combine the actions of findBlockInfo and processRawBlockList into a single
# function that adds relevant info to given dictionaries. 
# Environment argument allows tracking name scoping details that were untracked before. 
# [lyn,  2017/06/22] Fixed major bug where wasn't traversing:
#   * arg or next of variable setter
#   * nexts of loops or local decl statements
# [audrey, 2018/06/29] Added capability for handling disabled blocks, which also meant
# adding a new parameter, isDisabled with a default value of false, because only the block
# the user right-clicks on and marks "disable" is labeled as disabled.
def addBlockInfo(xmlBlock, env, allSummaryDict, rootSummaryDict, isDisabled=False):
    blkType = blockType(xmlBlock) # [lyn, 2015/11/11] Specially handle component_event, component_method, component_set_get 
                                  # [Maja, 2015/11/15] passing down zippedFile and bkyFileName to be able to handle old formatting
    if blkType == '*IGNORE*': # Special string meaning something's malformed about block
        return 
    blkName = blockName(xmlBlock)

    # [audrey, 2018/06/29] check if the block is disabled, and set isDisabled accordingly
    if not isDisabled:
        if "disabled" in xmlBlock.attrib:
            if xmlBlock.attrib["disabled"] == "true":
                #logwrite("{0} of block type {1} is disabled".format(blkName, blkType))
                isDisabled = True
    #else:
    #    logwrite("{0} of block type {1} is within a disabled block".format(blkName, blkType))
    #***debugging: print "addBlockInfo", blkType, blkName
    # Debugging
    # print('addBlocksInfo for type {} and name {} in env {}'.format(blkType, blkName,env))
    
    # First do generic updates to both summary dicts
    # [audrey, 2018/06/29] also handles updates for new values in summary dicts
    #   such as "*Number of Active Blocks", "*Number of Disabled Blocks",
    #   "*Number of Disabled Block Types", "*Number of Active Block Types",
    #   and "Disabled Types".
    for dict in [allSummaryDict, rootSummaryDict]:
        dict['*Number of Blocks'] += 1
        if isDisabled:
            dict['*Number of Disabled Blocks'] += 1
        else:
            dict['*Number of Active Blocks'] += 1

        typesDict = dict['Types']
        disabledTypesDict = dict['Disabled Types']
        if isDisabled:
            if blkType in disabledTypesDict:
                disabledTypesDict[blkType] += 1
            else:
                disabledTypesDict[blkType] = 1
                dict['*Number of Disabled Block Types'] += 1
        
        if blkType in typesDict:
            typesDict[blkType] += 1
        else:
            typesDict[blkType] = 1
            dict['*Number of Block Types'] += 1
            if not isDisabled:
                dict['*Number of Active Block Types'] += 1

    # Now handle top blocks specially 
    if isComponentEvent(xmlBlock):
        params = eventParams(blkType)
        addEventDecl(params, blkName, allSummaryDict)
        eventEnv = envExtend(env, params, blkName, 'component_event') # blkType is something like 'Canvas.Flung'
        for child in childBlocks(xmlBlock): # only body block
            addBlockInfo(child, eventEnv, allSummaryDict, rootSummaryDict, isDisabled)
    
    elif blkType  == 'global_declaration':
        globalName = globalDeclName(xmlBlock)
        addGlobalDecl(globalName, allSummaryDict)
        for child in childBlocks(xmlBlock): # defn block and next block
            addBlockInfo(child, env, allSummaryDict, rootSummaryDict, isDisabled)

    elif blkType == 'procedures_defnoreturn' or blkType == 'procedures_defreturn':
        procName, procParams = procDeclNameAndParams(xmlBlock)
        addProcDecl(procName, procParams, blkName, blkType, allSummaryDict)
        procEnv = envExtend(env, procParams, procName, blkType)
        for child in childBlocks(xmlBlock): # only body block
            addBlockInfo(child, procEnv, allSummaryDict, rootSummaryDict, isDisabled)

    # Now handle certain nontop blocks specially:
    elif blkType == 'text':
        addString(textString(xmlBlock), allSummaryDict)
        # This is a leaf, so has no subblocks

    elif blkType == 'lexical_variable_get' or  blkType == 'lexical_variable_set':
        lexName = lexicalVariableName(xmlBlock)
        if lexName.startswith('input '): # Only in "old-style" projects
            lexName = lexName[len('input '):] # Strip initial 'input '
        elif lexName.startswith('global '):
            baseName = lexName[len('global '):] # Strip initial 'global '
            addNameRef(baseName, blkType, 'ignore', 'global_declaration', allSummaryDict)
        elif lexName in env: 
            declName = env[lexName]['declName']
            declType = env[lexName]['declType']
            addNameRef(lexName, blkType, declName, declType, allSummaryDict)
        else: 
            addNameRef(lexName, blkType, 'ignore', 'unbound', allSummaryDict)
        if blkType == 'lexical_variable_set':
            for child in childBlocks(xmlBlock): # argument block and next block
                addBlockInfo(child, env, allSummaryDict, rootSummaryDict, isDisabled)

    elif blkType == 'procedures_callnoreturn' or blkType == 'procedures_callreturn':
        procName = procCallName(xmlBlock)
        addProcCall(procName, allSummaryDict, isDisabled) # [audrey, 2018/06/29] make it so that disabled proc calls aren't counted as the same thing as a regular proc call
        for child in childBlocks(xmlBlock): # argument blocks and next block
            addBlockInfo(child, env, allSummaryDict, rootSummaryDict, isDisabled)

    elif blkType == 'controls_forEach' or blkType == 'controls_forRange':
        loopVar,loopExps,loopBody,loopNexts = parseLoop(xmlBlock)
        addLoopDecl(loopVar, blkName, allSummaryDict)        
        loopEnv = envExtend(env, [loopVar], blkName, blkType)
        for exp in loopExps:
            addBlockInfo(exp, env, allSummaryDict, rootSummaryDict, isDisabled) # Use env here, not loopEnv, since outside loop scope
        if loopBody != None:
            addBlockInfo(loopBody, loopEnv, allSummaryDict, rootSummaryDict, isDisabled) # Use loopEnv here, since inside loop scope
        for next in loopNexts: #should be at most one
            addBlockInfo(next, env, allSummaryDict, rootSummaryDict, isDisabled) # Use env here, not loopEnv, since outside loop scope

    elif blkType == 'local_declaration_statement' or blkType == 'local_declaration_expression':
        localNames,localDefns,localBody,localNexts = parseLocalDecl(xmlBlock)
        addLocalDecls(localNames, blkName, allSummaryDict)
        localEnv = envExtend(env, localNames, blkName, blkType)
        for defn in localDefns:
            addBlockInfo(defn, env, allSummaryDict, rootSummaryDict, isDisabled) # Use env here, not localEnv, since outside local scope
        if localBody != None:
            addBlockInfo(localBody, localEnv, allSummaryDict, rootSummaryDict, isDisabled) # Use locanEnv here, since inside local scope
        for next in localNexts: #should be at most one
            addBlockInfo(next, env, allSummaryDict, rootSummaryDict, isDisabled) # Use env here, not localEnv, since outside local scope

    # Now handle all other blocks: descend into subblocks
    else: 
        for child in childBlocks(xmlBlock):
            addBlockInfo(child, env, allSummaryDict, rootSummaryDict, isDisabled)

def childBlocks(xmlBlock):
    '''Return a list of all child blocks of given block'''
    children = [] 
    for child in xmlBlock:
        for grandchild in child:
            if grandchild.tag == 'block':
                children.append(grandchild) # The "grandchildren" are the actual child blocks 
    return children

def eventParams(blkType):
    if blkType in AI2_component_specs_nb155:
        return AI2_component_specs_nb155[blkType]['paramNames']
    else: 
        logwrite('***eventParams not found for event {} in {}'.format(blkType, currentProjectPath))
        return [] 

def procDeclNameAndParams(xmlBlock): 
    '''Assume xmlProcDeclBlock has type procedures_defnoreturn or procedures_defreturn 

      Example: 

      <block type="procedures_defreturn" id="158" inline="false" x="425" y="788">
        <mutation>
          <arg name="lat1"></arg>
          <arg name="long1"></arg>
          <arg name="lat2"></arg>
          <arg name="long2"></arg>
        </mutation>
        <field name="NAME">distanceBetweenLatitudesLongitudesInMiles</field>
        <field name="VAR0">lat1</field>
        <field name="VAR1">long1</field>
        <field name="VAR2">lat2</field>
        <field name="VAR3">long2</field>

    '''
    name = "*UnknownProcedureName*"
    params = []
    for child in xmlBlock:
        if child.tag == 'mutation':
            for param in child:
                if param.tag == 'arg' and param not in params:
                    params.append(param.attrib['name'])
        elif child.tag == 'title' or child.tag == 'field':
            if child.attrib['name'] == "NAME":
                name = child.text
            elif child.attrib['name'].startswith("VAR"):
                # Have this in case for some reason not handled by mutation
                param = child.text
                if param not in params:
                    params.append(param)
    return (name, params)

def procCallName(xmlBlock):
    '''Return procedure name for blocks with type procedures_callnoreturn, procedures_callreturn '''
    for child in xmlBlock:
        if child.tag == 'mutation':
            return child.attrib['name']
        elif (child.tag == 'title' or child.tag == 'field') and child.attrib['name'] == 'PROCNAME':
            return child.text
    # Get here if fail to find name otherwise
    logwrite('***procCallName returns *UnknownProcCallName* for {} in {}'.format(xmlBlock, currentProjectPath))
    return '*UnknownProcCallName*'
             
def globalDeclName(xmlBlock):
    '''Return procedure name for blocks with type global_declaration '''
    for child in xmlBlock:
        if (child.tag == 'title' or child.tag == 'field') and child.attrib['name'] == 'NAME':
            return child.text
    # Get here if fail to find name otherwise
    logwrite('***globalDeclName returns *UnknownGlobalVarName* for {} in {}'.format(xmlBlock, currentProjectPath))
    return '*UnknownGlobalVarName*'

def parseLocalDecl(xmlBlock):
    '''Return names, defn, and body of block with type local_declaration_statement or local_declaration_expression'''
    names = [] 
    defns = [] 
    body = None
    nexts = []
    for child in xmlBlock:
        if child.tag == 'mutation':
            for localName in child:
                if localName.tag == 'localname':
                    names.append(localName.attrib['name'])
        elif child.tag == 'value' and child.attrib['name'].startswith('DECL'):
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    defns.append(grandchild)
        elif child.tag == 'value' and child.attrib['name'] == 'RETURN':
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    body = grandchild
        elif child.tag == 'statement' and child.attrib['name'] == 'STACK':
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    body = grandchild
        elif child.tag == 'next':
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    nexts.append(grandchild)
    if len(nexts) > 1:
        logwrite('***parseLocalDecl has len(nexts) > 1 for {} in {}'.format(xmlBlock, currentProjectPath))
    return (names, defns, body, nexts)
             
def parseLoop(xmlBlock):
    '''Return names, defns, body, and nexts (list of 0 or 1 elt) of block with type local_declaration_statement or local_declaration_expression'''
    var = None
    exps = [] 
    body = None
    nexts = [] 
    for child in xmlBlock:
        if (child.tag == 'title' or child.tag == 'field') and child.attrib['name'] == 'VAR':
            var = child.text
        elif child.tag == 'value':
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    exps.append(grandchild)
        elif child.tag == 'statement' and child.attrib['name'] == 'DO':
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    body = grandchild
        elif child.tag == 'next':
            for grandchild in child: # There should only be one
                if grandchild.tag == 'block':
                    nexts.append(grandchild)
    if var == None:
        logwrite('***parseLoop has None for var for {} in {}'.format(xmlBlock, currentProjectPath))
    elif len(nexts) > 1:
        logwrite('***parseLoop has len(nexts) > 1 for {} in {}'.format(xmlBlock, currentProjectPath))
    return (var, exps, body, nexts)

def lexicalVariableName(xmlBlock):
    '''Returns var name for lexical_variable_get or lexical_variable_set'''
    for child in xmlBlock:
        if (child.tag == 'title' or child.tag == 'field') and child.attrib['name'] == 'VAR':    
            return child.text
    logwrite('***lexicalVariableName returns None for var for {} in {}'.format(xmlBlock, currentProjectPath))

def textString(xmlBlock):
    '''Return string contents for blocks with type text'''
    for child in xmlBlock:
        if (child.tag == 'title' or child.tag == 'field') and child.attrib['name'] == 'TEXT':
            return child.text
    logwrite('***textToString returns None for var for {} in {}'.format(xmlBlock, currentProjectPath))

# END 2017/03/27-28 CODE
# **********************************************************************

""" NO LONGER USED AFTER 2017/03/27 CHANGES
#[2016-08-07] Added by Maja to append each block to its top level parent 
                # when "topSummary" is true
#[2016-08-07, Maja] rename for clarity
def processRawBlockList(inputList):
      blockDict = {}
      blockDict['Types'] = []
      blockDict['Procedure Names'] = []
      blockDict['Procedure Parameter Names'] = []
      blockDict['Global Variable Names'] = []
      blockDict['Local Variable Names'] = []
      blockDict['Strings'] = []
      blockDict['*Number of Blocks'] = 0 # [2016/08/07, Maja] number of blocks will not correspond to
                                        # length of input list since input list is nested
      #[2016-08-07] conditional added by Maja to append each block to its top level parent 
                # when "topSummary" is true, and do it the non-top level way if not
      for lyst in inputList:
        if topSummary:
            topBlockType = lyst[0]['Type']
            blockDict['Types'].append(topBlockType)
            blockDict['*Number of Blocks'] += 1
            for elt in lyst[1:]: # add all other blocks concatenated with topblock
                blockDict['Types'].append(topBlockType + '/' + elt['Type'])
                blockDict['*Number of Blocks'] += 1
            for dyct in lyst:
                for key in dyct:
                    if key != 'Type':
                        blockDict[key].extend(dyct[key]) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
        else:
            for dyct in lyst:
                blockDict['*Number of Blocks'] += 1
                for key in dyct:
                    if key == 'Type':
                        blockDict['Types'].append(dyct[key])
                    else:
                        blockDict[key].extend(dyct[key]) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
      for key in blockDict:
          if key != '*Number of Blocks':
              blockDict[key] = sortListToDict(blockDict[key])
      blockDict['*Number of Block Types'] = len(blockDict['Types']) # [2016/08/06, lyn] Add number of block types
      return blockDict
"""

#[2016-08-07, Maja] rename for clarity
def sortListToDict(list):
    '''Give a list of strings, return a dictionary of histogram for strings'''
    output = {}
    for elt in list:
        if elt not in output: # Lyn sez: no need to use output.keys():
            output[elt] = 1
        else:
            output[elt] += 1
    return output

""" NO LONGER USED AFTER 2017/03/27 CHANGES
# [2016/08/06] Fixed bug in handling of categorizing var getters/setters as global or local
def findBlockInfo(xmlBlock):
    '''Returns a list of dictionaries for blocks rooted at given block'''
    blockDict = {}
    tipe = blockType(xmlBlock) # [lyn, 2015/11/11] Specially handle component_event, component_method, component_set_get 
                               # [Maja, 2015/11/15] passing down zippedFile and bkyFileName to be able to handle old formatting
    blockDict['Type'] = tipe
    blockDict['Procedure Names'] = []
    blockDict['Procedure Parameter Names'] = []
    blockDict['Global Variable Names'] = []
    blockDict['Local Variable Names'] = []
    blockDict['Strings'] = []
    if tipe  == 'procedures_defnoreturn' or tipe == 'procedures_defreturn' or tipe == 'procedures_callnoreturn' or tipe == 'procedures_callreturn':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                blockDict['Procedure Names'] = [child.text]
            for param in child:
                if param.tag == 'arg':
                    blockDict['Procedure Parameter Names'].append(param.attrib['name'])
    if tipe  == 'global_declaration':
        for child in xmlBlock:
            if child.tag == 'field' or child.tag == 'title':
                blockDict['Global Variable Names'].append(child.text)
    if tipe == 'local_declaration_statement' or tipe == 'local_declaration_expression':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                blockDict['Local Variable Names'].append(child.text)
    # [2016/08/06] Fix bug in handling of categorizing var getters/setters as global or local
    if tipe == 'lexical_variable_get' or  tipe == 'lexical_variable_set':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                if child.text.startswith('global '):
                    blockDict['Global Variable Names'].append(child.text[len('global '):]) # Strip initial "global"
                elif child.text.startswith('input '): # Only in "old-style" projects
                    blockDict['Local Variable Names'].append(child.text[len('input '):]) # Strip initial "global"
                else: 
                    blockDict['Local Variable Names'].append(child.text)        
    if tipe == 'text':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                blockDict['Strings'].append(child.text)
    resultListOfDicts = [blockDict] # [2017/03/27, lyn] More efficient to create this list first and extend it, 
                                    # rather than say [blockDict] + subblocks later. 
    for child in xmlBlock:
        for grandchild in child:
            if grandchild.tag == 'block':
                resultListOfDicts.extend(findBlockInfo(grandchild)) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
    return resultListOfDicts
"""

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
    return componentTypeToBlockType(xmlBlock, xmlBlock.attrib['type'])

# [2018/06/21, audrey] Added to standardize a lot of the logs and generally make code cleaner.
def warningIgnoringMalformedBlock(callingFunctionName, hasMutation, tipe, xmlBlock):
    logwrite('*WARNING*: {} is ignoring malformed block{} with type {} in screen {} of project {} (block info: {})'.format(callingFunctionName, "" if hasMutation else " (no mutation)", tipe, currentScreenName, currentProjectPath, getBlockInfo(xmlBlock)))

# [2017/03/29, lyn] Factored out this helper function to call it recursively for mangled types
def componentTypeToBlockType(xmlBlock, tipe):
    # Debugging:
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
        return tipe

def getBlockInfo(xmlBlock):
    '''return a dict string of id, x, y (if available)'''
    attribs = xmlBlock.attrib
    return {'id': attribs.get('id', 'NO id'), 
            'x': attribs.get('x', 'NO x'), 
            'y': attribs.get('y', 'NO y')}



def formToScreen(comp):
    '''Change all occurrences of component Form to Screen'''
    if comp == 'Form':
        return 'Screen'
    else:
        return comp

def isComponentEvent(xmlBlock):    
    return xmlBlock.attrib['type'] == 'component_event'

# [Maja, 2015/11/15] Create
# [2016/08/06, lyn] Modified to handle generic types
# [2017/03/29, lyn] Modified to handle nonworking cases
def upgradeTypeFormat(tipe):
    action = tipe.split('_')[-1]
    compName = '_'.join(tipe.split('_')[:-1]) # Fixed by lyn
    compType = findComponentType(compName)
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

# [2017/03/26, lyn] Added
def blockName(xmlBlock):    
    ''' [2017/03/26, lyn] Return a unique name (assuming no dup errors) for the block from within the current screen.
        * Component event handler: e.g. Canvas$Canvas1.Flung#158
        * Component method: e.g. File$File1.ReadFrom#2
        * Component getter: e.g. Spinner$Spinner1.getElements#27
        * Component setter: e.g. Spinner$Spinner1.setElements#28
        * procedures_defreturn (noreturn similar): to_distanceBetweenLatitudesLongitudesInMiles#46
        * global_declaration: global_EarthRadiusInMiles#104
        * other block: math_number#102
        Note we include the blockID just in case there are (in error) duplicates of the same block,
        so they can be distinguished in a summary'''
    return componentTypeToBlockName(xmlBlock, xmlBlock.attrib['type'])

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
def upgradeNameFormat(tipe):
    action = tipe.split('_')[-1]
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

# [2017/03/29, lyn] Modified to handle nonworking cases
def findComponentType(compName): 
    if currentComponentDictionary == {}: 
        populateCurrentComponentDictionary() # Populate dictionary if not already populated. 
    if compName in currentComponentDictionary:
        return currentComponentDictionary[compName] # Return answer from populated dictionary.
    elif compName in AI2_component_names:
        return compName
    else:
        logwrite("*NOTE*: findComponentType is unable to find component name {} in screen {} of old-style project {}".format(compName, currentScreenName, currentProjectPath))
        return None

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


# ----------------------------------------------------------------------
# Changes by lyn



logStartTime = 0 
logPrefix = 'ai2summarizer2Lyn'
printMessagesToConsole = True

def createLogFile():
    global logFileName
    global logStartTime
    if not os.path.exists("logs"):
        os.mkdir("logs")
    logStartTime = datetime.datetime.now()
    startTimeString = logStartTime.strftime("%Y-%m-%d-%H-%M-%S")    
    logFileName = "logs/" + logPrefix + '-' + startTimeString

def logwrite (msg): 
    with open (logFileName, 'a') as logFile:
        # [2018/07/12, audrey] add conversion of logStartTime to a datetime.timedelta bc
        # otherwise python actually complains
        timeElapsed = datetime.datetime.now() - datetime.timedelta(milliseconds=logStartTime)
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

topSummary = False # Lyn sez: NEVER NECESSARY TO SET THIS TRUE IN NEW SUMMARIZER
                   # Because each summary also implicitly contains top information 

def processTutorials():
    allProjectsToJSONFiles(tutorialsInputDir, None, tutorialsOutputDir)

if __name__=='__main__':  
    
    
    logFileName = '*unopenedFilename*'

    # *** Added by Maja [2016-08-07]
    # topSummary = True # Global variable as flag for which kind of summary we are trying to produce
    createLogFile()

    # allProjectsToJSONFiles('TutorialsMore', None, 'TutorialsMoreSummaries/tutorial_summaries_nontop')
    # allProjectsToJSONFiles('cs117-fall15-global-tutorials')
    # allProjectsToJSONFiles('cs117-fall15-local-tutorials')
    # allProjectsToJSONFiles('cs117-fall15-local-tutorials-extra')
    # allProjectsToJSONFiles('cs117-fall15-local-tutorials-extra-more')

    if len(sys.argv) != 3: 
        print "Usage: python ai2summarizer2.py <inputDir> <outputDir>"
    else:
        allProjectsToJSONFiles(sys.argv[1], outputDir=sys.argv[2])

    '''
    # 2017/0328 tests

    allProjectsToJSONFiles('../../data/ai2_users_long_term_randomized/03/03433', 
                              outputDir='../../data/ai2_users_long_term_randomized_summary2_03433')
    
    allProjectsToJSONFiles('../../data/ai2_users_long_term_randomized', 
                            outputDir='../../data/ai2_users_long_term_randomized_summary2s')

    allProjectsToJSONFiles('../../data/ai2_users_long_term_randomized/00', 
                           outputDir='../../data/ai2_users_long_term_randomized_summary2s_00')

    allProjectsToJSONFiles('../../data/benji_ai2_users_random', 
                           outputDir='../../data/benji_ai2_users_random_summary2s')
    allProjectsToJSONFiles('../../data/benji_ai2_users_random', 
                           outputDir='../../data/benji_ai2_users_random_summary2s')
    '''



'''        
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

# Audrey trying to figure out things
#cleanup("/Users/audrey/Personal/School/College/Work/summer2018/ai2_tutorialfinder/outputs", "*.json")

# only runs the summarizer on my personal projects
#userToJSONFiles("myprojects", "/Users/audrey/Personal/School/College/Work/summer2018/ai2_tutorialfinder", "myoutputs")

# 10k users, 30,984 projects, takes about 6 minutes to execute
#allProjectsToJSONFiles('/Users/audrey/Downloads/ai2_10k_random_users_deidentified_aias', "outputs")

# 46k users, 1,546,283 projects, around 2 and a half hours to execute
#allProjectsToJSONFiles('/Users/audrey/Downloads/ai2_46K_prolific_users_deidentified_aias', "prolific_outputs")

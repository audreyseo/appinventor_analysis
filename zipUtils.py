"""
zipping/unzipping utilities

[lyn, 2018/07/27] Created 
"""

import os.path
import zipfile

def zipDir(dirPath, zipPath):
    """
    Given path to directory (dirPath) and path to resulting zipped file 
    (zipPath), create compressed zip file at zipPath whose archived filenames 
    are relative to dirPath (i.e., they do *not* include dirPath as a prefix). 
    This detail is important when unzipping the zipped directory, because it 
    means that directories in dirPath won't be created in the unzipped 
    directory.
    """
    zippedFile = zipfile.ZipFile(zipPath, "w")
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            fullFilePath = os.path.join(root, file)
            zippedFile.write(fullFilePath, 
                             # this 2nd arg is essential for relativizing
                             # archived path name to dirPath
                             os.path.relpath(fullFilePath, dirPath), 
                             zipfile.ZIP_DEFLATED # Need this for compression
                             )
    zippedFile.close()

def unzipDir(zipPath, dirPath): 
    """
    Given path to zipped file (zipPath) and path to desired directory (dirPath)
    create unzipped directory at dirPath. 
    """
    with zipfile.ZipFile(zipPath, 'r') as zippedFile:
        zippedFile.extractall(dirPath)

def zipDirs(dirPath, zippedDirsPath):
    """
    Given path to directory (dirPath) and a path to a directory of resulting 
    zipped files (zippedDirsPath), create zipped files in  zippedDirsPath for 
    each *top-level subdirectory* in the directory at dirPath. Also creates 
    directory for zippedDirsPath if it doesn't already exist. 

    This is helpful for zipping lots of directories, like the chunks in ai2 
    data. 
    """
    if not os.path.exists(zippedDirsPath):
        os.makedirs(zippedDirsPath)
    filesOrDirs = os.listdir(dirPath)
    for fileOrDir in filesOrDirs:
        fileOrDirPath = os.path.join(dirPath, fileOrDir)
        if os.path.isdir(fileOrDirPath):
            subDirZipPath = os.path.join(zippedDirsPath, fileOrDir + '.zip')
            print 'Zipping {} as {}'.format(fileOrDirPath, subDirZipPath)
            zipDir(fileOrDirPath, subDirZipPath)
    
def withUnzippedFiles(zipPath, fcn):
    """
    Given path to zipped file (zipPath) and a function fcn that takes two args
      (1) the name of an archived file
      (2) a file-like object for the contents of the archived file
    applies fcn to all the archived files in the zip archive. 
    This is useful for processing all the archived files without ever 
    unzipping all of them at once into an unzipped directory. 
    """
    with zipfile.ZipFile(zipPath, 'r') as zippedFile:
        archivedFileNames = zippedFile.namelist()
        for archivedFileName in archivedFileNames:
            with zippedFile.open(archivedFileName) as archivedFile:
                # archivedFile is file-like object
                # e.g., can use file methods like .read(), readlines() on it
                # and iterate over lines 
                fcn(archivedFileName, archivedFile)

'''
# Lyn's Testing

zipDir('../data/ai2_46K_prolific_users_deidentified_summary2s_test', 
       '../data/ai2_46K_prolific_users_deidentified_summary2s_test.zip')

unzipDir('../data/ai2_46K_prolific_users_deidentified_summary2s_test.zip', 
         '../data/ai2_46K_prolific_users_deidentified_summary2s_test_unzip)'

def printFile(name, file):
   print '-'*40
   print 'fileName:', name
   for line in file:
      print line, 

withUnzippedFiles('../data/ai2_46K_prolific_users_deidentified_summary2s_test.zip', printFile)
'''

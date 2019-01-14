''' findmissing.py
    Created by Audrey Seo on 2018/07/21

    Finds the .aia files that don't have corresponding jail files, given
    a location with project files and a location with jail files to compare.

    It also comprises a lot of useful stuff for file io.
'''

import os
import zipUtils as zu
import myutils as mu

def getDirectories(direct):
  tmp = os.listdir(direct)
  return [d for d in tmp if os.path.isdir(os.path.join(direct, d))]

def compareDirs(aiaDir, jailDir):
  ''' aiaDir:  an absolute path to the root directory of the project directories, i.e.
               the directory that contains the directories 00, 01, etc.
      jailDir: an absolute path to the root directory of the directories containing
               jail files, the same structure as in the aiaDir
  '''
  aiaDirectories = getDirectories(aiaDir)
  jailDirectories = getDirectories(jailDir)  

  onlyInAIA = []
  # This shouldn't happen, but I'd want to check it just in case
  onlyInJAIL = []

  for d in aiaDirectories:
    if d not in jailDirectories:
      onlyInAIA.append(d)
    elif os.path.isdir(os.path.join(aiaDir, d)) and os.path.isdir(os.path.join(jailDir, d)):
      tmp = compareDirs(os.path.join(aiaDir, d), os.path.join(jailDir, d))
      if len(tmp) > 0:
        onlyInAIA.extend(tmp)

  for d in jailDirectories:
    if d not in aiaDirectories:
      onlyInJAIL.append(d)

  if len(onlyInJAIL) > 0:
    print(','.join(onlyInJAIL))
  return onlyInAIA

def getFileNames(directory, relDir=None):
  currentDirectory = directory
  if relDir == None:
    relDir = ""
  else:
    currentDirectory = os.path.join(currentDirectory, relDir)
  files = os.listdir(currentDirectory)
  files = [f for f in files if f != ".DS_Store"]
  files = [f for f in files if (os.path.isfile(os.path.join(currentDirectory, f)) or f.endswith(".aia")) and not f.startswith(".") and f.find("#") == -1]
  if len(files) == 0:
    dirs = getDirectories(currentDirectory)
    if relDir != "":
      dirs = [os.path.join(relDir, d) for d in dirs]
    for d in dirs:
      files.extend(getFileNames(directory, d))
  elif relDir != "":
    files = [os.path.join(relDir, f) for f in files]

  return files

def stripExtension(files):
  return [os.path.splitext(f)[0] for f in files]

def compareFiles(aiaDir, jailDir):
  mu.logwrite("compareFiles:: beginning.")
  jailDirs = getDirectories(jailDir)
  mu.logwrite("compareFiles:: finished finding jail directory names.")
  aiaFiles = stripExtension(getFileNames(aiaDir))
  mu.logwrite("compareFiles:: finished finding aia files.")
  aiaFilesOnly = []
  jailFiles = []
  mu.logwrite("compareFiles:: about to begin.")
  if len(jailDirs) > 0:
    jailFiles = getFileNames(jailDir)
  else:
    mu.logwrite("compareFiles:: using zip directories for jail.")
    jailZips = os.listdir(jailDir)
    jailZips = [z for z in jailZips if z.endswith(".zip")]
    class Local:
      index = 0
      currentJail = ""
    def loopThroughJAILs(fileName, archiveName):
      usersDir = os.path.splitext(Local.currentJail)[0]
      jailName = os.path.join(usersDir, fileName)
      #jailName = os.path.splitext(jailName)[0]
      jailFiles.append(jailName)
      Local.index += 1
      if Local.index % 5000 == 0:
        mu.logwrite("loopThroughJAILs in compareFiles:: found " + str(Local.index) + " jail files.")
    for z in jailZips:
      Local.currentJail = z
      zu.withUnzippedFiles(os.path.join(jailDir, z), loopThroughJAILs)
  mu.logwrite("compareFiles:: finished finding jail file names.")
  jailFiles = stripExtension(jailFiles)
  mu.logwrite("compareFiles:: finished stripping jail extensions.")
  mu.logwrite("compareFiles:: #aias: " + str(len(aiaFiles)))
  mu.logwrite("compareFiles:: #jail: " + str(len(jailFiles)))
  index = 0
  for aia in aiaFiles:
    if aia not in jailFiles:
      aiaFilesOnly.append(aia)
    else:
      jailFiles.remove(aia)
    index += 1
    if index % 5000 == 0:
      mu.logwrite("compareFiles:: # of checked aias: " + str(index))
  return aiaFilesOnly


def iterateThroughAllJail(jailLocation, func, jailHolder):
  printMessagesEvery = 10000
  bigDirs = fm.getDirectories(jailLocation)

  if len(bigDirs) > 0:
    for big in bigDirs:
      littleDirs = getDirectories(os.path.join(jailLocation, big))
      for little in littleDirs:
        files = getFileNames(os.path.join(jailLocation, big, little))
        for f in files:
          func(bigdir, littledir, f, jailHolder)
  else:
    mu.logwrite("findmissing.py::iterateThroughAllJAil: No big directories found!")

if __name__=='__main__':
  mu.logFileName = "*whatever*"
  mu.createLogFile()
  aia10k = "/Users/audrey/Downloads/ai2_10k_random_users_deidentified_aias"
  jail10k = "/Users/audrey/Personal/School/College/Work/summer2018/jailconversion/10kjails"

  '''onlyaia = compareDirs(aia10k, jail10k)
  for d in onlyaia:
    print d
  
  print(len(onlyaia))'''

  only = compareFiles(aia10k, jail10k)

  for f in only:
    mu.logwrite(f)

  mu.logwrite("main:: # of files missing: " + str(len(only)))

  aia46k = "/Users/audrey/Downloads/ai2_46k_prolific_users_deidentified_aias"
  jail46kzipped = "/Users/audrey/Personal/School/College/Work/summer2018/jailconversion/46kjailzips"
  
  only46k = compareFiles(aia46k, jail46kzipped)

  mu.logwrite("main:: # of 46k files missing: " + str(len(only46k)))

  with open("46kaiamissings.txt", "w") as f:
    f.write("\n".join(only46k))

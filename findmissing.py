''' findmissing.py
    Created by Audrey Seo on 2018/07/21

    Finds the .aia files that don't have corresponding jail files, given
    a location with project files and a location with jail files to compare.
'''

import os


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
  files = [f for f in files if os.path.isfile(os.path.join(currentDirectory, f)) or f.endswith(".aia")]
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
  aiaFiles = stripExtension(getFileNames(aiaDir))
  jailFiles = stripExtension(getFileNames(jailDir))
  print len(aiaFiles)
  print len(jailFiles)
  aiaFilesOnly = []

  for aia in aiaFiles:
    if aia not in jailFiles:
      aiaFilesOnly.append(aia)

  return aiaFilesOnly
  

aia10k = "/Users/audrey/Downloads/ai2_10k_random_users_deidentified_aias"
jail10k = "/Users/audrey/Personal/School/College/Work/summer2018/jailconversion/10kjails"

onlyaia = compareDirs(aia10k, jail10k)



#for d in onlyaia:
#  print d

#print(len(onlyaia))

only = compareFiles(aia10k, jail10k)

for f in only:
  print f

print len(only)

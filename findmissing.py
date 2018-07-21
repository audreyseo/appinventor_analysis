''' findmissing.py
    Created by Audrey Seo on 2018/07/21

    Finds the .aia files that don't have corresponding jail files, given
    a location with project files and a location with jail files to compare.
'''

import os


def compareDirs(aiaDir, jailDir):
  ''' aiaDir:  an absolute path to the root directory of the project directories, i.e.
               the directory that contains the directories 00, 01, etc.
      jailDir: an absolute path to the root directory of the directories containing
               jail files, the same structure as in the aiaDir
  '''
  aiaDirectories = os.listdir(aiaDir)
  jailDirectories = os.listdir(jailDir)

  aiaDirectories = [d for d in aiaDirectories if os.path.isdir(os.path.join(aiaDir, d))]
  jailDirectories = [d for d in jailDirectories if os.path.isdir(os.path.join(jailDir, d))]
  

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

aia10k = "/Users/audrey/Downloads/ai2_10k_random_users_deidentified_aias"
jail10k = "/Users/audrey/Personal/School/College/Work/summer2018/jailconversion/10kjails"

onlyaia = compareDirs(aia10k, jail10k)


for d in onlyaia:
  print d

print(len(onlyaia))

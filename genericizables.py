"""genericizables.py

   Looks for genericizable objects in jail code.
"""

import myutils as mus
import findmissing as fm
import zipUtils as zu
import equivalenceclasses as eqclasses


import os
import argparse

def jailToEquivs(jailLocation, start=None, stop=None):
  printMessagesEverySoOften = 10000
  bigDirs = fm.getDirectories(jailLocation)
  equivs = []
  jailStats = {}
  class MyNum:
    num = 0
  def unarchivedFiles(usersDir, userID, projName, jailHolder):
    jail = mus.getJail(os.path.join(jailLocation, usersDir, userID, projName))
    equivify(usersDir, userID, projName, jailHolder, jail)

  
  #def archivedFiles(fileName, fileArchive):
  #  jail = json.load(fileArchive)
  #  splits = fileName.split("/")
  #  equivify("", splits[0], splits[1], jail)
        
  def equivify(usersDir, userID, projName, jailHolder, jail):
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
    #                      screen names --> vvvvvvvvvvvvv
    equivs.append(eqclasses.ProjectSet(code, screenNames=onlyUsedNames, name=projName, programmer=userID))
    #                                              the user's id --> ^^^^^^^
    MyNum.num += 1
    if MyNum.num % printMessagesEverySoOften == 0:
      mus.logwrite("equivify() in jailToEquivs()::" + str(MyNum.num) + ": " + os.path.join(usersDir, userID, projName))
  fm.iterateThroughAllJail(jailLocation, unarchivedFiles, jailStats, backupFunction=equivify, start=start, stop=stop)
  return equivs


def findGenerizables(equivs):
  jailStats = {
    "equivs": [],
    "cols": ["projectName", "programmer", "screen", "sizeOfEquivalenceClass", "numBlocks", "name"],
    "totalCount": 0
  }
  for projectSet in equivs:
    for screen,ec in projectSet.getScreenEquivItems():
      if ec.isGenericifiable():
        jailStats["equivs"].append({
          "projectName": projectSet.projectName,
          "programmer": projectSet.programmerName,
          "screen": screen.screenName,
          "sizeOfEquivalenceClass": str(ec.size()),
          "numBlocks": str(ec.numBlocks()),
          "name": ec.getName()
        })
        jailStats["totalCount"] += 1
        if jailStats["totalCount"] % 1000 == 0:
          mus.logwrite("genericizables.py::findGenerizables: {}\t{}\t{}\t{}\t{}".format(jailStats["totalCount"], projectSet.projectName, projectSet.programmerName, screen.screenName, ec.getName()))
  #for projectSet in equivs:
  #  for screen,ec,blk in projectSet.getScreenEquivBlockItems():
  #    mus.logwrite("{}: {}: {}".format(screen.screenName, ec.getName(), mus.getName(blk)))
  return jailStats

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
  location = loc10k if args.kind == 10 else loc46k
  start = None if args.kind == 10 else (0 if args.start == -1 else args.start)
  stop = None if args.kind == 10 else (5 if args.end == -1 else args.end)

  print(start, stop)

  jailEquivs = jailToEquivs(location, start, stop)

  #print(jailEquivs)

  eq = findGenerizables(jailEquivs)

  print(len(eq["equivs"]))

  csvLocation = "genericizables10k.csv" if args.kind == 10 else "genericizables46k_{}_{}.csv".format(start, stop)

  with open(csvLocation, "w") as f:
    csvlines = "\n".join([",".join(map(lambda x: x.encode("utf-8"), [d[colTag] for colTag in eq["cols"]])) for d in eq["equivs"]])
    f.write(",".join(eq["cols"]) + "\n")
    f.write(csvlines)
    f.flush()

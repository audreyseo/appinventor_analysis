import json
import os
import copy
import datetime

import myutils as mus

import findmissing as fm

import zipUtils as zu

import argparse



def enumerateLoops(jailLocation, start=None, stop=None, printEvery=2000):
  jailStats = {
    "loopStats": [],
    "forLoopsByScreen": [],
    "loopsByProject": [],
    "loopsByProgrammer": [],
    "numLoopsByProj": -1,
    "numLoopsByProgrammer": -1,
    "totalCount": 0
  }

  #mus.logwrite("enumerateLoops: jailLocation: " + jailLocation)

  def processJail(usersDir, userID, projName, jailDict):
    jail = mus.getJail(os.path.join(jailLocation, usersDir, userID, projName))
    furtherProcess(usersDir, userID, projName, jailDict, jail)
    
  def furtherProcess(usersDir, userID, projName, jailDict, jail):
    screens = jail["*Names of Screens"]
    screenJail = jail["screens"]
    userIDKey = "userID"
    projNameKey = "projectName"
    blockNameKey = "blockName"
    #mus.logwrite("furtherProcess::{}, {}, {}".format(usersDir, userID, projName))
    furtherProcess.numForLoops = 0
    furtherProcess.numWhileLoops = 0

    # Hopefully by short-circuiting, the second part won't actually throw any errors
    if (len(jailDict["loopsByProgrammer"]) == 0) or (jailDict["loopsByProgrammer"][jailDict["numLoopsByProgrammer"]][userIDKey] != userID):
      jailDict["loopsByProgrammer"].append({
        userIDKey: userID,
        "numForLoops": 0,
        "numWhileLoops": 0
      })
      jailDict["numLoopsByProgrammer"] += 1

    jailDict["loopsByProject"].append({
      userIDKey: userID,
      projNameKey: projName,
      "numForLoops": 0,
      "numWhileLoops": 0
    })
    jailDict["numLoopsByProj"] += 1
    def enumerateLoop(blk):
      t = mus.getType(blk)
      if t != None:
        if t == "controls_forRange":
          furtherProcess.numForLoops += 1
        elif t == "controls_while":
          furtherProcess.numWhileLoops += 1
    
    for s in screens:
      if "bky" in screenJail[s]:
        jailDict["forLoopsByScreen"].append({
          "screen": s,
          userIDKey: userID,
          projNameKey: projName,
          "numForLoops": 0,
          "numWhileLoops": 0
        })
        num = len(jailDict["forLoopsByScreen"]) - 1
        if mus.isADictionary(screenJail[s]["bky"]):
          for block in screenJail[s]["bky"]["topBlocks"]:
            if not mus.isGlobalDeclaration(block):
              furtherProcess.numForLoops = 0
              furtherProcess.numWhileLoops = 0
              mus.countSomething(block, enumerateLoop)
              minidict = {
                userIDKey: userID,
                projNameKey: projName,
                blockNameKey: "\"{}\"".format(mus.getName(block)),
                "screen": s,
                "numForLoops": furtherProcess.numForLoops,
                "numWhileLoops": furtherProcess.numWhileLoops
              }

              #minidict[userIDKey] = userID
              #minidict[projNameKey] = projName
              #minidict[blockNameKey] = "\"{}\"".format(mus.getName(block))
              #minidict["screen"] = s
              
              #minidict["numForLoops"] = furtherProcess.numForLoops
              jailDict["forLoopsByScreen"][num]["numForLoops"] += furtherProcess.numForLoops
              jailDict["forLoopsByScreen"][num]["numWhileLoops"] += furtherProcess.numWhileLoops
              #minidict["numWhileLoops"] = furtherProcess.numWhileLoops
              jailDict["loopStats"].append(copy.deepcopy(minidict))
              jailDict["totalCount"] += 1

              if jailDict["totalCount"] % printEvery == 0:
                mus.logwrite("{}\t{}\t{}\t{}".format(jailDict["totalCount"], usersDir, userID, projName))
        jailDict["loopsByProject"][jailDict["numLoopsByProj"]]["numForLoops"] += jailDict["forLoopsByScreen"][num]["numForLoops"]
        jailDict["loopsByProject"][jailDict["numLoopsByProj"]]["numWhileLoops"] += jailDict["forLoopsByScreen"][num]["numWhileLoops"]
    jailDict["loopsByProgrammer"][jailDict["numLoopsByProgrammer"]]["numForLoops"] += jailDict["loopsByProject"][jailDict["numLoopsByProj"]]["numForLoops"]
    jailDict["loopsByProgrammer"][jailDict["numLoopsByProgrammer"]]["numWhileLoops"] += jailDict["loopsByProject"][jailDict["numLoopsByProj"]]["numWhileLoops"]
  # end of the function furtherProcess
  # back into the function enumerateLoops
  fm.iterateThroughAllJail(jailLocation, processJail, jailStats, backupFunction=furtherProcess, start=start, stop=stop)

  return jailStats

if __name__=='__main__':
  parser = argparse.ArgumentParser(description="Find numbers of loops")
  parser.add_argument("--kind", action="store", type=int, choices=[10, 46], default=10, help="Choose which dataset enumerate loops in, either 10 or 46. Defaults to 10.")

  parser.add_argument("-s", "--start", action="store", type=int, help="Which batch of users to start with (inclusive). Default under 10k dataset is None, default under 46k dateset is 0. Values range from 0-46 for 46k. Only applies to 46k dataset.")

  parser.add_argument("-e", "--end", action="store", type=int, help="Which batch of users to end with (exclusive). Default under 10k dataset is None, default under 46k dataset is 5. Values range from 0-47 for 46k. Only applies to 46k dataset.")

  parser.add_argument("--printEvery", action="store", type=int, default=2000, help="How often to print out to the console. Defaults to 2000 for 10k and 10,000 for 46k.")
  

  args = parser.parse_args()
  print(args)



  mus.createLogFile()
  loc10k = "10kjails"
  loc46k = "46kjailzips"

  location = loc10k if args.kind == 10 else loc46k
  start = args.start if args.kind == 10 else (0 if args.start == None else args.start)
  stop = args.end if args.kind == 10 else (5 if args.end == None else args.end)
  strKind = "10k" if args.kind == 10 else "46k"
  startStop = "" if args.kind == 10 else "_{}_{}".format(start, stop)
  printEvery = args.printEvery
  jails = enumerateLoops(location, start=start, stop=stop, printEvery=printEvery)

  numLoopsLocation = "num_loops{}{}.csv".format(strKind, startStop)

  forLoopsLocation = "for_loops_by_screen{}{}.csv".format(strKind, startStop)

  loopsByProjLoc = "loops_by_proj{}{}.csv".format(strKind, startStop)

  loopsByUserLoc = "loops_by_programmer{}{}.csv".format(strKind, startStop)
  
  mus.logwrite("# loops location: {}".format(numLoopsLocation))
  mus.logwrite("loops by screen location: {}".format(forLoopsLocation))
  mus.logwrite("loops by project location: {}".format(loopsByProjLoc))
  mus.logwrite("loops by programmer loc: {}".format(loopsByUserLoc))
  
  with open(numLoopsLocation, "w") as f:
    cols = ["userID", "projectName", "screen", "blockName", "numForLoops", "numWhileLoops"]
    csvlines = mus.makeCSVLines(cols, jails["loopStats"])
    f.write(",".join(cols) + "\n")
    f.write(csvlines)
    f.flush()

  
  with open(forLoopsLocation, "w") as f:
    cols = ["userID", "projectName", "screen", "numForLoops", "numWhileLoops"]
    csvlines = mus.makeCSVLines(cols, jails["forLoopsByScreen"])
    f.write(",".join(cols) + "\n")
    f.write(csvlines)
    f.flush()

  with open(loopsByProjLoc, "w") as f:
    cols = ["userID", "projectName", "numForLoops", "numWhileLoops"]
    csvlines = mus.makeCSVLines(cols, jails["loopsByProject"])
    f.write(",".join(cols) + "\n")
    f.write(csvlines)
    f.flush()
  with open(loopsByUserLoc, "w") as f:
    cols = ["userID", "numForLoops", "numWhileLoops"]
    csvlines = mus.makeCSVLines(cols, jails["loopsByProgrammer"])
    f.write(",".join(cols) + "\n")
    f.write(csvlines)
    f.flush()

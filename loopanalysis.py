''' loopanalysis.py
    Created on 2019/01/14 by Audrey Seo
    
    Parses jail files for handlers that possibly contain something that needs to be turned into a loop.
'''

import json
import os
import copy
import datetime

import myutils as mus

import findmissing as fm

import zipUtils as zu
import argparse


thisDirectory = os.path.dirname(os.path.realpath(__file__))
usersKey = "usersIDs"
def getType(block):
  typeKey = "*type"
  if typeKey in block:
    tipe = block[typeKey]
    if mus.isColorBlock(block):
      oldTipe = tipe
      tipe = mus.getActualColorType(block)
      #if oldTipe != tipe:
      #  mus.logwrite("loopanalysis::countKindsOfBlocks::getType: {} to {}".format(oldTipe, tipe))
    if mus.isComponentBlock(block):
      oldTipe = tipe
      tipe = mus.getComponentBlockType(block)
      #if oldTipe != tipe:
      #  mus.logwrite("loopanalysis::countKindsOfBlocks::getType: {} to {}".format(oldTipe, tipe))
    return tipe
  return "loopanalysis::getType: block does not have type!"

def strDepth(depth):
  if isinstance(depth, float):
    return "{:.1f}".format(depth)
  return str(depth)

def countKindsOfBlocks(block):
  # Returns a dictionary with various counts of different kinds of blocks
  # [2019/01/16] Modified to make it so that it returns the counts of
  # different kinds of blocks designated by depth
  numBlocks = mus.countBlocksInside(block)
  if numBlocks < 10:
    return {
      "note": "less than five blocks inside this block."
      }

  def kindCounter(blk, record):
    typeKey = "*type"
    if typeKey in blk:
      tipe = blk[typeKey]
      if mus.isColorBlock(blk):
        oldTipe = tipe
        tipe = mus.getActualColorType(blk)
        #if oldTipe != tipe:
        #  mus.logwrite("loopanalysis::countKindsOfBlocks::kindCounter: {} to {}".format(oldTipe, tipe))
      if tipe not in record:
        record[tipe] = 0
      record[tipe] += 1

  def kindCounterWithDepth(blk, record, depth):
    typeKey = "*type"
    if typeKey in blk:
      tipe = getType(blk)
      depthString = strDepth(depth)
      if depthString not in record:
        record[depthString] = {}
      if tipe not in record[depthString]:
        record[depthString][tipe] = 0
      record[depthString][tipe] += 1
        

  #recordsDictionary = {
  #  "numBlocks": numBlocks
  #}
  recordsDictionary = {}
  #mus.countAndRecord(block, kindCounter, recordsDictionary)
  # [2019/01/16] This should record the depths of things
  mus.countAndRecordWithDepth(block, kindCounterWithDepth, recordsDictionary)

  #mus.logwrite(mus.prettyPrint(recordsDictionary))

  return recordsDictionary

def removeEmptyScreens(jails):
  global usersKey
  users = jails[usersKey]
  usersToRemove = []

  for u in users:
    allScreensEmpty = True
    for proj in jails[u].keys():
      for screen in jails[u][proj]["counts by screens"].keys():
        if not jails[u][proj]["counts by screens"][screen]:
          jails[u][proj]["counts by screens"].pop(screen, None)
      allScreensEmpty = allScreensEmpty and not jails[u][proj]["counts by screens"]
      if not jails[u][proj]["counts by screens"]:
        jails[u][proj].pop("counts by screens", None)
        jails[u].pop(proj, None)
    if allScreensEmpty:
      jails.pop(u, None)
      usersToRemove.append(u)
      
  for u in usersToRemove:
    jails[usersKey].remove(u)
      
def getAverageRatio(mydict):
  itemsList = list(mydict.iteritems())
  ratios = []
  for i in range(len(itemsList) - 1):
    ratios.append(float(itemsList[i][1])/float(itemsList[i+1][1]))
  return sum(ratios) / float(len(ratios))
def combThroughJails(jailLocation, start=None, stop=None):
  jailStats = {
    "usersIDs": [],
    "totalCount": 0
  }

  def processJail(usersDir, userID, projName, jailHolder):
    # AKA the big directory, the little directory, and the file name.
    jail = mus.getJail(os.path.join(jailLocation, usersDir, userID, projName))
    furtherProcess(usersDir, userID, projName, jailHolder, jail)

  def furtherProcess(usersDir, userID, projName, jailHolder, jail):
    screens = jail["*Names of Screens"]
    if userID not in jailHolder:
      jailHolder[userID] = {}
      jailHolder["usersIDs"].append(userID)
    jailHolder[userID][projName] = {}
    jailHolder[userID][projName]["jail"] = jail
    screenJail = jail["screens"]
    blockLimit = 10
    for s in screens:
      jailHolder[userID][projName]["counts by screens"] = {}
      jailHolder[userID][projName]["num blocks by screens"] = {}
      jailHolder[userID][projName]["num greater than limit"] = {}
      jailHolder[userID][projName]["kinds greater than limit"] = {}
      jailHolder[userID][projName]["kinds ratio"] = {}
      if "bky" in screenJail[s]:
        if mus.isADictionary(screenJail[s]["bky"]):
          #jailHolder[userID][projName]["counts by screens"][s] = {}
          for block in screenJail[s]["bky"]["topBlocks"]:
            if not mus.isGlobalDeclaration(block):
              count = countKindsOfBlocks(block)
              if "note" not in count:
                greaterThanLimit = False
                # [2019/01/16] The version before adding depths
                #for key in count:
                #  greaterThanLimit = greaterThanLimit or count[key] >= 5

                #[2019/01/16] The version with depths in account
                numGreaterThanLimit = 0
                commonRepeatedBlocks = {}
                for depth in count:
                  #mus.logwrite(mus.prettyPrint(count[depth]))
                  if not depth.endswith(".5") and not depth.endswith(".0"): 
                    for key in count[depth]:
                      #print key, count[depth][key]
                      #bigEnough = count[depth][key] >= blockLimit
                      #oldGreaterThanLimit = greaterThanLimit
                      #greaterThanLimit = greaterThanLimit or (count[depth][key] >= blockLimit)
                      if (count[depth][key] >= blockLimit):
                        numGreaterThanLimit += 1
                        commonRepeatedBlocks[str(depth) + "." + key] = count[depth][key]
                      #if (not oldGreaterThanLimit) and greaterThanLimit:
                      #  mus.logwrite(mus.prettyPrint(count))
                if numGreaterThanLimit >= 2:
                  if s not in jailHolder[userID][projName]["counts by screens"]:
                    jailHolder[userID][projName]["counts by screens"][s] = {}
                    jailHolder[userID][projName]["num blocks by screens"][s] = {}
                    jailHolder[userID][projName]["num greater than limit"][s] = {}
                    jailHolder[userID][projName]["kinds greater than limit"][s] = {}
                    jailHolder[userID][projName]["kinds ratio"][s] = {}
                  jailHolder[userID][projName]["counts by screens"][s][mus.getName(block)] = count
                  jailHolder[userID][projName]["num blocks by screens"][s][mus.getName(block)] = mus.countBlocksInside(block)
                  jailHolder[userID][projName]["num greater than limit"][s][mus.getName(block)] = numGreaterThanLimit
                  jailHolder[userID][projName]["kinds greater than limit"][s][mus.getName(block)] = ";".join([(k + ":" + str(v)) for k,v in commonRepeatedBlocks.iteritems()])
                  jailHolder[userID][projName]["kinds ratio"][s][mus.getName(block)] = getAverageRatio(commonRepeatedBlocks)
                  
    
    jailHolder["totalCount"] += 1
    if jailHolder["totalCount"] % 1000 == 0:
      print jailHolder["totalCount"], usersDir, userID, projName
    
  fm.iterateThroughAllJail(jailLocation, processJail, jailStats, backupFunction=furtherProcess, start=start, stop=stop)
  removeEmptyScreens(jailStats)
  print "Number of users:", len(jailStats["usersIDs"])
  for i in range(min(len(jailStats["usersIDs"]), 5)):
    uid = jailStats["usersIDs"][i]
    for proj in jailStats[uid]:
      mus.logwrite(uid + " " + proj)
      mus.logwrite(mus.prettyPrint(jailStats[uid][proj]["counts by screens"]))
  jailList = []
  numProjs = 0
  allBlocks = 0
  numHandlers = 0
  for uid in jailStats["usersIDs"]:
    for proj in jailStats[uid]:
      numProjs += 1
      for screen in jailStats[uid][proj]["counts by screens"]:
        for handler in jailStats[uid][proj]["counts by screens"][screen]:
          numHandlers += 1
          numBlocks = jailStats[uid][proj]["num blocks by screens"][screen][handler]
          numGreater = jailStats[uid][proj]["num greater than limit"][screen][handler]
          kindsGreater = jailStats[uid][proj]["kinds greater than limit"][screen][handler]
          kindsRatio = jailStats[uid][proj]["kinds ratio"][screen][handler]
          allBlocks += numBlocks
          item = {}
          item["programmer"] = uid
          item["project"] = proj
          item["screen"] = screen
          item["handler"] = handler
          item["numBlocks"] = str(numBlocks)
          item["numGreater"] = str(numGreater)
          item["kindsGreater"] = kindsGreater
          item["kindsRatio"] = str(kindsRatio)
          jailList.append(item)
  mus.logwrite("numHandlers: " + str(numHandlers))
  mus.logwrite("avgBlocks: " + str(float(allBlocks) / float(numHandlers)))
  mus.logwrite("numProjects: " + str(numProjs))
  return jailList


if __name__=='__main__':
  parser = argparse.ArgumentParser(description="Run loop analysis")

  parser.add_argument("--kind", action="store", nargs=1, type=int, choices=[10, 46], default=10, help="Choose which dataset to run analysis on, either 10 or 46. Defaults to 10.")

  parser.add_argument("-s", "--start", action="store", nargs=1, type=int, default=0, help="Which batch of users to start from (inclusive). Defaults to 0, values range from 0-46 for 46k. Only applies to the 46k dataset.")

  parser.add_argument("-e", "--end", action="store", nargs=1, type=int, default=5, help="Which batch of users to end with (exclusive). Defaults to 5, values range from 0-47 for 46k. Only applies to the 46k dataset.")

  args = parser.parse_args()
  print(args)
  mus.createLogFile()
  loc10k = "10kjails"
  loc46k = "46kjailzips"
  location = loc10k if args.kind[0] == 10 else loc46k
  start = args.start if not isinstance(args.start, list) else args.start[0]
  stop = args.end if not isinstance(args.end, list) else args.end[0]

  print(start, stop)
  jails = combThroughJails(location, start=start, stop=stop)
  #jails = combThroughJails(loc10k)

  possibleLoopsLocation = "possible_loops.csv"
  if location == loc46k:
    if start != None and stop != None:
      possibleLoopsLocation = "possible_loops46k_{}_{}.csv".format(start, stop)
    else:
      possibleLoopsLocation = "possible_loops46k.csv"

  with open(possibleLoopsLocation, "w") as f:
    cols = ["programmer", "project", "screen", "handler", "numBlocks", "numGreater", "kindsGreater", "kindsRatio"]
    csvlines = mus.makeCSVLines(cols, jails)
    f.write(",".join(cols) + "\n")
    f.write(csvlines)
    f.flush()


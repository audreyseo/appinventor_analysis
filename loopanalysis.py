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
      

def combThroughJails(jailLocation):
  jailStats = {
    "usersIDs": [],
    "totalCount": 0
  }

  def processJail(usersDir, userID, projName, jailHolder):
    # AKA the big directory, the little directory, and the file name.
    jail = mus.getJail(os.path.join(jailLocation, usersDir, userID, projName))
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
                for depth in count:
                  #mus.logwrite(mus.prettyPrint(count[depth]))
                  if not depth.endswith(".5") and not depth.endswith(".0"): 
                    for key in count[depth]:
                      #print key, count[depth][key]
                      #bigEnough = count[depth][key] >= blockLimit
                      #oldGreaterThanLimit = greaterThanLimit
                      greaterThanLimit = greaterThanLimit or (count[depth][key] >= blockLimit)
                      #if (not oldGreaterThanLimit) and greaterThanLimit:
                      #  mus.logwrite(mus.prettyPrint(count))
                if greaterThanLimit:
                  if s not in jailHolder[userID][projName]["counts by screens"]:
                    jailHolder[userID][projName]["counts by screens"][s] = {}
                  jailHolder[userID][projName]["counts by screens"][s][mus.getName(block)] = count
    
    jailHolder["totalCount"] += 1
    if jailHolder["totalCount"] % 1000 == 0:
      print jailHolder["totalCount"], usersDir, userID, projName
    
  fm.iterateThroughAllJail(jailLocation, processJail, jailStats)
  removeEmptyScreens(jailStats)
  print "Number of users:", len(jailStats["usersIDs"])
  for i in range(min(len(jailStats["usersIDs"]), 5)):
    uid = jailStats["usersIDs"][i]
    for proj in jailStats[uid]:
      mus.logwrite(uid + " " + proj)
      mus.logwrite(mus.prettyPrint(jailStats[uid][proj]["counts by screens"]))



if __name__=='__main__':
  mus.createLogFile()
  loc10k = "10kjails"
  combThroughJails(loc10k)

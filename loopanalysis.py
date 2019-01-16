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

def countKindsOfBlocks(block):
  # Returns a dictionary with various counts of different kinds of blocks
  numBlocks = mus.countBlocksInside(block)
  if numBlocks < 5:
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
        if oldTipe != tipe:
          mus.logwrite("loopanalysis::countKindsOfBlocks::kindCounter: {} to {}".format(oldTipe, tipe))
      if tipe not in record:
        record[tipe] = 0
      record[tipe] += 1

  recordsDictionary = {}
  mus.countAndRecord(block, kindCounter, recordsDictionary)

  #print mus.prettyPrint(recordsDictionary)

  return recordsDictionary

def removeEmptyScreens(jails):
  users = jails[usersKey]

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
    for s in screens:
      jailHolder[userID][projName]["counts by screens"] = {}
      if "bky" in screenJail[s]:
        if mus.isADictionary(screenJail[s]["bky"]):
          jailHolder[userID][projName]["counts by screens"][s] = {}
          for block in screenJail[s]["bky"]["topBlocks"]:
            if not mus.isGlobalDeclaration(block):
              count = countKindsOfBlocks(block)
              if "note" not in count:
                greaterThanFive = False
                for key in count:
                  greaterThanFive = greaterThanFive or count[key] >= 5
                if greaterThanFive:
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

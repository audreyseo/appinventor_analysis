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


def countKindsOfBlocks(block):
  # Returns a dictionary with various counts of different kinds of blocks
  numBlocks = countBlocksInside(block)
  if numBlocks < 5:
    return {
      "note": "less than five blocks inside this block."
      }

  def kindCounter(blk, record):
    typeKey = "*type"
    if typeKey in blk:
      tipe = blk[typeKey]
      if tipe not in record:
        record[tipe] = 0
      record[tipe] += 1

  recordsDictionary = {}
  countAndRecord(block, kindCounter, recordsDictionary)

  print mus.prettyPrint(recordsDictionary)

  return recordsDictionary

def combThroughJails(jailLocation):
  jails = []

  def processJail(usersDir, userID, projName):
    # AKA the big directory, the little directory, and the file name.
    jail = mus.getJail(os.path.join(jailLocation, usersDir, userID, projName))

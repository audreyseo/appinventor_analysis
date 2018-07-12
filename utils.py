import os
import datetime

logFileName = '*unopenedFilename*'
printMessagesToConsole = True

def createLogFile(logPrefix):
    global logFileName
    if not os.path.exists("logs"):
        os.mkdir("logs")
    startTimeString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")    
    logFileName = "logs/" + logPrefix + '-' + startTimeString

def logwrite (msg): 
    with open (logFileName, 'a') as logFile: 
        if printMessagesToConsole:
            print(msg) 
        logFile.write(msg + "\n")

def padWithZeroes(num, digits):
  s = str(num)
  digitsToGo = digits - len(s)
  if digitsToGo > 0:
    return ('0' * digitsToGo) + s
  else: 
    return s

def exists(pred, seq):
  for elt in seq:
    if pred(elt):
      return True
  return False

def unzip(listOfLists):
  # See https://stackoverflow.com/questions/19339/transpose-unzip-function-inverse-of-zip
  # and https://stackoverflow.com/questions/12974474/how-to-unzip-a-list-of-tuples-into-individual-lists
  if listOfLists == []: 
    return ([], []) # Assume an empty list of pairs. Otherwise () will be returned
  else:
    return tuple([list(t) for t in zip(*listOfLists)])


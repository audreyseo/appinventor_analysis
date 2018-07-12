import ai2summarizer2 as ai2
import jail2


jailtxt = ""
ai2txt = ""

with open("jail.txt", "r") as f:
  jailtxt = f.read()

jailtxt.strip()

jaillines = jailtxt.split("\n")



sepSpaces = 3

ai2FuncsVars = dir(ai2)
jail2FuncsVars = dir(jail2)

same = []
jailOnly = []
newJailOnly = []
removedFromNewJail = []
ai2Only = []


maxLen = 0

for thing in jaillines:
  if thing not in jail2FuncsVars:
    removedFromNewJail.append(thing)

for thing in ai2FuncsVars:
  if len(thing) > maxLen:
    maxLen = len(thing)
  if thing not in jaillines:
    #print thing, "is not in jaillines,", jaillines
    if thing in jail2FuncsVars:
      newJailOnly.append(thing)
    else:
      ai2Only.append(thing)
  else:
    same.append(thing)

for thing in jail2FuncsVars:
  if len(thing) > maxLen:
    maxLen = len(thing)
  if thing not in ai2FuncsVars:
    if thing not in jaillines:
      newJailOnly.append(thing)
    else:
      jailOnly.append(thing)

jailOnly.sort()
newJailOnly.sort()
removedFromNewJail.sort()
same.sort()
ai2Only.sort()

mx = max(len(jailOnly), len(newJailOnly), len(same), len(ai2Only))

print "max:", mx
print "maxLen:", maxLen

def padded(mystr=None):
  if mystr == None:
    return " " * (maxLen + sepSpaces)
  return mystr + " " * ((maxLen + sepSpaces) - len(mystr))

sepString = "-" * (maxLen + sepSpaces)

print padded("jailOnly") + "|" + padded("removedFromNewJail") + "|" + padded("newJailOnly") + "|" + padded("same") + "|" + padded("ai2Only")
print sepString + "|" + sepString + "|" + sepString + "|" + sepString + "|" + sepString
for i in range(mx):
  printstr = ""
  if i < len(jailOnly):
    printstr += padded(jailOnly[i]) + "|"
  else:
    printstr += padded("") + "|"
  if i < len(removedFromNewJail):
    printstr += padded(removedFromNewJail[i]) + "|"
  else:
    printstr += padded() + "|"
  if i < len(newJailOnly):
    printstr += padded(newJailOnly[i]) + "|"
  else:
    printstr += padded() + "|"
  if i < len(same):
    printstr += padded(same[i]) + "|"
  else:
    printstr += padded("") + "|"
  if i < len(ai2Only):
    printstr += padded(ai2Only[i])
  else:
    printstr += padded()
  print printstr

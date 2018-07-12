jailtxt = ""
ai2txt = ""

with open("jail.txt", "r") as f:
  jailtxt = f.read()

with open("ai2summarizer2.txt", "r") as f:
  ai2txt = f.read()

jailtxt.strip()
ai2txt.strip()

jaillines = jailtxt.split("\n")

print len(jaillines)

ai2lines = ai2txt.split("\n")

print len(ai2lines)

same = []
jailOnly = []
ai2Only = []


maxLen = 0

for thing in ai2lines:
  if len(thing) > maxLen:
    maxLen = len(thing)
  if thing not in jaillines:
    #print thing, "is not in jaillines,", jaillines
    ai2Only.append(thing)
  else:
    same.append(thing)

for thing in jaillines:
  if len(thing) > maxLen:
    maxLen = len(thing)
  if thing not in ai2lines:
    jailOnly.append(thing)

jailOnly.sort()
same.sort()
ai2Only.sort()

mx = max(len(jailOnly), len(same), len(ai2Only))

print "max:", mx
print "maxLen:", maxLen

def padded(mystr=None):
  if mystr == None:
    return " " * (maxLen + 10)
  return mystr + " " * ((maxLen + 10) - len(mystr))

sepString = "-" * (maxLen + 10)

print padded("jailOnly") + "|" + padded("same") + "|" + padded("ai2Only")
print sepString + "|" + sepString + "|" + sepString
for i in range(mx):
  printstr = ""
  if i < len(jailOnly):
    printstr += padded(jailOnly[i]) + "|"
  else:
    printstr += padded("") + "|"
  if i < len(same):
    printstr += padded(same[i]) + "|"
  else:
    printstr += padded("") + "|"
  if i < len(ai2Only):
    printstr += padded(ai2Only[i])
  else:
    printstr += padded()
  print printstr

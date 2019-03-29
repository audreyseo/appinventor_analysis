import pandas as pd

def getDataSets(myformat, kind="10k", sets=None):
  if sets != None:
    names = []
    for i in range(len(sets)-1):
      names.append(myformat.format(kind, sets[i], sets[i+1]))
    return appendDataSets(names)
  return pd.read_csv(myformat.format(kind))

def appendDataSets(strings):
  dfs = []
  for s in strings:
    dfs.append(pd.read_csv(s))
  if len(dfs) >= 1:
    mydf = dfs[0]
    for i in range(1, len(dfs)):
      mydf = mydf.append(dfs[i])
    return mydf

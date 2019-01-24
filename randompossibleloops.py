''' Created by Audrey Seo on 2019/01/21
    Randomly selects 20 projects that I haven't looked at before
    so that I can go look at them, and find out whether or not
    they are loop-able.
'''

import random as rand


lowNum = 5

def getLines():
  location = "possible_loops.csv"
  lines = []
  with open(location, "r") as f:
    lines = f.readlines()
  lines.pop(0)
  for i in range(5):
    lines.pop(0)
  return lines

def getRandomNumbers(limit):
  # Makes up 20 random numbers that are all distinct
  nums = []
  while len(nums) < 20:
    num = rand.randint(0, limit - 1)
    if num not in nums:
      nums.append(num)
  return nums

handlers = getLines()

indexes = getRandomNumbers(len(handlers))


chosen = [str(i) + "\t" + handlers[i].replace(",", "\t") for i in indexes]

print "".join(chosen) #"\n".join(chosen)

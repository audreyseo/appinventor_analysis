# Analyze result of .txt file produced by something like this:
# [fturbak@Franklyns-MacBook-Pro ai2_10K_random_users_deidentified_summary2s]$ find . -exec grep -H Generic {} \; 2>/dev/null > ../ai2_10K_random_users_deidentified_grep_Generic.txt
# [2019/09/07, audrey] welp the above is correct for the analyze generics grep file but this should mention something about "*Number of Screens", no?
# 
# lines look like:
# ./00/00008/p001_001_andruno_summary2.json:            "BluetoothServer.AcceptConnectionGeneric":1
# [2019/09/07, audrey] added some comments as I was reviewing this code

import sys

userNum10k = 10000
userNum46k = 46320
projNum10k = 30851
projNum46k = 1545284
printEvery = 1000

# [2019/09/07, audrey] added this so code would make more sense
def getProjectNameFromFileName(filename):
    if filename.find(".json") > -1:
        # Return just the project's name, before the file extension
        return filename.split(".json")[0]

def analyzeGrepFiles(filenames):
    maxSize = 0
    maxProj = ""
    lineNum = 0
    for filename in filenames:
        with open(filename, 'r') as inFile:
            print('Processing {}'.format(filename))
            for line in inFile:
                # [2019/09/07, audrey] does it always have a comma and a newline at the end? seems like this could be dangerous and could accidentally truncate a digit off
                # I'm sure it doesn't but the possibility is always there.
                sizeString = line.split('"*Number of Screens":')[1][:-2]
                # [:-2] gets rid of commma and newline at end
                # [2019/09/07, audrey] expanding on my previous comment, ideally we'd do:
                # sizeString = line.split('"*Number of Screens":')[1]
                # if sizeString.endswith(",\n"):
                #   sizeString = sizeString[:-2]
                # elif sizeString.endswith("\n"):
                #   sizeString = sizeString[:-1]
                size = int(sizeString)
                if size > maxSize:
                    maxSize = size
                    maxProj = getProjectNameFromFileName(line)
                lineNum += 1
                if lineNum % printEvery == 0:
                    print(lineNum)
    print('Max number of screens is {} for project {}'.format(
        maxSize, maxProj))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: analyzeNumberOfSCreensGrep.py grepFiles ...')
        exit(0)
    analyzeGrepFiles(sys.argv[1:])
            
# 
        
    


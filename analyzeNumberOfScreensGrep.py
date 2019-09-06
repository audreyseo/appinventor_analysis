# Analyze result of .txt file produced by something like this:
# [fturbak@Franklyns-MacBook-Pro ai2_10K_random_users_deidentified_summary2s]$ find . -exec grep -H Generic {} \; 2>/dev/null > ../ai2_10K_random_users_deidentified_grep_Generic.txt
# 
# lines look like:
# ./00/00008/p001_001_andruno_summary2.json:            "BluetoothServer.AcceptConnectionGeneric":1

import sys

userNum10k = 10000
userNum46k = 46320
projNum10k = 30851
projNum46k = 1545284
printEvery = 1000

def analyzeGrepFiles(filenames):
    maxSize = 0
    maxProj = ""
    lineNum = 0
    for filename in filenames:
        with open(filename, 'r') as inFile:
            print('Processing {}'.format(filename))
            for line in inFile: 
                sizeString = line.split('"*Number of Screens":')[1][:-2]
                # [:-2] gets rid of commma and newline at end
                size = int(sizeString)
                if size > maxSize:
                    maxSize = size
                    maxProj = line.split('.json')[0]
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
        
    


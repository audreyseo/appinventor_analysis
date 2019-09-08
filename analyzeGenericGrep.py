# Analyze result of .txt file produced by something like this:
# [fturbak@Franklyns-MacBook-Pro ai2_10K_random_users_deidentified_summary2s]$ find . -exec grep -H Generic {} \; 2>/dev/null > ../ai2_10K_random_users_deidentified_grep_Generic.txt
# 
# lines look like:
# ./00/00008/p001_001_andruno_summary2.json:            "BluetoothServer.AcceptConnectionGeneric":1
# [2019/09/07, audrey] just changed some whitespace / added comments as I was making sense of code. Also added some logic that I thought was missing but probably did not affect the accuracy when the code was ran previously

import sys

userNum10k = 10000
userNum46k = 46320
projNum10k = 30851
projNum46k = 1545284
printEvery = 1000

def analyzeGenericFiles(population, filenames):
    # Population is '10k' or '46k'
    userSet = set()
    projSet = set()
    lineNum = 0
    for filename in filenames:
        with open(filename, 'r') as inFile:
            print('Processing {}'.format(filename))
            for line in inFile: 
                path = line.split('.json:')[0]
                ignore1, ignore2, userID, project = path.split('/')
                userSet.add(userID)
                projSet.add('_'.join([userID, project]))
                lineNum += 1
                if lineNum % printEvery == 0:
                    print(lineNum)
    numGenericUsers = len(userSet)
    numGenericProjs = len(projSet)
    
    numUsers = userNum10k if population == '10k' else userNum46k
    numProjs = projNum10k if population == '10k' else projNum46k
    
    pctGenericUsers = round(100*numGenericUsers/numUsers, 1)
    pctGenericProjs = round(100*numGenericProjs/numProjs, 1)
    print('Generic projects is {} out of {} ({}%)'.format(
        numGenericProjs, numProjs, pctGenericProjs))
    print('Generic users is {} out of {} ({}%)'.format(
        numGenericUsers, numUsers, pctGenericUsers))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: analyzeGenericGrep.py 10k/46k grepFiles ...')
        exit(0)
    population = sys.argv[1]
    if population not in ['10k', '46k']:
        print("First arg (population) must be one of 10k or 46k")
        exit(0)
    if len(sys.argv) <= 2: # [2019/09/07, audrey] added this if statement since  program expects three things in the args: the name of the program we're running, the string 10k or 46k, and the files containing the information from the grep
        print('Expected at least two args, but did not find grepFiles.\nUsage: analyzeGenericGrep.py 10k/46k grepFiles ...')
        exit(0)
    analyzeGenericFiles(population, sys.argv[2:]) # [2019/09/07, audrey] edited to use the population var created earlier
            
# python analyzeGenericGrep.py 10k ../../data/ai2_10K_random_users_deidentified_grep_Generic.txt            
        
    


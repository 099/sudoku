#!/usr/bin/env python3

import itertools
import copy

def sudokuSolve(arr):
    uniquenessProcess(arr, {})
    if not isFinish(arr):
        candidateDict = deletionProcess(arr)
        if not isFinish(arr):
            guessProcess(arr, candidateDict)
    if not isFinish(arr):
        print("no finish")
    else:
        print("finish")
    return arr

def isFinish(arr):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if arr[x][y] == 0:
                return False
    return True

def printData(arr):
    for i in arr:
        print(i)
    print()

def printCandidateDict(candidateDict):
    for key in candidateDict.keys():
        print(key, candidateDict[key])
    print()

def uniquenessProcess(arr, candidateDict):
    canContinue = True
    while canContinue:
        hasOnly = setOnlyNum(arr, candidateDict)
        canContinue = hasOnly
        while hasOnly:
            hasOnly = setOnlyNum(arr, candidateDict)
        
        hasSameXY = setSameXYNum(arr, candidateDict)
        canContinue = hasSameXY
        while hasSameXY:
            hasSameXY = setSameXYNum(arr, candidateDict)

def deletionProcess(arr):
    candidateDict = mergerCandidateDict(arr, {})
    canContinue = deletion(arr, candidateDict)
    while canContinue:
        candidateDict = mergerCandidateDict(arr, candidateDict)
        uniquenessProcess(arr, candidateDict)
        canContinue = deletion(arr, candidateDict)
    return candidateDict

def guessProcess(arr, candidateDict):
    result = 1
    while result == 1:
        candidateDict = mergerCandidateDict(arr, candidateDict)
        uniquenessProcess(arr, candidateDict)
        result = guess(arr, candidateDict)
    if result == -1:
        amount = 2
        while result == 1 or amount < 6:
            candidateDict = mergerCandidateDict(arr, candidateDict)
            uniquenessProcess(arr, candidateDict)
            result = combiGuess(arr, candidateDict, amount)
            if result == -1:
                amount += 1
            elif result == 0:
                break
    return candidateDict

def guess(arr, candidateDict):
    keys = sortedCandicdateKey(candidateDict)
    for key in keys:
        guessCandidateDict = copy.deepcopy(candidateDict)
        guessNums = guessCandidateDict.pop(key)
        for num in guessNums:
            myArr = copy.deepcopy(arr)
            myCandidateDict = copy.deepcopy(guessCandidateDict)
            myArr[key[0]][key[1]] = num
            uniquenessProcess(myArr, myCandidateDict)
            myCandidateDict = mergerCandidateDict(myArr, myCandidateDict)
            if isCorrect(myArr, myCandidateDict):
                if isFinish(myArr):
                    for x in range(len(arr)):
                        arr[x] = myArr[x]
                    return 0
            else:
                candidateDict[key].remove(num)
                return 1
    return -1

def combiGuess(arr, candidateDict, amount):
    keys = sortedCandicdateKey(candidateDict)
    keys = [key for key in keys if len(candidateDict[key]) <= amount]
    if len(keys) < amount:
        return -1
    combiKeys = list(itertools.combinations(keys, amount))
    for guessKeys in combiKeys:
        guessValues = [candidateDict[key] for key in guessKeys]
        combiGuessValues = combinationsInList(guessValues)
        correctValues = copy.deepcopy(combiGuessValues)
        for values in combiGuessValues:
            myArr = copy.deepcopy(arr)
            myCandidateDict = copy.deepcopy(candidateDict)
            for i in range(len(guessKeys)):
                key = guessKeys[i]
                myArr[key[0]][key[1]] = values[i]
                myCandidateDict.pop(key)
            uniquenessProcess(myArr, myCandidateDict)
            myCandidateDict = mergerCandidateDict(myArr, myCandidateDict)
            if isCorrect(myArr, myCandidateDict):
                if isFinish(myArr):
                    for x in range(len(arr)):
                        arr[x] = myArr[x]
                    return 0
            else:
                correctValues.remove(values)
        if(len(correctValues) == 1):
            for i in range(len(guessKeys)):
                key = guessKeys[i]
                arr[key[0]][key[1]] = correctValues[0][i]
                return 1
    return -1

def sortedCandicdateKey(candidateDict):
    items = candidateDict.items()
    items = sorted(items, key = lambda item:len(item[1]))
    return [item[0] for item in items]

def combinationsInList(arr):
    result = []
    if len(arr) < 2:
        return arr
    result = [(x, y) for x in arr[0] for y in arr[1]]
    for z in range(2, len(arr)):
        result = [x + (y,) for x in result for y in arr[z]]
    return result

def mergerCandidateDict(arr, candidateDict):
    result = {}
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if arr[x][y] == 0:
                p = getPossibleNums(arr, x, y)
                if (x, y) in candidateDict.keys() and len(candidateDict[(x, y)]) < len(p):
                    p = candidateDict[(x, y)]
                result[(x, y)] = p
    return result

def deletion(arr, candidateDict):
    canContinue = True
    while canContinue:
        canContinue = amountDeletion(arr, candidateDict, onlyGridUseNum)
        if not canContinue:
            canContinue = amountDeletion(arr, candidateDict, gridOnlyUseNum)
        if canContinue:
            return True
    return False

def amountDeletion(arr, candidateDict, amountMethod):
    for amount in range(2, 6):
        for key in candidateDict.keys():
            unit = getUnitX(arr, key[0])
            success = amountMethod(unit, candidateDict, amount)
            if not success:
                unit = getUnitY(arr, key[1])
                success = amountMethod(unit, candidateDict, amount)
            if not success:
                unit = getUnitXY(arr, key[0], key[1])
                success = amountMethod(unit, candidateDict, amount)
            if success:
                return True
    return False

def gridOnlyUseNum(unit, candidateDict, amount):
    unitKeys = [key for key in unit if key in candidateDict.keys()]
    if len(unitKeys) <= amount:
        return False
    result = False
    combiKeys = list(itertools.combinations(unitKeys, amount))
    for keys in combiKeys:
        setNums = getSetNums(keys, candidateDict)
        if len(setNums) == amount:
            for key in unitKeys:
                if key not in keys:
                    tmp = candidateDict[key]
                    candidateDict[key] = [num for num in tmp if num not in setNums]
                    if (tmp != candidateDict[key]):
                        result = True
            if result:
                return result
    return result

def onlyGridUseNum(unit, candidateDict, amount):
    unitKeys = [key for key in unit if key in candidateDict.keys()]
    if len(unitKeys) < amount:
        return False
    result = False
    combiKeys = list(itertools.combinations(unitKeys, amount))
    for keys in combiKeys:
        setNums = getSetNums(keys, candidateDict)
        combiNums = list(itertools.combinations(setNums, amount))
        for nums in combiNums:
            if not hasNumsInUnitKeys(candidateDict, unitKeys, keys, nums):
                for key in keys:
                    tmp = candidateDict[key]
                    candidateDict[key] = [num for num in tmp if num in nums]
                    if (tmp != candidateDict[key]):
                        result = True
                if result:
                    return result
    return result

def getSetNums(keys, candidateDict):
    setNums = set()
    for key in keys:
        setNums |= set(candidateDict[key])
    return setNums

def hasNumsInUnitKeys(candidateDict, unitKeys, exceptKeys, nums):
    keys = [key for key in unitKeys if key not in exceptKeys]
    for key in keys:
        for num in candidateDict[key]:
            if num in nums:
                return True
    return False

def setOnlyNum(arr, candidateDict):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if arr[x][y] == 0:
                p = getPossibleNums(arr, x, y)
                if (x, y) in candidateDict.keys() and len(candidateDict[(x, y)]) < len(p):
                    p = candidateDict[(x, y)]
                if len(p) == 1:
                    arr[x][y] = p[0]
                    return True
    return False

def setSameXYNum(arr, candidateDict):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if arr[x][y] != 0:
                positions = getSameXPossiblePositions(arr, x, y)
                positions = filterPositionsByCandidateDict(candidateDict, positions, arr[x][y])
                if len(positions) == 1:
                    arr[positions[0][0]][positions[0][1]] = arr[x][y]
                    return True
                positions = getSameYPossiblePositions(arr, x, y)
                positions = filterPositionsByCandidateDict(candidateDict, positions, arr[x][y])
                if len(positions) == 1:
                    arr[positions[0][0]][positions[0][1]] = arr[x][y]
                    return True
    return False

def filterPositionsByCandidateDict(candidateDict, positions, num):
    result = []
    for position in positions:
        tmp = candidateDict.get(position,[])
        if len(tmp) == 0 or num in tmp:
            result.append(position)
    return result

def getSameXPossiblePositions(arr, x, y):
    result = []
    otherX = x
    emptyX = x
    otherY = y
    emptyY = y
    sameXs = getOtherSameXY(arr, x)
    hasNum0 = hasXNum(arr, sameXs[0], arr[x][y])
    hasNum1 = hasXNum(arr, sameXs[1], arr[x][y])
    if(hasNum0 and not hasNum1):
        emptyX = sameXs[1]
        otherX = sameXs[0]
    elif(hasNum1 and not hasNum0):
        emptyX = sameXs[0]
        otherX = sameXs[1]
    elif(not hasNum0 and not hasNum1):
        return guessOtherXPossiblePositions(arr, x, y)
    else:
        return result

    if otherX != emptyX:
        for j in range(len(arr)):
            if arr[otherX][j] == arr[x][y]:
                otherY = j
        emptyY = getOtherGrid(y//3, otherY//3)
        if emptyY != y:
            result = getXPossiblePositionsByNum(arr, emptyX, emptyY, arr[x][y])
    
    return result

def getSameYPossiblePositions(arr, x, y):
    result = []
    otherY = y
    emptyY = y
    otherX = x
    emptyX = x
    sameYs = getOtherSameXY(arr, y)
    hasNum0 = hasYNum(arr, sameYs[0], arr[x][y])
    hasNum1 = hasYNum(arr, sameYs[1], arr[x][y])
    if(hasNum0 and not hasNum1):
        emptyY = sameYs[1]
        otherY = sameYs[0]
    elif(hasNum1 and not hasNum0):
        emptyY = sameYs[0]
        otherY = sameYs[1]
    elif(not hasNum0 and not hasNum1):
       return guessOtherYPossiblePositions(arr, x, y)
    else:
        return result

    if otherY != emptyY:
        for i in range(len(arr[x])):
            if arr[i][otherY] == arr[x][y]:
                otherX = i
        emptyX = getOtherGrid(x//3, otherX//3)
        if emptyX != x:
            result = getYPossiblePositionsByNum(arr, emptyY, emptyX, arr[x][y])

    return result

def guessOtherXPossiblePositions(arr, x, y):
    sameXs = getOtherSameXY(arr, x)
    otherGridY = [grid for grid in range(3) if grid != y//3]
    guessPosition = []
    if isXGridFull(arr, sameXs[0], otherGridY[0]) or isXGridFull(arr, sameXs[1], otherGridY[1]):
        guessPosition = getXPossiblePositionsByNum(arr, sameXs[0], otherGridY[1], arr[x][y])
        guessPosition1 = getXPossiblePositionsByNum(arr, sameXs[1], otherGridY[0], arr[x][y])
        if len(guessPosition1) < len(guessPosition):
            guessPosition = guessPosition1
    elif isXGridFull(arr, sameXs[1], otherGridY[0]) or isXGridFull(arr, sameXs[0], otherGridY[1]):
        guessPosition = getXPossiblePositionsByNum(arr, sameXs[1], otherGridY[1], arr[x][y])
        guessPosition1 = getXPossiblePositionsByNum(arr, sameXs[0], otherGridY[0], arr[x][y])
        if len(guessPosition1) < len(guessPosition):
            guessPosition = guessPosition1

    return guessPosition

def guessOtherYPossiblePositions(arr, x, y):
    sameYs = getOtherSameXY(arr, y)
    otherGridX = [grid for grid in range(3) if grid != x//3]
    guessPosition = []
    if isYGridFull(arr, sameYs[0], otherGridX[0]) or isYGridFull(arr, sameYs[1], otherGridX[1]):
        guessPosition = getYPossiblePositionsByNum(arr, sameYs[0], otherGridX[1], arr[x][y])
        guessPosition1 = getYPossiblePositionsByNum(arr, sameYs[1], otherGridX[0], arr[x][y])
        if len(guessPosition1) < len(guessPosition):
            guessPosition = guessPosition1
    elif isYGridFull(arr, sameYs[1], otherGridX[0]) or isYGridFull(arr, sameYs[0], otherGridX[1]):
        guessPosition = getYPossiblePositionsByNum(arr, sameYs[1], otherGridX[1], arr[x][y])
        guessPosition1 = getYPossiblePositionsByNum(arr, sameYs[0], otherGridX[0], arr[x][y])
        if len(guessPosition1) < len(guessPosition):
            guessPosition = guessPosition1
    return guessPosition

def getXPossiblePositionsByNum(arr, x, gridY, num):
    result = []
    for j in range(gridY*3, (gridY+1)*3):
        if arr[x][j] == 0 and not hasYNum(arr, j, num):
            result.append((x, j))
    return result

def getYPossiblePositionsByNum(arr, y, gridX, num):
    result = []
    for i in range(gridX*3, (gridX+1)*3):
        if arr[i][y] == 0 and not hasXNum(arr, i, num):
            result.append((i, y))
    return result

def getOtherGrid(one, tow):
    for i in range(0, 3):
        if i != one and i != tow:
            return i
    return 0

def getOtherSameXY(arr, p):
    result = []
    tmpP = p//3
    for i in range(tmpP*3, (tmpP+1)*3):
        if i != p:
            result.append(i)
    return result

def isXGridFull(arr, x, gridY):
    for j in range(gridY*3, (gridY+1)*3):
        if arr[x][j] == 0:
            return False
    return True

def isYGridFull(arr, y, gridX):
    for i in range(gridX*3, (gridX+1)*3):
        if arr[i][y] == 0:
            return False
    return True

def getSameUnitPositions(arr, position1, position2):
    if position1[0] == position2[0]:
        return getUnitX(arr, position1[0])
    elif position1[1] == position2[1]:
        return getUnitY(arr, position1[1])
    elif position1[0]//3 == position2[0]//3 and position1[1]//3 == position2[1]//3:
        return getUnitXY(arr, position1[0], position1[1])
    else:
        return []

def getUnitX(arr, x):
    return [(x, y) for y in range(len(arr[0]))]

def getUnitY(arr, y):
    return [(x, y) for x in range(len(arr))]

def getUnitXY(arr, x, y):
    tmpX = x//3
    tmpY = y//3
    return [(x, y) for x in range(tmpX*3, (tmpX+1)*3) for y in range(tmpY*3, (tmpY+1)*3)]

def hasXNum(arr, x, num):
    nums = getXNums(arr, x)
    return num in nums

def hasYNum(arr, y, num):
    nums = getYNums(arr, y)
    return num in nums

def hasGridNum(arr, x, y, num):
    nums = getGridNums(arr, x, y)
    return num in nums

def getPossibleNums(arr, x, y):
    result = getXNums(arr, x)
    result.extend(getYNums(arr, y))
    result.extend(getGridNums(arr, x, y))
    return [num for num in range(1, 10) if num not in result]

def getXNums(arr, x):
    return [num for num in arr[x] if num != 0]

def getYNums(arr, y):
    return [arr[i][y] for i in range(len(arr)) if arr[i][y] != 0]

def getGridNums(arr, x, y):
    result = []
    tmpX = x//3
    tmpY = y//3
    for i in range(tmpX*3, (tmpX+1)*3):
        for j in range(tmpY*3, (tmpY+1)*3):
            if arr[i][j] != 0:
                result.append(arr[i][j])
    return result

def isCorrect(arr, candidateDict):
    for i in range(len(arr)):
        if not isUnitCorrect(arr, getUnitX(arr, i)):
            return False
        if not isUnitCorrect(arr, getUnitY(arr, i)):
            return False
    for x in range(len(arr))[::3]:
        for y in range(len(arr))[::3]:
            if not isUnitCorrect(arr, getUnitXY(arr, x, y)):
                return False
    for nums in candidateDict.values():
        if len(nums) == 0:
            return False
    return True

def isUnitCorrect(arr, unit):
    nums = [arr[position[0]][position[1]] for position in unit if arr[position[0]][position[1]] != 0]
    setNums = set(nums)
    return len(nums) == len(setNums)


if __name__ == "__main__":
    import os
    
    def openDataFile(path):
        f = open(path)
        arr = [line.split(",") for line in f];
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                arr[i][j] = int(arr[i][j])
        f.close()
        
        answer = sudokuSolve(arr)
        filePaths = os.path.split(f.name)
        index = filePaths[1].index(".")
        answerFilePath = filePaths[0] + "/" + filePaths[1][0:index] + "_answer" + filePaths[1][index:]
        f = open(answerFilePath, "w")
        for row in answer:
            line = ""
            for num in row:
                line += str(num) + ","
            line = line[0:len(line)-1] + "\n"
            f.write(line)
        f.close()

    path = os.path.split(os.path.realpath(__file__))[0]
    dir = os.listdir(path)
    for name in dir:
        if(name.endswith(".txt") and not name.endswith("answer.txt")):
            openDataFile(path + "/" + name)



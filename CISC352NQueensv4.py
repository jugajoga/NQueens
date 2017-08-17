import random

queens = [] #index: col, value: row
conflictRows = []
conflictRightDia = []
conflictLeftDia = []
emptyRows = []
queensInConflict = [] #cols of queens in conflict

def numConflicts(row, col):
    val = conflictRows[row] + conflictLeftDia[size - 1 - row + col] + conflictRightDia[row + col]
    return val

def addQueensInConflict(row, col):
    conflictsRemRow = conflictRows[row]
    conflictsRemLeft = conflictLeftDia[size - 1 - row + col]
    conflictsRemRight = conflictRightDia[row + col]
    i = 0
    while (conflictsRemRow + conflictsRemLeft + conflictsRemRight != 0):
        if (conflictsRemRow != 0):
            if (queens[i] == row):
                if (i not in queensInConflict):
                    queensInConflict.extend([i])
                conflictsRemRow -= 1    
        if (conflictsRemLeft != 0):
            if (row - col == queens[i] - i):
                if (i not in queensInConflict):
                    queensInConflict.extend([i])
                conflictsRemLeft -= 1
        if (conflictsRemRight != 0):
            if (row + col == queens[i] + i):
                if (i not in queensInConflict):
                    queensInConflict.extend([i])
                conflictsRemRight -= 1
        i += 1
    
def addQueen(row, col):
    conflictRows[row] += 1
    conflictLeftDia[size - 1 - row + col] += 1
    conflictRightDia[row + col] += 1
    queens[col] = row

def subQueen(row, col):
    conflictRows[row] -= 1
    if (conflictRows[row] == 0):
        emptyRows.extend([row])
    conflictLeftDia[size - 1 - row + col] -= 1
    conflictRightDia[row + col] -= 1

def bestHelper(i, col, empties):
    row = emptyRows[i]
    if (conflictLeftDia[size - 1 - row + col] +
    conflictRightDia[row + col] == 0):
        if (i != empties - 1):
            emptyRows[i] = emptyRows.pop()
        else:
            emptyRows.pop()
        return True
    return False
    
def findBestNewPosition(col): #only looking along the columns
    empties = len(emptyRows)
    #constant time pseudo-randomize the order the rows are looked at
    #3 is the most we can do since the min value board size is 4:
    first = random.randint(0, empties / 3)
    second = random.randint(first, empties / 3 * 2)
    third = random.randint(second, empties - 1)
    for i in range(second, third): #empty row and diagonals
        row = emptyRows[i]
        if (bestHelper(i, col, empties)):
            return row
    for i in range(0, first):
        row = emptyRows[i]
        if (bestHelper(i, col, empties)):
            return row
    for i in range(third, empties):
        row = emptyRows[i]
        if (bestHelper(i, col, empties)):
            return row
    for i in range(first, second):
        row = emptyRows[i]
        if (bestHelper(i, col, empties)):
            return row
    floor = 1
    while (True):
        for i in range(0, size/4):
            row = random.randint(0, size - 1)
            if (numConflicts(row, col) <= floor and row not in emptyRows):
                addQueensInConflict(row, col)
                return row 
        floor += 1

def createStartingBoard(boardSize): #board is stored as [row][col]
    global size
    size = int(boardSize)
    queens.extend([0 for i in range(0, size)])
    conflictRows.extend([0 for i in range(0, size)])
    conflictLeftDia.extend([0 for i in range(0, (2*size) - 1)])
    conflictRightDia.extend([0 for i in range(0, (2*size) - 1)])
    emptyRows.extend([i for i in range(0, size)])
    row = random.randint(0, size - 1)
    addQueen(row, 0)
    emptyRows.remove(row)
    for i in range (1, size):
        row = findBestNewPosition(i)
        addQueen(row, i)
    return solveQueens()

def checkSolution():
    if (len(queensInConflict) == 0):
        return True
    return False

def solveQueens():
    maxIterations = 100 #only count when a queen moves
    while (maxIterations > 0):
        if (checkSolution()):
            print maxIterations
            return True
        index = random.randint(0, len(queensInConflict) - 1)
        currentCol = queensInConflict[index]
        currentRow = queens[currentCol]
        queensInConflict.remove(currentCol)
        if (numConflicts(currentRow, currentCol) != 3): # 3 means it only
            subQueen(currentRow, currentCol)            # conflicts with self
            newRow = findBestNewPosition(currentCol)
            addQueen(newRow, currentCol)
            maxIterations -= 1
    return False #restart
    

def writeToFile(file):
    if (size < 256): 
        for i in range (0, size):
            for j in range (0, size):
                if (queens[j] == i):
                    file.write("q")
                else:
                    file.write("x")
            file.write("\n\r")
    file.write("[")
    for i in range (0, size):
        file.write(str(queens[i]))
        if (i + 1 != size):
            file.write(', ')
    file.write("]\n\r\n\r")

def main():
    file = open("nqueens.txt", 'r')
    outFile = open("nqueens_out.txt", 'w')
    for line in file:
        del queens[:], conflictRows[:], conflictLeftDia[:], conflictRightDia[:], emptyRows[:], queensInConflict[:]
        while (not createStartingBoard(line.rstrip("\n\r"))):
            del queens[:], conflictRows[:], conflictLeftDia[:], conflictRightDia[:], emptyRows[:], queensInConflict[:]
        writeToFile(outFile)

if __name__ == "__main__":
    main()

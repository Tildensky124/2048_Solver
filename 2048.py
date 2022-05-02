import random, curses

class Engine:
    
    def playMove(self, moveDir):
        if self.stopGame(): 	
            pass

        board = self.board		

        rotateCount = self.moveList.index(moveDir) 
        moved = False

        if rotateCount:				
            board = self.turnBoard(board, rotateCount)

        merged = [[0 for i in range(self.size)] for i in range(self.size)] 


        for row in range(self.size - 1):
            for col in range(self.size):

                currentTile = board[row][col]
                nextTile = board[row+1][col]

                if not currentTile:
                    continue 

                if not nextTile:
                    for x in range(row+1):
                        board[row-x+1][col] = board[row-x][col]
                    board[0][col] = 0
                    moved = True
                    continue
                if merged[row][col]:
                    continue

                if currentTile == nextTile:
                    if (row < self.size - 2 and nextTile == board[row+2][col]):
                        continue     

                    board[row+1][col] *= 2                      
                    for x in range(row):
                        board[row-x][col] = board[row-x-1][col]
                    board[0][col] = 0

                    merged[row+1][col] = 1                      
                    self.score += self.scoreCount(currentTile)  
                    moved = True

        if rotateCount:
            board = self.turnBoard(board, 4 - rotateCount)

        self.board = board

        if moved:
            self.numMoves += 1
            self.addNewBlock()



    def addNewBlock(self, val=None):
        avail = self.openSpots()

        if avail:
            (row, column) = avail[random.randint(0, len(avail) - 1)]

            if random.randint(0,9) == 9:
                self.board[row][column] = 4
            else:
                self.board[row][column] = 2



    def turnBoard(self, board, count):
        for c in range(count):
            rotated = [[0 for i in range(self.size)] for i in range(self.size)]

            for row in range(self.size):
                for col in range(self.size):
                    rotated[self.size - col - 1][row] = board[row][col]

            board = rotated

        return rotated



    def openSpots(self):
        spots = []
        for row in enumerate(self.board):
            for col in enumerate(row[1]):
                if col[1] == 0:
                    spots.append((row[0], col[0]))
        return spots



    def scoreCount(self, val):
        score = {
            2: 4, 
            4: 8, 
            8: 16, 
            16: 32, 
            32: 64, 
            64: 128, 
            128: 256, 
            256: 512, 
            512: 1024, 
            1024: 2048, 
            2048: 4096, 
            4096: 8192,
            8192: 16384,
            16384: 32768,
            32768: 65536,
            65536: 131072,
        }
        return score[val]

    def __init__(self):
        self.size = 4
        self.board = [[0 for i in range(self.size)] for i in range(self.size)]
        self.score = 0
        self.numMoves = 0
        self.moveList = ['d','l','u','r']
        self.addNewBlock()
        self.addNewBlock()



    def stopGame(self):
        if self.openSpots():
            return False

        board = self.board
        for row in range(self.size):
            for col in range(self.size):
                if (row < self.size - 1 and board[row][col] == board[row+1][col]) \
                or (col < self.size - 1 and board[row][col] == board[row][col+1]):
                    return False  
        return True
            
def findBestMove(game, runs):
    average = 0
    bestScore = 0
    moveList = game.moveList

    for moveDir in moveList:
        average = 0
        for x in range(runs):
            result = startRandom(game.board, moveDir)
            average += result
        average = average/runs
        if average >= bestScore:
            bestScore = average
            move = moveDir
    return move

def startRandom(board, firstMove):
	randomGame = startGame()
	moveList = randomGame.moveList
	randomGame.board = copyBoard(board)
	randomGame.playMove(firstMove)

	while True:
		if randomGame.stopGame():
			break
		randMove = random.choice(moveList)
		randomGame.playMove(randMove)

	return randomGame.score

def createBoard(board, screen):
	for row in enumerate(board):
		for item in enumerate(row[1]):
			screen.addstr(8+3*row[0], 40+6*item[0], str(item[1]), curses.color_pair(COLORS[item[1]]))
	screen.refresh()
def copyBoard(board):
	newBoard = startGame().board
	for row in enumerate(board):
		for item in enumerate(row[1]):
			newBoard[row[0]][item[0]] = item[1]
	return newBoard

def startGame():
	game = Engine()
	return game

def playGame(runs, screen):

	mainGame = startGame()
	moveList = mainGame.moveList
	isDynamic = False

	if runs == 'Dynamic':
		isDynamic = True

	while True:
		if mainGame.stopGame():
			break

		if isDynamic:
			runs = int(1 + (0.01)*mainGame.score)

		if runs > 0:
			move = findBestMove(mainGame, runs)
		else:
			move = random.choice(moveList)
			
		mainGame.playMove(move)
		screen.clear()
		createBoard(mainGame.board, screen)

	return(mainGame)

COLORS = {0:0,2:1,4:2,8:3,16:4,32:5,64:6,128:7,256:8,512:9,1024:10,2048:11,4096:12,8192:13,16384:13,32768:12,65536:12}

def giveOutcome(game, screen):
	screen.clear()
	createBoard(game.board, screen)
	screen.addstr(19, 45, "Score: " + str(game.score))
	screen.addstr(20, 45, "Moves: " + str(game.numMoves))
	screen.addstr(21, 45, "GAME OVER")
	screen.refresh()

def chooseRuns():
	curses.echo()
	screen.clear()
	screen.border(0)
	screen.addstr(13, 14, "(reccomended: 100)")
	screen.addstr(12, 14, "Enter the number of runs per move: ")
	screen.refresh()
	try:
		runs = int(screen.getstr(12, 50, 4))
	except ValueError:
		runs = 0
	screen.clear()
	curses.noecho()
	return runs

x = 0
runs = 100

screen = curses.initscr()

curses.curs_set(0)
curses.noecho()

screen.clear()
curses.start_color()
curses.init_pair(1, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(2, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(3, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(4, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(5, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(6, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(7, 
curses.COLOR_BLACK, 
curses.COLOR_GREEN)
curses.init_pair(8, 
curses.COLOR_BLACK, 
curses.COLOR_CYAN)
curses.init_pair(9, 
curses.COLOR_BLACK, 
curses.COLOR_MAGENTA)
curses.init_pair(10, 
curses.COLOR_BLACK, 
curses.COLOR_RED)
curses.init_pair(11, 
curses.COLOR_BLACK, 
curses.COLOR_BLUE)
curses.init_pair(12, 
curses.COLOR_BLACK, 
curses.COLOR_YELLOW)
curses.init_pair(13, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(14, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(15, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(16, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
curses.init_pair(17, 
curses.COLOR_BLACK, 
curses.COLOR_WHITE)
createBoard(startGame().board, screen)

while True:
	screen.border(0)
	screen.addstr(2, 30, "2048 Self Solver", curses.color_pair(14))
	screen.addstr(22, 64, "- Tilden Polsky", curses.color_pair(15))
	screen.addstr(6, 41, "Runs per move: " + str(runs), curses.color_pair(16))
	screen.addstr(9, 5, "Please select an option", curses.color_pair(17))
	screen.addstr(11, 5, "1. Set runs per move")
	screen.addstr(13, 5, "2. Enable smart runs per move")
	screen.addstr(15, 5, "3. Start Solver")
	screen.addstr(17, 5, "4. Terminate")
	screen.refresh()

	x = screen.getch()
	if x == ord('1'):
		runs = chooseRuns()
	if x == ord('2'):
		runs = 'Smart'		
	if x == ord('3'):
		giveOutcome(playGame(runs, screen), screen)
	if x == ord('4'):
		break

curses.echo()
curses.endwin()

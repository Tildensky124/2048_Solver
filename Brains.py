import Game, random, curses

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
	game = Game.Engine()
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

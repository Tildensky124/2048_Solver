import Game, random, curses

COLORS = {0:0,2:1,4:2,8:3,16:4,32:5,64:6,128:7,256:8,512:9,1024:10,2048:11,4096:12,8192:13,16384:13,32768:12,65536:12}

def H():
	game = Game.Engine()
	return game

def I(board, screen):
	for row in enumerate(board):
		for item in enumerate(row[1]):
			screen.addstr(8+3*row[0], 40+6*item[0], str(item[1]), curses.color_pair(COLORS[item[1]]))
	screen.refresh()

def J(board):
	newBoard = H().board
	for row in enumerate(board):
		for item in enumerate(row[1]):
			newBoard[row[0]][item[0]] = item[1]
	return newBoard

def K(board, firstMove):
	randomGame = H()
	moveList = randomGame.moveList
	randomGame.board = J(board)
	randomGame.D(firstMove)

	while True:
		if randomGame.G():
			break
		randMove = random.choice(moveList)
		randomGame.D(randMove)

	return randomGame.score

def L(game, runs):
	average = 0
	bestScore = 0
	moveList = game.moveList

	for moveDir in moveList:
		average = 0
		for x in range(runs):
			result = K(game.board, moveDir)
			average += result
		average = average/runs
		if average >= bestScore:
			bestScore = average
			move = moveDir
	return move

def M(runs, screen):

	mainGame = H()
	moveList = mainGame.moveList
	isDynamic = False

	if runs == 'Smart':
		isDynamic = True

	while True:
		if mainGame.G():
			break

		if isDynamic:
			runs = int(1 + (0.01)*mainGame.score)

		if runs > 0:
			move = L(mainGame, runs)
		else:
			move = random.choice(moveList)
			
		mainGame.D(move)
		screen.clear()
		I(mainGame.board, screen)

	return(mainGame)
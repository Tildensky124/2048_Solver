from Brains import *

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

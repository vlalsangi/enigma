#! /usr/bin/python
#by Vaishak Lalsangi
#andrewid: vnl

from Tkinter import *
import random

class Struct:
	pass

def run(row, col, size):
	global root
	root = Tk()
	global canvas 
	width = 2*col + 1
	height = 2*row + 1
	woffset = 40
	canvas = Canvas(root, width = width * size + woffset, height = height * size)
	canvas.pack()
	canvas.data = Struct()
	canvas.data.row = row
	canvas.data.col = col
	canvas.data.height = height
	canvas.data.width = width 
	canvas.data.size = size
	canvas.data.woffset = woffset
	canvas.focus_set()
	canvas.bind("<Up>", keyPressedUp)
	canvas.bind("<Down>", keyPressedDown)
	canvas.bind("<Left>", keyPressedLeft)
	canvas.bind("<Right>", keyPressedRight)
	canvas.bind("q", keyPressedQ)
	canvas.data.playerCoord = 0
	canvas.focus_set()
	startScreen()
	root.mainloop()

def initGame():
	startButton.pack_forget()
	canvas.delete(ALL)
	canvas.data.masterradius = 3
	canvas.data.radius = canvas.data.masterradius
	canvas.data.poweruplevel = canvas.data.radius - canvas.data.masterradius
	canvas.data.score = 0
	canvas.data.time = 300
	canvas.data.isGameOver = False
	initMap()
	genMap()
	if canvas.data.isGameOver == False:
		canvas.after(1000, tick)
		canvas.after(1000, drawSideBar)
	drawPlayer()
	letThereBeLight(canvas.data.playerCoord, canvas.data.playerCoord, canvas.data.radius)
	redrawAll()

def redrawAll():
	canvas.delete(ALL)
	drawMap()
	drawSideBar()
	drawPlayer()

def endGame():
	canvas.delete(ALL)
	canvas.create_rectangle(0, 0, canvas.data.width * canvas.data.size, canvas.data.height * canvas.data.size, fill = "purple")
	canvas.create_text(canvas.data.width * canvas.data.size / 2, canvas.data.height * canvas.data.size / 2, anchor = "center", text = "GAME OVER")
	global startButton
	startButton = Button(root, text = "Restart", command = initGame)
	startButton.pack()

def tick():
	canvas.data.time = canvas.data.time - 1
	if canvas.data.time <= 0:
		canvas.data.isGameOver = True
	if canvas.data.isGameOver == False:
		canvas.after(1000, tick)
	if canvas.data.isGameOver:
		endGame()

def drawSideBar():
	x0 = canvas.data.width * canvas.data.size
	y0 = 0
	x1 = canvas.data.width * canvas.data.size + canvas.data.woffset
	y1 = canvas.data.height * canvas.data.size 
	score_string = "l: " + str(canvas.data.score)
	powerup_string = "p: " + str(canvas.data.poweruplevel)
	time_string = "t: " + str(canvas.data.time)
	canvas.create_rectangle(x0, y0, x1, y1, fill = "purple")
	canvas.create_text(x1 - canvas.data.woffset / 2, y0 + canvas.data.woffset/2, text = score_string)
	canvas.create_text(x1 - canvas.data.woffset / 2, y0 + canvas.data.woffset, text = powerup_string)
	canvas.create_text(x1 - canvas.data.woffset / 2, y0 + canvas.data.woffset * 1.5, text = time_string)
	canvas.after(1000, drawSideBar)

def initMap():
	# [pass, lit, visited, cell/wall, trap, stairs, loop]
	h = canvas.data.height
	w = canvas.data.width
	board = []

	for x in range(h):
		
		newRow = []

		if (x % 2 == 0):
			newRow = []
			for z in range(w):
				newRow.insert(0, [False, False, False, False, False, False, False, False])
		

		else:
			newRow = []
			for y in range(w):
				if (y % 2 == 0):
					newRow.insert(0, [False, False, False, False, False, False, False, False])
				else:
					newRow.insert(0, [True, False, False, True, False, False, False, False])
		
		board.append(newRow)

	canvas.data.board = board

def genMap():
	
	board = canvas.data.board
	currentCell = getStartCoord()
	canvas.data.playerCoord = currentCell
	stack = []
	stack.append(currentCell)
	y = currentCell[0]
	x = currentCell[1]
	board[y][x][2] = True

	while(len(stack) != 0):
		neighbors = getNeighbors(currentCell)
		if len(neighbors) > 0:
			rand = len(neighbors)
			rand = random.randint(0,rand-1)
			#print neighbors
			newCell = neighbors[rand]
			stack.append(currentCell)
			wall = getWall(currentCell, newCell)
			#print wall
			board[wall[0]][wall[1]][0] = True
			currentCell = newCell
			y = currentCell[0]
			x = currentCell[1]
			board[y][x][2] = True
			#print currentCell
		elif len(stack) > 0:
			currentCell = stack.pop()
		else:
			currentCell = getStartCoord()
	for x in range(levelCurveDown()):
		placeLoops()	
		placePowerUps()

	for y in range(levelCurveUp()):
		placeTraps()

	placeEnd()

	canvas.data.board = board
	
def getStartCoord():
	board = canvas.data.board
	y = 0
	x = 0
	while (y % 2 != 1):
		y = random.randint(0, len(board) - 1)
	while (x % 2 != 1):
		x = random.randint(0, len(board[0]) - 1)
	return (y, x)

def getNeighbors(coord):
	board = canvas.data.board
	y = coord[0]
	x = coord[1]
	#print (y,x)
	neighbors = []

	try:
		if ((board[y+2][x][2] == False) and (y+2 > 0) and (x > 0) and (y+2 < len(board)-1) and (x < len(board[0])-1)):
			neighbors.append((y+2, x))
	except IndexError:
		pass
	#print neighbors
	try:
		if ((board[y-2][x][2] == False) and (y-2 > 0) and (x > 0) and (y-2 < len(board)-1) and (x < len(board[0])-1)):
			neighbors.append((y-2, x))
	except IndexError:
		pass
	#print neighbors
	try:
		if ((board[y][x+2][2] == False) and (y > 0) and (x+2 > 0) and (y < len(board)-1) and (x+2 < len(board[0])-1)):
			neighbors.append((y, x+2))
	except IndexError:
		pass
	#print neighbors
	try:
		if ((board[y][x-2][2] == False) and (y > 0) and (x-2 > 0) and (y < len(board)-1) and (x-2 < len(board[0])-1)):
			neighbors.append((y, x-2))
	except IndexError:
		pass
	#print neighbors
	return neighbors

def getWall(coord0, coord1):
	y0 = coord0[0]
	x0 = coord0[1]
	y1 = coord1[0]
	x1 = coord1[1]

	diffx = x1 - x0
	diffy = y1 - y0

	#print (diffy, diffx)

	return (y0 + diffy/2, x0 + diffx/2)

def drawMap():
	# [pass, lit, visited, cell/wall, trap, stairs, loop, powerup]
	board = canvas.data.board
	size = canvas.data.size
	for y in range(len(board)):
		for x in range(len(board[0])):
			x0 = x * size
			y0 = y * size
			if board[y][x][0] and board[y][x][1]:
				canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill = "brown")
			if board[y][x][0] and board[y][x][4]:
				canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill = "red")
			if board[y][x][0] and board[y][x][5]:
				canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill = "blue")
			if board[y][x][0] and board[y][x][7]:
				canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill = "magenta")
			if board[y][x][0] == False and board[y][x][1]:
				canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill = "black")
			if board[y][x][1] == False:
				canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill = "black")

def placeLoops():
	board = canvas.data.board
	coord = genWallCoord()
	y = coord[0]
	x = coord[1]
	
	while(testAdjacent(coord) == False):
		coord = genWallCoord()
		y = coord[0]
		x = coord[1]

	board[y][x][0] = True
	board[y][x][6] = True

	canvas.data.board = board

def placePowerUps():
	board = canvas.data.board
	coord = genWallCoord()
	y = coord[0]
	x = coord[1]
	
	while(testAdjacent(coord) == False):
		coord = genWallCoord()
		y = coord[0]
		x = coord[1]

	board[y][x][0] = True
	board[y][x][7] = True

	canvas.data.board = board

def placeTraps():
	board = canvas.data.board
	coord = genPassCoord()
	y = coord[0]
	x = coord[1]

	while(board[y][x][0] == False or canvas.data.playerCoord == (y,x)):
		coord = genPassCoord()
		y = coord[0]
		x = coord[1]
		#print (y, x), board[y][x][0]

	board[y][x][4] = True

def placeEnd():
	board = canvas.data.board
	coord = genPassCoord()
	y = coord[0]
	x = coord[1]

	while(board[y][x][0] == False):
		coord = genPassCoord()
		y = coord[0]
		x = coord[1]
		print (y, x), board[y][x][0]

	board[y][x][5] = True

def genWallCoord():

	board = canvas.data.board
	y = random.randint(0, len(board) - 1)
	x = random.randint(0, len(board[0]) - 1)
	
	while (board[y][x][0]):
		y = random.randint(0, len(board) - 1)
		x = random.randint(0, len(board[0]) - 1)

	return (y, x)

def genPassCoord():
	board = canvas.data.board
	y = random.randint(0, len(board) - 1)
	x = random.randint(0, len(board[0]) - 1)
	
	while (board[y][x][0] == False):
		y = random.randint(0, len(board) - 1)
		x = random.randint(0, len(board[0]) - 1)

	return (y, x)

def testAdjacent(coord):
	y = coord[0]
	x = coord[1]
	board = canvas.data.board
	try:
		if (board[y+2][x][0] and board[y-2][x][0] and y-2 > 0 and y+2 >0):
			return True
	except IndexError:
		return False
	try:
		if (board[y][x+2][0] and board[y][x-2][0]) and x-2 > 0 and x-2 > 0:
			return True
	except IndexError:
		return False
	return False

def letThereBeLight(coord0, coord1, radius):
	board = canvas.data.board
	y0 = coord0[0]
	x0 = coord0[1]
	y1 = coord1[0]
	x1 = coord1[1]

	for y in range(y0-radius, y0+radius+1):
		for x in range(x0-radius, x0+radius+1):
			try:
				if (x > 0 and y > 0):
					board[y][x][1] = False
			except IndexError:
				continue

	for y in range(y1-radius, y1+radius+1):
		for x in range(x1-radius, x1+radius+1):
			try:
				if (x > 0 and y > 0):
					board[y][x][1] = True
			except IndexError:
				continue

def drawPlayer():
	coord = canvas.data.playerCoord
	x0 = coord[1] * canvas.data.size
	y0 = coord[0] * canvas.data.size
	x1 = x0 + canvas.data.size
	y1 = y0 + canvas.data.size

	canvas.create_rectangle(x0, y0, x1, y1, fill = "cyan")

def levelUp(coord):
	board = canvas.data.board
	board[coord[0]][coord[1]][5] = False
	canvas.data.score = canvas.data.score + 1
	canvas.data.radius = canvas.data.masterradius
	canvas.data.poweruplevel = canvas.data.radius - canvas.data.masterradius
	initMap()
	genMap()
	letThereBeLight(canvas.data.playerCoord, canvas.data.playerCoord, canvas.data.radius)
	redrawAll()

def powerUp(y1, x1):
	canvas.data.board[y1][x1][7] = False
	canvas.data.radius = canvas.data.radius + 1
	canvas.data.poweruplevel = canvas.data.poweruplevel + 1

def movePlayer(dy, dx):
	coord = canvas.data.playerCoord
	board = canvas.data.board
	x0 = coord[1]
	y0 = coord[0]
	#print "x"

	try:
		
		if ((board[y0+dy][x0+dx][0] == True) and (board[y0+dy][x0+dx][4] == True) and (y0+dy > 0) and (x0+dx > 0) and (y0+dy < len(board)-1) and (x0+dx < len(board[0])-1)):
			canvas.data.playerCoord = genPassCoord()
			letThereBeLight(coord, canvas.data.playerCoord, canvas.data.radius)
			return None

		if ((board[y0+dy][x0+dx][0] == True) and (board[y0+dy][x0+dx][5] == True) and (y0+dy > 0) and (x0+dx > 0) and (y0+dy < len(board)-1) and (x0+dx < len(board[0])-1)):
			temp = (y0 + dy, x0 + dx)
			levelUp(temp)
			return None

		if ((board[y0+dy][x0+dx][0] == True) and (board[y0+dy][x0+dx][7] == True) and (y0+dy > 0) and (x0+dx > 0) and (y0+dy < len(board)-1) and (x0+dx < len(board[0])-1)):
			x1 = x0 + dx
			y1 = y0 + dy
			powerUp(y1, x1)

			

		if ((board[y0+dy][x0+dx][0] == True) and (y0+dy > 0) and (x0+dx > 0) and (y0+dy < len(board)-1) and (x0+dx < len(board[0])-1)):
			x1 = x0 + dx
			y1 = y0 + dy
		
		else:
			#print "Can't move there. #notlegal"
			y1 = y0
			x1 = x0
	except IndexError:
		print "Can't move there. #indexerror"
		y1 = y0
		x1 = x0
	newCoord = (y1, x1)
	#print coord, newCoord
	letThereBeLight(coord, newCoord, canvas.data.radius)
	canvas.data.playerCoord = newCoord

def keyPressedUp(event):
	if canvas.data.isGameOver == False:
		movePlayer(-1, 0)
		redrawAll()

def keyPressedDown(event):
	if canvas.data.isGameOver == False:
		movePlayer(1, 0)
		redrawAll()

def keyPressedRight(event):
	if canvas.data.isGameOver == False:
		movePlayer(0, 1)
		redrawAll()

def keyPressedLeft(event):
	if canvas.data.isGameOver == False:
		movePlayer(0, -1)
		redrawAll()

def keyPressedQ(event):
	quit()
	x = 2

def levelCurveUp():
	#min 10, max 30

	score = canvas.data.score

	if (score >= 0 and score < 5):
		x = random.randint(10, 20)

	if (score >= 5 and score < 10):
		x = random.randint(20, 25)

	if (score >= 10):
		x = random.randint(20, 25)

	return x

def levelCurveDown():
	#min 5, max 20

	score = canvas.data.score

	if (score >= 0 and score < 5):
		x = random.randint(15, 20)

	if (score >= 5 and score < 10):
		x = random.randint(10, 15)

	if (score >= 10):
		x = random.randint(5, 10)

	return x

def startScreen():
	canvas.create_rectangle(0, 0, canvas.data.width * canvas.data.size, canvas.data.height * canvas.data.size, fill = "purple")
	canvas.create_text(canvas.data.width * canvas.data.size / 2, canvas.data.height * canvas.data.size / 2, anchor = "center", text = "ENIGMA")
	global startButton
	startButton = Button(root, text = "Start Game", command = initGame)
	startButton.pack()
	
run(20, 15, 15)





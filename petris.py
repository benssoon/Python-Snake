#!/usr/bin/python3

import subprocess,sys,termios
from time import sleep
from copy import deepcopy
from random import choice

SQUARE = [[11,-2],[12,-2],
	  [11,-1],[12,-1]]

LINE = [[10,-1],[11,-1],[12,-1],[13,-1]]

J =    [[12,-3],
	[12,-2],
[11,-1],[12,-1]]

L = [[11,-3],
     [11,-2],
     [11,-1],[12,-1]]

SHAPES = ['square','line','l','j']
BLOCK = '0'
UP = '\x1b[A'
DOWN = '\x1b[B'
RIGHT = '\x1b[C'
LEFT = '\x1b[D'


class Tetrimino:

	def __init__(self, shape):
		self.shape = shape
		self.position = self.parseShape(shape)
		self.rotation = 0

	def parseShape(self, shape):
		return {
			'square':deepcopy(SQUARE),
			'line':deepcopy(LINE),
			'l':deepcopy(L),
			'j':deepcopy(J),
			'all':[]
			}[shape]

	def fall(self):
		for block in self.position:
			block[1] += 1

	def rotate(self):
		if self.shape == 'line':
			if self.rotation%4 == 0:
				for block in self.position:
					block[0] = self.position[1][0]
				self.position[0][1] -= 1
				self.position[2][1] += 1
				self.position[3][1] += 2
			elif self.rotation%4 == 1:
				for block in self.position:
					block[1] = self.position[1][1]
				self.position[0][0] += 1
				self.position[2][0] -= 1
				self.position[3][0] -= 2
			elif self.rotation%4 == 2:
				for block in self.position:
					block[0] = self.position[1][0]
				self.position[0][1] += 1
				self.position[2][1] -= 1
				self.position[3][1] -= 2
			elif self.rotation%4 == 3:
				for block in self.position:
					block[1] = self.position[1][1]
				self.position[0][0] -= 1
				self.position[2][0] += 1
				self.position[3][0] += 2
		elif self.shape == 'j':
			if self.rotation%4 == 0:
				self.position[0][0] += 1
				self.position[0][1] += 1
				self.position[2][1] -= 2
				self.position[3][0] -= 1
				self.position[3][1] -= 1
			elif self.rotation%4 == 1:
				self.position[0][0] -= 1
				self.position[0][1] += 1
				self.position[2][0] += 2
				self.position[3][0] += 1
				self.position[3][1] -= 1
			if self.rotation%4 == 2:
				self.position[0][0] -= 1
				self.position[0][1] -= 1
				self.position[2][1] += 2
				self.position[3][0] += 1
				self.position[3][1] += 1
			elif self.rotation%4 == 3:
				self.position[0][0] += 1
				self.position[0][1] -= 1
				self.position[2][0] -= 2
				self.position[3][0] -= 1
				self.position[3][1] += 1
		elif self.shape == 'l':
			if self.rotation%4 == 0:
				self.position[0][0] += 1
				self.position[0][1] += 1
				self.position[2][0] -= 1
				self.position[2][1] -= 1
				self.position[3][0] -= 2
			elif self.rotation%4 == 1:
				self.position[0][0] -= 1
				self.position[0][1] += 1
				self.position[2][0] += 1
				self.position[2][1] -= 1
				self.position[3][1] -= 2
			if self.rotation%4 == 2:
				self.position[0][0] -= 1
				self.position[0][1] -= 1
				self.position[2][0] += 1
				self.position[2][1] += 1
				self.position[3][0] += 2
			elif self.rotation%4 == 3:
				self.position[0][0] += 1
				self.position[0][1] -= 1
				self.position[2][0] -= 1
				self.position[2][1] += 1
				self.position[3][1] += 2
		self.rotation += 1

class Game:

	def __init__(self):
		self.dead = False
		self.speed = .3
		self.start = True
		self.still = Tetrimino('all')
		self.screen = []
		for y in range(23):
			self.screen.append([])
			for x in range(25):
				self.screen[y].append(x)

	def collide(self, direction):
		nextpos = deepcopy(self.moving.position)
		if direction == 'down':
			for block in nextpos:
				block[1] += 1
				if block in self.still.position or block[1] == len(self.screen)-1:
					return True
		elif direction == 'side':
			for block in nextpos:
				block[0] += 1
				if block in self.still.position or block[0] == len(self.screen[0])-1:
					return True
				block[0] -= 2
				if block in self.still.position or block[0] == 0:
					return True
		else:
			return False

	def events(self):
		key = sys.stdin.read(3)
		if self.start == True:
			self.moving = Tetrimino(choice(SHAPES))
			self.start = False
		if key == LEFT:
			if not self.collide('side'):
				for block in self.moving.position:
					block[0] -= 1
		elif key == RIGHT:
			if not self.collide('side'):
				for block in self.moving.position:
					block[0] += 1
		elif key == DOWN:
			x=1
		elif key == UP:
			self.moving.rotate()

	def logic(self):
		if not self.collide('down'):
			self.moving.fall()
		else:
			for block in self.moving.position:
				self.still.position.append(list(block))
			self.moving = Tetrimino(choice(SHAPES))
		for block in self.still.position:
			if block[1] == 0:
				self.dead = True

	def draw(self):
		if not self.dead:
			for y in range(len(self.screen)):
				for x in range(len(self.screen[0])):
					if (x == 0 and y == 0) or (x == len(self.screen[0])-1 and y == 0) or (x == 0 and y == len(self.screen)-1) or (x == len(self.screen[0])-1 and y == len(self.screen)-1):
						print('+',end='')
					elif x == 0 or x == len(self.screen[0])-1:
						print('|',end='')
					elif y == 0 or y == len(self.screen)-1:
						print('-',end='')
					elif [x,y] in self.moving.position or [x,y] in self.still.position:
						print(BLOCK,end='')
					else:
						print(' ',end='')
				print()
			sleep(self.speed)
		else:
			print("Game Over")

	def run(self):
		subprocess.call(["xset","-r"])
		oldterm = termios.tcgetattr(sys.stdin)
		newterm = termios.tcgetattr(sys.stdin)
		newterm[3] &= ~termios.ICANON & ~termios.ECHO
		newterm[6][termios.VTIME] = 0
		newterm[6][termios.VMIN] = 0
		termios.tcsetattr(sys.stdin, termios.TCSANOW, newterm)
		while not self.dead:
			try:
				self.events()
				self.logic()
				self.draw()
			except:
				self.dead = True
				termios.tcsetattr(sys.stdin, termios.TCSANOW, oldterm)
				subprocess.call(["xset","r"])
				raise
		termios.tcsetattr(sys.stdin, termios.TCSANOW, oldterm)
		subprocess.call(["xset","r"])

def main():
	game = Game()
	game.run()

if __name__ == "__main__":
	main()

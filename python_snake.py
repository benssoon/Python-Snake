#!/usr/bin/python3

from time import sleep
import random
import subprocess
import sys
import termios

DHEAD = '^'
UHEAD = 'v'
LHEAD = '>'
RHEAD = '<'
UP = [0,1]
RIGHT = [-1,0]
DOWN = [0,-1]
LEFT = [1,0]

SEG = 'o'
APPLE = '@'
HEIGHT = 23
WIDTH = 79
EASY = .2
NORMAL = .1
HARD = .06
INSANE = .04
IMPOSSIBLE = .01
PATH = '/home/ben/Documents/programming/python/snake'


class Game:

	def __init__(self):
		self.snake = [[39,12],[40,12],[41,12],[42,12]]
		self.head = LHEAD
		self.direction = LEFT
		self.change = []
		self.apple = [12,12]
		self.dead = False
		self.eaten = False
		self.paused = False
		self.quit = False
		self.score = 0
		self.text = "Score: %s"%self.score
		self.speed = 1
		if len(sys.argv) == 1:
			self.difficulty = "normal"	# Default difficulty
		else:
			self.difficulty = sys.argv[1]	# Set it to a command line specified difficulty
		self.parse_difficulty()

	def parse_difficulty(self):
		if self.difficulty == "easy":
			self.speed = EASY
			self.apple = [random.randint(10, WIDTH-10), random.randint(5,HEIGHT-5)]
		elif self.difficulty == "normal":
			self.speed = NORMAL
			self.apple = [random.randint(2,WIDTH-2), random.randint(2,HEIGHT-2)]
		elif self.difficulty == "hard":
			self.speed = HARD
			hard = []
			for x in range(2,11):
				for y in range(2,HEIGHT-1):
					hard.append([x,y])
			for x in range(WIDTH-10,WIDTH-1):
				for y in range(2,HEIGHT-1):
					hard.append([x,y])
			self.apple = random.sample(hard,1)[0]
		elif self.difficulty == "insane":
			self.speed = INSANE
			insane = []
			for x in range(1,2):
				for y in range(2,HEIGHT-1):
					insane.append([x,y])
			for x in range(WIDTH-1,WIDTH):
				for y in range(2,HEIGHT-1):
					insane.append([x,y])
			for x in range(1,WIDTH):
				for y in range(2,3):
					insane.append([x,y])
			for x in range(1,WIDTH):
				for y in range(HEIGHT-2,HEIGHT-1):
					insane.append([x,y])
			self.apple = random.sample(insane,1)[0] # Index to 0 because random.sample returns a list. Even though it's only a one-long list, you still need to index into it to get the coordinates.
		elif self.difficulty == "impossible":
			self.speed = IMPOSSIBLE
			impossible = [[1,2],[WIDTH-1,2],[1,HEIGHT-2],[WIDTH-1,HEIGHT-2]]
			self.apple = random.sample(impossible,1)[0]

	def changeDirection(self, direction):
		if (direction == "w" or direction == "k" or direction == "\x1b[A") and self.direction != [0,-1] and not self.paused:
			self.direction = UP
			self.head = UHEAD
			return
		elif (direction == "d" or direction == "l" or direction == "\x1b[C") and self.direction != [1,0] and not self.paused:
			self.direction = RIGHT
			self.head = RHEAD
			return
		elif (direction == "s" or direction == "j" or direction == "\x1b[B") and self.direction != [0,1] and not self.paused:
			self.direction = DOWN
			self.head = DHEAD
			return
		elif (direction == "a" or direction == "h" or direction == "\x1b[D") and self.direction != [-1,0] and not self.paused:
			self.direction = LEFT
			self.head = LHEAD
			return

	def pause(self):
		if self.direction != [0,0]:
			self.paused = True
			self.text = "PAUSED"
			self.pausedir = self.direction
			self.direction = [0,0]
			return
		else:
			self.text = "Score: %s"%self.score
			self.direction = self.pausedir
			self.paused = False
			return

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
				if self.apple in self.snake and self.apple != self.snake[0]:
					self.parse_difficulty()
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

	### Events ###
	def events(self):
		key = sys.stdin.read(3)
		if key != '':
			if key == "q" and not self.paused:
				self.quit = True
				self.pause()
				self.text = "Are you sure you want to quit? [Y/n]"
			elif key == " ":
				self.pause()
			elif key != "n" and self.quit:
				self.dead = True
			elif self.quit:
				self.pause()
				self.quit = False
			else:
				self.changeDirection(key)

	### Logic ###
	def logic(self):
		if not self.dead and not self.paused:
			head = [self.snake[0][0], self.snake[0][1]]
			self.snake[0][0] -= self.direction[0]
			self.snake[0][1] -= self.direction[1]
			for segment in range(1,len(self.snake)):
				seg = self.snake[segment]
				self.snake[segment] = head
				head = seg
			if self.eaten == True:
				self.eaten = False
				self.parse_difficulty() 
			elif self.snake[0] == self.apple:	# Grow snake
				self.eaten = True
				self.score += 1
				self.text = "Score: %s"%self.score
				s = self.snake[-1]
				self.snake.append([s[0]+self.direction[0], s[1]+self.direction[1]])
		if self.snake[0][0] == 0 or self.snake[0][1] == 1 or self.snake[0][0] == WIDTH or self.snake[0][1] == HEIGHT-1 or self.snake[0] in self.snake[1:]:
			self.dead = True

	### Draw ###
	def draw(self):
		if self.dead:
			highscores = open("%s/%s.data"%(PATH,self.difficulty))
			highscore = []
			for score in highscores:
				highscore.append(int(score.rstrip()))
			highscores.close()
			if highscore[0] < self.score:
				if highscore[0]-self.score == 1:
					print("You got a high score! Your score of %d beat the previous high score by %d point!"%(self.score, self.score-highscore[0]))
				else:
					print("You got a high score! Your score of %d beat the previous high score by %d points!"%(self.score, self.score-highscore[0]))
				highscores = open("%s/%s.data"%(PATH,self.difficulty),'w')
				highscores.write(str(self.score))
			"""
			else:
				highscores.close()
				print("Game Over")
			highscores = open("highscores.data",'r')
			highscores = list(highscores)
			for item in range(len(highscores)):
				highscores[item].rstrip()
				highscores[item] = int(highscores[item])
			print(highscores)
			f = open("highscores.data",'w')
			written = False
			temp = 0
			for score in highscores:
				if self.score > score:
					f.write(str(self.score))
					temp = score
					written = True
				elif temp > score:
					f.write(str(temp))
					temp = score
				else:
					f.write(str(score))
			if len(highscores) < 10 and not written:
				f = open("highscores.data",'a')
				f.write(str(self.score))
				f.close()
			f.close()
			"""
		elif not self.dead:
			for y in range(0,HEIGHT+1):
				printed = False
				for x in range(0,WIDTH+1):
					if (x == 0 or x == WIDTH) and y != 0:
						if y == HEIGHT and not printed:
							print(self.text)
							printed = True
						elif y == 1 or y == HEIGHT-1:
							print('+',end='')
						elif y != HEIGHT:
							print('|',end='')
					elif y == 1 or y == HEIGHT-1:
						print('-',end='')
					elif [x,y] in self.snake:
						if [x,y] == self.snake[0]:
							print(self.head,end='')
						else:
							print(SEG,end='')
					elif [x,y] == self.apple:
						print(APPLE,end='')
					elif y != HEIGHT and y != 0:
						print(' ',end='')
			sleep(self.speed)


def main():
	game = Game()
	game.run()

if __name__ == "__main__":
	main()

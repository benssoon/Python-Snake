#!/usr/bin/python3

################# To Do #################
# Add a query to ask where the player would like high scores to be saved.
#########################################

from time import sleep
import random
import subprocess
import sys
import termios
import os.path

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
EASY = ["easy",.2,.99,10,1]	#[speed, increment, mod] where speed refers to how much time between each frame and increment refers to how much this decreases when the the player gets more points.
NORMAL = ["normal",.1,.8,5,3]
HARD = ["hard",.06,.7,3,4]
INSANE = ["insane",.04,.6,2,5]
IMPOSSIBLE = ["impossible",.01,.5,1,6]
DIFFICULTY = 0	# For clearer indexing into the self.difficulty variable.
SPEED = 1	# For clearer indexing into the self.difficulty variable.
INCREMENT = 2	# For clearer indexing into the self.difficulty variable.
MOD = 3		# For clearer indexing into the self.difficulty variable.
GROWTH = 4	# For clearer indexing into the self.difficulty variable.
PATH = '.'	#Set path to save directory equal to current directory.		#'/home/ben/Documents/programming/python/snake'


class Game:

	def __init__(self):
		self.snake = [[39,12],[40,12],[41,12],[42,12]]
		self.head = LHEAD
		self.direction = LEFT
		self.change = []
		self.growing = 0
		self.apple = [12,12]
		self.appleLoc = []	# Possible locations for the apple.
		self.dead = False
		self.eaten = False
		self.paused = False
		self.quit = False
		self.score = 0
		self.text = "Score: %s"%self.score
		self.speed = 1
		self.difficulty = ["", 0, 0, 0]
		if len(sys.argv) == 1:
			self.difficulty[DIFFICULTY] = "normal"	# Default difficulty
		else:
			self.difficulty[DIFFICULTY] = sys.argv[1]	# Set it to a command line specified difficulty
		self.path = "%s/%s.data"%(PATH,self.difficulty[DIFFICULTY])
		if os.path.isfile(self.path) == False:
			new = open(self.path, 'w+')		#Make a new highscores file.
			new.write(str('0'))
			new.close()
		self.parse_difficulty()



	def parse_difficulty(self):			#Parse the difficulty passed to a speed and spawn behavior for the apple
		if self.difficulty[DIFFICULTY] == "easy":
			self.difficulty = EASY
			easy = []
			for x in range(10,WIDTH-10):
				for y in range(10,HEIGHT-10):
					easy.append([x,y])
			self.appleLoc = easy
		elif self.difficulty[DIFFICULTY] == "normal":
			self.difficulty = NORMAL
			normal = []
			for x in range(2,WIDTH-2):
				for y in range(2,HEIGHT-2):
					normal.append([x,y])
			self.appleLoc =	normal
		elif self.difficulty[DIFFICULTY] == "hard":
			self.difficulty = HARD
			hard = []
			for x in range(2,11):
				for y in range(2,HEIGHT-1):
					hard.append([x,y])
			for x in range(WIDTH-10,WIDTH-1):
				for y in range(2,HEIGHT-1):
					hard.append([x,y])
			self.appleLoc = hard
		elif self.difficulty[DIFFICULTY] == "insane":
			self.difficulty = INSANE
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
			self.appleLoc = insane
		elif self.difficulty[DIFFICULTY] == "impossible":
			self.difficulty = IMPOSSIBLE
			impossible = [[1,2],[WIDTH-1,2],[1,HEIGHT-2],[WIDTH-1,HEIGHT-2]]
			self.appleLoc = impossible
		self.speed = self.difficulty[SPEED]



	def placeApple(self):
		self.apple = random.sample(self.appleLoc,1)[0] # Index to 0 because random.sample returns [[x,y]]. I want to set self.apple to simply [x,y].



#############################################		USE THIS TO BETTER GROW THE SNAKE.       #########################
	def growSnake(self):
		if self.growing != 0:
			self.snake.append([self.snake[-1][0]+self.direction[0], self.snake[-1][1]+self.direction[1]])	# Grow snake
			self.growing -= 1
##########################################################################################################################



	def faster(self):
		if self.score%self.difficulty[MOD] == 0 and self.score != 0:
			self.speed *= self.difficulty[INCREMENT]



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
				if self.apple in self.snake and self.apple != self.snake[0]: # The apple spawned inside the body of the snake.
					self.placeApple
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
			head = [self.snake[0][0], self.snake[0][1]] # Set the head of the snake.
			self.snake[0][0] -= self.direction[0]	# Move head forward according to its direction.
			self.snake[0][1] -= self.direction[1]	
			for segment in range(1,len(self.snake)): # Move the rest of the snake forward.
				seg = self.snake[segment]
				self.snake[segment] = head
				head = seg
			self.growSnake() # Test if the snake needs to grow and grow it.
			if self.eaten == True:	# Place a new apple.
				self.eaten = False
				self.placeApple()
			elif self.snake[0] == self.apple: # Eat apple
				self.eaten = True
				self.score += 1
				self.faster()
				self.text = "Score: %s"%self.score
				self.growing = self.difficulty[GROWTH]
		if self.snake[0][0] == 0 or self.snake[0][1] == 1 or self.snake[0][0] == WIDTH or self.snake[0][1] == HEIGHT-1 or self.snake[0] in self.snake[1:]:	# Kill snake
			self.dead = True



	### Draw ###
	def draw(self):
		if self.dead:
			highscores = open(self.path)		#Open the highscore file for the current difficulty and read it.
			highscore = []
			for score in highscores:
				highscore.append(int(score.rstrip()))
			highscores.close()
			if highscore[0] < self.score:				#Check if the score is a high score, then save it.
				if highscore[0]-self.score == 1:
					print("You got a high score! Your score of %d beat the previous high score by %d point!"%(self.score, self.score-highscore[0]))
				else:
					print("You got a high score! Your score of %d beat the previous high score by %d points!"%(self.score, self.score-highscore[0]))
				highscores = open(self.path,'w')
				highscores.write(str(self.score))
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

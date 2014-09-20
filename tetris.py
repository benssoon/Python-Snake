#!/usr/bin/python3.3

import random
import pygame
pygame.init()

##########################################
#	Colors
##########################################
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
GREEN   = (   0, 255,   0)
RED     = ( 255,   0,   0)
BLUE    = (   0,   0, 255)
ORANGE  = ( 255, 128,   0)
PINK    = ( 245, 111, 176)
YELLOW  = ( 255, 255, 100)



##########################################
#	Screen Size
##########################################
WIDTH = 500
HEIGHT = 900



##########################################
#	Game Frame
##########################################
class Frame(pygame.sprite.Sprite):
	width = 400
	height = 543
	position = [50,50]

	#---------------------------------
	#	Init
	#---------------------------------
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(BLACK)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, WHITE, [0, 0, self.width, self.height], 3)
		self.rect.x = self.position[0]
		self.rect.y = self.position[1]

	#---------------------------------
	#	Update
	#---------------------------------
	#def update(self):



##########################################
#	Block
##########################################
class Block(pygame.sprite.Sprite):
	fall = 20

	#---------------------------------
	#	Init
	#---------------------------------
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)



##########################################
#	I
##########################################
class I(pygame.sprite.Sprite):
	fall = 30

	#---------------------------------
	#	Init
	#---------------------------------
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([125, 32])
		self.image.fill(WHITE)
		#self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, RED, [self.rect.x+ 1, self.rect.y+1, 30, 30], 0)
		pygame.draw.rect(self.image, RED, [self.rect.x+32, self.rect.y+1, 30, 30], 0)
		pygame.draw.rect(self.image, RED, [self.rect.x+63, self.rect.y+1, 30, 30], 0)
		pygame.draw.rect(self.image, RED, [self.rect.x+94, self.rect.y+1, 30, 30], 0)

	#---------------------------------
	#	Update
	#---------------------------------
	def update(self):
		self.rect.x = 200
		if self.rect.y < 50:
			self.rect.y = 50
		else:
			self.rect.y += self.fall



##########################################
#	J
##########################################
class J(Block):
	print("hello")



##########################################
#	L
##########################################
class L(Block):
	print("hello")



##########################################
#	O
##########################################
class O(Block):
	print("hello")



##########################################
#	S
##########################################
class S(Block):
	print("hello")



##########################################
#	T
##########################################
class T(Block):
	print("hello")



##########################################
#	Z
##########################################
class Z(Block):
	print("hello")



##########################################
#	Game Class
##########################################
class Game():

	#---------------------------------
	#	Attributes
	#---------------------------------
	blocks = None
	allSprites = None
	stillSprites = None
	gameOver = False
	score = 0
	activeBlock = None

	#---------------------------------
	#	Init
	#---------------------------------
	def __init__(self):
		self.blocks = pygame.sprite.Group()
		self.allSprites = pygame.sprite.Group()
		self.stillSprites = pygame.sprite.Group()
		self.gameOver = False
		self.score = 0

		# Create sprites. Do not add them to a list, this is just for easier access later.
		self.i = I()
		self.j = J()
		self.l = L()
		self.o = O()
		self.s = S()
		self.t = T()
		self.z = Z()
		self.frame = Frame()

		self.stillSprites.add(self.frame)
		self.allSprites.add(self.frame)
		self.blocks.add(self.i)
		self.allSprites.add(self.i)

	#---------------------------------
	#	Process Events
	#---------------------------------
	def process(self):
		for event in pygame.event.get():										# Step through pygame's list of events.
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):			# Quit if the x is clicked or if the user types Q.
				return True
			elif event.type == pygame.KEYDOWN:										# If a key was pressed, check if it was an arrow key.
				if event.key == pygame.K_LEFT:											# Move the piece left.
					print("LEFT")
				if event.key == pygame.K_RIGHT:											# Move the piece right.
					print("RIGHT")
				if event.key == pygame.K_UP:											# Rotate 90° clockwise.
					print("UP")
				if event.key == pygame.K_DOWN:											# Rotate 90° counterclockwise.
					print("DOWN")

	#---------------------------------
	#	Run Logic
	#---------------------------------
	def logic(self):
		if not self.gameOver:
			self.allSprites.update()		# Move any sprite that should be moving.
			#collisions = pygame.sprite.spritecollideany(self.activeBlock, self.stillSprites)

	#---------------------------------
	#	Display Frame
	#---------------------------------
	def display(self, screen):
		screen.fill(BLACK)

		if self.gameOver:
			print("Hello")
		else:
			self.allSprites.draw(screen)

		pygame.display.flip()



##########################################
#	Main
##########################################
def main():
	size = (WIDTH, HEIGHT)					# Size of the game screen.
	screen = pygame.display.set_mode(size)			# Create the screen.
	pygame.display.set_caption("Tetris")			# Title of window.
	done = False						# Used with the game over attribute.
	clock = pygame.time.Clock()
	pygame.mouse.set_visible(False)

	game = Game()

	while not done:
		done = game.process()
		game.logic()
		game.display(screen)
		clock.tick(3)

	pygame.quit()						# If the loop has ended, then game over attribute is true and therefore the game should quit.



if __name__ == "__main__":
	main()

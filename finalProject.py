import os
import random
import pygame
from pygame.locals import *

#Initializes Pygame. Variables are set here.
pygame.init()

img_dir = os.path.dirname(os.path.abspath(__file__))
#file_path = os.path.join(img_dir, filename)

screen_width = 1200
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Final Platformer')


#rect_1 = pygame.Rect(200, 100, 150, 100)

clock = pygame.time.Clock()

tile_size = 30

game_won = 0


#random color list
color_list = ["Red", "Blue", "Green"]
index = random.randrange(len(color_list))
rand_color = str(color_list[index])

#load images
#sun_img = pygame.image.load(os.path.join(img_dir, 'sun.png'))
bg_img = pygame.image.load(os.path.join(img_dir, 'bg1.png'))


#player stats
movement_spd = 10
jump_vel = 30
fall_spd = 3


def draw_grid():
	for line in range(0, 50):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Win(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_dir, 'goal.png'))
		self.image = pygame.transform.scale(self.image, (90, 60))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class WinScreen(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_dir, 'win.png'))
		self.image = pygame.transform.scale(self.image, (1200, 900))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self,game_won):
		
		if game_won == 1:
			screen.blit(self.image, self.rect)


class Player():
	def __init__(self, x, y):
		img = pygame.image.load(os.path.join(img_dir, 'guy1.png'))
		self.image = pygame.transform.scale(img, (30, 30))
		self.image_right = pygame.transform.scale(self.image, (30, 30))
		self.image_left = pygame.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.in_midair = False
		self.direction = 1
		self.do_once = 0
		
		

	def update(self,game_won):
		dx = 0
		dy = 0
		

		#get keypresses
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and self.in_midair == False:
			self.vel_y = -jump_vel
			self.in_midair = True
		#if key[pygame.K_SPACE] == False:
		#	self.jumped = False
		if key[pygame.K_LEFT]:
			dx -= movement_spd
			self.direction = -1
			self.image = self.image_left
			#self.image = pygame.transform.flip(self.image, True, False)
			#self.image = pygame.transform.rotate(self.image, 180)
		if key[pygame.K_RIGHT]:
			dx += movement_spd
			self.direction = 1
			self.image = self.image_right
			#self.image = pygame.transform.flip(self.image, False, False)
			#self.image = pygame.transform.rotate(self.image, 0)
		if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
			if self.direction == 1:
				self.image = self.image_right
				#self.image = pygame.transform.flip(self.image, False, False)
			if self.direction == -1:
				self.image =  self.image_left
				#self.image = pygame.transform.flip(self.image, True, False)
			


		#gravity
		self.vel_y += fall_spd
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y

		#collision
		for tile in world.tile_list:
			#check for collision in x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			#check for collision in y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground i.e. jumping
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				#	self.in_midair = False
				#check if above the ground i.e. falling
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
					self.in_midair = False

		#if pygame.sprite.spritecollide(self, Win, False):
		#		print("You Win!")

		if pygame.sprite.spritecollide(self, goal_group, False):
			game_won = 1


		self.rect.x += dx
		self.rect.y += dy



		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0
		
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

		if game_won == 1 and self.do_once == 0:
			print("You Win!")
			self.do_once = 1
			#screen.blit(WinScreen, self.rect)
			#pygame.transform.scale(img, (30, 30))


		
	
		return game_won

class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load(os.path.join(img_dir, 'wall2.png'))
		grass_img = pygame.image.load(os.path.join(img_dir, 'wall.png'))

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					goal = Win(col_count * tile_size, row_count * tile_size + 15)
					goal_group.add(goal)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])



world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1],
[1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 2, 1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


goal_group = pygame.sprite.Group()

player = Player(60, screen_height - 90)
goal = Win(80, screen_height - 90)
world = World(world_data)
winScreen = WinScreen(0, 0)


#Game Loop
running = True

while running:
	
    screen.blit(bg_img, (0, 0))
    #screen.blit(sun_img, (100, 100))
    
    world.draw()


    goal.update()
    #player.update()
	

    if game_won == 0:
        goal_group.update()
	
    goal_group.draw(screen)

    #draw_grid()
    game_won = player.update(game_won)
    winScreen.update(game_won)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type ==  pygame.KEYDOWN and event.key == pygame.K_f:
            pygame.display.toggle_fullscreen()
    
    pygame.display.update()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()


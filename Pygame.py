import pygame

pygame.init()

#Create the window
screen = pygame.display.set_mode((800, 600))
#Create a clock object
clock = pygame.time.Clock()
#Set the title of the window
pygame,display.set_caption("My Python Game")

#Start the game loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	#Fill the screen with the color
	screen.fill((0,0,0))
	#Updates the WHOLE screen
	pygame.display.flip()
	#or uptdate only a part of the screen - w/o an argument
	pygame.display.update(objects_to_update)
	clock.tick(60)
pygame.quit()
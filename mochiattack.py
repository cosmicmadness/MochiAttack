#---------------------------------------------------------------------------------------------------
# Description:      Mochi Attack game             
# Python Author:    Joanne Quan
# Date created:     September 27, 2022
#---------------------------------------------------------------------------------------------------

# Play instructions
# Use the left and right arrow keys to control the player's left and right movements.
# Use the up arrow key to fire a laser. Only one laser can be fired at a time. Once fired,
# the laser can't be fired again until either it hits a mochi or it goes off the screen. 
# There are three types of mochi: blue - large; pink - medium; green - small. Blue mochis
# move the slowest and they convert to a pink mochi when hit. Pink mochis move faster than
# large mochis but move slower than green mochis and they convert to a green mochi when hit.
# Green mochis move the fastest and disappear when hit.
# The player earns 1 point for hitting a blue mochi; 2 points for hitting a pink mochi; 3
# points for hitting a green mochi.

# In V1, the player loses as soon as they are hit by a mochi. In subsequent improvements of this
# game, I may consider changing this so that the player has more chances to survive.

import pygame, random


# Define screen properties
screen_width = 600
screen_height = 800
game_width = screen_width * 0.9
game_height = screen_height * 0.9
fps = 30

# Define the boundaries of the game screen 
boundary_left = (screen_width - game_width)/2
boundary_right = boundary_left + game_width
boundary_top = (screen_height - game_height)/2
boundary_bottom = boundary_top + game_height

# Initiate PyGame
pygame.init()

# Define a font
myfont = pygame.font.Font('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Fonts\\press_start.ttf', 18)
title_font = pygame.font.Font('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Fonts\\press_start.ttf', 24)

# Define the game display 
screen = pygame.display.set_mode((screen_width, screen_height))
game_screen = pygame.Surface((game_width, game_height))

# Display the window title
pygame.display.set_caption("Mochi Attack!")

# Create an instance of the clock
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Images\\spaceship_sprite.png')
laser_img = pygame.image.load('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Images\\laser.png')
mochi_green_img = pygame.image.load('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Images\\mochi_green.png')
mochi_blue_img = pygame.image.load('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Images\\mochi_blue.png')
mochi_pink_img = pygame.image.load('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Images\\mochi_pink.png')


# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = player_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_speed(self):
        return self.speed
    
    def set_speed(self, speed):
        self.speed = speed
    
    def shoot(self, screen):
        self.shoot_sound = pygame.mixer.Sound('D:\\Joanne\\PythonPractice\\MochiAttack\\Assets\\Sounds\\shoot.wav')
        self.shoot_sound.set_volume(0.5)
        self.shoot_sound.play()


# Define the laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.speed = 15
        self.rect.topleft = [x, y]
    def update(self):
        self.rect.y -= self.speed
        self.rect.x += 0
    
    def set_speed(self, speed):
        self.speed = speed


# Define the mochi (enemy) class
class Mochi(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        if self.size == 'small':
            self.image = mochi_green_img
            self.speed = random.randint(7, 10)
            mochi_size = 0.3
        elif self.size == 'medium':
            self.image = mochi_pink_img
            self.speed = random.randint(5, 7)
            mochi_size = 0.4
        elif self.size == 'large':
            self.image = mochi_blue_img
            self.speed = random.randint(2, 4)
            mochi_size = 0.5
        else:
            self.speed = random.randint(7, 10)
            mochi_size = 0.3
            
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * mochi_size, self.image.get_height() * mochi_size)) 
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        #self.mochi_change_x = 1
        #self.mochi_change_y = -1
        self.mochi_change_x = random.choice([-1, 1])
        self.mochi_change_y = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.mochi_change_x
        self.rect.y += self.speed * self.mochi_change_y

    def change_direction_x(self):
        self.mochi_change_x = -self.mochi_change_x

    def change_direction_y(self):
        self.mochi_change_y = -self.mochi_change_y

    def getSize(self):
        return self.size

# Define button class
class Button():
    def __init__(self, x, y, button_width, button_height, text, font, text_color, button_color, hover_color):
        self.x = x
        self.y = y
        self.button_width = button_width
        self.button_height = button_height
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.font = font
        self.text = self.font.render(text, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(x, y))


    def update(self, screen):
        pygame.draw.rect(screen, self.button_color, (self.x - (self.button_width//2), self.y - (self.button_height//2), self.button_width, self.button_height))
        screen.blit(self.text, self.text_rect)

    def isClicked(self, mouse_position):
        if mouse_position[0] in range(self.x - (self.button_width//2), self.x + (self.button_width//2)) and mouse_position[1] in range(self.y - (self.button_height//2), self.y + (self.button_height//2)):
            return True
        return False


# Instantiate the player
player_speed = 8
player = Player(player_speed)
player.rect.x = screen_width/2 - player.image.get_width()/2
player.rect.y = screen_height - (screen_height - game_height)/2 - player.image.get_height()


SPAWN_MOCHI = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_MOCHI, 4000)
mochi_sizes = ['small', 'medium', 'large']

# Instantiate the sprite groups
mochi_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()


# Onboarding screen
def intro():
    #pygame.display.set_caption("Mochi Attack!")
    
    # Game loop
    while True:
        screen.fill("black")
        mouse_position = pygame.mouse.get_pos()
        welcome_text = title_font.render("Mochi Attack!", True, "White")
        welcome_rect = welcome_text.get_rect(center=(screen_width//2, 260))
        # Display text
        screen.blit(welcome_text, welcome_rect)

        # Display play button
        play_button = Button(((screen_width//2) - (200//2) - 10), screen_height//2, 150, 50, "PLAY", myfont, "White", "Blue", "White")
        play_button.update(screen)

        # Display quit button
        quit_button = Button(((screen_width//2) + (200//2) + 10), screen_height//2, 150, 50, "QUIT", myfont, "White", "Blue", "White")
        quit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If play button is clicked then show game screen
                if play_button.isClicked(mouse_position):
                    main()
                # If quit button is clicked then quit the game
                if quit_button.isClicked(mouse_position):
                    quit()
        
        pygame.display.update()

def gameover():
    #pygame.display.set_caption("Mochi Attack!")
    
    # Game loop
    while True:
        mouse_position = pygame.mouse.get_pos()
        gameover_text = title_font.render("Game Over", True, "White")
        gameover_rect = gameover_text.get_rect(center=(screen_width//2, 260))
        # Display text
        screen.blit(gameover_text, gameover_rect)


        # Display play button
        play_button = Button(((screen_width//2) - (200//2) - 10), screen_height//2, 200, 50, "PLAY AGAIN", myfont, "White", "Blue", "White")
        play_button.update(screen)

        # Display quit button
        quit_button = Button(((screen_width//2) + (200//2) + 10), screen_height//2, 200, 50, "QUIT", myfont, "White", "Blue", "White")
        quit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If play button is clicked then show game screen
                if play_button.isClicked(mouse_position):
                    main()
                # If quit button is clicked then quit the game
                if quit_button.isClicked(mouse_position):
                    quit()
        
        #pygame.display.update()
        pygame.display.flip()


def main():
    # Initialize parameters
    score = 0
    laser_fired = False
    killed = False
    mochi_group.empty()
    laser_group.empty()

    # Begin the game with mochis already spawned
    for mochi in range(3):
        mochi_size = random.choice(mochi_sizes)
        new_mochi = Mochi(random.randint(boundary_left, (boundary_right-100)), boundary_top, mochi_size)
        mochi_group.add(new_mochi)

    # Game loop
    while True:

        screen.fill("darkgrey")
        game_screen.fill("black")
        screen.blit(game_screen, (boundary_left, boundary_top))

        # Add the player to the screen
        screen.blit(player.image, (player.rect.x, player.rect.y))

        # Score label
        score_label = myfont.render(f"Score: {score}", True, (0, 255, 0))

        # Event handler
        for event in pygame.event.get():
            # Quit the game if the user closes the window
            if event.type == pygame.QUIT:
                exit()
            # If the K_UP key is pressed, fire the laser. Limit to one fire at a time to prevent spamming
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if laser_fired == False:
                        player.shoot(screen)
                        laser_fired = True
                        laser = Laser(player.rect.x + player_img.get_width()/2, player.rect.y)
                        laser_group.add(laser)
            # Spawn new mochi 
            if event.type == SPAWN_MOCHI:
                mochi_size = random.choice(mochi_sizes)
                new_mochi = Mochi(random.randint(boundary_left, (boundary_right-100)), boundary_top, mochi_size)
                mochi_group.add(new_mochi)
            
                
        # Get pressed keys and handle user key inputs to move the player
        key = pygame.key.get_pressed()
        # Move left
        if key[pygame.K_LEFT] and player.rect.left > boundary_left:
            player.rect.x += -player.get_speed()
        # Move right
        if key[pygame.K_RIGHT] and player.rect.right < boundary_right:
            player.rect.x += player.get_speed()


        # Keep the mochi within the bounds of the game area
        for mochi in mochi_group:
            # Collision with left and right walls
            if mochi.rect.x < boundary_left or mochi.rect.x > (boundary_right - mochi.image.get_width()):
                mochi.change_direction_x()
            # collision with top and bottom walls
            if mochi.rect.y < boundary_top or mochi.rect.y > (boundary_bottom - mochi.image.get_height()):
                mochi.change_direction_y()



        # Handle laser behaviour
        for laser in laser_group:
            # If laser goes off screen then remove it
            if laser.rect.y < boundary_top:
                laser_group.remove(laser)
                laser_fired = False
            # Handle behaviour if mochi and laser collide
            collided = pygame.sprite.spritecollide(laser, mochi_group, False)
            
            # If mochi sizes are large or medium, split the mochi down a size
            for collided_mochi in collided:
                if collided_mochi.getSize() == 'large':
                    score += 1
                    laser_group.remove(laser)
                    laser_fired = False
                    new_mochi = Mochi(collided_mochi.rect.x, collided_mochi.rect.y, 'medium')
                    mochi_group.add(new_mochi)
                    mochi_group.remove(collided_mochi)
                    
                elif collided_mochi.getSize() == 'medium':
                    score += 2
                    laser_group.remove(laser)
                    laser_fired = False
                    new_mochi = Mochi(collided_mochi.rect.x, collided_mochi.rect.y, 'small')
                    mochi_group.add(new_mochi)
                    mochi_group.remove(collided_mochi)
                    
                else:
                    laser_group.remove(laser)
                    laser_fired = False
                    mochi_group.remove(collided_mochi)
                    score += 3


        # Update the score
        screen.blit(score_label, (boundary_left + 10, boundary_top + 10))

        # Update the mochi
        mochi_group.draw(screen)
        mochi_group.update()
        
        laser_group.draw(screen)
        laser_group.update()

        # Handle collisions between player and mochis
        #killed = pygame.sprite.spritecollide(player, mochi_group, False)
        for mochi in mochi_group:
            killed = pygame.sprite.collide_mask(player, mochi)
            if killed:
                gameover()

        # Update the screen
        pygame.display.flip()
        clock.tick(fps)

# Initiate the intro screen
intro()



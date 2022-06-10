#import libraries
import pygame
import random

#initialise pygame
pygame.init()

#game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Strawberry climbing')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game variables
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
MAX_BERRY = 5
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0
Strawberry_health = 30

#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#define font
font_small = pygame.font.SysFont('Caveat', 20)
font_big = pygame.font.SysFont('Caveat', 24)

#load images
jumpy_image = pygame.image.load('FlipStrawberry.png').convert_alpha()
bg_image = pygame.image.load('bg.png').convert_alpha()
platform_image = pygame.image.load('SMALL PLATFORM.png').convert_alpha()
blueberry = pygame.image.load('ItemBlueberry.png').convert_alpha()

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

#function for drawing the background
def draw_bg(bg_scroll):
        screen.blit(bg_image, (0, 0 + bg_scroll))
        screen.blit(bg_image, (0, -600 + bg_scroll))

#player class
class Player():
        def __init__(self, x, y):
                self.image = pygame.transform.scale(jumpy_image, (45, 45))
                self.width = 25
                self.height = 40
                self.rect = pygame.Rect(0, 0, self.width, self.height)
                self.rect.center = (x, y)
                self.vel_y = 0
                self.flip = False

        def move(self):
                #reset variables
                scroll = 0
                dx = 0
                dy = 0

                #process keypresses
                key = pygame.key.get_pressed()
                if key[pygame.K_a]:
                        dx = -10
                        self.flip = True
                if key[pygame.K_d]:
                        dx = 10
                        self.flip = False

                #gravity

                self.vel_y += GRAVITY
                dy += self.vel_y
                # manual jump
                self.is_jumping = True
                self.is_falling = False
                #WORK ON  THIS 6/9/22
                #https://opensource.com/article/19/12/jumping-python-platformer-game
                def Gravity(self):
                        if (self.is_jumping):
                                self.moveY += 3.5
                                

                #ensure player doesn't go off the edge of the screen
                if self.rect.left + dx < 0:
                        dx = -self.rect.left
                if self.rect.right + dx > SCREEN_WIDTH:
                        dx = SCREEN_WIDTH - self.rect.right


                #check collision with platforms
                for platform in platform_group:
                        #collision in the y direction
                        if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                #check if above the platform
                                if self.rect.bottom < platform.rect.centery:
                                        if self.vel_y > 0:
                                                self.rect.bottom = platform.rect.top
                                                dy = 0
                                                self.vel_y = -20

                #check if the player has bounced to the top of the screen
                if self.rect.top <= SCROLL_THRESH:
                        #if player is jumping
                        if self.vel_y < 0:
                                scroll = -dy

                #update rectangle position
                self.rect.x += dx
                self.rect.y += dy + scroll

                return scroll

        def draw(self):
                screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
                pygame.draw.rect(screen, WHITE, self.rect, 2)



#platform class
class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, width):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(platform_image, (width, 60))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

        def update(self, scroll):

                #update platform's vertical position
                self.rect.y += scroll

                #check if platform has gone off the screen
                if self.rect.top > SCREEN_HEIGHT:
                        self.kill()
class Blueberry(pygame.sprite.Sprite):
        def __init__(self, x, y, width):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(blueberry, (80, 80))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
        def update(self, scroll):
                self.rect.y += scroll
                if self.rect.top > SCREEN_HEIGHT:
                        self.kill()

#player instance
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()
berry_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)
#create starting blueberry
berry = Blueberry(SCREEN_WIDTH // 2 -45, SCREEN_HEIGHT -45, 80)
berry_group.add(berry)

#game loop
run = True
while run:

        clock.tick(FPS)

        if game_over == False:
                scroll = jumpy.move()

                #draw background
                bg_scroll += scroll
                if bg_scroll >= 600:
                        bg_scroll = 0
                draw_bg(bg_scroll)

                #generate platforms
                if len(platform_group) < MAX_PLATFORMS:
                        p_w = random.randint(40, 60)
                        p_x = random.randint(0, SCREEN_WIDTH - p_w)
                        p_y = platform.rect.y - random.randint(80, 120)
                        platform = Platform(p_x, p_y, p_w)
                        platform_group.add(platform)
                #generate blueberries
                if len(berry_group) < MAX_BERRY:
                        b_w = 5
                        b_y = p_y - 30
                        b_x = p_x - 100
                        berry = Blueberry(p_x, p_y - 30, b_w)
                        berry_group.add(berry)


                #update platforms and blueberries
                platform_group.update(scroll)
                berry_group.update(scroll)

                #draw sprites
                platform_group.draw(screen)
                jumpy.draw()
                berry_group.draw(screen)

                #check game over
                if jumpy.rect.top > SCREEN_HEIGHT:
                        game_over = True
        else:
                if fade_counter < SCREEN_WIDTH:
                        fade_counter += 5
                        for y in range(0, 6, 2):
                                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
                draw_text('GAME OVER!', font_big, WHITE, 130, 200)
                draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
                draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                        #reset variables
                        game_over = False
                        score = 0
                        scroll = 0
                        fade_counter = 0
                        #reposition jumpy
                        jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                        #reset platforms
                        platform_group.empty()
                        berry_group.empty()
                        #create starting platform
                        platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
                        platform_group.add(platform)


        #event handler
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False


        #update display window
        pygame.display.update()

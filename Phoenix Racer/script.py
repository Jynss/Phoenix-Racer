import pygame
import random
import os        
import sys                     
# WHAT IS MISSING
# - Stop obstacles from coming one ontop of each other
# - Levels?

WIDTH = 1280
HEIGHT = 720
DURATION = 1504
FPS = 30
GOLD = (255, 217, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0 )
RED = (255, 0,0 )
BLUE = (0, 0, 255)
BACKGROUND = 'desert.jpg'
SONG = 'racing.wav'
CARS = ['car.png', 'car2.png', 'car3.png']
TORNADO = 'tornado.jpg'
TORNADO_ICON = 'tornado.png'
TREASURE = 'treasure.png'
FONT = 'Retro Gaming'
LOGO = 'logo2.png'
GATE1= 'gate left.png'
GATE2 = 'gate right.png'
POWER_UP = 'coin.png'
POWER_SONG = 'coin.wav'
CRASH = 'crash.wav'
WIN = 'win.wav'
HIGH_SCORE_FILE = 'high_score.txt'
progress_bar_width = 5
player_score = 0
multiplier = 1
count = 0
highest_score = 0
new_high_score = True

game_folder = os.path.dirname(__file__)
auxiliary_files = os.path.join(game_folder, 'media')

#High Score
with open(os.path.join(auxiliary_files, HIGH_SCORE_FILE), 'r') as file:
    highest_score = int(file.read())

font_name = pygame.font.match_font(FONT)
def draw_text(surface, text, colour, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect) 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        car = random.choice(CARS)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(auxiliary_files, car)).convert()
        self.image = pygame.transform.scale(self.image, (300,200))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 80
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH/2 , HEIGHT - 100)
        self.y_speed = 0 
        self.x_speed = 0

    def update(self):
        self.x_speed = 0
        self.y_speed = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x_speed = -15
        if keystate[pygame.K_RIGHT]:
            self.x_speed = 15
        if keystate[pygame.K_DOWN]:
            self.y_speed = 10
        if keystate[pygame.K_UP]:
            self.y_speed = -10
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.right > WIDTH-165:
            self.rect.right = WIDTH-165
        elif self.rect.left < 165:
            self.rect.left = 165
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class ObstacleCreator:
    def __init__(self, obstacle_group):
        self.time = 0
        bird = Obstacle('bird.png', 120, 120)
        bird2 = Obstacle('bird.png', 120, 120)
        rock = Obstacle('rock.png')
        rock2 = Obstacle('rock2.png')
        cactus = Obstacle('cactus.png')
        cactus2 = Obstacle('cactus2.png')
        self.tornado_icon = Obstacle(TORNADO_ICON)
        self.tornado_icon.rect.y = 0
        self.obstacles = [bird, rock, cactus, rock2, cactus2, bird2]
        self.obstacle_group = obstacle_group
        for obstacle in self.obstacles:
            self.obstacle_group.add(obstacle)


    def reposition(self):
        for obstacle in self.obstacles:
            if obstacle.rect.top > HEIGHT:
                obstacle.rect.x = random.randint(250, WIDTH-400)
                obstacle.rect.y = random.randint(-1500, -40)

    def update(self):
        if self.time == 650:
            self.obstacle_group.add(self.tornado_icon)
        elif self.time >= 950:
            self.tornado_icon.kill()
 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, width = 80, length =80):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(auxiliary_files, image)) #.convert()
        #self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (width, length))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .7 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #self.rect.center = (WIDTH/2 , HEIGHT/2)
        self.rect.right = random.randint(250 + width , WIDTH-400)
        self.rect.y = random.randint(-6000, 0)
        self.y_speed = 10

    def update(self):
        self.rect.y += self.y_speed

class PowereUpCreator:
    def __init__(self, group):
        self.time = 0
        coin = PowerUp(POWER_UP)
        coin1 = PowerUp(POWER_UP)
        coin2 = PowerUp(POWER_UP)
        coin3 = PowerUp(POWER_UP)
        coin4 = PowerUp(POWER_UP)
        coin5 = PowerUp(POWER_UP)
        self.power_ups = [coin, coin2, coin3, coin1, coin4, coin5]
        self.power_up_group = group
        for power in self.power_ups:
            self.power_up_group.add(power)


    def reposition(self):
        for power in self.power_up_group:
            if power.rect.top > HEIGHT:
                power.rect.x = random.randint(250, WIDTH-400)
                power.rect.y = random.randint(-50000, -40)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, width = 80, length =80):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(auxiliary_files, image)) #.convert()
        #self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (width, length))
        self.rect = self.image.get_rect()
        self.radius = 32
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #self.rect.center = (WIDTH/2 , HEIGHT/2)
        self.rect.right = random.randint(250 + width , WIDTH-400)
        self.rect.y = random.randint(-50000, 0)
        self.y_speed = 15

    def update(self):
        self.rect.y += self.y_speed

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, explosion_images):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate =  30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Road:

    PARTITION_WIDTH = 10
    PARTITION_HEIGHT = 100
    SPACE_IN_BETWEEN_INC = 140
    OFFSET = 10
    
    def __init__(self):
        self.road_partitions = []
        space_in_between = 0
        start_position = -Road.SPACE_IN_BETWEEN_INC # Start offscreen

        # Get road partitions starting with the first one in an offscreen location
        for i in range(6):
            self.road_partitions.append([WIDTH/2, start_position + Road.OFFSET + space_in_between, \
                                        Road.PARTITION_WIDTH, Road.PARTITION_HEIGHT])
            space_in_between += Road.SPACE_IN_BETWEEN_INC

        
    def draw(self, screen, speed):
        """
        Description: draws the road
        screen :- the display surface to draw on
        speed :- the speed at which road partitions move
        """
        pygame.draw.rect(screen, BLACK, (250,0,WIDTH-500, HEIGHT))

        for partition in self.road_partitions:
            pygame.draw.rect(screen, WHITE, partition)
            partition[1] += speed

        # If a road partition that is last in the queue goes offscreen then move to the front.
        INDEX_OF_LAST_ELEMENT = len(self.road_partitions) - 1
        INDEX_OF_Y_COORDINATE = 1

        if self.road_partitions[INDEX_OF_LAST_ELEMENT][INDEX_OF_Y_COORDINATE] >= HEIGHT + Road.OFFSET:
            last_element = self.road_partitions.pop()
            first_element = self.road_partitions[0]
            last_element[INDEX_OF_Y_COORDINATE] = first_element[INDEX_OF_Y_COORDINATE] - (Road.SPACE_IN_BETWEEN_INC + Road.OFFSET)
            self.road_partitions.insert(0, last_element)

class Gates(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(auxiliary_files, image)).convert()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (100,200))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2 , HEIGHT/2)
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 10

    def update(self):
        self.rect.y += self.y_speed

def tornado(screen):
    tornado = pygame.image.load(os.path.join(auxiliary_files, TORNADO)).convert()
    tornado = pygame.transform.scale(tornado, (1280,720))
    tornado.set_alpha(230)
    screen.blit(tornado, (0,0))

def progress_bar(time, progress_bar_width):
    draw_text(screen, 'Progress Bar', WHITE,20, 90 , 0)
    if time % 100 == 0:
        progress_bar_width += (50/3)
    pygame.draw.rect(screen, BLACK, (0, 25, 249, 20))
    pygame.draw.rect(screen, GREEN, (0,25, progress_bar_width, 20))
    return progress_bar_width

def score(screen, time, multiplier):
    draw_text(screen, 'Score', WHITE, 20, 1150 , 0)
    pygame.draw.rect(screen, BLACK, (1100, 24, 110, 20))
    draw_text(screen, str(time* 4 *multiplier), WHITE, 15, 1150,24)
    return time * 4 * multiplier

def coins(screen, count):
    draw_text(screen, 'Coins', WHITE,20, 1150 , 100)
    pygame.draw.rect(screen, BLACK, (1120, 124, 48, 20))
    draw_text(screen,'X', WHITE,20,1180, 120)
    draw_text(screen, str(count), WHITE, 15, 1142,124)
    coin_pic = pygame.image.load(os.path.join(auxiliary_files, POWER_UP)).convert()
    coin_pic = pygame.transform.scale(coin_pic, (20,20))
    coin_pic.set_colorkey(BLACK)
    screen.blit(coin_pic, (1200,124 ))

def high_score(screen, score):
    draw_text(screen, 'High Score', WHITE, 20, 1150 , 200)
    pygame.draw.rect(screen, BLACK, (1100, 224, 110, 20))
    draw_text(screen, str(score), WHITE, 15, 1153,224)
    
def show_splash_screen(screen):
    screen.blit(desert, (0,0))
    logo = pygame.image.load(os.path.join(auxiliary_files, LOGO))
    logo = pygame.transform.scale(logo, (300,300))
    #logo.set_colorkey(BLACK)
    logo_rect = logo.get_rect()
    logo_rect.bottomright = (WIDTH + 45, HEIGHT + 50)
    ex_why = logo_rect.topleft
    draw_text(screen, "Welcome to Phoenix Racer: ", WHITE, 64 , WIDTH/2, 0)
    draw_text(screen, "Gatekeeper's Treasure", GOLD, 64 , WIDTH/2, 60)

    draw_text(screen, "Watch out for vultures, cacti, rocks", WHITE, 45 , WIDTH/2, 300)
    draw_text(screen, "and the occasional TORNADO!!", WHITE, 45 , WIDTH/2, 360)
    draw_text(screen, "Collect coins for extra points", GOLD, 35 , WIDTH/2, 410)

    draw_text(screen, "Use the arrow keys to move", WHITE, 40, WIDTH/2, (HEIGHT/2) +200)
    draw_text(screen, 'Press any key to begin', WHITE, 40, WIDTH/2, (HEIGHT * 3/4) +100)
    screen.blit(logo, (ex_why))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    pygame.time.delay(500)

def show_game_over_screen(screen, score, new_high_score):
    screen.blit(desert, (0,0))  
    draw_text(screen, "GAME OVER", WHITE,64 , WIDTH/2, HEIGHT/4)
    draw_text(screen, "Score: "+ str(score), WHITE, 40 , (WIDTH/2), (HEIGHT/4)+100)
    draw_text(screen, "Use the arrow keys to move", WHITE, 22, WIDTH/2, (HEIGHT/2) + 100)
    draw_text(screen, 'Press any key to start over', WHITE, 18, WIDTH/2, HEIGHT * 3/4)
    if new_high_score:
        draw_text(screen, 'New High Score !!!', GOLD,35, WIDTH/2, (HEIGHT/4)+160)
        with open(os.path.join(auxiliary_files, HIGH_SCORE_FILE), 'w') as file:
            file.write(str(highest_score))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    pygame.time.delay(800)

def show_player_win(screen, score, new_high_score):
    draw_text(screen, "You Win", WHITE,64 , WIDTH/2, HEIGHT/4)
    draw_text(screen, "Score: "+ str(score), WHITE, 40 , (WIDTH/2), (HEIGHT/4)+100)
    draw_text(screen, 'Press any key to play again', WHITE, 22, WIDTH/2, HEIGHT -200)
    treasure = pygame.image.load(os.path.join(auxiliary_files, TREASURE)).convert()
    treasure = pygame.transform.scale(treasure, (120,120))
    #treasure.set_colorkey(BLACK)
    screen.blit(treasure, ((WIDTH/2) - 40,(HEIGHT/3) + 145 ))
    if new_high_score:
        draw_text(screen, 'New High Score !!!', GOLD, 35, WIDTH/2, (HEIGHT/4)+160)
        with open(os.path.join(auxiliary_files, HIGH_SCORE_FILE), 'w') as file:
             file.write(str(highest_score))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    pygame.time.delay(1500)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Phoenix Racer: Gatekeeper\'s Treasure')
clock = pygame.time.Clock()

explosion_images = []
for i in range(9):
    filename =  'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(auxiliary_files, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (60, 60))
    explosion_images.append(img)

song = pygame.mixer.Sound(os.path.join(auxiliary_files, SONG))
song.set_volume(0.03)
song.play(-1)
power_up_music = pygame.mixer.Sound(os.path.join(auxiliary_files, POWER_SONG))
crash_music = pygame.mixer.Sound(os.path.join(auxiliary_files, CRASH))
crash_music.set_volume(0.15)
win_music = pygame.mixer.Sound(os.path.join(auxiliary_files, WIN))

desert = pygame.image.load(os.path.join(auxiliary_files, BACKGROUND))
desert = pygame.transform.scale(desert, (WIDTH,HEIGHT))
logo = pygame.image.load(os.path.join(auxiliary_files, LOGO))
logo = pygame.transform.scale(logo, (200,200))
logo_rect = logo.get_rect()
logo_rect.bottomright = (WIDTH + 45, HEIGHT + 50)
ex_why = logo_rect.topleft

#Game Loop
time = 0
lose_count_down = 9
start_game = True
player_win = False
game_over = True
game_about_to_end = False
running = True
while running:
    if start_game:
        show_splash_screen(screen)
        start_game = False
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        gates = pygame.sprite.Group()
        tornado_sprite = Obstacle(TORNADO_ICON)
        player = Player()
        all_sprites.add(player)
        obstacles_creator = ObstacleCreator(obstacles)
        powers = pygame.sprite.Group()
        power_up_creator = PowereUpCreator(powers)
        road = Road()
        gate_l = Gates(GATE1, 250, 0)
        gate_r = Gates(GATE2, WIDTH-350, 0)
        time = 0
        progress_bar_width = 0
        multiplier = 1
        game_over = False
        count = 0
        new_high_score = True

    if game_over:   
        game_over = False
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        tornado_sprite = Obstacle(TORNADO_ICON)
        gates = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        obstacles_creator = ObstacleCreator(obstacles)
        road = Road()
        gate_l = Gates(GATE1, 250, 0)
        gate_r = Gates(GATE2, WIDTH-350, 0)
        powers = pygame.sprite.Group()
        power_up_creator = PowereUpCreator(powers)
        time = 0
        progress_bar_width = 0
        multiplier = 1
        game_about_to_end  = False
        count = 0
        if player_score > highest_score:
            highest_score = player_score
            new_high_score = True
        else:
            new_high_score = False
        show_game_over_screen(screen, player_score, new_high_score)
        

    if player_win:
        win_music.play()
        player_win = False
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        tornado_sprite = Obstacle(TORNADO_ICON)
        gates = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        obstacles_creator = ObstacleCreator(obstacles)
        road = Road()
        gate_l = Gates(GATE1, 250, 0)
        gate_r = Gates(GATE2, WIDTH-350, 0)
        powers = pygame.sprite.Group()
        power_up_creator = PowereUpCreator(powers)
        time = 0
        multiplier = 1
        progress_bar_width = 0
        count = 0
        if player_score > highest_score:
            highest_score = player_score
            new_high_score = True
        else:
            new_high_score = False
        show_player_win(screen, player_score, new_high_score)

    clock.tick(FPS)
    time += 1
    obstacles_creator.time = time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    obstacles.update()
    powers.update()
    explosions.update()
    gates.update()
    obstacles_creator.update()
    obstacles_creator.reposition()
    power_up_creator.reposition()

    # Draw
    screen.blit(desert, (0,0))
    screen.blit(logo, (ex_why))
    road.draw(screen, 10)

    crashes = pygame.sprite.groupcollide(all_sprites, obstacles, False, True, pygame.sprite.collide_circle)
    if crashes:
        crash_music.play()
        for crash in crashes:
            explosion = Explosion( crash.rect.midtop,explosion_images)
            explosions.add(explosion)
        game_about_to_end = True
        start_end_time = pygame.time.get_ticks()

    if game_about_to_end:
        if pygame.time.get_ticks() - start_end_time > 350:
           game_over = True

    power_ups = pygame.sprite.groupcollide(all_sprites, powers, False, True, pygame.sprite.collide_circle)
    if power_ups:
        power_up_music.play()
        multiplier += 9 
        count += 100
        new_coin = PowerUp(POWER_UP)
        powers.add(new_coin)

    all_sprites.draw(screen)
    obstacles.draw(screen)
    powers.draw(screen)
    explosions.draw(screen) 
    gates.draw(screen)
    progress_bar_width = progress_bar(time, progress_bar_width)
    player_score = score(screen, time, multiplier)
    high_score(screen, highest_score)
    coins(screen, count)

    if time >= 700 and time <= 950:
        tornado(screen)
    if time ==  DURATION - 53:
        gates.add(gate_l)
        gates.add(gate_r)
    if time == DURATION:
        player_win = True

    pygame.display.flip()

pygame.quit()


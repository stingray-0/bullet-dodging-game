import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
from patterns import patterns

pygame.init()
pygame.display.set_caption("Platformer")

try:
    pygame.mixer.init()
except Exception as e:
    print("Mixer Initialization Failed:", e)

if pygame.mixer.get_init():
    pygame.mixer.set_num_channels(8)

# audio files (create folder assets/sounds and put music.mp3, death.wav etc)
MAIN_MUSIC_PATH = join("assets", "Sounds", "megalovania.mp3")
MENU_MUSIC_PATH = join("assets", "Sounds", "start_menu.mp3")
DEATH_SFX_PATH = join("assets", "Sounds", "metal_pipe.wav")
HURT_SFX_PATH = join("assets", "Sounds", "classic_hurt.wav")

main_music_loaded = False
menu_music_loaded = False
death_sfx = None
hurt_sfx = None


if isfile(DEATH_SFX_PATH):
    try:
        death_sfx = pygame.mixer.Sound(DEATH_SFX_PATH)
        death_sfx.set_volume(0.8)
    except Exception as e:
        print("Could not load death sfx:", e)

if isfile(HURT_SFX_PATH):
    try:
        hurt_sfx = pygame.mixer.Sound(HURT_SFX_PATH)
        hurt_sfx.set_volume(0.6)
    except Exception as e:
        print("Could not load hurt sfx:", e)


BG_COLOR = (0, 0, 0)
WIDTH, HEIGHT = 880, 960
FPS = 60
PLAYER_VEL = 5
MAX_BULLET_NUMBER = 20
high_score = 0
bullet_speed = 10
bullet_wait = 60 
BLOCK_SIZE = 40

window = pygame.display.set_mode((WIDTH, HEIGHT))

def show_start_menu(window):
    font = pygame.font.SysFont("Times New Roman", 100)  
    small_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 50)  
    middle_font = pygame.font.Font("assets/fonts/UbuntuMono-B.ttf", 80)
    menu_text = font.render("gEnsHin imPaCt", True, (255, 255, 255))

    clock = pygame.time.Clock()
    instruction_y = HEIGHT // 2
    amplitude = 20  
    frequency = 1   
    if isfile(MENU_MUSIC_PATH):
        try:
            pygame.mixer.music.load(MENU_MUSIC_PATH)
            menu_music_loaded = True
        except Exception as e:
            print("Could not load menu music:", e)

    if menu_music_loaded and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    running = True
    while running:
        window.fill(BG_COLOR)  
        
        offset = amplitude * math.sin(pygame.time.get_ticks() / 1000 * frequency)
        animated_y = instruction_y + offset + 100

        instruction_text = middle_font.render("Click to Start", True, (255, 255, 255))
        credits = small_font.render("credits", True, (255,255,255))
        title_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, animated_y))
        credits_rect = credits.get_rect(center = (WIDTH // 2, HEIGHT // (1.2)))

        mouse_pos = pygame.mouse.get_pos()
        if credits_rect.collidepoint(mouse_pos):
            credits = small_font.render("credits", True, (200, 200, 200))
        if instruction_rect.collidepoint(mouse_pos):
            instruction_text = middle_font.render("Click to Start", True, (200, 200, 200))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if credits_rect.collidepoint(event.pos):
                            show_credits_screen(window)
                        if instruction_rect.collidepoint(event.pos):
                            running = False
                                                     
        window.blit(menu_text, title_rect)
        window.blit(instruction_text, instruction_rect)
        window.blit(credits, credits_rect)

        pygame.display.update()
        clock.tick(FPS)
        
def show_credits_screen(window):
    big_font = pygame.font.Font(None, 100)
    small_font = pygame.font.Font(None, 60)

    credits_title_text = big_font.render("Game Developed by: ", True, (255,255,255))
    credits_text_1 = small_font.render("BlueStingray, Treeman,", True, (255, 255, 255))
    credits_text_2 = small_font.render("abbabba, Chamber,", True, (255, 255, 255))
    credits_text_3 = small_font.render("and Ycccccccccc", True, (255, 255, 255))

    credits_title_text_rect = credits_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 20))
    credits_text_rect_1 = credits_text_1.get_rect(center=(WIDTH // 2 , HEIGHT // 3 + 70))
    credits_text_rect_2 = credits_text_2.get_rect(center=(WIDTH // 2 , HEIGHT // 3 + 140))
    credits_text_rect_3 = credits_text_3.get_rect(center=(WIDTH // 2 , HEIGHT // 3 + 210))



    clock = pygame.time.Clock()
    running = True

    while running:
        window.fill(BG_COLOR)

        back_button = small_font.render("Back to Main Menu", True, (255,255,255)) 
        back_button_rect = back_button.get_rect(center=(WIDTH // 2, HEIGHT - 100))

        mouse_pos = pygame.mouse.get_pos()
        if (back_button_rect.collidepoint(mouse_pos)):
            back_button = small_font.render("Back to Main Menu", True, (200, 200, 200))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if back_button_rect.collidepoint(event.pos):
                        return  
        window.blit(credits_title_text, credits_title_text_rect)
        window.blit(credits_text_1, credits_text_rect_1)
        window.blit(credits_text_2, credits_text_rect_2)
        window.blit(credits_text_3, credits_text_rect_3)
        window.blit(back_button, back_button_rect)  

        pygame.display.update()
        clock.tick(FPS)

def killed_by_paimon(window,score):
    font = pygame.font.Font("assets/fonts/Butcherman-Regular.ttf", 200)
    font_2 = pygame.font.Font(None, 100) 
    # font_3 = pygame.font.SysFont("asset/fonts/PixelifySans-Regular.tff", 75)
    font_3 = pygame.font.Font("assets/fonts/Bidenatrial.ttf", 75)
    death_text = font.render("YOU DIED" , True, (255, 0, 0)) 
    score_text = font_2.render("Score: " + str(score), True, (255, 255, 255))
    death_text_rect = death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    global high_score 
    high_score_text = font_2.render("High Score: " + str(high_score), True, (255, 255, 255))
    high_score_text_rect = high_score_text.get_rect(center = (WIDTH//2, HEIGHT // 2 - 50))

    darken = pygame.Surface((WIDTH, HEIGHT))
    darken.fill((0, 0, 0))  
    transparency = 0  

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        if death_sfx:
            death_sfx.play()

    clock = pygame.time.Clock()
    run = True

    while run:
        home_text = font_3.render("Home", True, (255, 255, 255))
        retry_text = font_3.render("Try Again", True, (255, 255, 255))
        retry_text_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        home_text_rect = home_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 300))

        mouse_pos = pygame.mouse.get_pos()
        if retry_text_rect.collidepoint(mouse_pos):
            retry_text = font_3.render("Try Again", True, (200, 200, 200))
        if home_text_rect.collidepoint(mouse_pos):
            home_text = font_3.render("Home", True, (200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if retry_text_rect.collidepoint(event.pos):
                            main(window)
                            run = False
                        if home_text_rect.collidepoint(event.pos):
                            show_start_menu(window)
                            run = False

        
        if transparency < 255:
            transparency = (transparency + 0.5)*1.1
        if transparency > 255:
            transparency = 255

        faded_text = death_text.copy()  
        faded_text.fill((255, 0, 0, transparency), special_flags=pygame.BLEND_RGBA_MULT)
        darken.set_alpha(transparency)
        
        window.blit(darken, (0, 0))  
        window.blit(retry_text, retry_text_rect.topleft)
        window.blit(faded_text, death_text_rect.topleft)
        window.blit(score_text, score_text_rect.topleft)
        window.blit(high_score_text, high_score_text_rect.topleft)
        window.blit(home_text, home_text_rect.topleft)
        
        clock.tick(FPS)
        pygame.display.update()  


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def verti_flip(sprites, angle):
    return [pygame.transform.rotate(sprite, angle) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, horizontal_flip = False, vertical_flip = False, scale = False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i  in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32 )
            rect = pygame.Rect(i * width, 0,width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            if scale:
                sprites.append(pygame.transform.scale_by(surface, 1.5))
            else:
                sprites.append(surface)
        
        if horizontal_flip:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)

        if vertical_flip:
            all_sprites[image.replace(".png", "") + "_up"] = verti_flip(sprites, 90)
            all_sprites[image.replace(".png", "") + "_down"] = verti_flip(sprites, -90)
        
        else:
            all_sprites[image.replace(".png", "")] = sprites
    
    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "white_block.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0,0), rect)
    return surface

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SPRITES = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32, True, False, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.parry = 0
        self.die = False
    
    def move(self, dx, dy): #讓角色動
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel): #以下為向上下左右時角色要做的改變
        self.x_vel = -vel
        
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right(self, vel): 
        self.x_vel = vel
        
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def move_up(self, vel):
        self.y_vel = -vel
    
    def move_down(self, vel):
        self.y_vel = vel

    def loop(self, fps):    #角色必須一直做的事
        self.move(self.x_vel, self.y_vel)
        if self.parry != 0:
            self.parry -= 1
        self.update_sprite()
        self.update_hitbox()
    
    def update_sprite(self):    #角色本人動畫更新
        # if self.die == True:
        #     self.SPRITES = load_sprite_sheets("MainCharacters", "Desappearing",96, 96)
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"
        if self.parry != 0:
            sprite_sheet = "hit"

        sprite_sheet_name = sprite_sheet + "_" + self.direction   
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def update_hitbox(self):   #角色碰撞箱更新
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)   #這裡的mask可以當成碰撞箱，
                                                            #有助於完成所謂的pixel perfect(雖然我做的一點也不perfect)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))



class Health(): #血條
    frame_COLOR = (0, 0, 0)
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp
        self.thick = 3
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)    #血條本人
        self.frame = pygame.Rect(x - self.thick, y - self.thick, width + 2*self.thick, height + 2*self.thick)   #血條外框

    def draw(self, win):
        ratio = self.hp/self.max_hp #讓血條變化的東東
        pygame.draw.rect(win, self.frame_COLOR, self.frame, width = self.thick)
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width * ratio, self.height))



class Score():
    COLOR = (0, 0, 0)
    font = pygame.font.SysFont("Comic Sans MS", 30)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        pass
    def draw(self, win):
        text = self.font.render("Score: "+str(self.score), False, self.COLOR)
        win.blit(text, (self.x, self.y))
        


class Bullet(pygame.sprite.Sprite):
    COLOR = (255, 255, 255)
    ANIMATION_DELAY = 5
    SPRITES = load_sprite_sheets("Traps", "Bullet", 40, 40)

    def __init__(self,x, y, size, direction, vel, wait):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.size = size
        self.direction = direction
        self.wait = wait
        self.time = 0
        self.rect = pygame.Rect(x, y, 2*size, 2*size)
        self.animation_count = 0

    def move(self):
        if self.time > self.wait:
            if self.direction == "up":
                self.y -= self.vel
            elif self.direction == "down":
                self.y += self.vel
            elif self.direction == "left":
                self.x -= self.vel
            else:
                self.x += self.vel

        self.time += 1
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def loop(self):
        self.move()
        self.update_sprite()

    def update_sprite(self):
        if self.time >self.wait:
            sprite_sheet = "bullet_move_primo"
        else:
            sprite_sheet = "bullet_prepare_primo"

        sprite_sheet_name = sprite_sheet
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update_hitbox()
    
    def update_hitbox(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite) 

    def is_offscreen(self):
        if  self.y < 3*BLOCK_SIZE or self.y > HEIGHT:
            return True
        if self.x < 0 or self.x > WIDTH:
            return True
        return False
        
    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))



class Object(pygame.sprite.Sprite): #非玩家物品
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Block(Object):    #Block是作為框架的基本單元
    def __init__(self, x, y, size):
        super().__init__(x, y , size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name):   #拼出背景
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image, player, objects, health, bullets, score, highscore, highscore_rect):    #把遊戲畫面上看見的東西畫出來
    for tile in background:
        window.blit(bg_image, tile)
    for bullet in bullets:
        bullet.draw(window)

    for obj in objects:
        obj.draw(window)

    player.draw(window)
    health.draw(window)
    score.draw(window)
    window.blit(highscore, highscore_rect)
  
    pygame.display.update()

def hori_collide(player, objects, dx):  #水平碰撞的判斷
    player.move(dx, 0)
    player.update()
    collided_object = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()

    return collided_object

def verti_collide(player, objects, dy): #垂直碰撞的判斷
    player.move(0, dy)
    player.update()
    collided_object = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(0, -dy)
    player.update()

    return collided_object

def bullet_collide(player, bullets, health):
    for bullet in bullets:
        if pygame.sprite.collide_mask(player, bullet) and player.parry == 0:
            health.hp -= 10
            player.parry = 30
            return True
    return False

def handle_move(player, objects):   #控制上下左右
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    collide_left = hori_collide(player, objects, -3*PLAYER_VEL) #collide都是用來看有沒有碰到
    collide_right = hori_collide(player, objects, 3*PLAYER_VEL)

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(PLAYER_VEL)

    collide_up = verti_collide(player, objects, -3*PLAYER_VEL)
    collide_down = verti_collide(player, objects, 3*PLAYER_VEL)

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not collide_up:
        player.move_up(PLAYER_VEL)
    if (keys[pygame.K_DOWN] or keys[pygame.K_s])and not collide_down:
        player.move_down(PLAYER_VEL) 

def new_bullet(direction:str, index:int, position: int, slots: list[int]):
    match direction:
        case "down":
            x = position * BLOCK_SIZE
            y = 3 * BLOCK_SIZE
            bullet_dir = "down"
        case "up":
            x = position * BLOCK_SIZE
            y = HEIGHT - 2*BLOCK_SIZE
            bullet_dir = "up"
        case "right":
            x = BLOCK_SIZE
            y = (position+2) * BLOCK_SIZE
            bullet_dir = "right"
        case "left":
            x = WIDTH - 2*BLOCK_SIZE
            y = (position+2) * BLOCK_SIZE
            bullet_dir = "left"
        case "down_up":
            x = position * BLOCK_SIZE
            if (index < len(slots) / 2):
                y = 3 * BLOCK_SIZE
                bullet_dir = "down"
            else:
                y = HEIGHT - 2*BLOCK_SIZE
                bullet_dir = "up"
        case "up_down":
            x = position * BLOCK_SIZE
            if (index < len(slots) / 2):
                y = HEIGHT - 2*BLOCK_SIZE
                bullet_dir = "up"
            else:
                y = 3 * BLOCK_SIZE
                bullet_dir = "down"
        case "right_left":
            y = (position+2) * BLOCK_SIZE
            if (index < len(slots) / 2):
                x = BLOCK_SIZE
                bullet_dir = "right"
            else:
                x = WIDTH - 2*BLOCK_SIZE
                bullet_dir = "left"
        case "left_right":
            y = (position+2) * BLOCK_SIZE
            if (index < len(slots) / 2):
                x = WIDTH - 2*BLOCK_SIZE
                bullet_dir = "left"
            else:
                x = BLOCK_SIZE
                bullet_dir = "right"
        case "udlr":
            quarter = len(slots) / 4
            if index < quarter:
                x = position * BLOCK_SIZE
                y = HEIGHT - 2*BLOCK_SIZE
                bullet_dir = "up"
            elif index < 2*quarter:
                x = position * BLOCK_SIZE
                y = 3 * BLOCK_SIZE
                bullet_dir = "down"
            elif index < 3*quarter:
                x = WIDTH - 2*BLOCK_SIZE
                y = (position+2) * BLOCK_SIZE
                bullet_dir = "left"
            else:
                x = BLOCK_SIZE
                y = (position+2) * BLOCK_SIZE
                bullet_dir = "right"
        case "lrud":
            quarter = len(slots) / 4
            if index < quarter:
                x = WIDTH - 2*BLOCK_SIZE
                y = (position+2) * BLOCK_SIZE
                bullet_dir = "left"
            elif index < 2*quarter:
                x = BLOCK_SIZE
                y = (position+2) * BLOCK_SIZE
                bullet_dir = "right"
            elif index < 3*quarter:
                x = position * BLOCK_SIZE
                y = HEIGHT - 2*BLOCK_SIZE
                bullet_dir = "up"
            else:
                x = position * BLOCK_SIZE
                y = 3 * BLOCK_SIZE
                bullet_dir = "down"
    global bullet_speed
    global bullet_wait
    return Bullet(x, y, BLOCK_SIZE, bullet_dir, bullet_speed, bullet_wait)

def spawn_wave(pattern_index: int):
    global bullet_wait, bullet_speed
    spread = patterns[pattern_index][0]
    direction = patterns[pattern_index][1]
    if spread == 1:
        slots = list(random.sample(range(1, MAX_BULLET_NUMBER+1), k = MAX_BULLET_NUMBER-6))
    elif spread == 2:
        slots = list(i for i in range(1, MAX_BULLET_NUMBER+1) if (i-1)%4 < 2)
    elif spread == 3:
        slots = list(range(1, MAX_BULLET_NUMBER-3))
    elif spread == 4:
        slots = list(range(5, MAX_BULLET_NUMBER+1))
    else:
        slots = list(range(1, MAX_BULLET_NUMBER+1))  
    
    wave = []
    for i, pos in enumerate(slots):
        wave.append(new_bullet(direction, i, pos, slots))

    return wave
    
def main(window): #就main，沒什麼好說的?
    clock = pygame.time.Clock()
    pattern_index = 0
    background, bg_image = get_background("Blue.png")
    font = pygame.font.Font("assets/fonts/UbuntuMono-B.ttf", 50)
    player = Player(600, 480, 32, 32)
    health = Health(50, 50, 100, 10, 100)
    score = Score(0,0)
    global high_score
    dead = False
    #畫框框
    floor  = [Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE) for i in range(WIDTH // BLOCK_SIZE)]
    ceil = [Block(i * BLOCK_SIZE, 2 * BLOCK_SIZE, BLOCK_SIZE) for i in range(WIDTH // BLOCK_SIZE)]
    wall1 = [Block(0, HEIGHT - (i+1)* BLOCK_SIZE, BLOCK_SIZE) for i in range(1, HEIGHT // BLOCK_SIZE - 2)]
    wall2 = [Block(WIDTH - BLOCK_SIZE, HEIGHT - (i+1)* BLOCK_SIZE, BLOCK_SIZE) for i in range(1, HEIGHT // BLOCK_SIZE - 2)]
    frame = [*floor, *wall1, *wall2, *ceil]

    bullets = spawn_wave(pattern_index)
    if isfile(MAIN_MUSIC_PATH):
        try:
            pygame.mixer.music.load(MAIN_MUSIC_PATH)
            main_music_loaded = True
        except Exception as e:
            print("Could not load main music:", e)
    if main_music_loaded and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    #這裡的會一直跑
    run = True
    while run:
        while bullets:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if health.hp <= 0:
                dead = True
                break
            player.loop(FPS)

            for bullet in bullets:
                bullet.loop()
            
            bullets = [b for b in bullets if not b.is_offscreen()]

            if bullet_collide(player, bullets, health):
                if pygame.mixer.get_init() and hurt_sfx:
                    ch = pygame.mixer.find_channel()
                    if ch:
                        ch.play(hurt_sfx)

            handle_move(player, frame)

            score.score += 1

            # Highscore text changing
            high_score_text = font.render(f"HIGHSCORE: {high_score}", True, (255, 255, 255))
            high_score_text_rect = high_score_text.get_rect(center =(WIDTH - 200, 40))

            if (score.score > high_score):
                high_score = score.score
            
            draw(window, background, bg_image, player, frame, health, bullets, score, high_score_text, high_score_text_rect)

        pattern_index += 1
        if pattern_index == len(patterns):
            pattern_index = 0
            global bullet_speed, bullet_wait
            bullet_speed += 2
            bullet_wait = max(0, bullet_wait-20)
        bullets = spawn_wave(pattern_index)
        if dead:
            killed_by_paimon(window,score.score)
            break



if __name__ == "__main__":  #如果直接跑這個程式才會做main，import則不會
    while True:
        show_start_menu(window)
        main(window)
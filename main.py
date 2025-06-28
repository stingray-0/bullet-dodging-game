import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

BG_COLOR = (0, 0, 0)
WIDTH, HEIGHT = 880, 960
FPS = 60
PLAYER_VEL = 5
BULLET_NUMBER = 20

block_size = 40
g_pattern =[[1,"down"], [1,"up"], [1,"left"],[1,"right"],[1,"left"],[1,"down"],[1,"down"],
            [1,"down"], [1,"up"], [1,"left"],[1,"right"],[1,"left"],[1,"down"],[1,"down"],
            [1,"up_down"],[1,"up_down"],[1,"left_right"],[2,"left_right"],[1,"left_right"],
            [1,"up_down"],[3,"up_down"],[4,"left_right"],[3,"left_right"],[4,"left_right"],
            [1,"up_down"],[3,"up_down"],[1,"left_right"],[2,"left_right"],[1,"left_right"],
            [3,"udlr"],[4,"udlr"],[3,"udlr"],[4,"udlr"],[1,"udlr"],[1,"udlr"],[1,"udlr"],
            [1,"udlr"],[1,"udlr"],[1,"udlr"],[2,"udlr"],[1,"udlr"],[2,"udlr"],[1,"udlr"],
            [1,"udlr"],[1,"udlr"],[2,"udlr"],[1,"udlr"],[3,"udlr"],[1,"udlr"],[2,"udlr"],
            [1,"udlr"],[2,"udlr"],[3,"udlr"],[2,"udlr"],[1,"udlr"],[3,"udlr"],[1,"udlr"],
            [1,"udlr"],[1,"udlr"],[3,"udlr"],[2,"udlr"],[1,"udlr"],[2,"udlr"],[1,"udlr"]]

window = pygame.display.set_mode((WIDTH, HEIGHT))

def show_start_menu(window):
    font = pygame.font.SysFont("Times New Roman", 74)  
    small_font = pygame.font.SysFont("asset/fonts/PixelifySans-Regular.ttf", 50)  

    menu_text = font.render("gEnsHin imPaCt", True, (255, 255, 255))
    instruction_text = small_font.render("click to start", True, (255, 255, 255))
    credits = small_font.render("credits", True, (255,255,255))

    clock = pygame.time.Clock()
    instruction_y = HEIGHT // 2
    amplitude = 10  
    frequency = 1   

    running = True
    while running:
        window.fill(BG_COLOR)  

        
        offset = amplitude * math.sin(pygame.time.get_ticks() / 1000 * frequency)
        animated_y = instruction_y + offset

        
        title_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, animated_y))
        credits_rect = credits.get_rect(center = (WIDTH // 2, HEIGHT // (1.2)))

        
        window.blit(menu_text, title_rect)
        window.blit(instruction_text, instruction_rect)
        window.blit(credits, credits_rect)

        pygame.display.update()

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

        clock.tick(FPS)
        
def show_credits_screen(window):
    font = pygame.font.Font(None, 50)  
    back_button_font = pygame.font.Font(None, 40)

    credits_text = font.render("Game Developed by: rahhhhhhh", True, (255,255,255))
    back_button = back_button_font.render("back to Main Menu", True, (255,255,255))

    clock = pygame.time.Clock()
    running = True

    while running:
        window.fill(BG_COLOR)

        
        credits_text_rect = credits_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        back_button_rect = back_button.get_rect(center=(WIDTH // 2, HEIGHT - 100))

        
        window.blit(credits_text, credits_text_rect)
        window.blit(back_button, back_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if back_button_rect.collidepoint(event.pos):
                        return  

        clock.tick(FPS)

def killed_by_paimon(window,score):
    font = pygame.font.Font("assets/fonts/Butcherman-Regular.ttf", 200)
    font_2 = pygame.font.SysFont("asset/fonts/PixelifySans-Regular.ttf", 50) 
    death_text = font.render("YOU DIED" , True, (255, 0, 0)) 
    score_text = font_2.render("Score: " + str(score), True, (255, 0, 0))
    death_text_rect = death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 +200))


    darken = pygame.Surface((WIDTH, HEIGHT))
    darken.fill((0, 0, 0))  
    transparency = 0  

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        
        if transparency < 255:
            transparency += 0.05  

        
        faded_text = death_text.copy()  
        faded_text.fill((255, 0, 0, transparency*1.1), special_flags=pygame.BLEND_RGBA_MULT)

        
        darken.set_alpha(transparency)

        
        window.blit(darken, (0, 0))  
        window.blit(faded_text, death_text_rect.topleft)
        window.blit(score_text, score_text_rect.topleft)

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
                sprites.append(pygame.transform.scale2x(surface))
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

    def __init__(self,x, y, size, direction, vel):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.size = size
        self.direction = direction
        self.wait = 60
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
            sprite_sheet = "bullet_move"
        else:
            sprite_sheet = "bullet_prepare"

        sprite_sheet_name = sprite_sheet
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update_hitbox()
    
    def update_hitbox(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite) 
        
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

def draw(window, background, bg_image, player, objects, health, bullets, score):    #把遊戲畫面上看見的東西畫出來
    for tile in background:
        window.blit(bg_image, tile)
    
    for bullet in bullets:
        bullet.draw(window)

    for obj in objects:
        obj.draw(window)

    player.draw(window)
    health.draw(window)
    score.draw(window)
  
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

def next_run(bullets, pattern_index):
    direction = g_pattern[pattern_index][1]

    for i in range(len(bullets)):
        bullet = bullets[i]
        bullet.time = 0    

        if direction == "down":
            bullet.x = get_pattern(pattern_index,i)*bullet.size
            bullet.y = 3*block_size
            bullet.direction = "down"
        elif direction == "up":
            bullet.x = get_pattern(pattern_index,i)*bullet.size
            bullet.y = HEIGHT - 2*block_size
            bullet.direction = "up"
        elif direction == "right":
            bullet.x = block_size
            bullet.y = (get_pattern(pattern_index,i)+3)*bullet.size
            bullet.direction = "right"
        elif direction == "left":
            bullet.x = WIDTH - 2*block_size
            bullet.y = (get_pattern(pattern_index,i)+3)*bullet.size
            bullet.direction = "left"
        elif direction == "up_down":
            if i < 10:
                bullet.x = get_pattern(pattern_index,i)*bullet.size
                bullet.y = 3*block_size
                bullet.direction = "down"
            else:
                bullet.x = get_pattern(pattern_index,i)*bullet.size
                bullet.y = HEIGHT - 2*block_size
                bullet.direction = "up"
        elif direction == "left_right":
            if i < 10:
                bullet.x = block_size
                bullet.y = (get_pattern(pattern_index,i)+3)*bullet.size
                bullet.direction = "right"
            else:
                bullet.x = WIDTH - 2*block_size
                bullet.y = (get_pattern(pattern_index,i)+3)*bullet.size
                bullet.direction = "left"
        else:
            if i < 5:
                bullet.x = get_pattern(pattern_index,i)*bullet.size
                bullet.y = 3*block_size
                bullet.direction = "down"
            elif i < 10:
                bullet.x = get_pattern(pattern_index,i)*bullet.size
                bullet.y = HEIGHT - 2*block_size
                bullet.direction = "up"
            elif i < 15:
                bullet.x = block_size
                bullet.y = (get_pattern(pattern_index,i)+3)*bullet.size
                bullet.direction = "right"
            else:
                bullet.x = WIDTH - 2*block_size
                bullet.y = (get_pattern(pattern_index,i)+3)*bullet.size
                bullet.direction = "left"


def get_pattern(pattern_index, slot):
    if g_pattern[pattern_index][0] == 1:
        return random.randint(1,20)
    elif g_pattern[pattern_index][0] == 2:
        if slot % 2 == 0:
            return slot
        else:
            return slot + 1
    elif g_pattern[pattern_index][0] == 3:
        return slot
    elif g_pattern[pattern_index][0] == 4:
        return 20-slot


def main(window): #就main，沒什麼好說的?
    clock = pygame.time.Clock()
    pattern_index = 0
    background, bg_image = get_background("Blue.png")

    player = Player(600, 480, 32, 32)
    health = Health(50, 50, 100, 10, 100)
    score = Score(0,0)

    #畫框框
    floor  = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(WIDTH // block_size)]
    ceil = [Block(i * block_size, 2 * block_size, block_size) for i in range(WIDTH // block_size)]
    wall1 = [Block(0, HEIGHT - (i+1)* block_size, block_size) for i in range(1, HEIGHT // block_size - 2)]
    wall2 = [Block(WIDTH - block_size, HEIGHT - (i+1)* block_size, block_size) for i in range(1, HEIGHT // block_size - 2)]
    frame = [*floor, *wall1, *wall2, *ceil]

    bullet1 = [Bullet(random.randint(1,20)*block_size, 3*block_size, 40, "down", 10) for i in range(BULLET_NUMBER)]

    #這裡的會一直跑
    run = True
    while run:
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if health.hp <= 0:
                killed_by_paimon(window,score.score)
            player.loop(FPS)

            for bullet in bullet1:
                bullet.loop()
                

            bullet_collide(player,bullet1, health)


            handle_move(player, frame)
            draw(window, background, bg_image, player, frame, health, bullet1, score)
            score.score += 1

            if (bullet1[0].y < 3*block_size) or (bullet1[0].y > HEIGHT) or (bullet1[0].x < 0) or (bullet1[0].x > WIDTH):
                break
        next_run(bullet1, pattern_index)
        pattern_index += 1
        if pattern_index >= len(g_pattern):
            pattern_index = 0
        

    pygame.quit()
    quit()

if __name__ == "__main__":  #如果直接跑這個程式才會做main，import則不會
    show_start_menu(window)
    main(window)

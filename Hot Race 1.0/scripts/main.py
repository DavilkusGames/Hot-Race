import pygame, random, os

os.getcwd()
os.chdir('..')

class OurCar():
    def __init__(self):
        self.sprite = ourCarImages[0]
        self.x = 0
        self.y = display_height * 0.6
        self.health = 5
        self.fuel = 20
        self.max_health = 5
        self.max_fuel = 20
        
class OtherCar1():
    def __init__(self):
        self.sprite = enemyCarsImages[0]
        self.x = 410
        self.y = -100
        self.visible = 0
        self.speed = -4
        
class OtherCar2():
    def __init__(self):
        self.sprite = ourCarImages[0]
        self.x = 335
        self.y = -100
        self.visible = 0
        self.speed = 4
        
class Fuel():
    def __init__(self):
        self.sprite = pygame.image.load('images/fuel_icon.png')
        self.x = 0
        self.y = 0
        self.visible = 0
        self.counter = 0
        self.time = 0

class Bonus():
    def __init__(self):
        self.sprite = pygame.image.load('images/hp_icon.png')
        self.x = 0
        self.y = 0
        self.visible = 0
        self.counter = 0
        self.time = 0

background1 = pygame.image.load('images/background.png')
background2 = pygame.image.load('images/background.png')

ourCarImages = [pygame.image.load('images/car1.png'),
                pygame.image.load('images/car2.png'),
                pygame.image.load('images/car3.png')]
imagesCoords = [(150, 220), (378, 220), (606, 220)]
enemyCarsImages = [pygame.image.load('images/enemy_car1.png'),
                   pygame.image.load('images/enemy_car2.png'),
                   pygame.image.load('images/enemy_car3.png')]
cursor = pygame.image.load('images/cursor.png')

display_width = 800
display_height = 600
game_exit = False
win = 0

faza = 0

background_height = 2352
background_y = display_height - background_height
world_speed = 0
accelerate = 0

score_data = open('saves/score.txt', 'r')
score = int(score_data.read())
score_data.close()

dist = 0

music_volume = 2

max_dist = 5000

car = OurCar()
fuel = Fuel()
bonus = Bonus()
cars = [OtherCar1(), OtherCar2(), OtherCar1()]

car.x = 335

red_car_x = 335
red_car_y = -100
red_car_speed = 5
red_car_line = 1

pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Hot Race 1.0')
clock = pygame.time.Clock()

main_music = pygame.mixer.Sound('sounds/main_music.ogg')
game_music = pygame.mixer.Sound('sounds/game_music.ogg')

music_channel = main_music.play(loops = -1)
music_channel.set_volume(music_volume)

pygame.mouse.set_visible(False)

def draw_background():
    global background_y
    
    world_speed = accelerate
    
    game_display.blit(background1, (0, background_y))
    game_display.blit(background2, (0, background_y - background_height))
    
    background_y += world_speed
    
    if background_y > display_height:
        background_y = display_height - background_height

def draw_car():
    game_display.blit(car.sprite, (car.x, car.y))

def draw_cars():
    global cars, score
    
    for i in range(len(cars)):
        if cars[i].visible == 0:
            probability_visible = random.randint(0, 150)
            if probability_visible == 1:
                cars[i].visible = 1
        if cars[i].visible == 1:
            game_display.blit(cars[i].sprite, (cars[i].x, cars[i].y))
            cars[i].y += world_speed + accelerate - cars[i].speed
        else:
            car_x = random.randint(0, 1)
            if car_x == 1:
                cars[i] = OtherCar2()
            else:
                cars[i] = OtherCar1()
            if cars[i].x == 335:
                cars[i].sprite = ourCarImages[random.randint(0, 2)]
            else:
                cars[i].sprite = enemyCarsImages[random.randint(0, 2)]
        if cars[i].y > display_height + 300:
            cars[i].visible = 0
            score+=100
            
def draw_score():
    global score
    draw_text(30, "SCORE:", (15,0))
    draw_text(30, str(score), (105,0))

def draw_dist():
    global dist, win
    draw_text(30, "DIST:", (15,35))
    draw_text(30, str(int(dist)), (105,35))
    
    dist += accelerate / 10
    
    pygame.draw.rect(game_display, (0, 255, 0), (0, display_height - 30, dist / max_dist * display_width, 30))    
    
    if dist - 1 > max_dist:
        win = 1

def draw_health():
    game_display.blit(bonus.sprite, (10, 80))

    pygame.draw.rect(game_display, (255, 0, 0), (75, 88, car.health * 40, 30))

def draw_fuel():
    global win
    
    game_display.blit(fuel.sprite, (10, 140))
    
    pygame.draw.rect(game_display, (255, 255, 0), (75, 148, car.fuel * 10, 30))
    
    if car.fuel >= 0:
        car.fuel -= accelerate / 150
    else:
        win = -1

def draw_fuels():
    if car.fuel < 5 and not accelerate == 0:
        if fuel.visible == 0:
            if fuel.time == 0:
                fuel.time = random.randint(260, 280) - (accelerate * 80)
                fuel_line = random.randint(0, 1)
                if fuel_line == 0:
                    fuel.x = 335
                else:
                    fuel.x = 410
            else:
                fuel.counter += 1
                if fuel.counter >= fuel.time:
                    fuel.visible = 1
                    fuel.time = 0
                    fuel.counter = 0
    if fuel.visible == 1:
        game_display.blit(fuel.sprite, (fuel.x, fuel.y))
        fuel.y += accelerate
        if fuel.y > display_height + 300:
            fuel.visible = 0
            fuel.y = -100
            
def draw_bonuses():
    if car.health < 2 and not accelerate == 0:
        if bonus.visible == 0:
            if bonus.time == 0:
                bonus.time = random.randint(300, 320) - (accelerate * 80)
                bonus_line = random.randint(0, 1)
                if bonus_line == 0:
                    bonus.x = 335
                else:
                    bonus.x = 410
            else:
                if bonus.counter >= bonus.time:
                    bonus.visible = 1
                    bonus.time = 0
                    bonus.counter = 0
                bonus.counter += 1
    if bonus.visible == 1:
        game_display.blit(bonus.sprite, (bonus.x, bonus.y))
        bonus.y += accelerate
        if bonus.y > display_height + 300:
            bonus.visible = 0
            bonus.y = -100

def draw_lose(event):
    global faza
    
    game_display.blit(background1, (0, background_y))
    game_display.blit(background2, (0, background_y - background_height))
    
    draw_text(60, "YOU LOSE", (280, 180))
    menu_button = pygame.draw.rect(game_display, (180, 180, 180), (290, 260, 220, 60))
    draw_text(45, "MENU", (345, 260))
    
    game_music.stop()
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if menu_button.collidepoint(pos):
                faza = 0
                reset_variables()
                music_channel = main_music.play(loops = -1)
                music_channel.set_volume(music_volume)                

def draw_win(event):
    global faza
    
    score += max_dist
    
    game_display.blit(background1, (0, background_y))
    game_display.blit(background2, (0, background_y - background_height))    
    
    draw_text(60, "YOU WIN", (290, 180))
    menu_button = pygame.draw.rect(game_display, (180, 180, 180), (290, 260, 220, 60))
    draw_text(45, "MENU", (345, 260))  
    
    game_music.stop()
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if menu_button.collidepoint(pos):
                faza = 0
                reset_variables()
                game_music.stop()
                music_channel = main_music.play(loops = -1)
                music_channel.set_volume(music_volume)
    
def draw_text(fontsize, text, coord):
    font = pygame.font.Font("fonts/Pixel.ttf", fontsize)
    text_image = font.render(text, True, (255,255,255))
    game_display.blit(text_image, coord)

def draw_cursor():
    pos = pygame.mouse.get_pos()
    game_display.blit(cursor, pos)

def process_keyboard(event):
    global accelerate
    
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if car.x == 335:
                    car.x = 410
            elif event.key == pygame.K_LEFT:
                if car.x == 410:
                    car.x = 335
            elif event.key == pygame.K_UP:
                if accelerate <= 20:
                    accelerate += 1
            elif event.key == pygame.K_DOWN:
                if accelerate >= 1:
                    accelerate -= 1
            elif event.key == pygame.K_SPACE:
                accelerate = 0
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

def collision():
    global score, counter_colission, win
    car_rect = car.sprite.get_rect().move((car.x, car.y))
    bonus_rect = bonus.sprite.get_rect().move((bonus.x, bonus.y))
    fuel_rect = fuel.sprite.get_rect().move((fuel.x, fuel.y))
    for i in range(len(cars)):
        other_rect = cars[i].sprite.get_rect().move((cars[i].x, cars[i].y))
        if car_rect.colliderect(other_rect):
            cars[i].visible = 0
            score -= 200
            car.health -= 1
            if car.health <= 0:
                win = -1
    if car_rect.colliderect(fuel_rect):
        car.fuel = car.max_fuel
        fuel.visible = 0
        fuel.y = -100
    if car_rect.colliderect(bonus_rect):
        car.health = car.max_health
        bonus.visible = 0
        bonus.y = -100

def reset_variables():
    global win, world_speed, score, dist, accelerate, background_y
    
    background_y = display_height - background_height    
    win = 0
    world_speed = 0
    accelerate = 0    
    score = 0
    dist = 0
    car.x = 335
    car.health = 5
    car.fuel = 20
    fuel.x = 0
    fuel.y = 0
    fuel.visible = 0
    fuel.counter = 0
    fuel.time = 0
    bonus.x = 0
    bonus.y = 0
    bonus.visible = 0
    bonus.counter = 0
    bonus.time = 0
    for i in range(len(cars)):
        cars[i].y = -100
        cars[i].visible = 0
        
def draw_logo(event):
    global faza, game_exit
    
    pygame.draw.rect(game_display, (0, 92, 188), (0, 0, display_width, display_height))
    draw_text(90, "HOT RACE", (230, 30))
    start_button = pygame.draw.rect(game_display, (180, 180, 180), (300, 190, 220, 80))
    draw_text(45, "START", (355, 200))
    exit_button = pygame.draw.rect(game_display, (180, 180, 180), (300, 300, 220, 80))
    draw_text(45, "EXIT", (370, 310))    
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if start_button.collidepoint(pos):
                faza = 1
        if exit_button.collidepoint(pos):
                game_exit = True

def select_car(event):
    global faza
    exit_button = pygame.draw.rect(game_display, (0, 92, 188), (0, 0, display_width, display_height))
    draw_text(60, "SELECT CAR", (250, 10))
    
    for i in range(len(ourCarImages)):
        game_display.blit(ourCarImages[i], imagesCoords[i])
        if event.type == pygame.MOUSEBUTTONDOWN:
            car_rect = ourCarImages[i].get_rect().move(imagesCoords[i])
            pos = pygame.mouse.get_pos()
            if car_rect.collidepoint(pos):
                car.sprite = ourCarImages[i]
                faza = 2
                main_music.stop()
                music_channel = game_music.play(loops = -1)
                music_channel.set_volume(music_volume - 1.5)                

def game():
    collision()        

    draw_background()
    draw_car()
    draw_cars()
    draw_fuels()
    draw_bonuses()
    draw_score()
    draw_dist()
    draw_health()
    draw_fuel()

def game_loop(update_time):
    global game_exit
    while not game_exit:
        for event in pygame.event.get():
            process_keyboard(event)
            if event.type == pygame.QUIT:
                score_data = open('saves/score.txt', 'w')
                score_data.write(str(score))
                score_data.close()
                game_exit = True
        
        if faza == 2:
            if win == 0:
                game()
            else:
                if win == -1:
                    draw_lose(event)
                else:
                    draw_win(event)
                draw_cursor()
        elif faza == 1:
            select_car(event)
            draw_cursor()
        else:
            draw_logo(event)
            draw_cursor()
            
        pygame.display.update()
        clock.tick(update_time)
game_loop(30)
pygame.quit()
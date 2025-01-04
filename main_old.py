import pygame, sys
from random import randint, uniform


def laser_update(laser_lst, speed=500):
    for rect in laser_lst:
        rect.y -= round(speed * dt)
        if rect.bottom < 0:
            laser_lst.remove(rect)


def meteor_update(meteor_lst, speed=300):
    for meteor_tuple in meteor_lst:
        meteor_rect = meteor_tuple[0]
        direction = meteor_tuple[1]
        meteor_rect.center += direction * speed * dt
        if meteor_rect.top > WINDOW_HEIGHT:
            meteor_lst.remove(meteor_tuple)


def display_score(_can_shoot, _score):
    color = "white" if _can_shoot else "gray"
    score_text = f"Score: {_score}"
    text_surf = font.render(score_text, True, "White")
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, color, text_rect.inflate((30, 30)), width=8, border_radius=5)


def laser_timer(_can_shoot, duration=500):
    if not _can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            _can_shoot = True
    return _can_shoot


# main window size
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# game init
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid shooter")
clock = pygame.time.Clock()

# ship import
ship_surf = pygame.image.load("graphics/ship.png").convert_alpha()
ship_reversed_surf = pygame.transform.flip(ship_surf, False, True)
ship_rect = ship_surf.get_rect(center = (640, 360))

# background
bg_surf = pygame.image.load("graphics/background.png").convert()

# laser import
laser_surf = pygame.image.load("graphics/laser.png").convert_alpha()
laser_list = []

# laser timer
can_shoot = True
shoot_time = None

# text import
font = pygame.font.Font("graphics/subatomic.ttf", 50)

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 750)

# meteor import
meteor_surf = pygame.image.load("graphics/meteor.png").convert_alpha()
meteor_list = []

# import sound
laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
background_music = pygame.mixer.Sound("sounds/music.wav")

laser_sound.set_volume(0.25)
explosion_sound.set_volume(0.25)
background_music.set_volume(0.25)

background_music.play(loops=-1)

# score
score = 0

# main loop
while True:

    # inputs / events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)

            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # play laser sound
            laser_sound.play()
        
        if event.type == meteor_timer:
            # random position
            x_pos = randint(-100, WINDOW_WIDTH + 100)
            y_pos = randint(-100, -50)

            # createing a rect
            meteor_rect = meteor_surf.get_rect(center = (x_pos, y_pos))

            # random direction
            direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

            meteor_list.append((meteor_rect, direction))

    # framerate limit
    dt = clock.tick(120) / 1000

    # mouse input
    ship_rect.center = pygame.mouse.get_pos()

    # update
    laser_update(laser_list)
    meteor_update(meteor_list)
    can_shoot = laser_timer(can_shoot, 500)

    # meteor ship collisions
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            score = 0

    # laser meteor collisions
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if laser_rect.colliderect(meteor_rect):
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)
                explosion_sound.play()
                score += 1

    # drawing
    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_surf, (0, 0))
    display_score(can_shoot, score)

    for rect in laser_list:
        display_surface.blit(laser_surf, rect)
    
    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])

    display_surface.blit(ship_surf, ship_rect)

    # draw the final frame
    pygame.display.update()

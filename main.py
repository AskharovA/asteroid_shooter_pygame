import pygame, sys
from random import randint, uniform


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

        self.can_shoot = True
        self.shoot_time = None

        self.laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
        self.laser_sound.set_volume(0.25)
    
    def laser_timer(self):
        if not self.can_shoot:
            current_timer = pygame.time.get_ticks()
            if current_timer - self.shoot_time > 500:
                self.can_shoot = True
    
    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
    
    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.rect.midtop, laser_group)
            self.laser_sound.play()
    
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            pass

    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()
        self.meteor_collision()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.explosion_sound.set_volume(0.25)
    
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
    
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom < 0:
            self.kill()

        self.meteor_collision()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        meteor_surf = pygame.image.load("graphics/meteor.png").convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(meteor_surf, meteor_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

        self.rotation = 0
        self.rotation_speed = randint(20, 50)
    
    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotation_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotation_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Score:
    def __init__(self):
        self.font = pygame.font.Font("graphics/subatomic.ttf", 50)
    
    def display(self):
        text = self.font.render(f"Score: {pygame.time.get_ticks() // 1000}", True, "White")
        rect = text.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(text, rect)
        pygame.draw.rect(display_surface, "white", rect.inflate((30, 30)), width=8, border_radius=5)


# basic setup
pygame.init()
clock = pygame.time.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid shooter")

# background
background_surf = pygame.image.load("graphics/background.png").convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

ship = Ship(spaceship_group)
score = Score()

# timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

background_music = pygame.mixer.Sound("sounds/music.wav")
background_music.set_volume(0.25)
background_music.play(loops=-1)

# main loop
while True:

    # inputs / events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            meteor_y_pos = randint(-100, -50)
            Meteor((meteor_x_pos, meteor_y_pos), meteor_group)
    
    # delta time
    dt = clock.tick(120) / 1000

    # background
    display_surface.blit(background_surf, (0, 0))

    # update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    # score
    score.display()

    # graphics
    meteor_group.draw(display_surface)
    laser_group.draw(display_surface)
    spaceship_group.draw(display_surface)

    # draw the final frame
    pygame.display.update()

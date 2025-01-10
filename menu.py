import pygame
import sys


class Menu:
    def __init__(self, display):
        self.background = pygame.image.load("graphics/background.png").convert()
        self.display = display

        self.font = pygame.font.Font("graphics/subatomic.ttf", 50)
        self.text = self.font.render("Start game", True, "White")
        self.rect = self.text.get_rect(midbottom=(1280 / 2, 720 / 2))

        self.laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
        self.laser_sound.set_volume(0.25)

    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.rect.collidepoint(event.pos):
                        return
                if event.type == pygame.MOUSEMOTION:
                    if self.rect.collidepoint(event.pos):
                        self.text = self.font.render("Start game", True, "Green")
                        self.laser_sound.play()
                    else:
                        self.text = self.font.render("Start game", True, "White")

            self.display.blit(self.background, (0, 0))
            self.display.blit(self.text, self.rect)

            pygame.display.update()

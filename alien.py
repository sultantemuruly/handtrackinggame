import pygame
import random
import os

class Alien:
    def __init__(self, width, height):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "ufo.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = 0

        self.dy = random.uniform(1, 5)

        self.health = 10
        self.screen_width = width
        self.screen_height = height

    def update(self):
        self.rect.y += self.dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # Draw health bar
        health_bar_width = self.rect.width
        health_ratio = self.health / 10
        health_bar_color = (0, 255, 0) if self.health > 5 else (255, 0, 0)  # Green if > 25, Red otherwise
        pygame.draw.rect(surface, health_bar_color, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))
        pygame.draw.rect(surface, (0, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_width, 5), 1)  # Black border

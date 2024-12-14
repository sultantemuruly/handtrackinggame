import pygame

class UIManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        title_text = self.font.render("Cosmo Blaster", True, (255, 255, 255))
        instruction_text = self.font.render("Press 'W' to Start", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 3))
        self.screen.blit(instruction_text, (self.width // 2 - instruction_text.get_width() // 2, self.height // 2))
        pygame.display.flip()

    def draw_game_over(self, score):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(f"Your Score: {score}", True, (255, 255, 255))
        restart_text = self.font.render("Press 'R' to Restart", True, (255, 255, 255))
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 3))
        self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 2))
        self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, self.height // 1.5))
        pygame.display.flip()

    def draw_game_ui(self, score, time_left):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        timer_text = self.font.render(f"Time: {int(time_left)}s", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Top-left corner
        self.screen.blit(timer_text, (self.width - timer_text.get_width() - 10, 10))  # Top-right corner

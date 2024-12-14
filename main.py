import pygame
import cv2
import mediapipe as mp
import time
from alien import Alien
from ui_manager import UIManager

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmo Blaster")

BLACK = (0, 0, 0)
RED = (255, 0, 0)

player_image = pygame.image.load("jet.png")
player_width, player_height = player_image.get_width(), player_image.get_height()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height

balls = []
ball_speed = -10
ball_radius = 5

aliens = []
alien_spawn_interval = 2  # Spawn aliens every 2 seconds
last_alien_spawn_time = time.time()

aliens_destroyed = 0
game_time = 59  # 59 seconds game duration
start_time = None
game_active = False
game_over = False

ui_manager = UIManager(screen, WIDTH, HEIGHT)

# Initialize OpenCV and Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not game_active and not game_over:
                game_active = True
                start_time = time.time()
                aliens_destroyed = 0
                balls = []
                aliens = []
            if event.key == pygame.K_r and game_over:
                game_over = False
                game_active = False

    if game_active:
        elapsed_time = time.time() - start_time
        time_left = game_time - elapsed_time

        if time_left <= 0:
            game_active = False
            game_over = True

        # Capture frame
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                index_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                player_x = int(index_finger_tip_x * WIDTH) - player_width // 2

                # Check hand squeeze
                distance = ((index_finger_tip_x - thumb_tip_x) ** 2 + (index_finger_tip_y - thumb_tip_y) ** 2) ** 0.5
                if distance < 0.05:
                    balls.append([player_x + player_width // 2, player_y])

        player_x = max(0, min(WIDTH - player_width, player_x))
        player_y = HEIGHT - player_height

        for ball in balls[:]:
            ball[1] += ball_speed
            if ball[1] < 0:
                balls.remove(ball)

        aliens_to_remove = []
        for alien in aliens:
            for ball in balls[:]:
                if alien.rect.collidepoint(ball[0], ball[1]):
                    alien.health -= 1
                    balls.remove(ball)
                    if alien.health <= 0:
                        aliens_to_remove.append(alien)

        for alien in aliens_to_remove:
            if alien in aliens:
                aliens.remove(alien)
                aliens_destroyed += 1

        current_time = time.time()
        if current_time - last_alien_spawn_time > alien_spawn_interval:
            new_alien = Alien(WIDTH, HEIGHT)
            aliens.append(new_alien)
            last_alien_spawn_time = current_time

        for alien in aliens[:]:
            alien.update()
            if alien.rect.y > HEIGHT:
                aliens.remove(alien)

        screen.fill(BLACK)
        screen.blit(player_image, (player_x, player_y))
        for ball in balls:
            pygame.draw.circle(screen, RED, (ball[0], ball[1]), ball_radius)
        for alien in aliens:
            alien.draw(screen)

        ui_manager.draw_game_ui(aliens_destroyed, time_left)

    elif game_over:
        ui_manager.draw_game_over(aliens_destroyed)
    else:
        ui_manager.draw_menu()

    pygame.display.flip()
    clock.tick(30)

cap.release()
hands.close()
pygame.quit()

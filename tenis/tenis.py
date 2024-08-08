import pygame
import sys
import tkinter as tk
import time


pygame.init()

# okno, barvy, hodiny, palky, velikost mice, skore, font skore
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tenis')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

paddle_width = 15
paddle_height = 100
paddle_speed = 7

ball_size = 20

player1_score = 0
player2_score = 0

score_font = pygame.font.Font(None, 74)
names_font = pygame.font.Font(None, 48)

def show_welcome_screen():
    # Tkinter 
    root = tk.Tk()
    root.title("Welcome to Tenis Game")
    root.geometry("400x450")

    tk.Label(root, text="Welcome to Pong!", font=("Arial", 16)).pack(pady=20)
    tk.Label(root, text="Controls:", font=("Arial", 14)).pack(pady=5)
    tk.Label(root, text="Player 1: W and S keys", font=("Arial", 12)).pack(pady=2)
    tk.Label(root, text="Player 2: Arrow keys", font=("Arial", 12)).pack(pady=2)
    tk.Label(root, text="Game ends when a player scores 10 points.", font=("Arial", 12)).pack(pady=10)
    player1_name = tk.StringVar(value="Player 1")
    player2_name = tk.StringVar(value="Player 2")
    tk.Label(root, text="Enter Player 1 name:").pack(pady=5)
    tk.Entry(root, textvariable=player1_name).pack()
    tk.Label(root, text="Enter Player 2 name:").pack(pady=5)
    tk.Entry(root, textvariable=player2_name).pack()

    # zavre tkinkter
    def start_game():
        root.destroy()

    # Po zmacknuti "start" se hra spusti
    tk.Button(root, text="START", command=start_game, font=("Arial", 14)).pack(pady=20)

    # Start Tkinter 
    root.mainloop()

    # vrati jmena hracu
    return player1_name.get(), player2_name.get()

def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        countdown_text = score_font.render(f"{i}", True, WHITE)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

def select_difficulty_tk():
    ball_speed = None

    # fce na vyber narocnosti
    def set_difficulty(speed):
        nonlocal ball_speed
        ball_speed = speed
        root.destroy()

    # Create Tkinter root window
    root = tk.Tk()
    root.title("Select Difficulty")
    root.geometry("300x300")

    # tkinkter vyber narocnosti
    tk.Label(root, text="Choose Difficulty", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Beginner", command=lambda: set_difficulty(5), font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="Guru", command=lambda: set_difficulty(7), font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="Djokovic", command=lambda: set_difficulty(10), font=("Arial", 14)).pack(pady=5)

    # Start tkinkter
    root.mainloop()

    return ball_speed

def main_game(ball_speed_x, ball_speed_y, player1, player2):
    global player1_score, player2_score

    # pozice palek
    left_paddle = pygame.Rect(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

    # pozice mice
    ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)

    # rychlost mice
    ball_speed_x = ball_speed_x
    ball_speed_y = ball_speed_y

    # hraci smycka
    while True:
        # eventy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # pohyb palek
        keys = pygame.key.get_pressed()

        # klavesy hrac 1
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < screen_height:
            left_paddle.y += paddle_speed

        # klavesy hrac 2
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < screen_height:
            right_paddle.y += paddle_speed

        # pohyb mice
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # kolize mice nahore a dole
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        # kolize mice s palkami
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            # Ensure ball does not get stuck in the paddles
            if ball_speed_x > 0 and ball.colliderect(right_paddle):
                ball.right = right_paddle.left
            elif ball_speed_x < 0 and ball.colliderect(left_paddle):
                ball.left = left_paddle.right
            ball_speed_x *= -1

        # mic mimo limity (reset)
        if ball.left <= 0:
            player2_score += 1
            ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
            ball_speed_x *= -1

        if ball.right >= screen_width:
            player1_score += 1
            ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
            ball_speed_x *= -1

        # Check jestli nekdo z hracu dosahl 10 bodu=vyhral
        if player1_score == 10:
            display_winner(player1)
            break
        if player2_score == 10:
            display_winner(player2)
            break

        # kresleni
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height))

        # zobrazeni jmen hracu s pozadim
        names_text = names_font.render(f"{player1} : {player2}", True, WHITE)
        names_rect = pygame.Rect(screen_width // 2 - names_text.get_width() // 2 - 10, 10, names_text.get_width() + 20, names_text.get_height() + 10)
        pygame.draw.rect(screen, (0, 0, 0), names_rect)  # Background color for names
        screen.blit(names_text, (screen_width // 2 - names_text.get_width() // 2, 15))

        # zobr. skore s pozadim
        score_text = score_font.render(f"{player1_score}:{player2_score}", True, WHITE)
        score_rect = pygame.Rect(screen_width // 2 - score_text.get_width() // 2 - 10, 80, score_text.get_width() + 20, score_text.get_height() + 10)
        pygame.draw.rect(screen, (0, 0, 0), score_rect)  # Background color for score
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 85))

        pygame.display.flip()
        clock.tick(60)

def display_winner(winner_name):
    screen.fill(BLACK)
    winner_text = score_font.render(f"{winner_name} Wins!", True, WHITE)
    screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - winner_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)  # Display winner for 3 seconds before exiting
    pygame.quit()
    sys.exit()

# Main game flow
player1, player2 = show_welcome_screen()
ball_speed = select_difficulty_tk()
countdown()
main_game(ball_speed, ball_speed, player1, player2)

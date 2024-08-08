import pygame
import sys
import tkinter as tk
import time

pygame.init()

# Zjistit velikost obrazovky
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Nastavit výchozí režim (okno)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tenis')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

clock = pygame.time.Clock()

# Velikosti a rychlosti relativní k velikosti obrazovky
paddle_width = screen_width // 50
paddle_height = screen_height // 4
paddle_speed = screen_height // 100

ball_size = screen_width // 40

player1_score = 0
player2_score = 0

score_font = pygame.font.Font(None, screen_width // 10)
names_font = pygame.font.Font(None, screen_width // 20)

# Pozice a velikost tlačítka Zavřít
close_button_width = 30
close_button_height = 30
close_button_rect = pygame.Rect(screen_width - close_button_width, 0, close_button_width, close_button_height)

def draw_close_button():
    pygame.draw.rect(screen, GRAY, close_button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render('X', True, BLACK)
    screen.blit(text, (close_button_rect.x + 8, close_button_rect.y + 2))

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

    # Zavře Tkinter
    def start_game():
        root.destroy()

    # Po zmáčknutí "START" se hra spustí
    tk.Button(root, text="START", command=start_game, font=("Arial", 14)).pack(pady=20)

    # Start Tkinter
    root.mainloop()

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

    # Funkce na výběr náročnosti
    def set_difficulty(speed):
        nonlocal ball_speed
        ball_speed = speed
        root.destroy()

    # Vytvořit Tkinter root okno
    root = tk.Tk()
    root.title("Select Difficulty")
    root.geometry("300x300")

    # Tkinter výběr náročnosti
    tk.Label(root, text="Choose Difficulty", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Beginner", command=lambda: set_difficulty(5), font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="Guru", command=lambda: set_difficulty(7), font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="Djokovic", command=lambda: set_difficulty(10), font=("Arial", 14)).pack(pady=5)

    # Start Tkinter
    root.mainloop()

    return ball_speed

def main_game(ball_speed_x, ball_speed_y, player1, player2):
    global player1_score, player2_score

    # Pozice palek
    left_paddle = pygame.Rect(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

    # Pozice míče
    ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)

    # Rychlost míče
    ball_speed_x = ball_speed_x
    ball_speed_y = ball_speed_y

    while True:
        # Eventy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Zpracování kliknutí na tlačítko Zavřít
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Pohyb palek
        keys = pygame.key.get_pressed()

        # Klávesy hráč 1
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < screen_height:
            left_paddle.y += paddle_speed

        # Klávesy hráč 2
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < screen_height:
            right_paddle.y += paddle_speed

        # Pohyb míče
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Kolize míče nahoře a dole
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        # Kolize míče s palkami
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            if ball_speed_x > 0 and ball.colliderect(right_paddle):
                ball.right = right_paddle.left
            elif ball_speed_x < 0 and ball.colliderect(left_paddle):
                ball.left = left_paddle.right
            ball_speed_x *= -1

        # Míč mimo limity (reset)
        if ball.left <= 0:
            player2_score += 1
            ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
            ball_speed_x *= -1

        if ball.right >= screen_width:
            player1_score += 1
            ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
            ball_speed_x *= -1

        # Check jestli někdo z hráčů dosáhl 10 bodů = vyhrál
        if player1_score == 10:
            display_winner(player1)
            break
        if player2_score == 10:
            display_winner(player2)
            break

        # Kreslení
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height))

        # Zobrazení jmen hráčů s pozadím
        names_text = names_font.render(f"{player1} : {player2}", True, WHITE)
        names_rect = pygame.Rect(screen_width // 2 - names_text.get_width() // 2 - 10, 10, names_text.get_width() + 20, names_text.get_height() + 10)
        pygame.draw.rect(screen, (0, 0, 0), names_rect)  
        screen.blit(names_text, (screen_width // 2 - names_text.get_width() // 2, 15))

        # Zobrazení skóre s pozadím
        score_text = score_font.render(f"{player1_score}:{player2_score}", True, WHITE)
        score_rect = pygame.Rect(screen_width // 2 - score_text.get_width() // 2 - 10, 80, score_text.get_width() + 20, score_text.get_height() + 10)
        pygame.draw.rect(screen, (0, 0, 0), score_rect)  
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 85))

        # Zobrazit tlačítko Zavřít (pri zvetseni na obrazovku se da manualne vypnout)
        draw_close_button()

        pygame.display.flip()
        clock.tick(60)

def display_winner(winner_name):
    screen.fill(BLACK)
    winner_text = score_font.render(f"{winner_name} Wins!", True, WHITE)
    screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - winner_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)  
    pygame.quit()
    sys.exit()

# Main game flow
player1, player2 = show_welcome_screen()
ball_speed = select_difficulty_tk()
countdown()
main_game(ball_speed, ball_speed, player1, player2)

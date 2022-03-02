'''
TODO(Return l8r)
1 - clear/ reset variabels on gameover/won.🥱
2 - make clock timer.👍
3 - add sounds/ music.🥱
4 -optimize the code.🥱
'''
import pygame
from sys import exit
from math import sqrt

from random_word import words
from random import choice
from time import sleep # make it more realistic
from string import ascii_uppercase

pygame.init()
WIDTH = 900
HEIGHT = 500
run = True
lives = 7
start_time = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
icon = pygame.image.load("images/default/game_icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# font
Font = pygame.font.SysFont("comicsans", 36)
Font1 = pygame.font.SysFont("comicsans", 42)
lcd = pygame.font.Font("font/Lcd.ttf", 50)

# buttons
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RADIUS = 20
GAP = 15
A = 65
letters = []
start_x = round((WIDTH - ((RADIUS * 2 + GAP)*13))/2)
start_y = 400
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i//13)*(GAP + RADIUS * 2))
    letters.append([x, y, chr(A+i), True])


# lives
def lives_function():
    lives_surf = Font.render(
        f"LIVES {lives}", True, BLACK
    )
    lives_rect = lives_surf.get_rect(center=(50, 50))
    screen.blit(lives_surf, lives_rect)


# timer
def timer_function():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    min_time = current_time//60
    if current_time >= 60:
        sec_time = current_time % 60
    else:
        sec_time = current_time
    if sec_time <= 9:
        timer_surf = lcd.render(
            f" {min_time}:0{sec_time}", True, BLACK
        )
    else:
        timer_surf = lcd.render(
            f" {min_time}:{sec_time}", True, BLACK
        )
    timer_rect = timer_surf.get_rect(center=(800, 50))
    screen.blit(timer_surf, timer_rect)


# hangman images
hangman_images = []
for i in range(7):
    hangman_images.append(pygame.image.load(
        f"images/hangman/hangman{i}.png").convert_alpha())


def show_hangman():
    hangman_rect = hangman_images[(7 - (lives))].get_rect(
        center=(WIDTH/2, 150)
    )
    screen.blit(hangman_images[7 - (lives)], hangman_rect)


# get valid
def get_valid(words):
    word = choice(words)
    while '-' in word or ' ' in word:
        word = choice(words)
    return word.upper()


# show word
word = get_valid(words)
word_letters = set(word)
alphabet = set(ascii_uppercase)
used_letters = set()
word_list = [
    letter if letter in used_letters else '-' for letter in word
]


def show_word():
    guess_word = ''.join(word_list)
    word_surf = Font1.render(f"{guess_word}", True, BLACK)
    word_rect = word_surf.get_rect(center=(WIDTH/2, HEIGHT/1.5))
    screen.blit(word_surf, word_rect)


# game over screen
def game_over():
    game_over_surf = Font1.render(f"GAME OVER", True, BLACK)
    game_over_rect = game_over_surf.get_rect(center=(WIDTH/2, HEIGHT/2.5))
    word_over_surf = Font1.render(f"THE WORD IS {word}", True, BLACK)
    word_over_rect = word_over_surf.get_rect(center=(WIDTH/2, HEIGHT/1.75))
    restart_surf = Font1.render("PRESS SPACE TO RESTART", True, BLACK)
    restart_rect = restart_surf.get_rect(center=(WIDTH/2, HEIGHT/1.25))
    screen.blit(game_over_surf, game_over_rect)
    screen.blit(restart_surf, restart_rect)
    screen.blit(word_over_surf, word_over_rect)



# won
def won():
    win_surf = Font1.render(f"YOU WON!!🥳", True, (0, 0, 0, 0.5))
    win_rect = win_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(win_surf, win_rect)


def hangman():
    global lives, letters, run, used_letters, current_time, word_list, word, word_letters
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # button pressed --> disappear
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = sqrt((x - m_x)**2 + (y - m_y)**2)
                        if (dis < RADIUS) and (lives > 0):
                            letter[3] = False
                            if ltr in word_letters:
                                used_letters.add(ltr)
                                word_letters.remove(ltr)
                            else:
                                lives -= 1
                        word_list = [
                            letter if letter in used_letters else '-' for letter in word
                        ]
                        show_word()

                if len(word_letters) == 0 and lives > 1:
                    won()

            # space pressed --> restart
            if (event.type == pygame.KEYDOWN) and (lives == 1):
                if event.key == pygame.K_SPACE:
                    lives = 7
                    current_time = 0
                    run = True
                    used_letters.clear()
                    word_list.clear()
                    for letter in letters:
                        letter[3] = True
                    word = get_valid(words)
                    word_letters = set(word)

        if run and lives > 1:
            # background
            bg_surf = pygame.image.load(
                "images/default/blackboard.jpg").convert_alpha()
            bg_rect = bg_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(bg_surf, bg_rect)

            # call functions
            show_word()
            lives_function()
            timer_function()
            show_hangman()

            # draw buttons
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    pygame.draw.circle(screen, BLACK, (x, y), RADIUS, 2)
                    text = Font.render(ltr, True, WHITE)
                    screen.blit(text, (x - text.get_width()/2,
                                       y - text.get_height()/2))
        else:
            screen.fill(WHITE)
            game_over()
        pygame.display.update()
        clock.tick(60)


# run it
if __name__ == "__main__":
    hangman()

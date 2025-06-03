import pygame 
import pygame.event
import pygame_gui
from colors import Colors
import random
import sys


pygame.init()

WIDTH = 1500
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('KILL ZOMBIE | Mate o máximo de zumbis que conseguir')

manager = pygame_gui.UIManager((WIDTH, HEIGHT), "themes.json")

score = 0

start_ticks = pygame.time.get_ticks()

font = pygame.font.SysFont('Chiller', 50)

x_position = 1
y_position = 90

ZOMBIE_WIDTH = 190 
ZOMBIE_HEIGHT = 190

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

background = pygame.image.load("background3.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

zombie = pygame.image.load("zombie.png")
zombie = pygame.transform.scale(zombie, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))

gun = pygame.image.load("gun.png")
gun = pygame.transform.scale(gun, (300, 300))

shot_gun = pygame.image.load("shot_gun.png")
shot_gun = pygame.transform.scale(shot_gun, (410, 410))
showing_shot_gun = False
shot_gun_timer = 0
SHOT_GUN_DISPLAY_TIME = 100 

shot = pygame.mixer.Sound("pistol_shot.mp3")


def draw_rect():
    screen.blit(zombie, (x_position, y_position))

def random_position():
    global x_position
    x_position = random.randint(0,WIDTH - ZOMBIE_WIDTH)
    global y_position
    y_position = random.randint(90,HEIGHT - ZOMBIE_HEIGHT)

def score_counter():
    global score
    score += 1

restart_button = pygame_gui.elements.UIButton(
    relative_rect= pygame.Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/1.7-BUTTON_HEIGHT/2) , (BUTTON_WIDTH,BUTTON_HEIGHT)),
    text= 'Jogar novamente',
    manager= manager,
    object_id= "#restart_button"
)
end_button = pygame_gui.elements.UIButton(
    relative_rect= pygame.Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/1.5-BUTTON_HEIGHT/2) , (BUTTON_WIDTH,BUTTON_HEIGHT)),
    text= 'Sair',
    manager= manager,
    object_id= "#end_button"
)
restart_button.hide()
end_button.hide()

running =  True
game_over = False
random_position()

while running:
    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (x_position <= mouse_x <= x_position + ZOMBIE_WIDTH and y_position <= mouse_y <= y_position + ZOMBIE_HEIGHT):
                    random_position()
                    score_counter()
                    showing_shot_gun = True
                    shot_gun_timer = pygame.time.get_ticks()
                    shot.play()
        else:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    score = 0
                    start_ticks = pygame.time.get_ticks()
                    game_over = False
                    restart_button.hide()
                    end_button.hide()
                    random_position()
                    showing_shot_gun = False 
                elif event.ui_element == end_button:
                    running = False

    screen.fill(Colors.BLACK)
    screen.blit(background, (0,0))

    if not game_over:
        draw_rect()

        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        temporizador = font.render(f'Tempo: {seconds}  - Mate o máximo de zumbis que conseguir', True, Colors.YELLOW)
        screen.blit(temporizador, (10, 3))

        current_score = font.render(f'Pontuação: {score}', True, Colors.YELLOW)
        screen.blit(current_score, (10, 50))

        if seconds >= 30:
            game_over = True
    else:
        text_score = font.render(f'Pontuação final: {score}', True, Colors.YELLOW)
        text_width = text_score.get_width()
        text_height = text_score.get_height()
        text_x = (WIDTH - text_width) // 2
        text_y = (HEIGHT - text_height) // 2
        screen.blit(text_score, (text_x, text_y))
        restart_button.show()
        end_button.show()

    if showing_shot_gun:
        screen.blit(shot_gun, (WIDTH // 2 - shot_gun.get_width() // 2, HEIGHT - shot_gun.get_height()))
        if pygame.time.get_ticks() - shot_gun_timer > SHOT_GUN_DISPLAY_TIME:
            showing_shot_gun = False
    else:
        screen.blit(gun, (WIDTH // 2 - gun.get_width() // 2, HEIGHT - gun.get_height()))

    manager.update(1/60)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
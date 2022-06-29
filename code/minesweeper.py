import sys
import pygame
from minefield import Minefield

WIDTH, HEIGHT = 500, 600
FPS = 30
ROWS, COLS = 8, 8
MINES = 8
CELL_GAP = 2
CELL_WIDTH = (486 - (COLS+1) * CELL_GAP) // COLS
CELL_HEIGHT = (486 - (ROWS+1) * CELL_GAP) // ROWS

pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

img_background = pygame.image.load('CrackedMineSweeper/assets/images/background.png').convert()
img_mine_flag_icon = pygame.image.load('CrackedMineSweeper/assets/images/mine_flag.png')
img_mine_flag = pygame.transform.scale(img_mine_flag_icon, (CELL_WIDTH, CELL_HEIGHT)).convert_alpha()
img_hidden_cell = pygame.transform.scale(pygame.image.load('CrackedMineSweeper/assets/images/hidden_cell.png'), (CELL_WIDTH, CELL_HEIGHT)).convert()
img_mine = pygame.transform.scale(pygame.image.load('CrackedMineSweeper/assets/images/mine.png'), (CELL_WIDTH, CELL_HEIGHT)).convert_alpha()
img_nums = [pygame.transform.scale(pygame.image.load(f'CrackedMineSweeper/assets/images/num_{i + 1}.png'), (CELL_WIDTH, CELL_HEIGHT)).convert_alpha() for i in range(8)]

snd_mine = pygame.mixer.Sound('CrackedMineSweeper/assets/sounds/explosion.mp3')
snd_win = pygame.mixer.Sound('CrackedMineSweeper/assets/sounds/win.mp3')

pygame.display.set_caption('MineSweeper')
pygame.display.set_icon(img_mine_flag)


def game():
    field = Minefield(ROWS, COLS, MINES)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

            elif field.run and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_events(field, event.button)

        draw(field)

        if field.run:
            field.mine_counter = field.get_mine_counter()
            field.timer += 1/FPS


def mouse_events(field, mouse_click):
    cell_position = get_clicked_cell(*pygame.mouse.get_pos())
    if not cell_position:
        return

    cell = field.matrix[cell_position[0]][cell_position[1]]
    if cell['is_visible']:
        return

    if mouse_click == 1 and not cell['is_flagged']:
        cell['is_visible'] = True
        if cell['value'] == 'Mine':
            game_over(field)
        else:
            field.update_neighbors(cell_position)
            if field.game_is_finished():
                game_won(field)
    elif mouse_click == 3:
        cell['is_flagged'] = not cell['is_flagged']


def get_clicked_cell(mouse_x, mouse_y):
    for y in range(ROWS):
        cur_y = 109 + y * (CELL_HEIGHT + CELL_GAP)
        if not (cur_y < mouse_y < cur_y + CELL_HEIGHT + CELL_GAP):
            continue

        for x in range(COLS):
            cur_x = 9 + x * (CELL_WIDTH + CELL_GAP)
            if cur_x < mouse_x < cur_x + CELL_WIDTH + CELL_GAP:
                return y, x
    return False


def draw(field):
    window.blit(img_background, (0, 0))
    draw_menu(field)
    draw_matrix(field)
    pygame.display.update()
    clock.tick(FPS)


def draw_menu(field):
    font = pygame.font.SysFont('Arial', 60)
    window.blit(font.render(str(field.mine_counter), False, (255, 0, 0)), (160, 12))
    window.blit(font.render(str(int(field.timer)), False, (255, 0, 0)), (320, 12))


def draw_matrix(field):
    for y, row in enumerate(field.matrix):
        cur_y = 109 + y * (CELL_HEIGHT + CELL_GAP)
        for x, cell in enumerate(row):
            cur_x = 9 + x * (CELL_WIDTH+CELL_GAP)

            if not cell['is_visible']:
                window.blit(img_hidden_cell, (cur_x, cur_y))
                if cell['is_flagged']:
                    window.blit(img_mine_flag, (cur_x, cur_y))

            elif cell['value'] == 'Mine':
                window.blit(img_mine, (cur_x, cur_y))

            elif cell['value'] != 0:
                window.blit(img_nums[cell['value'] - 1], (cur_x, cur_y))


def game_over(field):
    field.run = False
    mines = field.get_mines()
    group_size = (len(mines)+1)//3
    mine_groups = (mines[:group_size], mines[group_size:-group_size], mines[-group_size:])

    for group in mine_groups:
        for y, x in group:
            field.matrix[y][x]['is_visible'] = True
        draw(field)
        snd_mine.play()
        pygame.time.wait(1000)


def game_won(field):
    field.run = False
    snd_win.play()

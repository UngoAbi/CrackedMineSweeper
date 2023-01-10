import sys
import pygame
from minefield import Minefield


WIDTH, HEIGHT = 500, 600
FPS = 30
ROWS, COLS = 20, 20  # size of the matrix
MINES = 50  # amount of mines
CELL_GAP = 2
CELL_WIDTH = (486 - (COLS+1) * CELL_GAP) // COLS
CELL_HEIGHT = (486 - (ROWS+1) * CELL_GAP) // ROWS

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

img_background = pygame.image.load("../assets/images/background.png").convert()
img_mine_flag_icon = pygame.image.load("../assets/images/mine_flag.png")
img_mine_flag = pygame.transform.scale(img_mine_flag_icon, (CELL_WIDTH, CELL_HEIGHT)).convert_alpha()
img_hidden_cell = pygame.transform.scale(pygame.image.load("../assets/images/hidden_cell.png"), (CELL_WIDTH, CELL_HEIGHT)).convert()
img_mine = pygame.transform.scale(pygame.image.load("../assets/images/mine.png"), (CELL_WIDTH, CELL_HEIGHT)).convert_alpha()
img_nums = [pygame.transform.scale(pygame.image.load(f"../assets/images/num_{i + 1}.png"), (CELL_WIDTH, CELL_HEIGHT)).convert_alpha() for i in range(8)]

snd_mine = pygame.mixer.Sound('../assets/sounds/explosion.mp3')
snd_win = pygame.mixer.Sound('../assets/sounds/win.mp3')

pygame.display.set_caption("MineSweeper")
pygame.display.set_icon(img_mine_flag)


def game() -> None:
    mf = Minefield(ROWS, COLS, MINES)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and mf.run:
                handle_event(mf, event.button)

        draw(mf)

        if mf.run:
            mf.mine_counter = mf.get_mine_counter()
            mf.timer += 1/FPS


def handle_event(mf: Minefield, mouse_click: int) -> None:
    cell_position = y, x = get_clicked_cell(*pygame.mouse.get_pos())
    if not cell_position:
        return

    cell = mf.matrix[y][x]
    if cell.is_visible:
        return

    if mouse_click == 1 and not cell.is_flagged:
        cell.is_visible = True
        if cell.value == -1:
            game_over(mf)
            return

        mf.update_neighbors(cell_position)
        if mf.all_cells_cleared():
            game_won(mf)

    elif mouse_click == 3:
        cell.is_flagged = not cell.is_flagged


def get_clicked_cell(mouse_x, mouse_y) -> tuple[int, int] | bool:
    for y in range(ROWS):
        cur_y = 109 + y * (CELL_HEIGHT + CELL_GAP)
        if not (cur_y < mouse_y < cur_y + CELL_HEIGHT + CELL_GAP):
            continue

        for x in range(COLS):
            cur_x = 9 + x * (CELL_WIDTH + CELL_GAP)
            if cur_x < mouse_x < cur_x + CELL_WIDTH + CELL_GAP:
                return y, x
    return False


def draw(mf: Minefield) -> None:
    window.blit(img_background, (0, 0))
    draw_hud(mf)
    draw_matrix(mf)
    pygame.display.update()
    clock.tick(FPS)


def draw_hud(mf: Minefield) -> None:
    font = pygame.font.SysFont("Arial", 60)
    window.blit(font.render(str(mf.mine_counter), False, (255, 0, 0)), (160, 12))
    window.blit(font.render(str(int(mf.timer)), False, (255, 0, 0)), (320, 12))


def draw_matrix(mf: Minefield) -> None:
    for y, row in enumerate(mf.matrix):
        cur_y = 109 + y * (CELL_HEIGHT + CELL_GAP)
        for x, cell in enumerate(row):
            cur_x = 9 + x * (CELL_WIDTH + CELL_GAP)
            cur_pos = cur_x, cur_y

            if not cell.is_visible:
                window.blit(img_hidden_cell, cur_pos)
                if cell.is_flagged:
                    window.blit(img_mine_flag, cur_pos)

            elif cell.value == -1:
                window.blit(img_mine, cur_pos)

            elif cell.value != 0:
                window.blit(img_nums[cell.value - 1], cur_pos)


def game_over(mf: Minefield) -> None:
    mf.run = False
    mines = mf.get_mines()
    group_size = (len(mines)+1)//3
    mine_groups = (mines[:group_size], mines[group_size:-group_size], mines[-group_size:])

    for group in mine_groups:
        for y, x in group:
            mf.matrix[y][x].is_visible = True
        draw(mf)
        snd_mine.play()
        pygame.time.wait(1000)


def game_won(mf: Minefield) -> None:
    mf.run = False
    snd_win.play()

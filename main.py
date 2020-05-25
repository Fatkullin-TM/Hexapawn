# -*- coding: utf-8 -*-

"""
Программа с помощью модуля pygame реализует игру 'Шесть пешек'
в отдельном окне.

"""

# %% 

import random

import numpy as np
import pygame

from board import Board
from button import Button

# %% глобальные переменные

WIDTH, HEIGHT = 600, 300
FPS = 30
CAPTION = "Hexapawn"

# размеры клеток на доске
SQUARE_LENGTH = 100
SQUARE_GAP = 5

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (105, 240, 105)
ORANGE = (250, 200, 60)

# вспомогательные словари
colors_dict = {1: BLACK, -1: WHITE,
               0: GREY, 2: ORANGE, 3: ORANGE}
locations_dict = {"Menu": 0,  "PvP": 1, "PvC": 2, "Rules": 3}
curr_player_dict = {"black": 1, "white": -1}

# правила игры
RULES = ""
RULES += "Игроки ходят по очереди, передвигая по одной пешке;\n"
RULES += "начинают белые. Доступные ходы:\n"
RULES += "1) пешка может передвинуться на одну клетку вперёд,\n"
RULES += "если эта клетка пуста;\n"
RULES += "2) пешка может взять пешку другого цвета, стоящую\n"
RULES += "справа или слева на соседней клетке по диагонали.\n\n"
RULES += "Партия считается выигранной в следующих трёх случаях:\n"
RULES += "1) когда одну из пешек удалось провести в третий ряд;\n"
RULES += "2) когда взяты все пешки противника;\n"
RULES += "3) когда противник заблокирован и не может сделать\n"
RULES += "очередного хода."

# %% вспомогательные функции

def list_mouse_update ():
    """
    Функция добавляет в список list_mouse клетку доски,
    на которую нажал пользователь.
    
    """
    
    global list_mouse
    
    x_mouse, y_mouse = pygame.mouse.get_pos()
    if  (0 < x_mouse < (WIDTH // 2))  and (0 < y_mouse < HEIGHT):
        col_m = x_mouse // SQUARE_LENGTH
        row_m = y_mouse // SQUARE_LENGTH
        list_mouse.append((row_m, col_m))
    
def user_move ():
    """
    Функция обрабатывает ходы игрока, введённые нажатиями кнопки мыши
    и хранящиеся в списке list_mouse.
    
    """
    
    global board, list_mouse
    
    if list_mouse:
        row_1, col_1 = list_mouse[0]
        
        if board.right_pawn(row_1, col_1):
            # выбрана пешка текущего игрока
            board.possible_moves(row_1, col_1)
            
            if 2 == len(list_mouse):
                # обработка клика по доске после выбора пешки
                row_2, col_2 = list_mouse[1]
                
                if board.right_move(row_2, col_2):
                    board.do_move(row_1, col_1,
                                  row_2, col_2)
                    
                    if not board.win_check():
                        board.change_player()
                    
                    board.clear_sub_board()
                    list_mouse =  []
                    
                elif board.right_pawn(row_2, col_2):
                    # выбрана другая пешка
                    board.possible_moves(row_2, col_2)
                    list_mouse.pop(0)
                    
                else:  # не выбран ни один ход
                    board.clear_sub_board()
                    list_mouse =  []
        else:  # не выбрана ни одна из пешек
            board.clear_sub_board()
            list_mouse =  []
    else:  # не было кликов по доске
        board.clear_sub_board()

def print_text (x, y, text, surface,
                font_size, font_clr):
    """
    Функция отображает на поверхности surface по координатам (x, y) текст.
    
    """
    
    font = pygame.font.SysFont("couriernew", font_size, bold=True)
    surface.blit(font.render(text, True, font_clr), (x,y))
    
def draw_board (board, list_mouse, surface,
                length=SQUARE_LENGTH, gap=SQUARE_GAP):
    """
    Функция отображает на левой половине поверхности surface доску
    для игры, с выделением цветом выбранных пешек текущего игрока
    и возможных для них ходов.
    
    """
    
    # отрисовка пустой доски
    for col in range(3):
        for row in range(3):
            x = gap + col * length
            y = gap + row * length
            pygame.draw.rect(surface, GREY,
                             (x, y, length - 2 * gap, length - 2 * gap))
            
    # выделение цветом клетки под выбранной пешкой
    if list_mouse:
        row, col = list_mouse[0]
        if board.right_pawn(row, col):
            x = gap + col * length
            y = gap + row * length
            pygame.draw.rect(surface, GREEN,
                             (x, y, length - 2 * gap, length - 2 * gap))
            
    # выделение цветом возможных ходов
    for (row, col), value in np.ndenumerate(board.sub_board):
        if value:
            x = gap + col * length
            y = gap + row * length
            pygame.draw.rect(surface, colors_dict[value],
                             (x, y, length - 2 * gap, length - 2 * gap))
        
    # отрисовка пешек
    for (row, col), value in np.ndenumerate(board.board):
        if value:
            vert = [(length // 2 + col * length,
                     15 + row * length),
                    (length // 4 + col * length,
                     length - 15 + row * length),
                    (3 * length // 4 + col * length,
                     length - 15 + row * length)]
            pygame.draw.polygon(surface, colors_dict[value], vert)
            pygame.draw.polygon(surface, BLACK, vert, 2)
            
# %% реализация главного меню игры и основных режимов игры
    
def Menu_script (surface):
    """
    Функция отрисовывает главное меню игры с тремя интерактивными кнопками.
    
    """ 
    
    # верхняя кнопка "Player vs Player"
    PvP_btn = Button(width=400, height=40,
                     inactive_clr=GREEN, active_clr=ORANGE)
    PvP_btn.draw(100, 45, "Player vs Player",
                 surface, font_size=33, font_clr=BLACK)
    
    # средняя кнопка "Player vs Computer"
    PvС_btn = Button(width=400, height=40,
                     inactive_clr=GREEN, active_clr=ORANGE)
    PvС_btn.draw(100, 130, "Player vs Computer",
                 surface, font_size=33, font_clr=BLACK)
    
    # нижняя кнопка "Правила"
    Rules_btn = Button(width=240, height=40,
                       inactive_clr=GREEN, active_clr=ORANGE)
    Rules_btn.draw(180, 215, "Правила",
                   surface, font_size=33, font_clr=BLACK)
    
    # проверка нажатия кнопок
    if PvP_btn.active:
        pygame.time.delay(200)
        return locations_dict["PvP"]
    elif PvС_btn.active:
        pygame.time.delay(200)
        return locations_dict["PvC"]
    elif Rules_btn.active:
        pygame.time.delay(200)
        return locations_dict["Rules"]
    else:
        return locations_dict["Menu"]
    
def Rules_script (surface):
    """
    Функция отрисовывает страницу с правилами игры и кнопкой 'Назад'.
    
    """
    
    # отображение текста с правилами
    lines = RULES.splitlines()
    for i, line in enumerate(lines):
        print_text(20, 10 + 20*i, line, surface,
                   font_size=17, font_clr=WHITE)
    
    # кнопка "Назад"
    Menu_btn = Button(width=200, height=40,
                     inactive_clr=GREEN, active_clr=ORANGE)
    Menu_btn.draw(350, 240, "Назад",
                 surface, font_size=33, font_clr=BLACK)
    
    # проверка нажатия кнопок
    if Menu_btn.active:
        pygame.time.delay(200)
        return locations_dict["Menu"]
    else:
        return locations_dict["Rules"]    
    
def PvP_script (surface):
    """
    Функция реализует режим игры 'Player vs Player'
    
    """
    
    global board, list_mouse
    
    # обработка ходов, введённых нажатиями кнопки мыши
    user_move()
    
    # отрисовка доски с пешками
    draw_board(board, list_mouse, surface)
    
    # отображение текущего состояния игры
    line1 = line2 = ""
    line1 = "Победа" if board.game_over() else "Ход"
    line2 = "чёрных" if curr_player_dict["black"] == board.curr_player else "белых"
    print_text(350, 30, line1, surface,
               font_size=33, font_clr=WHITE)
    print_text(350, 60, line2, surface,
               font_size=33, font_clr=WHITE)
    
    # кнопка 'Заново'
    Restart_btn = Button(width=200, height=40,
                         inactive_clr=GREEN, active_clr=ORANGE)
    Restart_btn.draw(350, 180, "Заново",
                     surface, font_size=33, font_clr=BLACK)
    if Restart_btn.active:
        board = Board()
        pygame.time.delay(200)
    
    # кнопка 'Меню'
    Menu_btn = Button(width=200, height=40,
                     inactive_clr=GREEN, active_clr=ORANGE)
    Menu_btn.draw(350, 240, "Меню",
                 surface, font_size=33, font_clr=BLACK)
    if Menu_btn.active:
        board = Board()
        pygame.time.delay(200)
        return locations_dict["Menu"]
    else:
        return locations_dict["PvP"]

def PvC_script (surface):    
    """
    Функция реализует режим игры 'Player vs Computer'
    
    """
    
    global board, list_mouse
    
    if curr_player_dict["white"] == board.curr_player:
        # обработка хода пользователя, введённого нажатиями кнопки мыши
        user_move()
    else:
        # ответный ход алгоритма
        if not board.game_over():
            pygame.time.delay(350)
            computer_move = []
            for row_from, col_from in board.pawns[board.curr_player]:
                board.possible_moves(row_from, col_from)
                for (row_to, col_to), value in np.ndenumerate(board.sub_board):
                    if value:                    
                        tmp = (row_from, col_from, row_to, col_to)
                        computer_move.append(tmp)
                        
            row_from, col_from, row_to, col_to = random.choice(computer_move)
            board.possible_moves(row_from, col_from)
            board.do_move(row_from, col_from,
                          row_to, col_to)
            
            if not board.win_check():
                board.change_player()
            board.clear_sub_board()
    
    # отрисовка доски с пешками
    draw_board(board, list_mouse, surface)
    
    # отображение текущего состояния игры
    line1 = line2 = ""
    line1 = "Победа" if board.game_over() else "Ход"
    line2 = "чёрных" if curr_player_dict["black"] == board.curr_player else "белых"
    print_text(350, 30, line1, surface,
               font_size=33, font_clr=WHITE)
    print_text(350, 60, line2, surface,
               font_size=33, font_clr=WHITE)
    
    # кнопка 'Заново'
    Restart_btn = Button(width=200, height=40,
                         inactive_clr=GREEN, active_clr=ORANGE)
    Restart_btn.draw(350, 180, "Заново",
                     surface, font_size=33, font_clr=BLACK)
    if Restart_btn.active:
        board = Board()
        pygame.time.delay(200)
    
    # кнопка 'Меню'
    Menu_btn = Button(width=200, height=40,
                     inactive_clr=GREEN, active_clr=ORANGE)
    Menu_btn.draw(350, 240, "Меню",
                 surface, font_size=33, font_clr=BLACK)
    if Menu_btn.active:
        board = Board()
        pygame.time.delay(200)
        return locations_dict["Menu"]
    else:
        return locations_dict["PvC"]

# %% тело прогораммы
if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)
    
    clock = pygame.time.Clock()
    
    board = Board()
    
    # основной цикл
    curr_location = locations_dict["Menu"]  # текущий режим игры
    list_mouse = []  # список выбранных пользователем клеток доски
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        
        # обработка ввода
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if locations_dict["PvP"] == curr_location:
                    if not board.game_over():
                        list_mouse_update()
                elif locations_dict["PvC"] == curr_location:
                    if (not board.game_over() and 
                        curr_player_dict["white"] == board.curr_player):
                        list_mouse_update()
        
        # отрисовка текущего режима игры
        if locations_dict["Menu"] == curr_location:
            curr_location = Menu_script(screen)
        elif locations_dict["PvP"] == curr_location:
            curr_location = PvP_script(screen)
        elif locations_dict["PvC"] == curr_location:
            curr_location = PvC_script(screen)
        elif locations_dict["Rules"] == curr_location:
            curr_location = Rules_script(screen)
    
        pygame.display.update()
    
    pygame.quit()
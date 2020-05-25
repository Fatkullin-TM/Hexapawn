# -*- coding: utf-8 -*-

import numpy as np
    
# %% описание класса
        
class Board:
    """
    Класс описывает доску для игры 'Шесть пешек'.
    
    """
    
    def __init__ (self, curr_player=-1, winner=0):
        
        tmp = np.zeros((3,3))
        tmp[0, :] = 1  # black pawns
        tmp[2, :] = -1  # white pawns
        self.board = tmp  # основное поле
        
        self.sub_board = np.zeros((3,3))  # вспомогательное поле
        
        self.pawns = {1: [(0, i) for i in range(3)],
                          -1: [(2, i) for i in range(3)]}
        
        self.curr_player = curr_player  # текущий игрок
        self.winner = winner  # победитель
        
    def __repr__ (self):
        
        return str(self.board)
    
    def copy_game (self, board, pawns):        
        
        self.board = board
        self.pawns = pawns
        
    def game_over (self):
        
        if self.winner:
            return True
        return False
    
    def clear_sub_board (self):
        
        self.sub_board = np.zeros((3,3))
        
    def change_player (self):
        
        self.curr_player *= -1
        
    def right_pawn (self, row, col):
        """
        Функция возвращает True, если на клетке (row, col) стоит
        пешка текущего игрока.
        
        """
        
        if (row, col) in self.pawns[self.curr_player]:
            return True
        return False
    
    def right_move (self, row, col):
        """
        Функция возвращает True, если можно сделать ход на клетку (row, col).
        
        """
        
        if self.sub_board[row, col]:
            return True
        return False
    
    def possible_moves (self, row, col):
        """
        Функция записывает возможные ходы пешки, стоящей на клетке (row, col),
        в виде матрицы self.sub_board.
        
        """
        
        self.sub_board = np.zeros((3,3))
        row_next = row + self.curr_player
        
        # возможен ход на одну клетку вперед
        if 0 == self.board[row_next, col]:
            self.sub_board[row_next, col] = 2
        
        # возможно взятие пешки соперника
        enemy = self.curr_player * (-1)
        if (0 == col) or (2 == col):
            if (row_next, 1) in self.pawns[enemy]:
                self.sub_board[row_next, 1] = 3
        elif 1 == col:
            if (row_next, 0) in self.pawns[enemy]:
                self.sub_board[row_next, 0] = 3
            if (row_next, 2) in self.pawns[enemy]:
                self.sub_board[row_next, 2] = 3
        
    def do_move (self,
                 row_from, col_from,
                 row_to, col_to):
        """
        Функция делает ход пешкой с клетки (row_from, col_from) на клетку
        (row_to, col_to).
        
        """
        
        if 2 == self.sub_board[row_to, col_to]:
            # ход на одну клетку вперед
            
            self.board[row_from, col_from] = 0
            self.pawns[self.curr_player].remove((row_from, col_from))
            
            self.board[row_to, col_to] = self.curr_player
            self.pawns[self.curr_player].append((row_to, col_to))
            
        elif 3 == self.sub_board[row_to, col_to]:
            # взятие пешки соперника
            
            self.board[row_from, col_from] = 0
            self.pawns[self.curr_player].remove((row_from, col_from))
            
            enemy = self.curr_player * (-1)
            self.pawns[enemy].remove((row_to, col_to))
            
            self.board[row_to, col_to] = self.curr_player
            self.pawns[self.curr_player].append((row_to, col_to))
        
    def win_check (self):
        """
        Функция возвращает True, если для текущего игрока выполнено
        хотя бы одно условие победы.
        
        """
        
        enemy = self.curr_player * (-1)
        
        # взяты все пешки соперника
        if not self.pawns[enemy]:
            self.winner = self.curr_player
            return True
        
        # одна из пешек в третьем ряду
        last_row = None
        if 1 == self.curr_player:
            last_row = 2
        elif -1 == self.curr_player:
            last_row = 0
            
        for (row, col) in self.pawns[self.curr_player]:
            if last_row == row:
                self.winner = self.curr_player
                return True
        
        # противник не может сделать ход
        self.change_player()
        sum_moves = 0
        for (row, col) in self.pawns[self.curr_player]:
            self.possible_moves(row, col)
            sum_moves += self.sub_board.sum()
        
        self.change_player()
        if not sum_moves:
            self.winner = self.curr_player
            return True
        
        return False
    
# %%

if __name__ == '__main__':
    pass    
# -*- coding: utf-8 -*-

import pygame

# %% описание класса

class Button:
    """
    Класс описывает кнопку, которая меняет свой цвет при наведение курсора.
    
    """
    
    def __init__ (self, width, height,
                  inactive_clr, active_clr):
        
        self.width = width
        self.height = height
        self.inactive_clr = inactive_clr  # обычный цвет кнопки
        self.active_clr = active_clr  # цвет кнопки при наведении курсора
        
        self.active = False
        
    def draw (self, x, y, text,
              surface, font_size, font_clr):
        """
        Функция отрисовывает кнопку на поверхности surface 
        по координатам (x, y).
        
        """
        
        click = pygame.mouse.get_pressed()  # нажатие на кнопку мыши
        x_mouse, y_mouse = pygame.mouse.get_pos()  # координаты курсора
        
        if ((x < x_mouse < (x + self.width)) and 
            (y < y_mouse < (y + self.height))):
            # курсор находиться на кнопке
                pygame.draw.rect(surface, self.active_clr,
                                 (x, y, self.width, self.height))
                if click[0]:
                    # на кнопку нажали левой кнопкой мыши
                    self.active = True
        else:
            pygame.draw.rect(surface, self.inactive_clr,
                             (x, y, self.width, self.height))
        
        # отображение текста по центру кнопки
        font = pygame.font.SysFont("couriernew", font_size, bold=True)
        tmp = font.render(text, True, font_clr)
        surface.blit(tmp,
                     ((x + ((self.width - tmp.get_width()) // 2)),
                     (y + ((self.height - tmp.get_height()) // 2))))
    
# %%
    
if __name__ == '__main__':
    pass
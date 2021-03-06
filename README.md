## Пошаговая игра "Шесть пешек" (реализация через модуль pygame)
Программа с помощью модуля pygame реализует игру "Шесть пешек" (англ. "[Hexapawn](https://ru.wikipedia.org/wiki/Hexapawn)")
в отдельном окне. Управление с помощью мыши. Есть режим игры против компьютера или с другим игроком.

## Файлы
- "main.py": основной цикл игры
- "button.py": реализации класса Button – описывает кнопку (объект для отрисовки на экране),
которая меняет свой цвет при наведение курсора и отображает текст по центру
- "board.py": реализации класса Board – доска для игры, по которой перемещаются пешки согласно правилам,
реализованная с помощью модуля numpy

## Правила игры "Шесть пешек"
Игроки ходят по очереди, передвигая по одной пешке; начинают белые. Доступные ходы:
1. пешка может передвинуться на одну клетку вперёд, если эта клетка пуста;
2. пешка может взять пешку другого цвета, стоящую справа или слева на соседней клетке по диагонали.

Партия считается выигранной в следующих трёх случаях:
1. когда одну из пешек удалось провести в третий ряд;
2. когда взяты все пешки противника;
3. когда противник заблокирован и не может сделать очередного хода.

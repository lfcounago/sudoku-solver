import numpy as np
import time


class SudokuSolver:

    # Este método inicializa la instancia de la clase con un sudoku dado como una matriz de 9x9.
    # También crea un mapa de bits de 9x9x9 que indica qué números se pueden colocar en cada celda del sudoku.
    def __init__(self, sudoku):
        self.bitmap = np.ones((9, 9, 9), dtype=bool)
        self.sudoku = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] != 0:
                    self.place_number(i, j, sudoku[i][j])

    # Este método resuelve el sudoku y devuelve la solución como una matriz de 9x9.
    # También mide el tiempo que tarda en resolverlo y lo almacena en el atributo solve_time.
    def solve(self):
        start = time.time()
        self.backtrack()
        end = time.time()
        self.solve_time = end - start
        return self.sudoku

    # Este método implementa el algoritmo de backtracking recursivo para encontrar la solución del sudoku.
    # Busca la celda con menos opciones posibles y prueba cada número que se puede colocar en ella.
    # Si el número lleva a una solución, lo devuelve. Si no, deshace el movimiento y prueba otro número.
    # Si no hay ningún número que lleve a una solución, devuelve None.
    def backtrack(self):
        if self.is_solved():
            return self.sudoku
        i, j = self.least_options_cell()
        for number in range(1, 10):
            if self.can_place_number(i, j, number):
                curr_bitmap = self.bitmap.copy()
                curr_sudoku = self.sudoku.copy()
                self.place_number(i, j, number)
                self.trivial_moves()
                if self.backtrack() is not None:
                    return self.sudoku
                self.bitmap = curr_bitmap
                self.sudoku = curr_sudoku
        return None

    # Este método comprueba si el sudoku está resuelto, es decir, si no hay ninguna celda vacía.
    def is_solved(self):
        return np.sum(self.sudoku == 0) == 0

    # Este método encuentra la celda con menos opciones posibles, es decir, la que tiene menos números que se pueden colocar en ella según el mapa de bits.
    def least_options_cell(self):
        cell_sums = np.sum(self.bitmap, axis=2)
        cell_sums[cell_sums == 0] = 10
        min_sum_indices = np.unravel_index(
            np.argmin(cell_sums), cell_sums.shape)
        return min_sum_indices

    #  Este método comprueba si se puede colocar un número dado en una celda dada según el mapa de bits.
    def can_place_number(self, i, j, number):
        return self.bitmap[i][j][number-1]

    # Este método coloca un número dado en una celda dada y actualiza el sudoku y el mapa de bits.
    # Elimina el número de las opciones posibles de la fila, la columna y el cuadrado de 3x3 que contienen la celda.
    def place_number(self, i, j, number):
        self.sudoku[i][j] = number
        self.bitmap[i][j] = np.zeros(9, dtype=bool)
        for k in range(9):
            self.bitmap[i][k][number-1] = False
            self.bitmap[k][j][number-1] = False
        for k in range(3):
            for l in range(3):
                self.bitmap[i//3*3+k][j//3*3+l][number-1] = False

    # Este método realiza los movimientos triviales, es decir, los que se pueden deducir sin necesidad de backtracking.
    # Estos son los que corresponden a las celdas que tienen una sola opción posible según el mapa de bits.
    def trivial_moves(self):
        changed = True
        while changed:
            changed = False
            for i in range(9):
                for j in range(9):
                    if self.is_trivial_cell(i, j):
                        changed = True
                        self.place_number(
                            i, j, np.argmax(self.bitmap[i][j]) + 1)

    # Este método comprueba si una celda es trivial, es decir, si tiene una sola opción posible según el mapa de bits.
    def is_trivial_cell(self, i, j):
        return self.sudoku[i][j] == 0 and np.sum(self.bitmap[i][j]) == 1

import numpy as np
import matplotlib.pyplot as plt


def matrix_init(rows_number: int) -> np.array:
    columns_number = rows_number*2 + 1
    matrix_2D = np.zeros((rows_number, columns_number), dtype=bool)
    column_center = columns_number // 2
    matrix_2D[0][column_center] = True
    return matrix_2D


def row_computing(matrix_2D: np.array, rule_number: int) -> np.array:
    if 0 > rule_number > 255:
        raise("Bad value of rule!")
    
    rule_binary_array = []
    for _ in range(8):
        bit = rule_number % 2
        rule_binary_array.insert(0, bit)
        rule_number = rule_number // 2
    matrix_shape = np.shape(matrix_2D)
    number_of_cells_to_modify = 3
    correction_number = 1
    higher_cells_options = {(True, True, True): 0,
                            (True, True, False): 1,
                            (True, False, True): 2,
                            (True, False, False): 3,
                            (False, True, True): 4,
                            (False, True, False): 5,
                            (False, False, True): 6,
                            (False, False, False): 7}
    for row in range(1, matrix_shape[0]):
        cell_to_modify = matrix_shape[1] // 2 - correction_number
        for _ in range(number_of_cells_to_modify):
            input_cells = (matrix_2D[row-1][cell_to_modify - 1: cell_to_modify + 2])
            # tuple is more efficient, and easier to compare than np.array
            input_cells = tuple(input_cells)
            n = higher_cells_options[input_cells]
            matrix_2D[row][cell_to_modify] = rule_binary_array[n]
            cell_to_modify += 1
        number_of_cells_to_modify += 2
        correction_number += 1
    return matrix_2D


def cell_automat_printing(cellular_automaton: np.array) -> None:
    plt.rcParams['image.cmap'] = 'binary'
    fig, ax = plt.subplots(figsize=np.shape(cellular_automaton))
    ax.matshow(cellular_automaton)
    ax.axis(False)
    plt.show


number_of_rows = 200
number_of_rule = 165
cellular_automaton = matrix_init(number_of_rows)
cellular_automaton = row_computing(cellular_automaton, number_of_rule)
cell_automat_printing(cellular_automaton)

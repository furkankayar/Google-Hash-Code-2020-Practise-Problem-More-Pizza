#!/bin/python3

"""
    Written by Furkan Kayar
    23 Jan 2020

    Google Hash Code 2020 Practise Problem:
        More Pizza

    Two approach has been implemented:
        1) Dynamic programming approach developed for small size of inputs.
        2) Greedy approach developed for big size of inputs.

    NOTE: You can set when to use dynamic approach, but dynamic approach requires much memory and time!
"""

def init(filename):
    pizza_types = []
    with open(filename, "r") as file:
        cnt = 0
        for line in file:
            line = line.replace('\n', '').split(' ')
            if cnt == 0:
                max_slices = int(line[0])
                num_pizza_type = int(line[1])
                cnt += 1
            elif cnt == 1:
                for type in line:
                    pizza_types.append(int(type))
                break
    return max_slices, num_pizza_type, pizza_types


def select_pizzas_greedy(max_slices, pizza_types):

    temp = max_slices
    selected_pizzas = []

    i = len(pizza_types) - 1

    while max_slices >= 0:
        if max_slices - pizza_types[i] > 0:
            max_slices = max_slices - pizza_types[i]
            selected_pizzas.append(i)
            if i == 0:
                break
            i = i - 1
        else:
            if i == 0:
                break
            i = i - 1

    print("Greedy approach has been used!\nScore: " + str(temp - max_slices))
    selected_pizzas.reverse()
    return temp - max_slices, selected_pizzas


def create_selection_matrix_for_dynamic_solution(max_slices, num_pizza_type, pizza_types):
    matrix = []

    for j in range(0, len(pizza_types) + 1):
        matrix.append([])
        for i in range(0, max_slices + 1):
            matrix[j].append(0)

    for i in range(1, len(pizza_types) + 1):
        for j in range(1, max_slices + 1):
            if pizza_types[i-1] > j:
                matrix[i][j] = matrix[i-1][j]
            else:
                matrix[i][j] = max(matrix[i-1][j], pizza_types[i-1] + matrix[i-1][j - pizza_types[i-1]])

    return matrix


def select_pizzas_dynamic(max_slices, pizza_types, matrix):


    i = len(pizza_types)
    w = max_slices
    marked_pizza_types = []

    print('Dynamic programming approach has been used!\nScore: ' + str(matrix[i][w]))

    while i > 0 and w > 0:
        if matrix[i][w] != matrix[i-1][w]:
            marked_pizza_types.append(i - 1)
            w = w - pizza_types[i-1]
            i = i - 1
        else:
            i = i - 1



    marked_pizza_types.reverse()
    return matrix[len(pizza_types)][max_slices], marked_pizza_types


def write_file(filename, pizzas):

    try:
        outfilename = filename.split('.')[0] + '.out'
        file = open("out/" + outfilename, "w")
        file.write(str(len(pizzas)) + "\n")
        for pizza in pizzas:
            file.write(str(pizza) + " ")
        file.write("\n")
        file.close()
        print(outfilename + " has been created succesfully!")
    except Exception:
        print("Error occured while writing to file!")


def operate(filename):
    max_slices, num_pizza_type, pizza_types = init(filename)
    filename = filename.split('/')[1]
    score = 0
    print(filename + " has been read succesfully!")
    if(max_slices > 10000 or num_pizza_type > 250):
        score, pizzas = select_pizzas_greedy(max_slices, pizza_types)
        write_file(filename, pizzas)
    else:
        matrix = create_selection_matrix_for_dynamic_solution(max_slices, num_pizza_type, pizza_types)
        score, pizzas = select_pizzas_dynamic(max_slices, pizza_types, matrix)
        write_file(filename, pizzas)

    return score

if __name__ == '__main__':

    files = [
        "in/a_example.in",
        "in/b_small.in",
        "in/c_medium.in",
        "in/d_quite_big.in",
        "in/e_also_big.in"
    ]
    total_score = 0
    print()
    for file in files:
        total_score += operate(file)
        print()

    print("Total Score: " + str(total_score) + "\n")

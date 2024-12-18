################################################
# Day 7: Bridge Repair - Part 1 (by RawbitDev) #
################################################

import os
import itertools
from typing import List

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


def get_equations(filepath: str) -> tuple[int, List[int]]:
    equations = []
    with open(filepath, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                splitted = line.split(": ")
                equations.append((int(splitted[0]), [int(n) for n in splitted[1].split(" ")]))
    return equations


def is_equation_possible(equation) -> bool:
    num_ops = len(equation[1]) - 1
    combinations = itertools.product(["*", "+", "||"], repeat=num_ops)
    for comb in combinations:
        calc = equation[1][0]
        for i, op in enumerate(comb, start=1):
            if op == "*":
                calc *= equation[1][i]
            elif op == "+":
                calc += equation[1][i]
            elif op == "||":
                calc = int(f"{calc}{equation[1][i]}")
        if calc == equation[0]:
            return True
    return False


def sum_possible_tests(filepath: str) -> int:
    equations = get_equations(filepath)
    sum_possible_test_values = 0
    for equation in equations:
        if is_equation_possible(equation):
            sum_possible_test_values += equation[0]
    return sum_possible_test_values


if __name__ == "__main__":
    assert(sum_possible_tests(in_file("test")) == 11387)

    total_calibration_result = sum_possible_tests(in_file("input"))
    print(f"The total calibration result of the possible equations is {total_calibration_result}.")
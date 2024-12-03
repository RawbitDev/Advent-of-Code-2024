###############################################
# Day 3: Mull It Over - Part 1 (by RawbitDev) #
###############################################

import os
import re

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


def mul(x: int, y: int) -> int:
    return x * y


def calc_memory(filepath: str) -> int:
    regex: str = r"mul\(\d+,\d+\)"
    with open(filepath, encoding="utf8") as file:
        corrupted_memory: str = file.read().strip()
        instructions: list[str] = re.findall(regex, corrupted_memory)
        result: int = sum([eval(i) for i in instructions])
        return result
        

if __name__ == "__main__":
    assert(calc_memory(in_file("test")) == 161)

    result: int = calc_memory(in_file("input"))
    print(f"The result of the add up multiplications is {result}.")
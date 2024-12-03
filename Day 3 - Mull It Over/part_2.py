###############################################
# Day 3: Mull It Over - Part 2 (by RawbitDev) #
###############################################

import os
import re

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


class Computer:
    def __init__(self):
        self.result: int = 0
        self.enabled: bool = True
        self.ignore_chars: list[str] = ["'"]
        self.valid_instr: list[str] = [
            r"do\(\)", 
            r"don\'t\(\)", 
            r"mul\(\d+,\d+\)"
        ]
        self.instr_regex: str = f"({'|'.join([instr for instr in self.valid_instr])})"

    def exec(self, instruction: str):
        instr: str = instruction
        for char in self.ignore_chars:
            instr = instr.replace(char, "")
        eval(f"self.{instr}")

    def run(self, memory: str) -> int:
        self.result = 0
        for instr in re.findall(self.instr_regex, memory):
            self.exec(instr)
        return self.result

    def mul(self, x: int, y: int):
        if self.enabled:
            self.result += (x * y)

    def do(self):
        self.enabled = True

    def dont(self):
        self.enabled = False


def calc_memory(filepath: str) -> int:
    with open(filepath, encoding="utf8") as file:
        corrupted_memory: str = file.read().strip()
        return Computer().run(corrupted_memory)
        

if __name__ == "__main__":
    assert(calc_memory(in_file("test")) == 48)

    result: int = calc_memory(in_file("input"))
    print(f"The result of the add up enabled multiplications is {result}.")
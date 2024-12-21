########################################################
# Day 8: Resonant Collinearity - Part 2 (by RawbitDev) #
########################################################

import os
import itertools
import numpy as np

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


def get_input_map(filepath: str) -> np.ndarray[str]:
    rows = []
    with open(filepath, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(list(line))
    return np.array(rows, dtype=str)


def get_antenna_positions(input_map: np.ndarray) -> dict:
    antennas = {}
    for y, x in zip(*np.where(input_map != '.')):
        freq = input_map[y, x]
        if freq not in antennas:
            antennas[freq] = []
        antennas[freq].append((x, y))
    return antennas


def in_map_range(input_map: np.ndarray, pos: tuple[int, int]) -> bool:
    rows, cols = input_map.shape
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols


def add_antinodes_line(input_map: np.ndarray, antinodes: set, x: int, y: int, dx: int, dy: int):
    m = 1
    while True:
        node = (x + dx * m, y + dy * m)
        if not in_map_range(input_map, node):
            break
        antinodes.add(node)
        m += 1


def count_antinodes(filepath: str) -> int:
    input_map = get_input_map(filepath)
    antennas = get_antenna_positions(input_map)
    antinodes = set()
    
    for positions in antennas.values():
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            dx, dy = x2 - x1, y2 - y1

            antinodes.add((x1, y1))
            antinodes.add((x2, y2))
            add_antinodes_line(input_map, antinodes, x1, y1, -dx, -dy)
            add_antinodes_line(input_map, antinodes, x2, y2, dx, dy)

    return len(antinodes)


if __name__ == "__main__":
    assert(count_antinodes(in_file("test")) == 34)

    number_antinodes = count_antinodes(in_file("input"))
    print(f"The number of unique locations that contain an antinode is {number_antinodes}.")
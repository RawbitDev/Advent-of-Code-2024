########################################################
# Day 8: Resonant Collinearity - Part 1 (by RawbitDev) #
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


def count_antinodes(filepath: str) -> int:
    input_map = get_input_map(filepath)
    antennas = get_antenna_positions(input_map)
    antinodes = set()
    
    for positions in antennas.values():
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            dx, dy = x2 - x1, y2 - y1

            node1 = ((x1 - dx), (y1 - dy))
            if in_map_range(input_map, node1):
                antinodes.add(node1)

            node2 = ((x2 + dx), (y2 + dy))
            if in_map_range(input_map, node2):
                antinodes.add(node2)

    return len(antinodes)


if __name__ == "__main__":
    assert(count_antinodes(in_file("test")) == 14)

    number_antinodes = count_antinodes(in_file("input"))
    print(f"The number of unique locations that contain an antinode is {number_antinodes}.")
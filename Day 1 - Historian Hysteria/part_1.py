#####################################################
# Day 1: Historian Hysteria - Part 1 (by RawbitDev) #
#####################################################

import os
import numpy as np

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


def parse_location_line(line: str) -> list[int]:
    locations = line.split(" ")
    locations = [int(loc) for loc in locations if loc]
    return locations


def get_location_matrix(filepath: str) -> np.ndarray[int]:
    location_matrix = np.empty((0, 2), dtype=int)
    with open(filepath, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                locations = parse_location_line(line)
                location_matrix = np.vstack((location_matrix, np.array(locations)))
    return location_matrix


def calc_total_distance(filepath: str) -> int:
    location_matrix = get_location_matrix(filepath)

    location_matrix = np.transpose(location_matrix)
    location_matrix =  np.sort(location_matrix, axis=1)
    location_matrix = np.transpose(location_matrix)

    left = location_matrix[:, 0]
    right = location_matrix[:, 1]
    distances = np.abs(left - right)
    
    total_distance = int(np.sum(distances))
    return total_distance


if __name__ == "__main__":
    assert(calc_total_distance(in_file("test")) == 11)

    total_distance = calc_total_distance(in_file("input"))
    print(f"The total distance between the lists is {total_distance}.")
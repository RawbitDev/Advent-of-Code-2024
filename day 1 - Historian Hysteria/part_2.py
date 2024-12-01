#####################################################
# Day 1: Historian Hysteria - Part 2 (by RawbitDev) #
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


def calc_similarity_score(filepath: str) -> int:
    location_matrix = get_location_matrix(filepath)

    location_matrix = np.transpose(location_matrix)
    location_matrix = np.transpose(location_matrix)

    left = location_matrix[:, 0]
    right = location_matrix[:, 1]
    counts = [np.sum(right == number) for number in left]

    similarity_scores = left * counts
    total_similarity_score = int(np.sum(similarity_scores))
    return total_similarity_score


if __name__ == "__main__":
    assert(calc_similarity_score(in_file("test")) == 31)

    similarity_score = calc_similarity_score(in_file("input"))
    print(f"The similarity score of the lists is {similarity_score}.")
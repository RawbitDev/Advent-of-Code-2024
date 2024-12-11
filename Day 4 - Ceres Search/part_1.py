###############################################
# Day 4: Ceres Search - Part 1 (by RawbitDev) #
###############################################

import os
import numpy as np

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


SEARCH_PATTERNS = [
    [["X","M","A","S"]],
    [["S","A","M","X"]],
    [["X"],
     ["M"],
     ["A"],
     ["S"]],
    [["S"],
     ["A"],
     ["M"],
     ["X"]],
    [["X","","",""],
     ["","M","",""],
     ["","","A",""],
     ["","","","S"]],
    [["S","","",""],
     ["","A","",""],
     ["","","M",""],
     ["","","","X"]],
    [["","","","X"],
     ["","","M",""],
     ["","A","",""],
     ["S","","",""]],
    [["","","","S"],
     ["","","A",""],
     ["","M","",""],
     ["X","","",""]],
]


def get_input_matrix(filepath: str) -> np.ndarray[str]:
    rows = []
    with open(filepath, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(list(line))
    return np.array(rows, dtype=str)


def count_sliding_window_matches(matrix: np.ndarray[str], pattern: np.ndarray[str]) -> int:
    count = 0
    for i in range(matrix.shape[0] - pattern.shape[0] + 1):
        for j in range(matrix.shape[1] - pattern.shape[1] + 1):
            window = matrix[i:i + pattern.shape[0], j:j + pattern.shape[1]]
            mask = (pattern != '') # Match pattern and window, also supporting wildcard ''
            if np.all(window[mask] == pattern[mask]):
                count += 1
    return count


def count_all_pattern_matches(filepath: str) -> int:
    matrix = get_input_matrix(filepath)
    count = 0
    for pattern in SEARCH_PATTERNS:
        count += count_sliding_window_matches(matrix, np.array(pattern))
    return count


if __name__ == "__main__":
    assert(count_all_pattern_matches(in_file("test")) == 18)

    word_count = count_all_pattern_matches(in_file("input"))
    print(f"The word 'XMAS' was found {word_count} times.")
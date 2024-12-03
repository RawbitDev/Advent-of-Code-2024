####################################################
# Day 2: Red-Nosed Reports - Part 1 (by RawbitDev) #
####################################################

import os

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


def parse_levels_line(line: str) -> list[int]:
    levels = line.split(" ")
    levels = [int(level) for level in levels if level]
    return levels


def check_report_levels(levels: list[int]) -> bool:
    diffs = [levels[i] - levels[i-1] for i in range(1, len(levels))]
    return (
        (all(diff > 0 for diff in diffs) or # all increasing
         all(diff < 0 for diff in diffs)) and # all decreasing
         all(abs(diff) <= 3 for diff in diffs) # at most three
    )


def count_safe_reports(filepath: str):
    safe_reports: int = 0
    with open(filepath, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                levels = parse_levels_line(line)
                if check_report_levels(levels):
                    safe_reports += 1
    return safe_reports


if __name__ == "__main__":
    assert(count_safe_reports(in_file("test")) == 2)

    num_safe_reports: int = count_safe_reports(in_file("input"))
    print(f"The total number of safe reports is {num_safe_reports}.")
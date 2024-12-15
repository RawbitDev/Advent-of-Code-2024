##############################################
# Day 5: Print Queue - Part 1 (by RawbitDev) #
##############################################

import os
from typing import Dict, List

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


def parse_rules_input(section: str) -> List[List[int]]:
    rules = []
    for line in section.split("\n"):
        page_numbers = line.split("|")
        rules.append([int(page_numbers[0]), int(page_numbers[1])])
    return rules


def parse_updates_input(section: str) -> List[List[int]]:
    updates = []
    for line in section.split("\n"):
        page_numbers = [int(id) for id in line.split(",")]
        updates.append(page_numbers)
    return updates


def get_input(filepath: str) -> tuple[List[List[int]], List[List[int]]]:
    with open(filepath, encoding="utf8") as file:
        content = file.read()
        sections = content.split("\n\n")
        rules = parse_rules_input(sections[0])
        updates = parse_updates_input(sections[1])
        return rules, updates


def build_graph(rules: List[List[int]]) -> Dict[int, List[int]]:
    graph: Dict[int, List[int]] = {}
    for x, y in rules:
        if x not in graph:
            graph[x] = []
        graph[x].append(y)
    return graph


def check_order(update: List[int], graph: Dict[int, List[int]]) -> bool:
    positions = {page: i for i, page in enumerate(update)}
    for x in graph:
        if x not in positions:
            continue
        for y in graph[x]:
            if y not in positions:
                continue
            if positions[x] > positions[y]:
                return False
    return True


def sum_valid_middles(filepath: str):
    rules, updates = get_input(filepath)
    graph = build_graph(rules)
    sum_middles: int = 0
    for update in updates:
        if check_order(update, graph):
            sum_middles += update[len(update) // 2]
    return sum_middles


if __name__ == "__main__":                     
    assert(sum_valid_middles(in_file("test")) == 143)

    total_middle = sum_valid_middles(in_file("input"))
    print(f"The sum of the middle pages of all correctly-ordered updates is {total_middle}.")
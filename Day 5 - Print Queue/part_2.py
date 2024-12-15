##############################################
# Day 5: Print Queue - Part 2 (by RawbitDev) #
##############################################

import os
from typing import Dict, List
from collections import deque

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


def get_in_degrees(update: List[int], graph: Dict[int, List[int]]) -> Dict[int, int]:
    in_degrees = {page: 0 for page in update}
    for x in graph:
        if x in in_degrees:
            for y in graph[x]:
                if y in in_degrees:
                    in_degrees[y] += 1
    return in_degrees


def fix_update(update: List[int], graph: Dict[int, List[int]]) -> List[int]:
    in_degrees = get_in_degrees(update, graph)
    queue = deque([page for page, degree in in_degrees.items() if degree == 0])
    sorted_update = []
    while queue:
        current_page = queue.popleft()
        sorted_update.append(current_page)
        for next_page in graph.get(current_page, []):
            if next_page in in_degrees:
                in_degrees[next_page] -= 1
                if in_degrees[next_page] == 0:
                    queue.append(next_page)
    return sorted_update


def sum_valid_middles(filepath: str):
    rules, updates = get_input(filepath)
    graph = build_graph(rules)
    sum_middles: int = 0
    for update in updates:
        if not check_order(update, graph):
            fixed_update = fix_update(update, graph)
            sum_middles += fixed_update[len(fixed_update) // 2]
    return sum_middles


if __name__ == "__main__":                     
    assert(sum_valid_middles(in_file("test")) == 123)

    total_middle = sum_valid_middles(in_file("input"))
    print(f"The sum of the middle pages of all correctly-ordered updates is {total_middle}.")
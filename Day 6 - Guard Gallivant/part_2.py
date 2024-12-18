##################################################
# Day 6: Guard Gallivant - Part 2 (by RawbitDev) #
##################################################

import os
import time
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


PRINT_FRAMES = False
FRAME_PAUSE = 0.01
VIEW_DIRECTIONS = ["^", ">", "v", "<"]


def get_input_map(filepath: str) -> np.ndarray[str]:
    rows = []
    with open(filepath, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(list(line))
    return np.array(rows, dtype=str)


class Guard():
    def __init__(self, filepath: str):
        self.base_map = get_input_map(filepath)
        self.current_map = None
        self.guard_pos = None
        self.guard_view_dir = None
        self.reset()

    def __repr__(self):
        return "\n" + "\n".join(["".join(row) for row in self.current_map])
    
    def reset(self):
        self.current_map = self.base_map.copy()
        self.guard_pos = np.where(np.isin(self.current_map, VIEW_DIRECTIONS))
        self.guard_view_dir = self.current_map[self.guard_pos]

    def turn_right(self):
        view_idx = VIEW_DIRECTIONS.index(self.guard_view_dir)
        next_view_idx = (view_idx + 1) % len(VIEW_DIRECTIONS)
        self.guard_view_dir = VIEW_DIRECTIONS[next_view_idx]
        self.current_map[self.guard_pos] = self.guard_view_dir

    def get_next_pos(self):
        pos = (int(self.guard_pos[1][0]), int(self.guard_pos[0][0]))
        if self.guard_view_dir == "^":
            pos = (pos[0], pos[1] - 1)
        elif self.guard_view_dir == ">":
            pos = (pos[0] + 1, pos[1])
        elif self.guard_view_dir == "v":
            pos = (pos[0], pos[1] + 1)
        elif self.guard_view_dir == "<":
            pos = (pos[0] - 1, pos[1])
        return (np.array([pos[1]]), np.array([pos[0]]))
    
    def get_next_field(self):
        next_pos = self.get_next_pos()
        if 0 <= int(next_pos[1][0]) < self.current_map.shape[0] and 0 <= int(next_pos[0][0]) < self.current_map.shape[1]:
            return self.current_map[next_pos]
        return None

    def step(self):
        self.current_map[self.guard_pos] = "X"
        self.guard_pos = self.get_next_pos()
        self.current_map[self.guard_pos] = self.guard_view_dir

    def leave(self):
        self.current_map[self.guard_pos] = "X"
        self.guard_view_dir = None
        self.guard_pos = None

    def print(self):
        if PRINT_FRAMES:
            print(self)
            time.sleep(FRAME_PAUSE)


def patrol_protocol(guard):
    guard.print()
    turn_history = []
    while guard.get_next_field() != None:
        if guard.get_next_field() in ["#", "O"]:
            if (guard.guard_pos, guard.guard_view_dir) in turn_history:
                if PRINT_FRAMES:
                    print("(Loop detected!)")
                    time.sleep(1)
                return None
            turn_history.append((guard.guard_pos, guard.guard_view_dir))
            guard.turn_right()
        else:
            guard.step()
        guard.print()
    guard.leave()
    guard.print()
    return np.where(guard.current_map == "X")


def try_possible_coordinates(args):
    guard, x, y = args
    guard.reset()
    guard.current_map[x, y] = "O"
    if PRINT_FRAMES:
        guard.print()
        time.sleep(1)
    if patrol_protocol(guard) is None:
        return 1
    return 0


def find_patrol_loops(filepath: str):
    guard = Guard(filepath)
    path = patrol_protocol(guard)
    all_coords = list(zip(path[0], path[1]))

    # One task for every possible obstruction position
    tasks = [(Guard(filepath), x, y) for x, y in all_coords]
    with Pool() as pool:
        counts = list(tqdm(pool.imap(try_possible_coordinates, tasks), total=len(tasks)))
    return sum(counts)


if __name__ == "__main__":
    assert(find_patrol_loops(in_file("test")) == 6)

    guard_loops = find_patrol_loops(in_file("input"))
    print(f"There are {guard_loops} different positions to get the guard stuck in a loop.")
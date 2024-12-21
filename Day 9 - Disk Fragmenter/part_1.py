##################################################
# Day 9: Disk Fragmenter - Part 1 (by RawbitDev) #
##################################################

import os
from typing import List

in_file = lambda filename : os.path.join(os.path.dirname(__file__), "data", filename)

#####################################################


class Block:
    def __init__(self, length):
        self.length: int = length

    def __repr__(self):
        return "." * self.length

class Free(Block):
    pass

class File(Block):
    def __init__(self, length, file_id):
        super().__init__(length)
        self.file_id: int = file_id

    def __repr__(self):
        return str(self.file_id) * self.length


def get_disk_map(filepath: str) -> str:
    with open(filepath, encoding="utf8") as file:
        disk_map = file.read()
    return disk_map


def calc_checksum(file_blocks) -> int:
    checksum = 0
    file_id = 0
    for file in file_blocks:
        if file == ".":
            break
        checksum += file_id * int(file)
        file_id += 1
    return checksum


def parse_disk_map(disk_map) -> list:
    disk_blocks = []
    file_id = 0
    for i, block in enumerate(disk_map):
        length = int(block)
        if i % 2 == 0:
            disk_blocks.append(File(length, file_id))
            file_id += 1
        else:
            disk_blocks.append(Free(length))
    return disk_blocks


def get_single_blocks(disk_blocks: List[Block]):
    blocks = []
    for disk_block in disk_blocks:
        block_id = "."
        if isinstance(disk_block, File):
            block_id = disk_block.file_id
        blocks += [block_id] * disk_block.length
    return blocks


def rearrange_blocks(disk_blocks) -> list:
    blocks = get_single_blocks(disk_blocks)
    j = len(blocks)
    for i, block in enumerate(blocks):
        if block == ".":
            while j > i:
                j -= 1
                if blocks[j] != ".":
                    blocks[i], blocks[j] = blocks[j], "."
                    break
    return blocks


def get_compact_checksum(filepath: str) -> int:
    disk_map = get_disk_map(filepath)
    disk_blocks = parse_disk_map(disk_map)
    rearranged_blocks = rearrange_blocks(disk_blocks)
    checksum = calc_checksum(rearranged_blocks)
    return checksum


if __name__ == "__main__":
    assert(get_compact_checksum(in_file("test")) == 1928)

    filesystem_checksum = get_compact_checksum(in_file("input"))
    print(f"The filesystem checksum of the compacted hard drive is {filesystem_checksum}.")
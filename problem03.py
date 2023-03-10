"""
--- Day 3: Rucksack Reorganization ---

One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately,
that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two
compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your
help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is,
a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the
same number of items in each of its two compartments, so the first half of the characters represent items in the
first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the
items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears
in both compartments is lowercase p. The second rucksack's compartments contain jqHRNqRjqzjGDLGL and
rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L. The third rucksack's
compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P. The fourth rucksack's
compartments only share item type v. The fifth rucksack's compartments only share item type t. The sixth rucksack's
compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a priority:

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p),
38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those
item types?
"""
from typing import List

from utility.rucksack import *


def main_problem_three_one(lines):
    print("the first three lines of input")
    for i in range(3):
        print(f"    {lines[i]}")
    print(f"the priority of characters of the first line of input {lines[0]}:")
    first_length = len(lines[0])
    priority_one = [evaluate_item_priority(lines[0][x]) for x in range(first_length)]
    print([[lines[0][i], priority_one[i]] for i in range(first_length)])
    print(f"Split pack #1 = {split_pack(lines[0])}")
    split_pack_one = split_pack(lines[0])
    print(f"Intersection of split pack #1 = {string_intersection(split_pack_one[0], split_pack_one[1])}")

    split_pack_list = [split_pack(lines[i]) for i in range(len(lines))]
    print(f"first couple split packs = {split_pack_list[:3]}")

    intersection_list = [string_intersection(split_pack_list[i][0], split_pack_list[i][1])
                         for i
                         in range(len(split_pack_list))]
    print(f"first couple intersections = {intersection_list[:3]}")

    intersection_list_list = [list(intersection_list[i]) for i in range(len(intersection_list))]
    print(f"first couple intersections, in list form = {intersection_list_list[:3]}")

    priority_list: List[int] = [sum([evaluate_item_priority(intersection_list_list[k][i])
                                     for i
                                     in range(len(intersection_list_list[k]))])
                                for k
                                in range(len(intersection_list_list))]
    print(f"first few priority values = {priority_list[:3]}")

    return sum(priority_list)


def read_input_file():
    file = open("data/problem03.txt")
    lines = [line[:-1] for line in file]
    return lines


"""
--- Part Two ---

As you finish identifying the misplaced items, the Elves come to you with another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg

And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. In the second group, their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
"""


def main_problem_three_two(lines):
    trios = [[lines[i], lines[i+1], lines[i+2]] for i in range(0, len(lines), 3) ]
    print(f"first three trios of rucksacks : {trios[:3]}")
    badges = [string_intersection(trios[i][0], trios[i][1]).intersection(string_intersection(trios[i][0], trios[i][2])) for i in range(len(trios))]
    print(f"the first three badges are {badges[:3]}")
    print(f"there are {len([x in badges for x in badges if len(x) > 1])} rucksacks with more than one badge")
    priorities = [evaluate_item_priority(x.pop()) for x in badges]
    print(f"the first three badges priorities are {priorities[:3]}")
    return sum(priorities)


if __name__ == '__main__':
    lines = read_input_file()

    problem_three_answer = main_problem_three_one(lines)
    print(f"ANSWER TO PROBLEM 3.1, total priority sum = {problem_three_answer}")
    problem_three_answer = main_problem_three_two(lines)
    print(f"ANSWER TO PROBLEM 3.2, total priority sum = {problem_three_answer}")

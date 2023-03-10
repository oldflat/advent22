"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

"""
import numpy as np


def main_problem_8_1(lines, debug_and_log):
    forest_array = np.array([[int(a) for a in line] for line in lines])
    (forest_height, forest_width) = forest_array.shape

    visibility_array = np.array([[0] * forest_width] * forest_height)

    if debug_and_log:
        print(f"part of the forest:")
        print(forest_array[:15, :15])
        print(f"dimensions of forest = {forest_array.shape}")
        print(f"dimensions of visibility array = {visibility_array.shape}")

    for y in range(forest_height):
        for x in range(forest_width):
            if x == 2 and y == 5 and debug_and_log:
                print(f"up {forest_array[:y, x]}")
                print(f"down (reverse) {forest_array[:y:-1, x]}")
                print(f"left {forest_array[y, :x]}")
                print(f"right (reverse) {forest_array[y, :x:-1]}")

            if x == 0 or y == 0 or x == forest_width - 1 or y == forest_height - 1:
                visibility_array[x, y] = 1
                continue

            up_sight_line = forest_array[:y, x]
            down_sight_line = forest_array[:y:-1, x]
            left_sight_line = forest_array[y, :x]
            right_sight_line = forest_array[y, :x:-1]
            if forest_array[y, x] > np.max(up_sight_line) or \
                    forest_array[y, x] > np.max(down_sight_line) or \
                    forest_array[y, x] > np.max(left_sight_line) or \
                    forest_array[y, x] > np.max(right_sight_line):
                visibility_array[y, x] = 1

    return np.sum(visibility_array)


def read_input_file():
    file = open("data/problem08.txt")
    lines = [line[:-1] for line in file]
    return lines


"""
--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

"""


def main_problem_8_2(lines, debug_and_log):
    forest_array = np.array([[int(a) for a in line] for line in lines])
    (forest_height, forest_width) = forest_array.shape

    scenic_score_array = np.array([[0] * forest_width] * forest_height)
    scenic_distance_array = np.array([[[0] * 4] * forest_width] * forest_height)  # Each [0, 0, 0, 0] is [N, S, W, E]

    if debug_and_log:
        print(f"part of the forest:")
        print(forest_array[:15, :15])
        print(f"dimensions of forest = {forest_array.shape}")
        print(f"dimensions of visibility array = {scenic_score_array.shape}")

    for y in range(1, forest_height - 1):
        for x in range(1, forest_width - 1):
            if x == 2 and y == 5 and debug_and_log:
                print(f"up {forest_array[:y, x]}")
                print(f"down (reverse) {forest_array[:y:-1, x]}")
                print(f"left {forest_array[y, :x]}")
                print(f"right (reverse) {forest_array[y, :x:-1]}")

            if x == 0 or y == 0 or x == forest_width - 1 or y == forest_height - 1:
                scenic_score_array[x, y, ::] = 1
                continue

            t = forest_array[y, x]  # current tree height

            north_sight_line = np.flip(forest_array[:y, x]).tolist()
            south_sight_line = np.flip(forest_array[:y:-1, x]).tolist()
            west_sight_line = np.flip(forest_array[y, :x]).tolist()
            east_sight_line = np.flip(forest_array[y, :x:-1]).tolist()

            scenic_distance_array[y, x, 0] = get_score(north_sight_line, t)
            scenic_distance_array[y, x, 1] = get_score(south_sight_line, t)
            scenic_distance_array[y, x, 2] = get_score(west_sight_line, t)
            scenic_distance_array[y, x, 3] = get_score(east_sight_line, t)

            scenic_score_array[y, x] = np.product(scenic_distance_array[y, x])

    return np.max(scenic_score_array)


def get_score(sight_line, t):
    sight_lengths = [len(sight_line[:d])
                     for d
                     in range(1, len(sight_line) + 1)
                     if max(sight_line[:d]) < t]
    if len(sight_lengths) > 0:
        if max(sight_lengths) == len(sight_line):
            return len(sight_line)
        else:
            return max(sight_lengths) + 1
    else:
        return 0


def main():
    input_file_lines = read_input_file()
    problem_answer = main_problem_8_1(input_file_lines, False)
    print(f"ANSWER TO PROBLEM 8.1, number of visible trees = {problem_answer}")
    problem_answer = main_problem_8_2(input_file_lines, False)
    print(f"ANSWER TO PROBLEM 8.2, max_scenic_score = {problem_answer}")

    # ANSWER TO PROBLEM 8.1, number of visible trees = 1700
    # ANSWER TO PROBLEM 8.2, max_scenic_score = 470596


if __name__ == '__main__':
    main()

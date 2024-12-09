from __future__ import division
from numpy import *


def link(a, b):
    return concatenate((a, b[1:]))


def edge(a, b):
    return concatenate(([a], [b]))


def qhull2D(sample):
    def dome(sample, base, depth=0, max_depth=1000):
        h, t = base
        dists = dot(sample - h, dot(((0, -1), (1, 0)), (t - h)))

        if len(dists) == 0:
            return base

        # Handle cases where all distances are very small
        if all(abs(dists) < 1e-10):
            return base

        outer = sample[dists > 0]
        # print("dists:",dists,"outer:",outer)
        # Handle empty outer case
        if len(outer) == 0:
            return base

        pivot_index = argmax(dists)
        pivot = sample[pivot_index]

        # Ensure depth does not exceed maximum allowed
        if depth > max_depth:
            return base

        # Recursive case
        left_dome = dome(outer, edge(h, pivot), depth + 1, max_depth)
        right_dome = dome(outer, edge(pivot, t), depth + 1, max_depth)

        return link(left_dome, right_dome)

    if len(sample) > 2:
        axis = sample[:, 0]
        base = take(sample, [argmin(axis), argmax(axis)], axis=0)
        left_dome = dome(sample, base)
        right_dome = dome(sample, base[::-1])

        return link(left_dome, right_dome)
    else:
        return sample

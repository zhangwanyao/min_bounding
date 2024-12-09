import numpy as np
import matplotlib.pyplot as plt
from .qhull_2d import qhull2D
from .min_bounding_rect import minBoundingRect

def min_area_rect(xy_points):
    # Find convex hull
    hull_points = qhull2D(xy_points)

    # Reverse order of points, to match output from other qhull implementations
    hull_points = hull_points[::-1]

    # print('Convex hull points: \n', hull_points, "\n")

    # Find minimum area bounding rectangle
    width, height, corner_points,area = minBoundingRect(hull_points)


    # # Visualization
    plt.figure()
    plt.plot(xy_points[:, 0], xy_points[:, 1], 'o', label='Points')
    plt.plot(hull_points[:, 0], hull_points[:, 1], 'r--', lw=2, label='Convex Hull')

    # Plot the bounding box
    box = np.vstack([corner_points, corner_points[0]])  # Close the box by repeating the first point
    plt.plot(box[:, 0], box[:, 1], 'g-', lw=2, label='Min Bounding Box')


    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Convex Hull and Minimum Area Bounding Box')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

    return  width, height,corner_points,area


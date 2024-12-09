import numpy as np
import sys

def minBoundingRect(hull_points_2d):
    # Compute edges (x2-x1, y2-y1)
    edges = np.zeros((len(hull_points_2d)-1, 2))  # empty 2 column array
    for i in range(len(edges)):
        edge_x = hull_points_2d[i+1, 0] - hull_points_2d[i, 0]
        edge_y = hull_points_2d[i+1, 1] - hull_points_2d[i, 1]
        edges[i] = [edge_x, edge_y]

    # Calculate edge angles   atan2(y/x)
    edge_angles = np.zeros(len(edges))  # empty 1 column array
    for i in range(len(edge_angles)):
        edge_angles[i] = np.arctan2(edges[i, 1], edges[i, 0])

    # Check for angles in 1st quadrant
    edge_angles = np.abs(edge_angles % (np.pi/2))  # want strictly positive answers

    # Remove duplicate angles
    edge_angles = np.unique(edge_angles)

    # Test each angle to find bounding box with smallest area
    min_bbox = (0, sys.maxsize, 0, 0, 0, 0, 0, 0)  # rot_angle, area, width, height, min_x, max_x, min_y, max_y
    # print("Testing", len(edge_angles), "possible rotations for bounding box... \n")
    for i in range(len(edge_angles)):
        # Create rotation matrix to shift points to baseline
        R = np.array([[np.cos(edge_angles[i]), np.cos(edge_angles[i]-(np.pi/2))],
                      [np.cos(edge_angles[i]+(np.pi/2)), np.cos(edge_angles[i])]])

        # Apply this rotation to convex hull points
        rot_points = np.dot(R, np.transpose(hull_points_2d))  # 2x2 * 2xn

        # Find min/max x,y points
        min_x = np.nanmin(rot_points[0], axis=0)
        max_x = np.nanmax(rot_points[0], axis=0)
        min_y = np.nanmin(rot_points[1], axis=0)
        max_y = np.nanmax(rot_points[1], axis=0)

        # Calculate height/width/area of this bounding rectangle
        width = max_x - min_x
        height = max_y - min_y
        area = width * height

        # Store the smallest rect found first
        if area < min_bbox[1]:
            min_bbox = (edge_angles[i], area, width, height, min_x, max_x, min_y, max_y)

    # Re-create rotation matrix for smallest rect
    angle = min_bbox[0]
    R = np.array([[np.cos(angle), np.cos(angle-(np.pi/2))],
                  [np.cos(angle+(np.pi/2)), np.cos(angle)]])

    # Project convex hull points onto rotated frame
    proj_points = np.dot(R, np.transpose(hull_points_2d))  # 2x2 * 2xn

    # min/max x,y points are against baseline
    min_x = min_bbox[4]
    max_x = min_bbox[5]
    min_y = min_bbox[6]
    max_y = min_bbox[7]

    # Calculate center point and project onto rotated frame
    # center_x = (min_x + max_x) / 2
    # center_y = (min_y + max_y) / 2
    # center_point = np.dot([center_x, center_y], R)

    # Calculate corner points and project onto rotated frame
    corner_points = np.zeros((4, 2))  # empty 2 column array
    corner_points[0] = np.dot([max_x, min_y], R)
    corner_points[1] = np.dot([min_x, min_y], R)
    corner_points[2] = np.dot([min_x, max_y], R)
    corner_points[3] = np.dot([max_x, max_y], R)

    return  min_bbox[2], min_bbox[3], corner_points,area


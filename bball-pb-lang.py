import numpy as np
import cv2 as cv
from loguru import logger

# Court Variables

# Define the court size, and the boundary around the court, and the colour
boundary = 200
court_colour = [200, 130, 50]
# court_line_colour = [60, 60, 60]
court_line_colour = [240, 240, 240]
court_size = {'height': 1400, 'width': 1500}
# court_size_h = 1400
# court_size_w = 1500

# Define the key size
key_size = {'height': 580, 'width': 490}
# key_w = 490
# key_h = 580
key_start = (court_size['width'] / 2) - (key_size['width'] / 2) + boundary

# Based on the court size, define the image size
image_h = court_size['height'] + boundary * 2
image_w = court_size['width'] + boundary * 2

# The thickness of the lines on the court
court_line_thickness = 8

# A numpy array of the base court colour
our_image = np.array([[court_colour] * image_w] * image_h)


# print(img)


def layout_court_boundary(img, boundary, court_size, court_line_thickness):
    # Define the out of bounds points on the court
    pts = np.array([[boundary, boundary], [boundary, court_size['height'] + boundary],
                    [court_size['width'] + boundary, court_size['height'] + boundary],
                    [court_size['width'] + boundary, boundary]], np.int32)
    # Rescape the array to what is expected by cv2
    pts = pts.reshape((-1, 1, 2))
    # print(pts)
    # Use cv to layout the court boundary
    cv.polylines(img, [pts], True, court_line_colour, court_line_thickness, cv.LINE_AA)
    return img


def layout_key_area(img, court_size, key_size, court_line_thickness):
    # Define the key area points on the court

    pts = np.array([[(court_size['width'] / 2) - (key_size['width'] / 2) + boundary, boundary],
                    [(court_size['width'] / 2) - (key_size['width'] / 2) + boundary, key_size['height'] + boundary],
                    [(court_size['width'] / 2) - (key_size['width'] / 2) + boundary + key_size['width'],
                     key_size['height'] + boundary],
                    [(court_size['width'] / 2) - (key_size['width'] / 2) + boundary + key_size['width'], boundary]],
                   np.int32)
    # Rescape the array to what is expected by cv2

    pts = pts.reshape((-1, 1, 2))
    # print(pts)
    # Use cv to layout the key area
    cv.polylines(img, [pts], True, court_line_colour, court_line_thickness, cv.LINE_AA)

    return img


def layout_court_markings(img, boundary, key_size, court_size, court_line_thickness):
    # Top of key semi circle
    cv.ellipse(img, (int((court_size['width'] / 2) + boundary), boundary + key_size['height']), (180, 180), 0, 0, 180,
               court_line_colour, court_line_thickness)
    # Three point line
    # Three point line radius is 675
    cv.ellipse(img, (int((court_size['width'] / 2) + boundary), boundary + 158), (675, 675), 0, 12, 168,
               court_line_colour, court_line_thickness)
    cv.line(img, (boundary + 90, boundary), (boundary + 90, boundary + 297), court_line_colour, court_line_thickness,
            cv.LINE_AA)
    cv.line(img, (boundary + court_size['width'] - 90, boundary), (boundary + court_size['width'] - 90, boundary + 297),
            court_line_colour, court_line_thickness, cv.LINE_AA)
    # Half court circle
    cv.ellipse(img, (int((court_size['width'] / 2) + boundary), boundary + court_size['height']), (180, 180), 180, 0,
               180, court_line_colour, court_line_thickness)
    # Charge circle
    # Radius of charge circle is 125
    baseline_to_hoop = 158
    cv.ellipse(img, (int((court_size['width'] / 2) + boundary), boundary + baseline_to_hoop), (125, 125), 0, 0, 180,
               court_line_colour, court_line_thickness)
    # Hoop location
    # Hoop radius is 30, hoop thickness is 5
    cv.ellipse(img, (int((court_size['width'] / 2) + boundary), boundary + baseline_to_hoop), (30, 30), 0, 0, 360,
               court_line_colour, 5)

    return img


def draw_hex(x, y, c_radius):
    apothem = c_radius * np.cos(np.pi / 6)
    # print(apothem)
    x_adjust = np.square(c_radius) - np.square(apothem)
    x_adjust = int(np.sqrt(x_adjust))
    y_adjust = apothem
    pts = np.array([[x - int(apothem / 2), y - apothem],
                    [x + int(apothem / 2), y - apothem],
                    [x + c_radius, y],
                    [x + int(apothem / 2), y + apothem],
                    [x - int(apothem / 2), y + apothem],
                    [x - c_radius, y]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    # logger.debug(locals())
    return [pts]


# print(draw_hex(court_size_w/2, court_size_h/2, 100))

# cv.polylines(img, draw_hex(court_size_w/2, court_size_h/2, 37), True, (140,140,140), 3, cv.LINE_AA)
# cv.circle(img, (int(court_size_w/2), int(court_size_h/2)), 37, (0, 0, 255), 2, cv.LINE_AA)

def layout_hex_grid(img, line_thickness=2):
    # Divide the court into hex grids, the layout that fits best is:
    # 25 grids high
    # 31 grids wide

    c_radius = 37
    grid_count_height = 25
    grid_count_width = 31
    # An apothem is a line segment from the center of a polygon to the middle point of any one side
    apothem = c_radius * np.cos(np.pi / 6)
    # Calculate the y offset for the next hexagon down
    y_adjust = apothem * 2
    # Calculate the x offset for the next column across (trig here, so the hexagons interlock
    x_adjust = np.square(c_radius) - np.square(apothem)
    x_adjust = int(np.sqrt(x_adjust)) + c_radius

    # Starting x cords for the first hexagon
    x_coord = 70
    # We are writing the hexagons in columns, top to bottom, then left to right
    for i in range(0, grid_count_width):
        # Starting y cords, on every second column, we offset the starting position down so the hexagons interlock
        if (i % 2) == 0:
            y_coord = 110
        else:
            y_coord = 110 + apothem

        x_coord = x_coord + x_adjust

        for j in range(0, grid_count_height):
            # logger.debug("X and Y: " + str(x_coord) + "," + str(y_coord))
            colour = ((i * 10) % 150) + 50
            colour = 65
            # cv.circle(img, (x_ord,y_ord), 37, (0, 0, 255), 1, cv.LINE_AA)
            # logger.debug(draw_hex(x_coord, y_coord, c_radius))
            cv.polylines(img, draw_hex(x_coord, y_coord, c_radius), True, (colour, colour, colour), line_thickness,
                         cv.LINE_AA)
            cv.putText(img, '(' + str(i) + "," + str(j) + ')', (int(x_coord) - 16, int(y_coord)), cv.FONT_HERSHEY_PLAIN,
                       0.8, (100, 100, 100), 1, cv.LINE_AA)
            y_coord = y_coord + y_adjust

    return img


# image_file = 'court.png'
# our_image = layout_hex_grid(our_image)
# our_image = layout_court_boundary(our_image, boundary, court_size, court_line_thickness)
# our_image = layout_key_area(our_image, court_size, key_size, court_line_thickness)
# our_image = layout_court_markings(our_image, boundary, key_size, court_size, court_line_thickness)
#
# cv.imwrite(image_file, our_image)

frames_per_action = 20

game_action = {1: {'O1':
                       {'action': 'Cut',
                        'type': 'Straight',
                        'start_grid': (20, 5),
                        'end_grid': (10, 4)},
                   'O2':
                       {'action': 'Cut',
                        'type': 'Straight',
                        'start_grid': (27, 10),
                        'end_grid': (12, 7)
                        } 
                   }
               }

for action in game_action.keys():
    logger.debug("Processing action : {}".format(action))
    for game_object in game_action[action].keys():
        logger.debug("Game Object: {}".format(game_action[action][game_object].keys()))
    for frame in range(frames_per_action):
        logger.debug("Processing action, frame : {}, {}".format(action,frame))
        for game_object in game_action[action].keys():
            pass
            # logger.debug("Game Object: {}".format(game_object))



# def create_object_path(object_action):

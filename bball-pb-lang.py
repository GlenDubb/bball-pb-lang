import numpy as np
import cv2 as cv

# Create a black image
boundary = 100
court_colour = [234, 182, 118]
court_line_colour = [60, 60, 60]
court_size_h = 1400
court_size_w = 1500

key_w = 490
key_h = 580
key_start = (court_size_w / 2) - (key_w / 2) + boundary

image_h = 1400 + boundary * 2
image_w = 1500 + boundary * 2
court_line_thickness = 15

img = np.array([[court_colour] * image_w] * image_h)
# print(img)


# Draw a diagonal blue line with thickness of 5 px
# cv.line(img, (0, 0), (511, 511), (255, 0, 0), 10, cv.LINE_AA)
# cv.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3, cv.LINE_AA)
# cv.circle(img, (447, 63), 63, (0, 0, 255), -1, cv.LINE_AA)

pts = np.array([[boundary, boundary], [boundary, court_size_h + boundary],
                [court_size_w + boundary, court_size_h + boundary], [court_size_w + boundary, boundary]], np.int32)
pts = pts.reshape((-1, 1, 2))
# print(pts)
cv.polylines(img, [pts], True, court_line_colour, court_line_thickness, cv.LINE_AA)

pts = np.array([[(court_size_w / 2) - (key_w / 2) + boundary, boundary],
                [(court_size_w / 2) - (key_w / 2) + boundary, key_h + boundary],
                [(court_size_w / 2) - (key_w / 2) + boundary + key_w, key_h + boundary],
                [(court_size_w / 2) - (key_w / 2) + boundary + key_w, boundary]], np.int32)
pts = pts.reshape((-1, 1, 2))
# print(pts)
cv.polylines(img, [pts], True, court_line_colour, court_line_thickness, cv.LINE_AA)

# cv.circle(img, (int((court_size_w / 2) + boundary), boundary + key_h),
# 180, court_line_colour, court_line_thickness, cv.LINE_AA)
cv.ellipse(img, (int((court_size_w / 2) + boundary), boundary + key_h ), (180, 180), 0, 0, 180, court_line_colour, court_line_thickness)

cv.ellipse(img, (int((court_size_w / 2) + boundary), boundary + 158 ), (675, 675), 0, 12, 168, court_line_colour, court_line_thickness)
cv.line(img, (boundary + 90, boundary), (boundary + 90, boundary + 297), court_line_colour, court_line_thickness, cv.LINE_AA)
cv.line(img, (boundary + court_size_w - 90, boundary), (boundary + court_size_w - 90, boundary + 297), court_line_colour, court_line_thickness, cv.LINE_AA)

cv.ellipse(img, (int((court_size_w / 2) + boundary), boundary + court_size_h ), (180, 180), 180, 0, 180, court_line_colour, court_line_thickness)
cv.ellipse(img, (int((court_size_w / 2) + boundary), boundary + 158 ), (125, 125), 0, 0, 180, court_line_colour, court_line_thickness)
cv.ellipse(img, (int((court_size_w / 2) + boundary), boundary + 158 ), (30, 30), 0, 0, 360, court_line_colour, 5)


image_file = 'court.png'
cv.imwrite(image_file, img)

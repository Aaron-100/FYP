# Author = Aaron Anderson
# Date = 17/11/2020

# Importing all libraries required
import cv2
import numpy as np


# Image orientation to flip it 180 degrees if necessary
def rotateImage(grayImg):
    (rows, cols) = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1)
    flippedImg = cv2.warpAffine(grayImg, M, (cols, rows))
    return flippedImg


# Detects the circular pattern and restructures image
def straightenCircle(img):
    circles = cv2.HoughCircles(img, method=cv2.HOUGH_GRADIENT, dp=1, minDist=3, circles=None, param1=200, param2=100,
                               minRadius=200, maxRadius=0)

    # Get the mean of centers and do offset
    circles = np.int0(np.array(circles))
    x, y, r = 0, 0, 0
    canvas = img.copy()
    for ptx, pty, radius in circles[0]:
        cv2.circle(canvas, (ptx, pty), radius, (0, 255, 0), 1, 16)
        x += ptx
        y += pty
        r += radius

    cnt = len(circles[0])
    x = x // cnt
    y = y // cnt
    r = r // cnt
    x += 5
    y -= 7

    # Draw the labels in red
    for r in range(100, r, 20):
        cv2.circle(canvas, (x, y), r, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.circle(canvas, (x, y), 3, (0, 0, 255), -1)
    # (5) Crop the image
    dr = r + 20
    croped = img[y - dr:y + dr + 1, x - dr:x + dr + 1].copy()
    # (6) logPolar and rotate
    polar = cv2.logPolar(croped, (dr, dr), 60, cv2.WARP_FILL_OUTLIERS)
    rotated = cv2.rotate(polar, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated = rotated[100:170, 0:490].copy()
    return rotated


# path to find image
path = r'C:\Users\aaron\OneDrive\Documents\4th Year\FYP\Solo_Img\3.jpg'

# Reading in image
img = cv2.imread(path)

# Using cv2.cvtColor() method
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# pass image into function and save new image to variable
digitsImage = straightenCircle(grayImg)

flippedImage = rotateImage(grayImg)

digitsImage2 = straightenCircle(flippedImage)

edges1 = cv2.Canny(digitsImage, 200, 300)
edges2 = cv2.Canny(digitsImage2, 200, 300)
cv2.imshow('edges1', edges1)
cv2.imshow('edges2', edges2)
cv2.waitKey(0)
cv2.destroyAllWindows()


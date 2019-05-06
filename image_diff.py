# USAGE
# python image_diff.py --first images/original_01.png --second images/modified_01.png

from skimage.measure import compare_ssim
import imutils
import cv2
import os
from PIL import Image

from conversion import *

def get_ssim(file1, file2, dir=''):
    imageA = cv2.imread(os.path.join(dir, file1))
    imageB = cv2.imread(os.path.join(dir, file2))

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    # print('{} and {}: '.format(file1, file2) + 'SSIM = {}'.format(score))
    return score

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # show the output images
    # cv2.imshow("Original", imageA)
    # cv2.imshow("Modified", imageB)
    # cv2.imshow("Diff", diff)
    # cv2.imshow("Thresh", thresh)
    # cv2.waitKey(0)

def is_rgb_equal(rgb1, rgb2, show_diff=False):
    if rgb1 == rgb2:
        return True

    if show_diff:
        for i in range(len(rgb1)):
            if rgb1[i] != rgb2[i]:
                print(i, rgb1[i], rgb2[i])

    return False

def total_comparison(dir):
    print('_total_comparison_')
    files = os.listdir(dir)
    total = av1 = wmk = 0
    with open(dir + '_comp.csv', 'w') as out:
        for f in files:
            if f[0] != '0':
                continue

            file, rgb = [], []
            for i in range(3):
                file.append(str(i) + f[1:])
                img = Image.open(os.path.join(dir, file[i]))
                rgb.append(get_rgb(img))
                img.close()

            line = [file[0][2:]]
            line.extend([get_ssim(file[0], file[1], dir), is_rgb_equal(rgb[0], rgb[1])])    # av1
            line.extend([get_ssim(file[1], file[2], dir), is_rgb_equal(rgb[1], rgb[2])])    # wmk
            out.write(' | '.join([str(i) for i in line]) + '\n')
            # print(file[0][2:])
            # print('av1:\tSSIM = {}\tRGB_equal = {}'.format(get_ssim(file[0], file[1], dir), is_rgb_equal(rgb[0], rgb[1])))
            # print('wmk:\tSSIM = {}\tRGB_equal = {}'.format(get_ssim(file[1], file[2], dir), is_rgb_equal(rgb[1], rgb[2])))
            # print()
            total += 1
            if is_rgb_equal(rgb[0], rgb[1]):
                av1 += 1
            if is_rgb_equal(rgb[1], rgb[2]):
                wmk += 1
    print("total: %d\tav1: %d\twmk: %d" % (total, av1, wmk))

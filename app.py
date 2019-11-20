import cv2
import os
import sys
import numpy
import matplotlib.pyplot as plt
from enhance import image_enhance
from skimage.morphology import skeletonize, thin


def removedot(invertThin):
    temp0 = numpy.array(invertThin[:])
    temp0 = numpy.array(temp0)
    temp1 = temp0 / 255
    temp2 = numpy.array(temp1)
    temp3 = numpy.array(temp2)

    enhanced_img = numpy.array(temp0)
    filter0 = numpy.zeros((10, 10))
    W, H = temp0.shape[:2]
    filtersize = 6

    for i in range(W - filtersize):
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize, j:j + filtersize]

            flag = 0
            if sum(filter0[:, 0]) == 0:
                flag += 1
            if sum(filter0[:, filtersize - 1]) == 0:
                flag += 1
            if sum(filter0[0, :]) == 0:
                flag += 1
            if sum(filter0[filtersize - 1, :]) == 0:
                flag += 1
            if flag > 3:
                temp2[i:i + filtersize, j:j +
                      filtersize] = numpy.zeros((filtersize, filtersize))

    return temp2


def get_descriptors(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    img = image_enhance.image_enhance(img)
    img = numpy.array(img, dtype=numpy.uint8)
    # Threshold
    ret, img = cv2.threshold(
        img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # Normalize to 0 and 1 range
    img[img == 255] = 1

    # Thinning
    skeleton = skeletonize(img)
    skeleton = numpy.array(skeleton, dtype=numpy.uint8)
    skeleton = removedot(skeleton)
    # Harris corners
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(
        harris_corners,
        0,
        255,
        norm_type=cv2.NORM_MINMAX,
        dtype=cv2.CV_32FC1)
    threshold_harris = 125
    # Extract keypoints
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))
    # Define descriptor
    orb = cv2.ORB_create()
    # Compute descriptors
    _, des = orb.compute(img, keypoints)
    return (keypoints, des)


def main():
    des = get_des_sample(sys.argv[1])

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    name = comparisons_with_permitted_images(des, bf)

    if name:
        print("The owner of the fingerprint is: " + name)
    else:
        print("Not found in the database")


def comparisons_with_permitted_images(sample_fingerprint, bf):
    score_threshold = 33

    for fingerprint in fingerprint_database():
        permitted_fingerprint = get_des_permitted(fingerprint["fingerprint"])

        matches = sorted(bf.match(sample_fingerprint, permitted_fingerprint), key=lambda match: match.distance)

        print(fingerprint["fingerprint"])

        score = 0
        for match in matches:
            score += match.distance

        actual_score = score / len(matches)
        print(actual_score)

        if actual_score < score_threshold:
            return fingerprint["name"]


def get_des_permitted(image_name):
    image_path = "database/permitted/" + image_name

    return get_des(image_path)


def get_des_sample(image_name):
    image_path = "database/samples/" + image_name

    return get_des(image_path)


def get_des(image_path):
    if os.path.exists(image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        kp, des = get_descriptors(img)

        return des
    else:
        raise BaseException


def fingerprint_database():
    database = (
                    {"name": "Dave", "fingerprint": "101_1.tif"},
                    {"name": "John", "fingerprint": "102_1.tif"},
                    {"name": "Foo", "fingerprint": "103_1.tif"},
                    {"name": "Bar", "fingerprint": "104_1.tif"},
                    {"name": "Tonico", "fingerprint": "105_1.tif"},
                    {"name": "Tinoco", "fingerprint": "106_1.tif"}
                )

    return database


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        raise

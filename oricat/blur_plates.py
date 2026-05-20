"""Blur plates module for oricat."""

import os

import cv2

from .logger import init


def _apply_blur(img, plates, logger, filename):
    """Apply Gaussian blur to detected license plate regions in an image."""
    # pylint: disable=no-member

    if len(plates) > 0:
        logger.info("Found %s plate(s) in %s, blurring...", len(plates), filename)
        for x, y, w, h in plates:
            roi = img[y : y + h, x : x + w]
            img[y : y + h, x : x + w] = cv2.GaussianBlur(roi, (51, 51), 0)
    else:
        logger.warning("No plates detected in %s", filename)
    return img


def _blur_plates(input_dir: str, output_dir: str) -> None:
    """Detect and blur license plates in image files."""
    # pylint: disable=no-member

    logger = init()
    plate_cascade_path = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"
    plate_cascade = cv2.CascadeClassifier(plate_cascade_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    exts = [".jpg", ".jpeg", ".png"]
    images = [
        f
        for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f))
        and f.lower().endswith(tuple(exts))
    ]

    logger.info("Processing %s images from %s...", len(images), input_dir)

    for filename in images:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        logger.debug("Processing %s", filename)
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        img = _apply_blur(img, plates, logger, filename)
        cv2.imwrite(output_path, img)
        logger.debug("Wrote %s", output_path)

    logger.info("Finished processing %s images to %s", len(images), output_dir)

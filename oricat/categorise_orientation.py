"""Categorise orientation module for oricat."""

import os

from PIL import Image

from .logger import init


def _read_orientation_images(input_dir: str, logger) -> list:
    """Read images from the input directory."""

    logger.info("Reading images from %s...", input_dir)

    exts = [".jpg", ".jpeg", ".png", ".gif"]
    images = []
    for image in os.listdir(input_dir):
        if image.endswith(tuple(exts)):
            logger.debug("Found %s", image)
            images.append(image)

    logger.info("Found %s images in %s", len(images), input_dir)

    return images


def _categorise_orientation_images(input_dir: str, images: list, logger) -> tuple:
    """Categorise images based on orientation: portrait, landscape, and square."""

    logger.info("Categorising %s images...", len(images))

    landscape_images = []
    portrait_images = []
    square_images = []

    for image in images:
        with Image.open(os.path.join(input_dir, image)) as img:
            width, height = img.size
            if width > height:
                logger.debug("%s is landscape", image)
                landscape_images.append(image)
            elif width < height:
                logger.debug("%s is portrait", image)
                portrait_images.append(image)
            else:
                logger.debug("%s is square", image)
                square_images.append(image)

    logger.info("Found %s landscape images", len(landscape_images))
    logger.info("Found %s portrait images", len(portrait_images))
    logger.info("Found %s square images", len(square_images))

    return (landscape_images, portrait_images, square_images)


def _write_orientation_images(
    images: list, orientation: str, input_dir: str, output_dir: str, logger
) -> None:
    """Write images to the output directory based on the orientation as sub-directory."""

    orientation_dir = os.path.join(output_dir, orientation)
    logger.info(
        "Writing %s %s images to %s...", len(images), orientation, orientation_dir
    )

    if not os.path.exists(orientation_dir):
        os.makedirs(orientation_dir)

    for image in images:
        logger.debug("Writing %s to %s/", image, orientation_dir)
        os.rename(os.path.join(input_dir, image), os.path.join(orientation_dir, image))

    logger.info(
        "Finished writing %s %s images to %s", len(images), orientation, orientation_dir
    )


def _categorise_orientation(input_dir: str, output_dir: str) -> None:
    """Categorise image files based on orientation:
    portrait, landscape, and square, one directory for each.
    """

    logger = init()

    images = _read_orientation_images(input_dir, logger)

    landscape_images, portrait_images, square_images = _categorise_orientation_images(
        input_dir, images, logger
    )

    _write_orientation_images(landscape_images, "landscape", input_dir, output_dir, logger)
    _write_orientation_images(portrait_images, "portrait", input_dir, output_dir, logger)
    _write_orientation_images(square_images, "square", input_dir, output_dir, logger)

# pylint: disable=too-many-locals
"""
oricat
=======
Tag any AWS resource via config file.
"""

import os
import click
from PIL import Image
from .logger import init

def categorise(input_dir: str, output_dir: str) -> None:
    """Categorise image files based on orientation:
    portrait, landscape, and square, one directory for each.
    """

    logger = init()

    images = _read_images(input_dir, logger)

    landscape_images, portrait_images, square_images = _categorise_images(input_dir, images, logger)

    _write_images(landscape_images, 'landscape', input_dir, output_dir, logger)
    _write_images(portrait_images, 'portrait', input_dir, output_dir, logger)
    _write_images(square_images, 'square', input_dir, output_dir, logger)

def _read_images(input_dir: str, logger) -> list:
    """Read images from the input directory."""

    logger.info(f'Reading images from {input_dir}...')

    exts = ['.jpg', '.jpeg', '.png', '.gif']
    images = []
    for image in os.listdir(input_dir):
        if image.endswith(tuple(exts)):
            logger.debug(f'Found {image}')
            images.append(image)

    logger.info(f'Found {len(images)} images in {input_dir}')

    return images

def _categorise_images(input_dir: str, images: list, logger) -> dict:
    """Categorise images based on orientation: portrait, landscape, and square."""

    logger.info(f'Categorising {len(images)} images...')

    landscape_images = []
    portrait_images = []
    square_images = []

    for image in images:
        with Image.open(os.path.join(input_dir, image)) as img:
            width, height = img.size
            if width > height:
                logger.debug(f'{image} is landscape')
                landscape_images.append(image)
            elif width < height:
                logger.debug(f'{image} is portrait')
                portrait_images.append(image)
            else:
                logger.debug(f'{image} is square')
                square_images.append(image)

    logger.info(f'Found {len(landscape_images)} landscape images')
    logger.info(f'Found {len(portrait_images)} portrait images')
    logger.info(f'Found {len(square_images)} square images')

    return (landscape_images, portrait_images, square_images)

def _write_images(images: list, orientation: str, input_dir: str, output_dir: str, logger) -> None:
    """Write images to the output directory based on the orientation as sub-directory."""

    orientation_dir = os.path.join(output_dir, orientation)
    logger.info(f'Writing {len(images)} {orientation} images to {orientation_dir}...')

    if not os.path.exists(orientation_dir):
        os.makedirs(orientation_dir)

    for image in images:
        logger.debug(f'Writing {image} to {orientation_dir}/')
        os.rename(os.path.join(input_dir, image), os.path.join(orientation_dir, image))

    logger.info(f'Finished writing {len(images)} {orientation} images '\
                f'to {orientation_dir}')

@click.command()
@click.option('--input-dir', default='oricat', show_default=True, type=str,
              help='Input directory where the files to be categorised are located')
@click.option('--output-dir', default='oricat-out', show_default=True, type=str,
              help='Output directory where the categorised files will be written to, '\
                   'under landscape/portrait/square sub-directories')
def cli(input_dir: str, output_dir: str) -> None:
    """Python CLI for tagging AWS resources based on a YAML configuration.
    """
    categorise(input_dir, output_dir)

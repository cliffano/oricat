# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
from unittest.mock import MagicMock, call, patch
import unittest

from oricat.categorise_orientation import (
    _categorise_orientation,
    _categorise_orientation_images,
    _read_orientation_images,
    _write_orientation_images,
)


class TestCategoriseOrientation(unittest.TestCase):

    @patch("oricat.categorise_orientation.os.listdir")
    def test_read_orientation_images_filters_supported_extensions(self, func_listdir):
        func_listdir.return_value = ["a.jpg", "b.txt", "c.png", "d.jpeg", "e.gif"]
        logger = MagicMock()

        result = _read_orientation_images("some/input", logger)

        self.assertEqual(result, ["a.jpg", "c.png", "d.jpeg", "e.gif"])
        logger.info.assert_has_calls(
            [
                call("Reading images from %s...", "some/input"),
                call("Found %s images in %s", 4, "some/input"),
            ]
        )

    @patch("oricat.categorise_orientation.Image.open")
    def test_categorise_orientation_images_groups_by_dimensions(self, func_open):
        logger = MagicMock()
        images = ["landscape.jpg", "portrait.jpg", "square.jpg"]

        landscape = MagicMock()
        landscape.size = (100, 50)
        portrait = MagicMock()
        portrait.size = (50, 100)
        square = MagicMock()
        square.size = (60, 60)

        landscape_cm = MagicMock()
        landscape_cm.__enter__.return_value = landscape
        landscape_cm.__exit__.return_value = None

        portrait_cm = MagicMock()
        portrait_cm.__enter__.return_value = portrait
        portrait_cm.__exit__.return_value = None

        square_cm = MagicMock()
        square_cm.__enter__.return_value = square
        square_cm.__exit__.return_value = None

        func_open.side_effect = [landscape_cm, portrait_cm, square_cm]

        landscape_images, portrait_images, square_images = (
            _categorise_orientation_images("some/input", images, logger)
        )

        self.assertEqual(landscape_images, ["landscape.jpg"])
        self.assertEqual(portrait_images, ["portrait.jpg"])
        self.assertEqual(square_images, ["square.jpg"])

    @patch("oricat.categorise_orientation.os.rename")
    @patch("oricat.categorise_orientation.os.makedirs")
    @patch("oricat.categorise_orientation.os.path.exists")
    def test_write_orientation_images_creates_directory_when_missing(
        self, func_exists, func_makedirs, func_rename
    ):
        func_exists.return_value = False
        logger = MagicMock()

        _write_orientation_images(
            ["a.jpg", "b.jpg"], "landscape", "some/in", "some/out", logger
        )

        func_makedirs.assert_called_once_with("some/out/landscape")
        self.assertEqual(func_rename.call_count, 2)

    @patch("oricat.categorise_orientation.os.rename")
    @patch("oricat.categorise_orientation.os.makedirs")
    @patch("oricat.categorise_orientation.os.path.exists")
    def test_write_orientation_images_skips_directory_creation_when_present(
        self, func_exists, func_makedirs, func_rename
    ):
        func_exists.return_value = True
        logger = MagicMock()

        _write_orientation_images([], "portrait", "some/in", "some/out", logger)

        func_makedirs.assert_not_called()
        func_rename.assert_not_called()

    @patch("oricat.categorise_orientation._write_orientation_images")
    @patch("oricat.categorise_orientation._categorise_orientation_images")
    @patch("oricat.categorise_orientation._read_orientation_images")
    @patch("oricat.categorise_orientation.init")
    def test_categorise_orientation_orchestrates_helpers(
        self,
        func_init,
        func_read_orientation_images,
        func_categorise_orientation_images,
        func_write_orientation_images,
    ):
        logger = MagicMock()
        func_init.return_value = logger
        func_read_orientation_images.return_value = ["a.jpg"]
        func_categorise_orientation_images.return_value = (
            ["l.jpg"],
            ["p.jpg"],
            ["s.jpg"],
        )

        _categorise_orientation("some/in", "some/out")

        func_read_orientation_images.assert_called_once_with("some/in", logger)
        func_categorise_orientation_images.assert_called_once_with(
            "some/in", ["a.jpg"], logger
        )
        func_write_orientation_images.assert_has_calls(
            [
                call(["l.jpg"], "landscape", "some/in", "some/out", logger),
                call(["p.jpg"], "portrait", "some/in", "some/out", logger),
                call(["s.jpg"], "square", "some/in", "some/out", logger),
            ]
        )

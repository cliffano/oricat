# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import shutil
import unittest
from pathlib import Path

from click.testing import CliRunner
from oricat import cli


class TestCategoriseOrientation(unittest.TestCase):

    def test_categorise_orientation(self):
        data_dir = "examples/fixtures/categorise/"
        input_dir = "stage/test-integration/input/"
        output_dir = "stage/test-integration/output/"

        Path(input_dir).mkdir(parents=True, exist_ok=True)
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for data_file in os.listdir(data_dir):
            src = os.path.join(data_dir, data_file)
            if os.path.isfile(src):
                shutil.copy(src, os.path.join(input_dir, data_file))

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "categorise-orientation",
                "--input-dir",
                input_dir,
                "--output-dir",
                output_dir,
            ],
        )
        self.assertEqual(result.exit_code, 0)

        landscape_files = os.listdir(os.path.join(output_dir, "landscape"))
        portrait_files = os.listdir(os.path.join(output_dir, "portrait"))
        square_files = os.listdir(os.path.join(output_dir, "square"))

        landscape_files.sort()
        self.assertEqual(len(landscape_files), 2)
        self.assertEqual(landscape_files[0], "cat_landscape_1.png")
        self.assertEqual(landscape_files[1], "cat_landscape_2.png")

        portrait_files.sort()
        self.assertEqual(len(portrait_files), 2)
        self.assertEqual(portrait_files[0], "cat_portrait_1.png")
        self.assertEqual(portrait_files[1], "cat_portrait_2.png")

        square_files.sort()
        self.assertEqual(len(square_files), 2)
        self.assertEqual(square_files[0], "cat_square_1.png")
        self.assertEqual(square_files[1], "cat_square_2.png")

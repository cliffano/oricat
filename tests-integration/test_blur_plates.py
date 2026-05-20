# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import shutil
import unittest
from pathlib import Path

from click.testing import CliRunner
from oricat import cli


class TestBlurPlates(unittest.TestCase):

    def test_blur_plates(self):
        data_dir = "examples/fixtures/blur-plates/"
        input_dir = "stage/test-integration/blur-plates/input/"
        output_dir = "stage/test-integration/blur-plates/output/"

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
                "blur-plates",
                "--input-dir",
                input_dir,
                "--output-dir",
                output_dir,
            ],
        )
        self.assertEqual(result.exit_code, 0)

        input_files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        output_files = [
            f
            for f in os.listdir(output_dir)
            if os.path.isfile(os.path.join(output_dir, f))
        ]
        self.assertEqual(len(output_files), len(input_files))

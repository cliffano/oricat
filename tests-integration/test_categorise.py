# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
from pathlib import Path
import shutil
import unittest
from oricat import categorise

class TestCategorise(unittest.TestCase):

    def test_categorise(self):
        data_dir = 'examples/fixtures/'
        input_dir = 'stage/test-integration/input/'
        output_dir = 'stage/test-integration/output/'

        Path(input_dir).mkdir(parents=True, exist_ok=True)
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for data_file in os.listdir(data_dir):
            shutil.copy(os.path.join(data_dir, data_file), os.path.join(input_dir, data_file))

        categorise(input_dir, output_dir)

        landscape_files = os.listdir(os.path.join(output_dir, 'landscape'))
        portrait_files = os.listdir(os.path.join(output_dir, 'portrait'))
        square_files = os.listdir(os.path.join(output_dir, 'square'))

        self.assertEqual(len(landscape_files), 2)
        self.assertEqual(landscape_files[0], 'cat_landscape_1.png')
        self.assertEqual(landscape_files[1], 'cat_landscape_2.png')
        self.assertEqual(len(portrait_files), 2)
        self.assertEqual(portrait_files[0], 'cat_portrait_1.png')
        self.assertEqual(portrait_files[1], 'cat_portrait_2.png')
        self.assertEqual(len(square_files), 2)
        self.assertEqual(square_files[0], 'cat_square_1.png')
        self.assertEqual(square_files[1], 'cat_square_2.png')

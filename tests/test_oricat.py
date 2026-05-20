# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest

from click.testing import CliRunner
from oricat import cli


class TestOricat(unittest.TestCase):

    @patch("oricat._categorise_orientation")
    def test_cli(self, func_categorise_orientation):  # pylint: disable=too-many-arguments

        func_categorise_orientation.return_value = None

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "categorise-orientation",
                "--input-dir",
                "some/input/dir/",
                "--output-dir",
                "some/output/dir/",
            ],
        )
        assert not result.exception
        assert result.exit_code == 0
        assert result.output == ""

        # should delegate call to _categorise_orientation
        func_categorise_orientation.assert_called_once_with(
            "some/input/dir/", "some/output/dir/"
        )

    @patch("oricat._categorise_orientation")
    def test_cli_default_invokes_categorise_orientation(
        self, func_categorise_orientation
    ):  # pylint: disable=too-many-arguments

        func_categorise_orientation.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert not result.exception
        assert result.exit_code == 0
        assert result.output == ""

        # should delegate to default subcommand with default options
        func_categorise_orientation.assert_called_once_with("oricat", "oricat-out")

    @patch("oricat._blur_plates")
    def test_blur_plates_cli(self, func_blur_plates):

        func_blur_plates.return_value = None

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "blur-plates",
                "--input-dir",
                "some/input/dir/",
                "--output-dir",
                "some/output/dir/",
            ],
        )
        assert not result.exception
        assert result.exit_code == 0
        assert result.output == ""

        # should delegate call to _blur_plates
        func_blur_plates.assert_called_once_with("some/input/dir/", "some/output/dir/")

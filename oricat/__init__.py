"""
oricat
=======
Tag any AWS resource via config file.
"""

import click

from .blur_plates import _blur_plates
from .categorise_orientation import _categorise_orientation


@click.command(name="categorise-orientation")
@click.option(
    "--input-dir",
    default="oricat",
    show_default=True,
    type=str,
    help="Input directory where the files to be categorised are located",
)
@click.option(
    "--output-dir",
    default="oricat-out",
    show_default=True,
    type=str,
    help="Output directory where the categorised files will be written to, "
    "under landscape/portrait/square sub-directories",
)
def categorise_orientation_command(input_dir: str, output_dir: str) -> None:
    """Categorise image files by orientation."""
    _categorise_orientation(input_dir, output_dir)


@click.command(name="blur-plates")
@click.option(
    "--input-dir",
    default="oricat",
    show_default=True,
    type=str,
    help="Input directory containing car images with license plates",
)
@click.option(
    "--output-dir",
    default="oricat-out",
    show_default=True,
    type=str,
    help="Output directory where blurred images will be written",
)
def blur_plates_command(input_dir: str, output_dir: str) -> None:
    """Detect and blur license plates in image files."""
    _blur_plates(input_dir, output_dir)


@click.group(invoke_without_command=True)
@click.version_option(package_name="oricat", prog_name="oricat")
@click.option(
    "--input-dir",
    default="oricat",
    show_default=True,
    type=str,
    help="Input directory where the files to be categorised are located",
)
@click.option(
    "--output-dir",
    default="oricat-out",
    show_default=True,
    type=str,
    help="Output directory where the categorised files will be written to, "
    "under landscape/portrait/square sub-directories",
)
@click.pass_context
def cli(ctx, input_dir: str, output_dir: str):
    """Oricat CLI"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            categorise_orientation_command,
            input_dir=input_dir,
            output_dir=output_dir,
        )


cli.add_command(categorise_orientation_command)
cli.add_command(blur_plates_command)

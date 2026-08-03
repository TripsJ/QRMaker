"""Tests for QRMakers main.py."""

from pathlib import Path

import pytest

from main import create_qr, remove_extension


def test_remove_extension() -> None:
    """Testing if extension removal works for different extensions."""
    assert remove_extension("photo.png") == "photo"
    assert remove_extension("photo.tar.gz") == "photo"
    assert remove_extension("photo.bmp") == "photo"


def test_raises_value_error_on_empty_name() -> None:
    """Testing if ValueError gets raised when expected."""
    with pytest.raises(ValueError):
        remove_extension("")

    with pytest.raises(
        ValueError
    ):  # the context manager gets exited as son as the first ValueError is encountered,
        # so you need one per check
        remove_extension(".bmp")


def test_file_creation_for_create_qr(
    tmp_path: Path,
) -> None:  # tmp_path:Path is used to create a temporary
    # directory that gets cleaned up after testing
    """Testing if create qr actually creates filesystem.

    Arguments:
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "test.png"
    create_qr(
        "https://example.com", str(target)
    )  # str makes sure the temporary path gets converted into a string
    assert target.is_file()  # check if test.png exists

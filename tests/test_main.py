"""Tests for QRMakers main.py."""

import pytest

from main import remove_extension


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

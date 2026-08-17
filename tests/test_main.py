"""Tests for QRMakers main.py."""

import filecmp
from pathlib import Path

import pytest

from main import cmd_mode, create_qr, remove_extension, text_mode


def test_remove_extension() -> None:
    """Testing if extension removal works for different extensions."""
    assert remove_extension("photo.png") == "photo"
    assert remove_extension("photo.tar.gz") == "photo"
    assert remove_extension("photo.bmp") == "photo"


@pytest.mark.xfail(reason="edge case not implemented yet")
def test_remove_extension_for_file_starting_with_dot() -> None:
    """Test if function ignores the first . if the filename starts with ."""
    assert remove_extension(".pic.jpg") == ".pic"


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

    Args:
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "test.png"
    create_qr(
        "https://example.com", str(target)
    )  # str makes sure the temporary path gets converted into a string
    assert target.is_file()  # check if test.png exists


def test_file_exist_error_for_create_qr(
    tmp_path: Path,
) -> None:  # tmp_path:Path is used to create a temporary
    # directory that gets cleaned up after testing
    """Testing if create qr raises Error on already existing file.

    Args:
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "error.png"
    target.write_bytes(b"uselesscontent")  # creates a bytefile named error.png
    with pytest.raises(FileExistsError):
        create_qr(
            "https://example.com", str(target)
        )  # str makes sure the temporary path gets converted into a string


def test_file_exist_error_skipped_on_overwrite_true(
    tmp_path: Path,
) -> None:  # tmp_path:Path is used to create a temporary
    # directory that gets cleaned up after testing
    """Testing if create qr overwrites existing file on overwrite = True.

    Args:
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "error.png"
    reference = tmp_path / "reference.png"
    target.write_bytes(b"uselesscontent")  # creates a bytefile named error.png
    reference.write_bytes(b"uselesscontent")
    assert filecmp.cmp(target, reference)
    create_qr(
        "https://example.com", str(target), overwrite=True
    )  # str makes sure the temporary path gets converted into a string
    assert not filecmp.cmp(target, reference)


def test_create_file_from_input(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Testing the text_mode() function.

    Args:
        monkeypatch: fixture used to simulate inputs temporarily
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "test.png"
    responses = iter(
        ["https://test.com", str(target)]
    )  # iterator containing the responses to the different
    # inputs in order of appearance
    monkeypatch.setattr(
        "builtins.input", lambda prompt="": next(responses)
    )  # next is a function that, on each call, returns the next item of an iterator
    text_mode()
    assert target.is_file()


def test_create_file_from_cmd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Testing the text_mode() function.

    Args:
        monkeypatch: fixture used to simulate inputs temporarily
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "test.png"
    monkeypatch.setattr("sys.argv", ["main.py", str(target), "https://test.com"])
    cmd_mode()
    assert target.is_file()


def test_invalide_filename_from_cmd(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Testing the cmd_mode() function raises the ValueError on invalid filename.

    Args:
        monkeypatch: fixture used to simulate inputs temporarily
        tmp_path: Fixture to create a temporary directory.

    """
    target = tmp_path / "\x00teeesst"
    monkeypatch.setattr("sys.argv", ["main.py", str(target), "https://test.com"])
    with pytest.raises(ValueError):
        cmd_mode()


@pytest.mark.parametrize("directory", ["hubble/", "1/", "??/"])
def test_invalide_directory_from_cmd(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, directory: str
) -> None:
    """Testing the cmd_mode() function raises correct Errors.

    Function should raise the OSError and Exits on invalid directory.

    Args:
        monkeypatch: fixture used to simulate inputs temporarily
        tmp_path: Fixture to create a temporary directory.
        directory: directory name from mark.parametrize

    """
    target = tmp_path / f"{directory}" / "test"
    monkeypatch.setattr("sys.argv", ["main.py", str(target), "https://test.com"])
    with pytest.raises(SystemExit):
        cmd_mode()

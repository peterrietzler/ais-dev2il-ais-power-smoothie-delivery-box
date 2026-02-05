import time
from pathlib import Path

import pyjokes
from rich.console import Console

from main import get_ingredients
from main import make_smoothie


def test_get_ingredients(tmp_path: Path):
    # Given: a recipe file with ingredients
    content = "Apple\nBanana\nOrange"
    recipe_file = tmp_path / "my_smoothie.txt"
    recipe_file.write_text(content)

    # When: get_ingredients is called
    result = get_ingredients(recipe_file)

    # Then: it returns the list of ingredients
    expected = ["Apple", "Banana", "Orange"]
    assert result == expected


def test_get_ingredients_file_does_not_exists(tmp_path: Path):
    # Given: a non-existent recipe file
    non_existent_file = tmp_path / "non_existent.txt"

    # When: get_ingredients is called
    result = get_ingredients(non_existent_file)

    # Then: it returns an empty list
    assert result == []


def test_get_ingredients_file_empty(tmp_path: Path):
    # Given: an empty recipe file
    empty_file = tmp_path / "smoothie_without_ingredients.txt"
    empty_file.write_text("")

    # When: get_ingredients is called
    result = get_ingredients(empty_file)

    # Then: it returns an empty list
    assert result == []


def test_make_smoothie_prints_added_ingredients_version_1(tmp_path, capsys):
    # Given: a recipe file with ingredients
    recipe_file = tmp_path / "my_smoothie.txt"
    recipe_file.write_text("Apple\nBanana")

    # When: make_smoothie is called
    make_smoothie(recipe_file)
    captured = capsys.readouterr()

    # Then: output contains both ingredients
    assert "Added Apple" in captured.out
    assert "Added Banana" in captured.out


def test_make_smoothie_prints_added_ingredients_version_2(tmp_path):
    # Given: a recipe file with ingredients
    recipe_file = tmp_path / "my_smoothie.txt"
    recipe_file.write_text("Apple\nBanana\n")
    console = Console(record=True)

    # When: make_smoothie is called
    make_smoothie(recipe_file, console)
    text_output = console.export_text()

    # Then: output contains both ingredients
    assert "Added Apple" in text_output
    assert "Added Banana" in text_output


def test_make_smoothie_prints_a_joke(tmp_path, monkeypatch):
    # Given: a recipe file and a joke
    recipe_file = tmp_path / "my_smoothie.txt"
    recipe_file.write_text("Mango\n")
    monkeypatch.setattr(pyjokes, "get_joke",
                        lambda: "A mock walks into a bar. The bartender asks, 'What can I get you?' The mock returns None.")
    monkeypatch.setattr(time, "sleep", lambda x: None)
    console = Console(record=True)

    # When: make_smoothie is called
    make_smoothie(recipe_file, console)
    output = console.export_text()

    # Then: output contains joke
    assert "The mock returns None" in output

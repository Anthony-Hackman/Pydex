# Archive.zip/tests/test_cli.py (Refined)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from typer.testing import CliRunner
import pydex

# Define a successful stub data matching the format *returned* by get_pokemon_data
# This should match the format expected by pydex.py
CHARIZARD_STUB = {
    "id": 6,
    "name": "Charizard",
    "sprite_url": "http://sprite.url/6.png",
    "types": ["Fire", "Flying"],
    "abilities": ["Blaze", "Solar Power"],
    "generation": "Generation I", # Note: Already formatted by fetch.py
    "fun_fact": "Spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally.",
    "stats": {"Hp": 78, "Attack": 84},
}

def test_cli_search_command_success():
    """Tests successful search output and formatting."""
    runner = CliRunner()

    # The mock data structure
    CHARIZARD_STUB = {
        "id": 6,
        "name": "Charizard",
        "sprite_url": "http://sprite.url/6.png",
        "types": ["Fire", "Flying"],
        "abilities": ["Blaze", "Solar Power"],
        "generation": "Generation I",  # Note: Already formatted by fetch.py
        "fun_fact": "Spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally.",
        "stats": {"Hp": 78, "Attack": 84},
    }

    with patch("pydex.get_pokemon_data", return_value=CHARIZARD_STUB):
        result = runner.invoke(pydex.app, ["search", "charizard"])

    # 1. Assert successful execution
    assert result.exit_code == 0
    assert "Error:" not in result.stdout

    # 2. Assert key information and formatting is present

    # Fix 1: Check the rule/title line for content only.
    assert "#6 - Charizard" in result.stdout

    # Fix 2: Check the generation line. The output must include the newline (\n)
    # because console.print() adds one.
    assert "Introduced in: GENERATION I\n" in result.stdout

    # Check key fields (These assertions are already correct)
    assert "Sprite: http://sprite.url/6.png" in result.stdout
    assert "Type(s): Fire, Flying" in result.stdout
    assert "Abilities: Blaze, Solar Power" in result.stdout
    
    # Check stats table items
    # Note: Rich tables have a complex structure. Checking key values is sufficient.
    assert "Hp" in result.stdout
    assert "78" in result.stdout
    assert "Attack" in result.stdout
    assert "84" in result.stdout
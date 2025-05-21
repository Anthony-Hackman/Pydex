"""
Smoke test the Typer CLI (main.py).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unittest.mock import patch
from typer.testing import CliRunner
import main
from pokeapi.fetch import get_pokemon_data
from pokeapi import fetch

def test_cli_search_command():
    runner = CliRunner()

    stub = {
        "id": 6,
        "name": "Charizard",
        "sprite_url": None,
        "types": ["Fire"],
        "abilities": ["Blaze"],
        "generation": "Generation I",
        "fun_fact": "Roars.",
        "stats": {"Hp": 1},
    }

    with patch("pokeapi.fetch.get_pokemon_data", return_value=stub):
        result = runner.invoke(main.app, ["search", "charizard"])

    assert result.exit_code == 0
    assert "Charizard" in result.output

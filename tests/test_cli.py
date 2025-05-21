"""
Smoke test the Typer CLI (main.py).
"""
from unittest.mock import patch
from typer.testing import CliRunner
import main  # main.app is the Typer app


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
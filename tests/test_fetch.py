"""
Basic unit test for pokeapi.fetch.get_pokemon_data
"""
from unittest.mock import Mock, patch
from pokeapi import fetch

def test_get_pokemon_data_charizard():
    # --- stub JSON that get_pokemon_data will parse -------------------------
    mon_json = {"id": 6, "name": "charizard", "types": [],
                "abilities": [], "stats": [], "sprites": {"front_default": None},
                "species": {"url": "url"}}
    species_json = {"generation": {"name": "generation-i"},
                    "flavor_text_entries": []}

    def fake_get(url, *_a, **_kw):
        m = Mock(status_code=200)
        m.json.return_value = species_json if "species" in url else mon_json
        m.raise_for_status = lambda: None
        return m

    with patch("pokeapi.fetch.requests.get", fake_get):
        data = fetch.get_pokemon_data("charizard")

    assert data["id"] == 6
    assert data["name"] == "Charizard"

"""
Test for pokeapi.fetch.get_pokemon_data
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock, patch
from pokeapi import fetch
import requests # Add HTTP
import pytest # Add pytest for clearer assertions and parametrization

def fake_not_found_get(url, *_a, **_kw):
    """Simulates a 404 Not Found error on the first API call."""
    mock_resp = Mock(status_code=404)
    # The side effect of raise_for_status() for a 4xx code is to raise an HTTPError
    mock_resp.raise_for_status.side_effect = requests.HTTPError("404 Client Error: Not Found")
    return mock_resp

@patch("pokeapi.fetch.requests.get", side_effect=fake_not_found_get)
def test_get_pokemon_data_not_found(mock_get):
    """Tests that a 404 error results in the expected RuntimeError."""
    import requests # Need to import requests in the test file
    
    with pytest.raises(RuntimeError, match="Failed to fetch Pokémon data"):
        fetch.get_pokemon_data("invalid-name")

# --- Mock Data Fixtures for Successful Calls ---

# Mock response for the main /pokemon/{name_or_id} endpoint
def mock_pokemon_response(name="charizard", id=6):
    mock_resp = Mock(status_code=200)
    mock_resp.json.return_value = {
        "id": id,
        "name": name.lower(),
        "types": [{"type": {"name": "fire"}}],
        "abilities": [{"ability": {"name": "blaze"}}],
        "stats": [{"stat": {"name": "hp"}, "base_stat": 78}],
        "sprites": {"front_default": "http://sprite.url/6.png"},
        "species": {"url": "http://fake.api/pokemon-species/6"},
    }
    mock_resp.raise_for_status = lambda: None
    return mock_resp

# Mock response for the /pokemon-species/{id} endpoint
def mock_species_response():
    mock_resp = Mock(status_code=200)
    mock_resp.json.return_value = {
        "generation": {"name": "generation-i"},
        "flavor_text_entries": [
            {"flavor_text": "Spits fire.", "language": {"name": "en"}},
            {"flavor_text": "Not in English.", "language": {"name": "fr"}},
        ],
    }
    mock_resp.raise_for_status = lambda: None
    return mock_resp

# Mock the requests.get function to return the appropriate responses
def fake_successful_get(url, *_a, **_kw):
    if "pokemon-species" in url:
        return mock_species_response()
    return mock_pokemon_response()

# --- Tests ---

@patch("pokeapi.fetch.requests.get", side_effect=fake_successful_get)
def test_get_pokemon_data_success(mock_get):
    """Tests a successful fetch and correct data transformation."""
    data = fetch.get_pokemon_data("charizard")

    # Verify requests.get was called twice with the correct URLs
    assert mock_get.call_count == 2
    mock_get.assert_any_call("https://pokeapi.co/api/v2/pokemon/charizard")
    mock_get.assert_any_call("https://pokeapi.co/api/v2/pokemon-species/6")

    # Check data transformation (title case, replacing hyphens, etc.)
    assert data["id"] == 6
    assert data["name"] == "Charizard"
    assert data["types"] == ["Fire"]
    assert data["abilities"] == ["Blaze"]
    assert data["stats"] == {"Hp": 78}
    assert data["generation"] == "Generation I"
    assert data["fun_fact"] == "Spits fire." # Check fun fact cleaning

@patch("pokeapi.fetch.requests.get", side_effect=fake_successful_get)
def test_get_pokemon_data_id_input(mock_get):
    """Tests that inputting an ID works correctly (pokeapi handles it)."""
    # The fake_successful_get implicitly uses 'charizard' and id 6, so this works
    data = fetch.get_pokemon_data("6")
    assert data["id"] == 6
    assert data["name"] == "Charizard"

# pokeapi/fetch.py
import requests

BASE = "https://pokeapi.co/api/v2"

def get_pokemon_data(name_or_id: str) -> dict:
    try:
        # 1) Get Pokémon JSON
        r = requests.get(f"{BASE}/pokemon/{name_or_id.lower()}")
        r.raise_for_status()
        raw = r.json()
        poke_id = raw["id"]

        # 2) Get species JSON
        r2 = requests.get(f"{BASE}/pokemon-species/{poke_id}")
        r2.raise_for_status()
        species = r2.json()

        # 3) Fields
        types      = [t["type"]["name"].title()     for t in raw["types"]]
        abilities  = [a["ability"]["name"].title()  for a in raw["abilities"]]
        stats      = {s["stat"]["name"].title(): s["base_stat"] for s in raw["stats"]}
        generation = species["generation"]["name"].replace("-", " ").title()
        sprite_url = raw["sprites"]["front_default"]

        # 4) Fun fact
        fun_fact = next(
            (
                entry["flavor_text"]
                      .replace("\n", " ")
                      .replace("\f", " ")
                for entry in species["flavor_text_entries"]
                if entry["language"]["name"] == "en"
            ),
            "No fun fact available."
        )

        return {
            "id":         poke_id,
            "name":       raw["name"].title(),
            "types":      types,
            "abilities":  abilities,
            "stats":      stats,
            "generation": generation,
            "sprite_url": sprite_url,
            "fun_fact":   fun_fact,
        }

    except Exception as e:
        raise RuntimeError(f"Failed to fetch Pokémon data: {e}")

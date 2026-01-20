# Pydex

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/github/actions/workflow/status/Anthony-Hackman/Pokedex/python-app.yml?branch=main)
![License](https://img.shields.io/github/license/Anthony-Hackman/pokedex_cli)

**Pydex** is a powerful **Python-based command-line tool** that lets you instantly retrieve detailed information about any Pokémon. Built using data from the [PokéAPI](https://pokeapi.co/), Pydex provides a clean, readable output right in your terminal, supporting queries by both **name** and **ID**.

## DexUI (Optional Graphical Interface)

For a visual experience, Pydex includes **DexUI**, a separate graphical user interface (GUI) built with the PyQt6 library.

### Features

* Search for Pokémon by **Name** or **ID**.
* Display **Type(s), Abilities, Base Stats,** and **Generation**.
* Show the official **Sprite Image URL**.
* Includes the official **flavor text** (fun fact) just like the original!

![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white)

## Setup Instructions

To get Pydex running quickly, this project uses a standard `requirements.txt` file to manage all necessary libraries.

---

### Prerequisites

* Python 3.10+

* `pip` -  (Python package installer)

### Dependencies

* **`requests`** -  For making HTTP calls to the PokéAPI
* **`rich`** - For generating readable terminal output and tables
* **`typer`** - For building the command-line interface
* **`PyQt6`** - Required to run the graphical user interface (Optional, if not using DexUI.py).

To ensure the ease of installation, all of the above (excluding prerequisites) are included in the `requirements.txt` file.

## Clone the repository

```bash
git clone https://github.com/anthony-hackman/Pydex.git
cd Pydex
   ```

## Install dependencies

Install all required packages using the requirements file:

```bash
python3 -m pip install -r requirements.txt
```

## Example Usage

You can run the CLI application by entering the name of the file `pydex.py`, the function `search`, followed by the Pokémon's `Name` or `ID`.

```bash
<file> <function> <name_or_id>
```

For example, to search for the Pokémon `Charizard`, navigate to the directory containing the pydex repository and enter:

```bash
pydex.py search Charizard
```

To run the graphic user interface, simply run:

```bash
python3 DexUI.py
```

### Sample Output from CLI

(pydex.py)

```text
───────────────────────────── #6 - Charizard ────────────────────────────────
Sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png
Type(s): Fire, Flying
Abilities: Blaze, Solar-Power
Introduced in: GENERATION I
Fun Fact: Spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally.

        Base Stats
┏━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Stat            ┃ Value ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Hp              │    78 │
│ Attack          │    84 │
│ Defense         │    78 │
│ Special-Attack  │   109 │
│ Special-Defense │    85 │
│ Speed           │   100 │
└─────────────────┴───────┘
```

### Sample from Graphic User Interface

(DexUI.py)

![DexUI](Resources/Screenshot-2025-05-15(2).png)

## Contributing

I welcome contributions! If you want to help improve Pydex, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request.

---

## Tests

Tests are available under the /tests directory.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

* [PokéAPI](https://pokeapi.co/) - Created by Paul Hallett and other contributors.

* [Pokémondb](https://pokemondb.net/) - Database, 2008-2026.

* [Pokémon](https://www.pokemon.com/) - Images & Names © 1995-2026 Nintendo/Game Freak.

# main.py
# Main CLI Entrypoint

import click
from rich.console import Console
from rich.table import Table
from pokeapi.fetch import get_pokemon_data

console = Console()

@click.group()
def app():
    """Pokedex CLI."""
    # Just a container for subcommands
    pass

@app.command()
@click.argument("name_or_id")
def search(name_or_id: str):
    """Search and display Pokémon info."""
    try:
        data = get_pokemon_data(name_or_id)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        # Abort with a non-zero exit code
        raise click.Abort()

    console.rule(f"[bold blue]#{data['id']} - {data['name']}")
    console.print(f"[bold green]Sprite:[/bold green] {data['sprite_url'] or 'N/A'}")
    console.print(f"[bold green]Type(s):[/bold green] {', '.join(data['types'])}")
    console.print(f"[bold green]Abilities:[/bold green] {', '.join(data['abilities'])}")

    # Only uppercase the Roman-numeral part of "generation"
    parts = data["generation"].rsplit(" ", 1)
    if len(parts) == 2:
        formatted_gen = f"{parts[0]} {parts[1].upper()}"
    else:
        formatted_gen = data["generation"]
    console.print(f"[bold green]Introduced in:[/bold green] {formatted_gen}")

    console.print(f"[bold green]Fun Fact:[/bold green] {data['fun_fact']}")

    table = Table(title="Base Stats")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", justify="right")
    for stat, val in data["stats"].items():
        table.add_row(stat, str(val))
    console.print(table)

if __name__ == "__main__":
    app()

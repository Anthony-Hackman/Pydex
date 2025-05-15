# app.py
# Main CLI Entrypoint

import typer
from rich.console import Console
from rich.table import Table
from pokeapi.fetch import get_pokemon_data

app = typer.Typer()
console = Console()

@app.command()
def search(name_or_id: str):
    """Search and display Pokémon info."""
    try:
        data = get_pokemon_data(name_or_id)
        console.rule(f"[bold blue]#{data['id']} - {data['name']}")
        console.print(f"[bold green]Sprite:[/bold green] {data['sprite_url'] or 'N/A'}")
        console.print(f"[bold green]Type(s):[/bold green] {', '.join(data['types'])}")
        console.print(f"[bold green]Abilities:[/bold green] {', '.join(data['abilities'])}")
        console.print(f"[bold green]Introduced in:[/bold green] {data['generation'].upper()}") # Changed 'generation' to 'generation'.upper()' to enforce roman numerals
        console.print(f"[bold green]Fun Fact:[/bold green] {data['fun_fact']}")

        table = Table(title="Base Stats")
        table.add_column("Stat", style="cyan")
        table.add_column("Value", justify="right")
        for stat, val in data['stats'].items():
            table.add_row(stat, str(val))
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()

# main.py
# Main CLI Entrypoint

import typer
from rich.console import Console
from rich.table import Table
from pokeapi.fetch import get_pokemon_data

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=False)
def _root():
    """
    Pokedex CLI entrypoint.
    """
    # no-op; exists so Typer will always produce a GROUP,
    # not collapse down to a single command.
    pass

@app.command()
def search(name_or_id: str):
    """
    Search and display Pokémon info.
    """
    try:
        data = get_pokemon_data(name_or_id)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    console.rule(f"[bold blue]#{data['id']} - {data['name']}")
    console.print(f"[bold green]Sprite:[/bold green] {data['sprite_url'] or 'N/A'}")
    console.print(f"[bold green]Type(s):[/bold green] {', '.join(data['types'])}")
    console.print(f"[bold green]Abilities:[/bold green] {', '.join(data['abilities'])}")

    # Only uppercase the Roman-numeral bit of the generation string
    parts = data["generation"].rsplit(" ", 1)
    if len(parts) == 2:
        gen = f"{parts[0]} {parts[1].upper()}"
    else:
        gen = data["generation"]
    console.print(f"[bold green]Introduced in:[/bold green] {gen}")

    console.print(f"[bold green]Fun Fact:[/bold green] {data['fun_fact']}")

    table = Table(title="Base Stats")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", justify="right")
    for stat, val in data["stats"].items():
        table.add_row(stat, str(val))
    console.print(table)

if __name__ == "__main__":
    app()

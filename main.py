from pathlib import Path
import time
import pyjokes
import urllib.request
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def get_ingredients(recipe_file: Path) -> list[str]:
    # mySecret = "hyddYR1i2srLYdKa" #gitleaks:allow

    if not recipe_file.exists():
        return []
    with open(recipe_file, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def make_smoothie(recipe_file: Path, console: Console = Console()):
    ingredients = get_ingredients(recipe_file)
    if not ingredients:
        console.print(f"[bold red]No ingredients found in {recipe_file.name}![/bold red]")
        return ingredients

    console.print(f"[bold green]Starting to make: {recipe_file.stem.replace('_', ' ').title()}[/bold green]")
    joke = pyjokes.get_joke()
    console.print(f"[bold cyan]Let met enlighten you with a joke while you wait: {joke}[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Adding ingredients
        for ingredient in ingredients:
            task = progress.add_task(f"Adding {ingredient}...", total=None)
            time.sleep(0.5)  # Simulate time to add ingredient
            progress.remove_task(task)
            console.print(f"  [green]✓[/green] Added {ingredient}")

        # Blending
        blend_task = progress.add_task("[bold magenta]Blending everything together...[/bold magenta]", total=None)
        time.sleep(2)
        progress.remove_task(blend_task)

    console.print(f"[bold yellow]✨ Smoothie '{recipe_file.stem.replace('_', ' ').title()}' is ready! Enjoy! ✨[/bold yellow]")


@click.command()
@click.argument('recipe')
def main(recipe):
    base_dir = Path(__file__).parent
    smoothies_dir = base_dir / "smoothies"
    console = Console()

    # Check if recipe is a URL
    if recipe.startswith('http://') or recipe.startswith('https://'):
        console.print(f"[bold cyan]Fetching recipe from {recipe}...[/bold cyan]")
        try:
            with urllib.request.urlopen(recipe) as response:
                content = response.read().decode('utf-8')
            
            # Write to temporary file
            temp_recipe = base_dir / "temp_recipe.txt"
            temp_recipe.write_text(content)
            make_smoothie(temp_recipe, console)
            temp_recipe.unlink()
        except Exception as e:
            console.print(f"[bold red]Failed to fetch recipe: {e}[/bold red]")
    else:
        # Treat as filename in smoothies folder
        recipe_file = smoothies_dir / recipe
        if not recipe_file.exists():
            console.print(f"[bold red]Recipe file '{recipe}' not found in smoothies folder![/bold red]")
            return
        make_smoothie(recipe_file, console)

if __name__ == "__main__":
    main()

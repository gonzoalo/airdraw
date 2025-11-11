import typer
import os

app = typer.Typer()

@app.command()
def init():
    """
    Creates the basic folder structure for using airdraw in your airflow project.
    |-- airdraw
    |   |-- dags
    |   |-- logs
    |   |-- objects
    |-- dags
    |   |-- airdraw_loader.py
    """

    folders = [
        "airdraw/dags",
        "airdraw/logs",
        "airdraw/objects",
        "dags"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    src_loader = os.path.join(os.path.dirname(__file__), "airdraw_loader.py")
    dest_loader = os.path.join(os.path.dirname(__file__), "dags", "airdraw_loader.py")
    if os.path.exists(src_loader) and not os.path.exists(dest_loader):
        typer.echo(f"Copying {src_loader} to {dest_loader}")
        with open(src_loader, "r") as s, open(dest_loader, "w") as d:
            d.write(s.read())
    typer.echo("Airdraw folder structure created.")

if __name__ == "__main__":
    app()
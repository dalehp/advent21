import importlib

import click


@click.command()
@click.argument("day")
def run(day: str):
    day = day.zfill(2)
    module_path = f"solutions.day_{day}.solution"
    module = importlib.import_module(module_path)
    try:
        getattr(module, "run")()
    except AttributeError:
        print(f"Module needs run function")


if __name__ == "__main__":
    run()

import sys
import os
from pathlib import Path
import typer

def sanity_check(in_file:Path, out_file:Path):
    if not in_file.is_file():
        sys.exit(f"Cant' find input kindle {in_file}")
    else:
        print(f"kindle cache file: {in_file}")

    print(f"output file: {out_file}")
    if not out_file.parent.absolute().is_dir():
        print(f"output_file.parent.absolute as folde not found.. creating it...")
        os.makedirs(out_file.parent.absolute(), exist_ok=True)


def main(in_file:Path, out_file:Path = None):
    if out_file is None:
        out_file = Path(".") / "kindle_cachefile.csv"
    sanity_check(in_file=in_file, out_file=out_file)
    
if __name__ == '__main__':
    typer.run(main)
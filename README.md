# pyle

Python package for filtering files from command line.
Add Command Line Options to `argparse` module for date and time filtering positional list of files.

## Install

```
git clone https://github.com/so07/pyle.git

cd pyle
pip install .
```

## Usage

Add command line options for date and time filtering for positional list of files

```
from pyle import add_pyle_parser, get_files

parser = argparse.ArgumentParser(prog="pyle example")

add_pyle_parser(parser)

args = parser.parse_args()

list_of_files = get_files(args)
```


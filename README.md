# python-package-template
The repository can be used as a template for Python packages.

## Installation

After cloning the repository to your machine, navigate to the directory and run

```
pip install .
```

## Usage

To see usage, run

```
greeter -h
```

which outputs

```
Greet yourself and someone else.

positional arguments:
  {hello,bye}    Choose task
    hello        Say hello
    bye          Say bye
  name           your name

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  activate verbose logging output (default: False)
```

Some example commands:

```
greeter hello hhunterzinck
greeter bye hhunterzinck
greeter hello -t afternoon hhunterzinck
greeter bye -f kcnizretnuhh hhunterzinck
```
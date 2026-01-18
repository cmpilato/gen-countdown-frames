# Installation and Development Guide

## Installation

### From source (development)

1. Clone the repository
2. Install in editable mode:
```bash
pip install -e .
```

Or with development dependencies:
```bash
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install gen-countdown-frames
```

## Building the Package

To build the package for distribution:

```bash
pip install build
python -m build
```

This will create both wheel and source distributions in the `dist/` directory.

## Usage

After installation, the `gen-countdown-frames` command will be available in your PATH:

```bash
gen-countdown-frames --help
gen-countdown-frames 5
gen-countdown-frames --enable-ring --ring-color FF0000 2
```

## Development

### Code formatting

Format code with black:
```bash
black src/
```

### Linting

Use the existing lint script:
```bash
./lint.sh
```

## Legacy Script

The original `gen-countdown-frames` script file is still available for backwards compatibility, but the recommended approach is to install the package and use the generated entry point.

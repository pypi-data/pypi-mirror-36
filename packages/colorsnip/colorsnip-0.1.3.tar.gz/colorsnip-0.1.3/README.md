# ColorSnip

[![PyPI version](https://badge.fury.io/py/colorsnip.svg)](https://badge.fury.io/py/colorsnip)
[![GitHub version](https://badge.fury.io/gh/ewjoachim%2Fcolorsnip.svg)](https://badge.fury.io/gh/ewjoachim%2Fcolorsnip)

Command line tool: Copies the content of the given file (or stdin) to the clipboard
with syntax coloring, so it can be pasted into a format-retaining software.

## Installation

Compatible with:
- MacOS via [richxerox](https://pypi.org/project/richxerox/)
- Linux and Windows (untested) via [klemboard](https://pypi.org/project/klembord/)

```console
$ pip install colorsnip
```

## Usage:

```console
$ colorsnip [filename|-]
```

## Use case

Pasting formatted code for a presentation in Keynote or the like.

If you want to access the `HTML`/`RTF` content directly, use `pygments` and the CLI tool
`pygmentize` that it provides.

## Caveats

- richxerox dependency seems to install half of PyPI
- Untested on Linux and Windows
- Linux and Windows get the `HTML` rich text format only, while MacOS get HTML and RTF.

## License

MIT (see top of code file)

## Code of conduct

This project follows the [contributor covenant](https://www.contributor-covenant.org/).

For any feedback, contact the author via an issue, or [twitter](https://twitter.com/ewjoachim)
or by email (first name at last name dot fr).

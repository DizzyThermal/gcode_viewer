# Viewer for Slic3r/PrusaSlic3r Generated G-Code Files

## Requirements

[Python 3+](https://www.python.org/downloads/)

## Usage

```shell
G-Code Settings Viewer

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  G-Code File
  -v VIEW, --view VIEW  Slic3r Settings to View: [simple|advanced|expert]
```

## Examples

```shell
./gcode_viewer.py -f test.gcode
./gcode_viewer.py -f test.gcode -v simple
```

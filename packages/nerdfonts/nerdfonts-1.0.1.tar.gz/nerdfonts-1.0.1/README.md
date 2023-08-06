# Nerd Fonts' icons for Python

## Installation

```sh
pip install nerdfonts
```

## Usage

```python
import nerdfonts as nf

print(nf.icons['fa_thumbs_up'])
>>> 
```

## Build

```sh
# Run the generate script to download nerd font's character mapping
# and generate a python-formatted version of it. Ensure that you have
# SVN installed. To change the nerd font version, use something like
# `./generate.sh 2.0.0`
./fontawesome/generate.py

python setup.py build

python setup.py install
```

## License

The code in this repository is licensed under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

The character codes included with this package are part of the [Nerd Fonts project](https://nerdfonts.com/).

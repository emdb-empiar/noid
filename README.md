# `noid` Python Package

[![PyPI version](https://badge.fury.io/py/noid.svg)](https://badge.fury.io/py/noid)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/noid)
![example workflow](https://github.com/paulkorir/noid/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/paulkorir/noid/branch/master/graph/badge.svg?token=OTVWS6LNU2)](https://codecov.io/gh/paulkorir/noid)

## Installation
Install from PyPI with
```
pip install noid
```
or from source with
```
pip install git+git@github.com:paulkorir/noid.git     # SSH
pip install git+https://github.com/paulkorir/noid.git # HTTPS
```

## CLI Usage
### Generating a noid
Use the `noid` command with no arguments:
```
noid
```
There are various options available using `-h/--help`:
```shell
noid -h
usage: noid [-h] [-c CONFIG_FILE] [-V | -d] [-s SCHEME] [-N NAA] [-t TEMPLATE] [-n INDEX] [-v] [noid]

generate nice and opaque identifiers

positional arguments:
  noid                  a noid

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        path to a config file with a noid section
  -V, --validate        validate the given noid [default: False]
  -d, --check-digit     compute and print the corresponding check digit for the given noid [default: False]
  -s SCHEME, --scheme SCHEME
                        the noid scheme [default: 'ark:/']
  -N NAA, --naa NAA     the name assigning authority (NAA) number [default: ]
  -t TEMPLATE, --template TEMPLATE
                        the template by which to generate noids [default: 'zeeddk']
  -n INDEX, --index INDEX
                        a number for which to generate a valid noid [default: random positive integer]
  -v, --verbose         turn on verbose text [default: False]

```

### Validating a noid
Validate a noid using the `-v/--validate` flag and pass a noid.
```shell
noid -v $(noid) # self-validation
```

### Compute the check digit for a noid
Compute the check digit using `-d/--check-digit` flag and pass a noid.
```shell
noid -d $(noid -t zeee -n 1234) && noid -t zeee -n 1234 && noid -t zeeek -n 1234
```
The example above prints out the check digit, the full noid without a check digit and the full noid with a check digit. 

### Options
#### Specify the NAA
Use the `-N/--naa` option.
```shell
noid --naa 1234
```

#### Specify the scheme
Use the `-s/--scheme` option.
```shell
noid --scheme darpa::
```

#### Specify a template
Use the `-t/--template` option.
```shell
noid -t zeeddeedeedk
```

#### Compute a noid for a value
Use the `-n/--index` option.
```shell
noid -n 42
```

#### Using a config file
A simple config file can be defined with the following structure:
```ini
# path/to/noid.cnf
[noid]
# start with 'z'; follow with as many 'e' or 'd' as needed; terminate with 'k' for a checkdigit 
template = zeededdek 
scheme = ark:/
naa = 92729
# the above configs will produce noids like so: ark:/92729/fn7Z344v
```
then use it as follows:
```shell
noid -c path/to/noid.cnf
```
## API Usage
You can also use this package's API in your code.
```python
import random

from noid import mint, validate, calculate_check_digit, generate_noid

# with default arguments
noid = mint()

# arguments: template, n, scheme, naa
noid = mint(template='zeedeeedk', n=37, scheme='https://', naa='802938')

# validating a noid
validate(noid) # True/False

# calculate the check digit
calculate_check_digit(noid)

# low-level generate a noid from a mask and number; no check digit is appended
noid = generate_noid('eeddeed', random.randint(100, 1000))
```

## Testing
```
pip install -r requirements.txt
tox
```

## Authors
* Current implementation:
    * [Paul K. Korir](https://github.com/paulkorir)
* Original source code was by:
    * [Yinlin Chen](https://github.com/yinlinchen)
    * [Tingting Jiang](https://github.com/tingtingjh)
    * [Lee Hunter](https://github.com/whunter)
    * [T. Johnson](https://github.com/no-reply)

See also the list of [contributors](https://github.com/paulkorir/noid/graphs/contributors) who participated in this project.

## Thanks
This tool was heavily influenced from [noid-mint](https://github.com/vt-digital-libraries-platform/NOID-mint)

## References
* https://confluence.ucop.edu/display/Curation/NOID
* https://metacpan.org/dist/Noid/view/noid
* https://en.wikipedia.org/wiki/Archival_Resource_Key
* https://www.gs1.org/standards/id-keys/global-model-number-gmn
* https://www.gs1.org/sites/default/files/docs/idkeys/gs1_gmn_executive_summary.pdf
* https://www.gs1.org/services/gmn-generator
* https://en.wikipedia.org/wiki/Check_digit

#`noid` Python Package

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

## Usage
###Generating a noid
Use the `noid` command with no arguments:
```
noid
```
There are various options available using `-h/--help`:
```shell
noid -h
usage: noid [-h] [-c CONFIG_FILE] [-v] [-s SCHEME] [-N NAA] [-t TEMPLATE] [-n INDEX] [--verbose] [noid]

generate nice and opaque identifiers (noids)

positional arguments:
  noid                  a noid

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        path to a config file with a noid section
  -v, --validate        validate the given noid [default: False]
  -s SCHEME, --scheme SCHEME
                        the noid scheme [default: 'ark:/']
  -N NAA, --naa NAA     the name assigning authority (NAA) number [default: ]
  -t TEMPLATE, --template TEMPLATE
                        the template by which to generate noids [default: 'zeeddk']
  -n INDEX, --index INDEX
                        a number for which to generate a valid noid [default: random positive integer]
  --verbose             turn on verbose text [default: False]

```

###Validating a noid
Validate a noid using the `-v/--validate` flag and pass a noid.
```shell
noid -v $(noid) # self-validation
```

###Options
####Specify the NAA
Use the `-N/--naa` option.
```shell
noid --naa 1234
```

####Specify the scheme
Use the `-s/--scheme` option.
```shell
noid --scheme darpa::
```

####Specify a template
Use the `-t/--template` option.
```shell
noid -t zeeddeedeedk
```

####Compute a noid for a value

## Testing
```
pip install -r requirements.txt
tox
```

## Authors
* Paul K. Korir - EMBL-EBI (current implementation)
    * [Paul Korir](https://github.com/paulkorir)
* Original source code was by:
    * [Yinlin Chen](https://github.com/yinlinchen)
    * [Tingting Jiang](https://github.com/tingtingjh)
    * [Lee Hunter](https://github.com/whunter)
    * [T. Johnson](https://github.com/no-reply)

See also the list of [contributors](https://github.com/paulkorir/noid/graphs/contributors) who participated in this project.

## Thanks
This tool was heavily influenced from [noid-mint](https://github.com/vt-digital-libraries-platform/NOID-mint)

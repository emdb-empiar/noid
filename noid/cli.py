import argparse
import shlex
import sys
from configparser import ConfigParser, ExtendedInterpolation

DEFAULT_NAA = ''
DEFAULT_SCHEME = 'ark:/'
DEFAULT_TEMPLATE = 'zeeddk'

# a global variable
parser = argparse.ArgumentParser(
    prog='noid',
    description='generate nice and opaque identifiers'
)
parser.add_argument(
    'noid',
    nargs='?',
    default=None,
    help="a noid"
)
parser.add_argument(
    '-c', '--config-file',
    help="path to a config file with a noid section"
)
noid_action = parser.add_mutually_exclusive_group()
noid_action.add_argument(
    '-V', '--validate',
    action='store_true',
    default=False,
    help="validate the given noid [default: False]"
)
noid_action.add_argument(
    '-d', '--check-digit',
    action='store_true',
    default=False,
    help="compute and print the corresponding check digit for the given noid [default: False]"
)
parser.add_argument(
    '-s', '--scheme',
    default=DEFAULT_SCHEME,
    help=f"the noid scheme [default: '{DEFAULT_SCHEME}']"
)
parser.add_argument(
    '-N', '--naa',
    default=DEFAULT_NAA,
    help=f"the name assigning authority (NAA) number [default: {DEFAULT_NAA}]"
)
parser.add_argument(
    '-t', '--template',
    default=DEFAULT_TEMPLATE,
    help=f"the template by which to generate noids [default: '{DEFAULT_TEMPLATE}']"
)
parser.add_argument(
    '-n', '--index',
    type=int,
    default=-1,
    help="a number for which to generate a valid noid [default: random positive integer]"
)
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    default=False,
    help="turn on verbose text [default: False]"
)


class _ConfigParser(ConfigParser):
    """String-printable version"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        string = ""
        for section in self.sections():
            string += f"[{section}]\n"
            for option in self[section]:
                string += f"{option} = {self.get(section, option, raw=True)}\n"
            string += "\n"
        return string


def read_configs(args):
    configs = _ConfigParser(interpolation=ExtendedInterpolation())
    configs.read(args.config_file)
    return configs


def parse_args():
    """Parse CLI args"""
    args = parser.parse_args()
    # attach configs to the args namespace
    if args.config_file:
        if args.verbose:
            print(f"using configs: {args.config_file}", file=sys.stderr)
        configs = read_configs(args)
        _options = ['template', 'scheme', 'naa']
        if 'noid' in configs.sections():
            # overwrite using whatever is available
            for o in _options:
                if o in configs['noid']:
                    setattr(args, o, configs.get('noid', o))
                else:
                    print(f"warning: configs missing option '{o}'; using default value ({getattr(args, o)})",
                          file=sys.stderr)
        else:
            print(f"warning: config file '{args.config_file}' lacks 'noid' section; ignoring config file",
                  file=sys.stderr)
    # argument validation
    if (args.validate or args.check_digit) and args.noid is None:
        print("error: missing noid to validate", file=sys.stderr)
        return None
    return args


def cli(cmd):
    sys.argv = shlex.split(cmd)
    return parse_args()

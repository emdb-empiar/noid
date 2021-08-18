import argparse
import shlex
import sys
from configparser import ConfigParser, ExtendedInterpolation

DEFAULT_NAA = 0
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
parser.add_argument(
    '-v', '--validate',
    action='store_true',
    default=False,
    help="validate the given noid [default: False]"
)
parser.add_argument(
    '-s', '--scheme',
    default=DEFAULT_SCHEME,
    help=f"the noid scheme [default: '{DEFAULT_SCHEME}']"
)
parser.add_argument(
    '-N', '--naa',
    default=DEFAULT_NAA,
    type=int,
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
    help="a number for which to generate a valid noid [default: random positive integer]"
)
parser.add_argument(
    '--verbose',
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
    if args.verbose:
        print(f"using configs: {args.config_file}", file=sys.stderr)
    # attach configs to the args namespace
    if args.config_file:
        args._configs = read_configs(args)
    return args


def cli(cmd):
    sys.argv = shlex.split(cmd)
    return parse_args()
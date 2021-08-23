import os
import sys
from random import randint

from noid import utils, cli


def mint(template: str = 'zek', n: int = -1, scheme: str = '', naa: str = '') -> str:
    """ Mint identifiers according to template with a prefix of scheme + naa.

    :param str template: a string consisting of GENTYPE + (DIGTYPE)+ [+ CHECKDIGIT]
    :param int n: a number to convert to a noid; default is -1 meaning create from random number
    :param str scheme: a scheme e.g. 'ark:/', 'doi:', 'http://', 'https://' etc.
    :param str naa: name assigning authority (number); can also be a string
    :return noid: a valid noid with/out check digit or the empty string (failure)
    :rtype str

    Template is of form [mask] or [prefix].[mask] where prefix is any URI-safe string and mask is a string of any
    combination 'e' and 'd', optionally beginning with a mint order indicator ('r'|'s'|'z') and/or ending
    with a checkdigit ('k'):

    Example Templates:
    d      : 0, 1, 2, 3
    zek    : 00, xt, 3f0, 338bh
    123.zek: 123.00, 123.xt, 123.3f0, 123.338bh
    seddee : 00000, k50gh, 637qg
    seddeek: 000000, k06178, b661qj

    The result is appended to the scheme and naa as follows: scheme + naa + '/' + [id].

    There is no checking to ensure ids are not reminted. Instead, minting can be controlled by supplying a (int)
    value for 'n'. It is possible to implement ordered or random minting from available ids by manipulating this
    number from another program. If no 'n' is given, minting is random from within the namespace. An indicator is
    added between '/' and [id] to mark these ids as for short term testing only. An override may be added later to
    accommodate applications which don't mind getting used ids.

    A note about 'r', 's', and 'z': 'z' indicates that a namespace should expand on its first element to accommodate
    any 'n' value (eg. 'de' becomes 'dde' then 'ddde' as numbers get larger). That expansion can be handled by this
    method. 'r' and 's' (typically meaning 'random' and 'sequential') are recognized as valid values, but ignored
    and must be implemented elsewhere.
    """
    # todo: handle 'r' and 's'
    prefix, mask = utils.remove_prefix(template)
    if not utils.validate_mask(mask):
        return ''
    if naa:
        naa += '/'
    _noid = generate_noid(mask, n)
    noid = f"{scheme}{naa}{prefix}{_noid}"
    if mask[-1] in utils.CHECKDIG:
        noid = f"{noid}{calculate_check_digit(_noid)}"
    return noid


def generate_noid(mask: str, n: int) -> str:
    """The actual noid generation

    :param str mask: the mask string
    :param int n: the number to use (default: -1, random number)
    :return str: the noid or an empty string
    """
    if n < 0:
        if mask[0] in utils.GENTYPES:
            mask = mask[1:]
        n = randint(0, utils.get_noid_range(mask) - 1)
    length = n
    noid = ''
    # construct the noid starting from the right
    # convert the numerical value 'n' to the digits specified in the mask
    for char in mask[::-1]:
        if char == 'e':
            div = len(utils.XDIGIT)
        elif char == 'd':
            div = len(utils.DIGIT)
        else:
            continue
        value = n % div
        n = n // div
        noid += (utils.XDIGIT[value])
    # if we have anytheng left over we continue using the leftmost mask character
    # this should not happen with 'z'
    if mask[0] == 'z':
        char = mask[1]
        while n > 0:
            if char == 'e':
                div = len(utils.XDIGIT)
            elif char == 'd':
                div = len(utils.DIGIT)
            else:
                print(f"error: template mask is corrupt; cannot process character: {char}", file=sys.stderr)
                return ''
            value = n % div
            n = n // div
            noid += (utils.XDIGIT[value])

    # if there is still something left over, we've exceeded our namespace.
    # checks elsewhere should prevent this case from ever evaluating true.
    if n > 0:
        print(f"error: cannot mint a noid for (counter = {length}) within this namespace.", file=sys.stderr)
        return ''
    # since we generated the noid from right to left we reverse it
    return noid[::-1]


def validate(noid: str) -> bool:
    """Checks if the final character is a valid checkdigit for the id. Will fail for ids with no checkdigit.

    This will also attempt to strip scheme strings (eg. 'doi:', 'ark:/') from the beginning of the string.
    This feature is limited, however, so if you haven't tested with your particular namespace,
    it's best to pass in ids with that data removed.

    :param str noid: a noid to validate
    :rtype bool: whether or not the noid is valid
    """
    return calculate_check_digit(noid[0:-1]) == noid[-1]


def calculate_check_digit(noid: str) -> str:
    """Given a noid determine the check digit to be appended from the alphabet

    :param str noid: a valid noid string
    :return str: a single character that is a check digit for the noid
    """
    # TODO: Fix checkdigit to autostrip scheme names shorter or longer than 3 chars.
    try:
        # if we have 'ark:/' remove them
        if noid[3] == ':':
            noid = noid[4:].lstrip('/')
    except IndexError:
        pass

    def index_of(x):
        """get the index of the extended digit"""
        try:
            return utils.XDIGIT.index(x)
        except:
            print(f"error: invalid character '{x}'; digits should be in '{''.join(utils.XDIGIT)}'", file=sys.stderr)
            return 0

    total = list()
    for i, index in enumerate(map(index_of, noid)):
        total += [index * (i + 1)]
    index = sum(total) % len(utils.XDIGIT)
    return utils.XDIGIT[index]


def main():
    """Main entry point"""
    args = cli.parse_args()
    if args is None:
        return os.EX_USAGE
    if args.validate:
        if args.verbose:
            print(f"info: validating '{args.noid}'...", file=sys.stderr)
        print(f"'{args.noid}' valid? {validate(args.noid)}")
    elif args.check_digit:
        if args.verbose:
            print(f"info: computing check digit for '{args.noid}'...", file=sys.stderr)
        check_digit = calculate_check_digit(args.noid)
        print(check_digit)
    else:
        if args.verbose:
            print(f"info: generating noid using template={args.template}, n={args.index}, "
                  f"scheme={args.scheme}, naa={args.naa}...", file=sys.stderr)
        noid = mint(args.template, args.index, scheme=args.scheme, naa=args.naa)
        print(noid)
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())

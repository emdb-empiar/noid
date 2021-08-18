import os
import sys
from random import randint

from noid import utils
# import get_noid_range, validate_mask, DIGIT, XDIGIT, GENTYPES, SHORT, InvalidTemplateError, \
#     NamespaceError




def mint(template='zek', n=None, scheme=None, naa=None):
    """ Mint identifiers according to template with a prefix of scheme + naa.

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
    # determine the prefix and mask
    if '.' in template:
        prefix, mask = template.rsplit('.', 1)
    else:
        mask = template
        prefix = ''

    # validate the mask
    validate_mask(mask)

    if n is None:
        if mask[0] in GENTYPES:
            mask = mask[1:]
        # If we hit this point, this is a random (and therefore, short-term) identifier. 
        prefix = SHORT + prefix
        n = randint(0, get_noid_range(mask) - 1)

    noid = f"{prefix}{generate_noid(n, mask)}"

    if naa:
        noid = naa.strip('/') + '/' + noid
    if template[-1] == 'k':
        noid += calculate_check_digit(noid)
    if scheme:
        noid = scheme + noid
    return noid


def mint_(args) -> str:
    prefix, mask = utils.remove_prefix(template, args)
    if not validate_mask(mask):
        return ''
    noid = generate_noid_(mask, args)
    noid = utils.add_prefix(prefix, noid, args)
    noid = utils.add_naa(noid, args)
    noid = append_check_digit(noid, args)
    noid = utils.add_scheme(noid, args)
    return noid


def generate_mask(args):
    # determine the prefix and mask
    if '.' in template:
        prefix, mask = template.rsplit('.', 1)
    else:
        mask = template
        prefix = ''
    # validate the mask
    validate_mask(mask)
    return prefix, mask


def generate_noid_(mask, args):
    if args.index is None:
        if mask[0] in utils.GENTYPES:
            mask = mask[1:]
        n = randint(0, utils.get_noid_range(mask) - 1)
    else:
        n = args.index
    length = n
    noid = ''
    # construct the noid starting from the right
    # convert the numerical value 'n' to the digits specified in the mask
    for char in mask[::-1]:
        if char == 'e':
            div = len(XDIGIT)
        elif char == 'd':
            div = len(DIGIT)
        else:
            continue
        value = n % div
        n = n // div
        noid += (XDIGIT[value])
    # if we have anytheng left over we continue using the leftmost mask character
    # this should not happen with 'z'
    if mask[0] == 'z':
        char = mask[1]
        while n > 0:
            if char == 'e':
                div = len(XDIGIT)
            elif char == 'd':
                div = len(DIGIT)
            else:
                raise utils.InvalidTemplateError("Template mask is corrupt. Cannot process character: " + char)
            value = n % div
            n = n // div
            noid += (XDIGIT[value])

    # if there is still something left over, we've exceeded our namespace.
    # checks elsewhere should prevent this case from ever evaluating true.
    if n > 0:
        raise utils.NamespaceError("Cannot mint a noid for (counter = " + str(length) + ") within this namespace.")

    # since we generated the noid from right to left we reverse it
    return noid[::-1]


def validate(s):
    """Checks if the final character is a valid checkdigit for the id. Will fail for ids with no checkdigit.

    This will also attempt to strip scheme strings (eg. 'doi:', 'ark:/') from the beginning of the string. This feature is limited, however, so if you haven't tested with your particular namespace, it's best to pass in ids with that data removed.

    Returns True on success, ValidationError on failure.
    """
    return calculate_check_digit(s[0:-1]) == s[-1]


def generate_noid(n, mask):
    """Generate the actual noid

    :param int n:
    """
    length = n
    noid = ''
    for char in mask[::-1]:
        if char == 'e':
            div = len(XDIGIT)
        elif char == 'd':
            div = len(DIGIT)
        else:
            continue
        value = n % div
        n = n // div
        noid += (XDIGIT[value])

    if mask[0] == 'z':
        char = mask[1]
        while n > 0:
            if char == 'e':
                div = len(XDIGIT)
            elif char == 'd':
                div = len(DIGIT)
            else:
                raise InvalidTemplateError("Template mask is corrupt. Cannot process character: " + char)
            value = n % div
            n = n // div
            noid += (XDIGIT[value])

    # if there is still something left over, we've exceeded our namespace. 
    # checks elsewhere should prevent this case from ever evaluating true.
    if n > 0:
        raise NamespaceError("Cannot mint a noid for (counter = " + str(length) + ") within this namespace.")

    return noid[::-1]


def calculate_check_digit(noid):
    """Given a noid determine the check digit to be appended from the alphabet

    :param str noid: a valid noid string
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
            return XDIGIT.index(x)
        except:
            return 0

    total = list()
    for i, index in enumerate(map(index_of, noid)):
        total += [index * (i + 1)]
    index = sum(total) % len(XDIGIT)
    # index = sum([x * (i + 1) for i, x in enumerate(map(index_of, noid))]) % len(XDIGIT)
    return XDIGIT[index]


def main():
    print(mint(template='eeddeede', n=None, scheme='ark:/', naa='53696'))
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())

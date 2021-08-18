DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # 10
XDIGIT = DIGIT + ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w',
                  'x', 'y', 'z'] + \
         ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
          'Z']
GENTYPES = ['r', 's', 'z']
DIGTYPES = ['d', 'e']
CHECKDIG = ['k']
SHORT = ''


#
# SHORT = '.shrt.'


def get_noid_range(mask):
    """Given the specified mask compute the maximum number of noids availabl

    :param str mask: the mask; if GENTYPE and CHECKDIG are present they will be ignored; only DIGTYPES are considered
    :return int max_int: the maximum number of noids
    """
    max_int = 1
    for c in mask:
        if c == 'e':
            max_int *= len(XDIGIT)
        elif c == 'd':
            max_int *= len(DIGIT)
    return max_int


def validate_mask(mask):
    """Check to make sure that we have a valid mask

    :param list mask: a sequence of characters
    :return bool: whether or not the mask is valid
    """
    # check the first character
    if not (mask[0] in GENTYPES or mask[0] in DIGTYPES):
        return False
    # check the last character
    elif not (mask[-1] in CHECKDIG or mask[-1] in DIGTYPES):
        return False
    # check all other characters
    else:
        for maskchar in mask[1:-1]:
            if not (maskchar in DIGTYPES):
                return False

    return True


def remove_prefix(template):
    """Split the template into the prefix and mask

    :param str template: a template string
    :return: the prefix
    :rtype str:
    :return: the mask
    :rtype str:
    """
    if '.' in template:
        prefix, mask = template.rsplit('.', 1)
        prefix += '.'
    else:
        mask = template
        prefix = ''
    return prefix, mask

import unittest
import secrets
from noid import cli, pynoid, utils

"""
Behaviours:

# generates a noid using arg defaults
noid    

# generates a noid according to config
noid -c path/to/conf/file

# validate a noid
noid -v/--validate <noid>
# validating: <noid>
# valid/invalid 

# overwrite scheme
noid -s/--scheme "doi:/"

# set naa
noid -N/--naa 1234

# overwrite template
noid -t/--template zeek

# set n
noid -n/--index

"""


class PynoidCLI(unittest.TestCase):
    def test_default(self):
        args = cli.cli(f"noid")
        self.assertIsNone(args.noid)
        self.assertIsNone(args.config_file)
        self.assertFalse(args.validate)
        self.assertEqual(args.scheme, cli.DEFAULT_SCHEME)
        self.assertEqual(args.naa, cli.DEFAULT_NAA)
        self.assertEqual(args.template, cli.DEFAULT_TEMPLATE)
        self.assertIsNone(args.index)
        self.assertFalse(args.verbose)


class PynoidAPI(unittest.TestCase):
    def test_mint(self):
        args = cli.cli(f"noid")
        noid = pynoid.mint_(args)
        print(f"noid: {noid}")


class PynoidUtils(unittest.TestCase):
    def test_validate_mask(self):
        """Validate a mask"""
        self.assertTrue(utils.validate_mask('zek'))
        self.assertTrue(utils.validate_mask('ze'))
        self.assertTrue(utils.validate_mask('zdk'))
        self.assertTrue(utils.validate_mask('zd'))
        self.assertTrue(utils.validate_mask('zededededdeeddk'))
        self.assertTrue(utils.validate_mask('zededededdeedd'))
        self.assertTrue(utils.validate_mask('rek'))
        self.assertTrue(utils.validate_mask('re'))
        self.assertTrue(utils.validate_mask('rdk'))
        self.assertTrue(utils.validate_mask('rd'))
        self.assertTrue(utils.validate_mask('rededededdeeddk'))
        self.assertTrue(utils.validate_mask('rededededdeedd'))
        self.assertTrue(utils.validate_mask('sek'))
        self.assertTrue(utils.validate_mask('se'))
        self.assertTrue(utils.validate_mask('sdk'))
        self.assertTrue(utils.validate_mask('sd'))
        self.assertTrue(utils.validate_mask('sededededdeeddk'))
        self.assertTrue(utils.validate_mask('sededededdeedd'))
        self.assertTrue(utils.validate_mask('ek'))
        self.assertTrue(utils.validate_mask('e'))
        self.assertTrue(utils.validate_mask('dk'))
        self.assertTrue(utils.validate_mask('d'))
        self.assertTrue(utils.validate_mask('ededededdeeddk'))
        self.assertTrue(utils.validate_mask('ededededdeedd'))
        self.assertFalse(utils.validate_mask('a'))
        self.assertFalse(utils.validate_mask('aa'))
        self.assertFalse(utils.validate_mask('zeeedddl'))
        self.assertFalse(utils.validate_mask('zeeedtddl'))
        self.assertFalse(utils.validate_mask('zeeedtdd'))
        self.assertFalse(utils.validate_mask('adddeeew'))

    def test_get_noid_range(self):
        """Get the max_size"""
        xsize = len(utils.XDIGIT)
        dsize = len(utils.DIGIT)
        self.assertEqual(xsize ** 2 * dsize, utils.get_noid_range('zedek'))
        self.assertEqual(dsize ** 4, utils.get_noid_range('zddddk'))
        self.assertEqual(xsize ** 4, utils.get_noid_range('zeeeek'))
        self.assertEqual(xsize ** 3, utils.get_noid_range('seee'))
        self.assertEqual(dsize ** 2 * xsize ** 2, utils.get_noid_range('rddee'))

    def test_remove_prefix(self):
        """Remove the prefix"""
        self.assertEqual(('something.', 'eedeede'), utils.remove_prefix('something.eedeede'))
        self.assertEqual(('', 'eedeede'), utils.remove_prefix('eedeede'))
        self.assertEqual(('something.', 'eedeedek'), utils.remove_prefix('something.eedeedek'))
        self.assertEqual(('', 'eedeedek'), utils.remove_prefix('eedeedek'))
        self.assertEqual(('something.', 'reddek'), utils.remove_prefix('something.reddek'))
        self.assertEqual(('', 'reddek'), utils.remove_prefix('reddek'))

    def test_add_naa(self):
        """Return the prefix"""

        prefix, mask = utils.remove_prefix('something.eeddeede')
        utils.add_prefix(prefix, noid)


class PynoidTests(unittest.TestCase):

    def test_naa_append(self):
        noid = pynoid.mint(naa='abc')
        self.assertTrue(noid.startswith('abc/'))

    def test_scheme_append(self):
        schemes = ['doi:', 'ark:/', 'http://']
        for scheme in schemes:
            noid = pynoid.mint(scheme=scheme)
            self.assertTrue(noid.startswith(scheme))

    def test_mint_short_term(self):
        noid = pynoid.mint()
        self.assertTrue(noid.startswith(utils.SHORT))

    def test_mint_ns(self):
        """Over the range of each digit-space the index produces the respective digit"""
        ns = range(len(utils.DIGIT))
        for n in ns:
            self.assertEqual(pynoid.mint('d', n), utils.DIGIT[n])
        ns = range(len(utils.XDIGIT))
        for n in ns:
            self.assertEqual(pynoid.mint('e', n), utils.XDIGIT[n])

    def test_namespace_overflow(self):
        """Overflow occurs when we require a value outside of the range of the template"""
        self.assertRaises(utils.NamespaceError, pynoid.mint, template='d', n=len(utils.DIGIT) + 1)
        self.assertRaises(utils.NamespaceError, pynoid.mint, template='e', n=len(utils.XDIGIT) + 1)

    def test_mint_z_rollover(self):
        """Rollover happens when we exhaust the character space"""
        self.assertEqual(pynoid.mint('zd', len(utils.DIGIT)), '10')
        self.assertEqual(pynoid.mint('ze', len(utils.XDIGIT)), '10')

    def test_validate_valid(self):
        """Given some valid noids check that they are valid"""
        valid = 'test31wqw0ws9'
        valid_scheme = 'ark:/test31wqw0ws9'
        self.assertTrue(pynoid.validate(valid))
        self.assertTrue(pynoid.validate(valid_scheme))

    def test_validate_invalid(self):
        """Invalid noids with/out scheme"""
        invalid = 'test31qww0wsr'
        invalid_scheme = 'ark:/test31qww0wsr'
        self.assertFalse(pynoid.validate(invalid))
        self.assertFalse(pynoid.validate(invalid_scheme))

    def test_checkdigit(self):
        """The check digit is sensitive to permutations"""
        self.assertEqual(pynoid.mint('eek', 100), '1MA')
        self.assertFalse(pynoid.validate('M1A'))


if __name__ == '__main__':
    unittest.main()

import unittest

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


class PynoidUtils(unittest.TestCase):
    def test__validate_mask(self):
        """Validate a mask"""
        self.assertTrue(noid.utils._validate_mask('zek'))
        self.assertTrue(noid.utils._validate_mask('ze'))
        self.assertTrue(noid.utils._validate_mask('zdk'))
        self.assertTrue(noid.utils._validate_mask('zd'))
        self.assertTrue(noid.utils._validate_mask('zededededdeeddk'))
        self.assertTrue(noid.utils._validate_mask('zededededdeedd'))
        self.assertTrue(noid.utils._validate_mask('rek'))
        self.assertTrue(noid.utils._validate_mask('re'))
        self.assertTrue(noid.utils._validate_mask('rdk'))
        self.assertTrue(noid.utils._validate_mask('rd'))
        self.assertTrue(noid.utils._validate_mask('rededededdeeddk'))
        self.assertTrue(noid.utils._validate_mask('rededededdeedd'))
        self.assertTrue(noid.utils._validate_mask('sek'))
        self.assertTrue(noid.utils._validate_mask('se'))
        self.assertTrue(noid.utils._validate_mask('sdk'))
        self.assertTrue(noid.utils._validate_mask('sd'))
        self.assertTrue(noid.utils._validate_mask('sededededdeeddk'))
        self.assertTrue(noid.utils._validate_mask('sededededdeedd'))
        self.assertTrue(noid.utils._validate_mask('ek'))
        self.assertTrue(noid.utils._validate_mask('e'))
        self.assertTrue(noid.utils._validate_mask('dk'))
        self.assertTrue(noid.utils._validate_mask('d'))
        self.assertTrue(noid.utils._validate_mask('ededededdeeddk'))
        self.assertTrue(noid.utils._validate_mask('ededededdeedd'))
        self.assertFalse(noid.utils._validate_mask('a'))
        self.assertFalse(noid.utils._validate_mask('aa'))
        self.assertFalse(noid.utils._validate_mask('zeeedddl'))
        self.assertFalse(noid.utils._validate_mask('zeeedtddl'))
        self.assertFalse(noid.utils._validate_mask('zeeedtdd'))
        self.assertFalse(noid.utils._validate_mask('adddeeew'))

    def test__get_noid_range(self):
        """Get the max_size"""
        xsize = len(noid.utils.XDIGIT)
        dsize = len(noid.utils.DIGIT)
        self.assertEqual(xsize ** 2 * dsize, noid.utils._get_noid_range('zedek'))
        self.assertEqual(dsize ** 4, noid.utils._get_noid_range('zddddk'))
        self.assertEqual(xsize ** 4, noid.utils._get_noid_range('zeeeek'))
        self.assertEqual(xsize ** 3, noid.utils._get_noid_range('seee'))
        self.assertEqual(dsize ** 2 * xsize ** 2, noid.utils._get_noid_range('rddee'))


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
        valid = 'test31wqw0wsr'
        valid_scheme = 'ark:/test31wqw0wsr'
        self.assertTrue(pynoid.validate(valid))
        self.assertTrue(pynoid.validate(valid_scheme))

    def test_validate_invalid(self):
        invalid = 'test31qww0wsr'
        invalidScheme = 'ark:/test31qww0wsr'
        self.assertRaises(ValidationError, validate, invalid)
        self.assertRaises(ValidationError, validate, invalidScheme)

    def test_checkdigit(self):
        self.assertEqual(mint('eek', 100), '3f0')
        self.assertRaises(ValidationError, validate, 'f30')


if __name__ == '__main__':
    unittest.main()

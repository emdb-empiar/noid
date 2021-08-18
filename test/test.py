import unittest

from noid import cli, pynoid

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
        self.assertTrue(pynoid._validate_mask('zek'))
        self.assertTrue(pynoid._validate_mask('ze'))
        self.assertTrue(pynoid._validate_mask('zdk'))
        self.assertTrue(pynoid._validate_mask('zd'))
        self.assertTrue(pynoid._validate_mask('zededededdeeddk'))
        self.assertTrue(pynoid._validate_mask('zededededdeedd'))
        self.assertTrue(pynoid._validate_mask('rek'))
        self.assertTrue(pynoid._validate_mask('re'))
        self.assertTrue(pynoid._validate_mask('rdk'))
        self.assertTrue(pynoid._validate_mask('rd'))
        self.assertTrue(pynoid._validate_mask('rededededdeeddk'))
        self.assertTrue(pynoid._validate_mask('rededededdeedd'))
        self.assertTrue(pynoid._validate_mask('sek'))
        self.assertTrue(pynoid._validate_mask('se'))
        self.assertTrue(pynoid._validate_mask('sdk'))
        self.assertTrue(pynoid._validate_mask('sd'))
        self.assertTrue(pynoid._validate_mask('sededededdeeddk'))
        self.assertTrue(pynoid._validate_mask('sededededdeedd'))
        self.assertTrue(pynoid._validate_mask('ek'))
        self.assertTrue(pynoid._validate_mask('e'))
        self.assertTrue(pynoid._validate_mask('dk'))
        self.assertTrue(pynoid._validate_mask('d'))
        self.assertTrue(pynoid._validate_mask('ededededdeeddk'))
        self.assertTrue(pynoid._validate_mask('ededededdeedd'))
        self.assertFalse(pynoid._validate_mask('a'))

    def test__get_noid_range(self):
        """Get the max_size"""

        print(pynoid._get_noid_range('zedek'))
        print(pynoid._get_noid_range('zdk'))

class PynoidTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_naa_append(self):
        noid = mint(naa='abc')
        self.assertTrue(noid.startswith('abc/'))

    def test_scheme_append(self):
        schemes = ['doi:', 'ark:/', 'http://']
        for scheme in schemes:
            noid = mint(scheme=scheme)
            self.assertTrue(noid.startswith(scheme))

    def test_mint_short_term(self):
        noid = mint()
        self.assertTrue(noid.startswith(SHORT))

    def test_mint_ns(self):
        ns = range(10)
        for n in ns:
            self.assertEqual(mint('d', n), DIGIT[n])
        ns = range(29)
        for n in ns:
            self.assertEqual(mint('e', n), XDIGIT[n])

    def test_namespace_overflow(self):
        self.assertRaises(pynoid.NamespaceError, pynoid.mint, template='d', n=10)
        self.assertRaises(pynoid.NamespaceError, pynoid.mint, template='e', n=29)

    def test_mint_z_rollover(self):
        self.assertEqual(mint('zd', 10), '10')
        self.assertEqual(mint('ze', 29), '10')

    def test_validate_valid(self):
        valid = 'test31wqw0wsr'
        validScheme = 'ark:/test31wqw0wsr'
        self.assertTrue(validate(valid))
        self.assertTrue(validate(validScheme))

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

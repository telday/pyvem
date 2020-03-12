
import unittest


class TestEnvironment(unittest.TestCase):


    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    def test_constructor(self):
        KWARGS = {
                'system_site_packages':1,
                'clear':2,
                'symlinks':3,
                'upgrade':4,
                'with_pip':5,
                'installed_packages':6,
                'python_version':7,
            }

        REQUIRED_KWARGS = {
                'prompt':8,
                'location':9,
            }

        combos = powerset(KWARGS + REQUIRED_KWARGS)
        for i in KWARGS:
            if 

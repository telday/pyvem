import itertools
import unittest
import pyvem.environment as e

class TestEnvironment(unittest.TestCase):
    """Tests the environment class"""
    def powerset(self, iterable):
        """Gets the powerset of the iterable"""
        s = list(iterable)
        return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

    def check_has_required(self, args):
        """Checks if the required kwargs are listed in the list args"""
        for i in e.Environment.REQUIRED_KWARGS:
            if i not in args:
                return False
        return True

    def test_constructor(self):
        """Tests the setup of getters and setters for the Environment class"""
        combos = self.powerset(e.Environment.OPTIONAL_KWARGS + e.Environment.REQUIRED_KWARGS)
        for i in range(len(combos)):
            kwargs = dict()
            for j in range(len(combos[i])):
                kwargs[combos[i][j]] = i
            if self.check_has_required(list(kwargs.keys())):
                tmp_env = e.Environment(**kwargs)
                for j in range(len(combos[i])):
                    self.assertEqual(tmp_env.__getattribute__(combos[i][j]), i)
            else:
                with self.assertRaises(Exception):
                    tmp_env = e.Environment(**kwargs)

import unittest

from lib.pairing_func import pairing_function, reverse_pairing_function
from lib.labels import label_to_ordinal, ordinal_to_label, is_valid_label
from lib.variables import variable_to_ordinal, ordinal_to_variable
from lib.primes import nth_prime
from lib.encoder import encode_program
from lib.decoder import decode_q


class PairingFunctionTests(unittest.TestCase):
    def test_reverse_undoes_pairing(self):
        for x, y in [(0, 0), (1, 1), (4, 9), (0, 12), (7, 0)]:
            paired = pairing_function(x, y)
            self.assertEqual(reverse_pairing_function(paired), {"x": x, "y": y})


class LabelTests(unittest.TestCase):
    def test_ordinal_round_trip(self):
        for label in ("A1", "E1", "A2", "C7", "E12"):
            self.assertEqual(ordinal_to_label(label_to_ordinal(label)), label)

    def test_valid_labels(self):
        for label in ("A1", "E12", "B3"):
            self.assertTrue(is_valid_label(label))

    def test_invalid_labels(self):
        for label in ("1A", "", "F1", "A0"):
            self.assertFalse(is_valid_label(label))


class VariableTests(unittest.TestCase):
    def test_ordinal_round_trip(self):
        for variable in ({"kind": "Y"}, {"kind": "X", "index": 1}, {"kind": "Z", "index": 3}):
            self.assertEqual(ordinal_to_variable(variable_to_ordinal(variable)), variable)


class RoundTripTests(unittest.TestCase):
    def encode_decode(self, program):
        encoded = encode_program(program)
        # rebuild q the way the godel number itself is defined, product of prime^exp, minus 1
        q = 1
        for i, exp in enumerate(encoded["instructionCode"]):
            q *= nth_prime(i + 1) ** exp
        q -= 1
        return decode_q(q)["instructions"]

    def test_simple_loop(self):
        program = [
            {"label": "A1", "variable": {"kind": "X", "index": 1}, "statementType": "increment", "targetLabel": None},
            {"label": None, "variable": {"kind": "X", "index": 1}, "statementType": "Goto", "targetLabel": "A1"},
        ]
        self.assertEqual(self.encode_decode(program), program)

    def test_mixed_instructions(self):
        program = [
            {"label": "A1", "variable": {"kind": "X", "index": 1}, "statementType": "increment", "targetLabel": None},
            {"label": "B2", "variable": {"kind": "Z", "index": 3}, "statementType": "Goto", "targetLabel": "A1"},
            {"label": None, "variable": {"kind": "Y"}, "statementType": "decrement", "targetLabel": None},
        ]
        self.assertEqual(self.encode_decode(program), program)

    def test_trailing_noop_does_not_survive(self):
        # a trailing Y <- Y with no label codes to 0, prime powers drop trailing zero exponents
        program = [
            {"label": "A1", "variable": {"kind": "X", "index": 1}, "statementType": "increment", "targetLabel": None},
            {"label": None, "variable": {"kind": "Y"}, "statementType": "dummy", "targetLabel": None},
        ]
        self.assertEqual(self.encode_decode(program), program[:1])


if __name__ == "__main__":
    unittest.main()

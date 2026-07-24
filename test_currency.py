import unittest

from currency import safe_float_element,safe_float,safe_int

class TestSafeFloatElement(unittest.TestCase):

    def test_safe_float_element_none(self):
        result = safe_float_element(None)
        self.assertEqual(result, 0.0)
    def test_safe_float_element_valid(self):
        class FakeElement:
            text = "32,50" 
        result = safe_float_element(FakeElement())
        self.assertEqual(result, 32.5)

class TestSafeFloat(unittest.TestCase):

    def test_safe_float_none(self):
        result = safe_float(None)
        self.assertEqual(result, 0.0)

class TestSafeInt(unittest.TestCase):

    def test_safe_int_none(self):
        result = safe_int(None)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
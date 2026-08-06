import unittest

from currency import (
    convert_string_to_float,
    safe_float,
    safe_int,
)


class TestExtractFloatFromElement(unittest.TestCase):
    def test_extract_float_from_element_none(self):
        result = safe_float(None)
        self.assertEqual(result, 0.0)

    def test_extract_float_from_element_valid(self):
        class FakeElement:
            text = "32,50"

        result = safe_float(FakeElement())
        self.assertEqual(result, 32.5)


class TestConvertStringToFloat(unittest.TestCase):
    def test_convert_string_to_float_none(self):
        result = convert_string_to_float(None)
        self.assertEqual(result, 0.0)


class TestConvertStringToInt(unittest.TestCase):
    def test_convert_string_to_int_none(self):
        result = safe_int(None)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

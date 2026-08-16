import unittest

from currency import (
    calculate_exchange,
    safe_float,
    safe_int,
    safe_str,
)


class TestSafeStr(unittest.TestCase):
    def test_ss_valid_element(self):
            class FakeElement:
                text = "test"
    
            result = safe_str(FakeElement())
            self.assertEqual(result, "test")

    def test_ss_valid_element_with_space(self):
        class FakeElement:
            text = "test "

        result = safe_str(FakeElement())
        self.assertEqual(result, "test")

    def test_ss_valid(self):
            result = safe_str("test")
            self.assertEqual(result, "test")

    def test_ss_valid_with_space(self):
        result = safe_str("test ")
        self.assertEqual(result, "test")
    
    def test_ss_none(self):
        result = safe_str(None)
        self.assertEqual(result, "Deger bos")

    def test_ss_none_str(self):
            result = safe_str(12)
            self.assertEqual(result, "Deger none_str")

    def test_ss_numeric_str(self):
        result = safe_str("123")
        self.assertEqual(result, "Deger none_str")

class TestSafeFloat(unittest.TestCase):
    def test_sf_valid_element(self):
            class FakeElement:
                text = "32.50"
    
            result = safe_float(FakeElement())
            self.assertEqual(result, 32.5)

    def test_sf_valid_element_with_comma(self):
        class FakeElement:
            text = "32,50"

        result = safe_float(FakeElement())
        self.assertEqual(result, 32.5)

    def test_sf_valid(self):
            result = safe_float("32.50")
            self.assertEqual(result, 32.50)

    def test_sf_valid_with_comma(self):
        result = safe_float("32,50")
        self.assertEqual(result, 32.50)

    def test_sf_valid_with_space(self):
            result = safe_float("32.50  ")
            self.assertEqual(result, 32.50)
    
    def test_sf_none(self):
        result = safe_float(None)
        self.assertEqual(result, 0.0)

    def test_sf_zero(self):
        result = safe_float("0")
        self.assertEqual(result, 0.0)

    def test_sf_str(self):
            result = safe_float("str")
            self.assertEqual(result, 0.0)

class TestSafeInt(unittest.TestCase):
    def test_si_valid(self):
            result = safe_int("32")
            self.assertEqual(result, 32)

    def test_si_valid_with_comma(self):
        result = safe_int("32,50")
        self.assertEqual(result, 3250)

    def test_si_valid_with_space(self):
            result = safe_int("32   ")
            self.assertEqual(result, 32)
    
    def test_si_none(self):
        result = safe_int(None)
        self.assertEqual(result, -1)

    def test_si_zero(self):
        result = safe_int("0")
        self.assertEqual(result, 0)

    def test_si_str(self):
            result = safe_int("str")
            self.assertEqual(result, -1)      

class TestCalculateExchange(unittest.TestCase):
    def test_ce_valid(self):
            result = calculate_exchange(250,50,1)
            self.assertEqual(result, 5)

    def test_ce_hundred_unit(self):
        result = calculate_exchange(250,50,100)
        self.assertEqual(result, 500)

    def test_ce_none_forex(self):
        result = calculate_exchange(250,None,1)
        self.assertEqual(result, 0.0)

    def test_ce_none_unit(self):
        result = calculate_exchange(250,50,None)
        self.assertEqual(result, 0.0)

    def test_ce_zero_forex(self):
        result = calculate_exchange(250,0,1)
        self.assertEqual(result, 0.0)

    def test_ce_zero_unit(self):
        result = calculate_exchange(250,50,0)
        self.assertEqual(result, 0.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
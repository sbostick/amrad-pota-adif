#!/usr/bin/env python
# https://docs.python.org/3/library/unittest.html
import unittest
import utc_offset

class TestUTCOffsetInvalidInputs(unittest.TestCase):
    """
    Test that invalid inputs raise exceptions.
    """

    def test_invalid_length(self):
        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("777")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("08001")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("-08001")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("-08:001")

    def test_invalid_chars(self):
        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("08OO")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("08xx")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("-08xx")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse(" 0800")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("0800 ")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("08:xx")

        with self.assertRaises(utc_offset.ValidationError) as err:
            (hh, mm) = utc_offset.parse("-x8")


class TestUTCOffset1(unittest.TestCase):
    """
    Match signed/unsigned H or HH
    """

    def test_unsigned_H(self):
        (hh, mm) = utc_offset.parse("8")
        self.assertEqual(hh, 8)
        self.assertEqual(mm, 0)

    def test_signed_H(self):
        (hh, mm) = utc_offset.parse("-8")
        self.assertEqual(hh, -8)
        self.assertEqual(mm, 0)

    def test_unsigned_HH(self):
        (hh, mm) = utc_offset.parse("08")
        self.assertEqual(hh, 8)
        self.assertEqual(mm, 0)

    def test_signed_HH(self):
        (hh, mm) = utc_offset.parse("-08")
        self.assertEqual(hh, -8)
        self.assertEqual(mm, 0)


class TestUTCOffset2(unittest.TestCase):
    """
    Match signed/unsigned HHMM
    """
    def test_unsigned_HHMM(self):
        (hh, mm) = utc_offset.parse("0830")
        self.assertEqual(hh, 8)
        self.assertEqual(mm, 30)

    def test_signed_HHMM(self):
        (hh, mm) = utc_offset.parse("-0830")
        self.assertEqual(hh, -8)
        self.assertEqual(mm, -30)


class TestUTCOffset3(unittest.TestCase):
    """
    Match signed/unsigned HH:MM (with separator)
    """

    def test_unsigned_HH_S_MM(self):
        (hh, mm) = utc_offset.parse("08:30")
        self.assertEqual(hh, 8)
        self.assertEqual(mm, 30)

    def test_signed_HH_S_MM(self):
        (hh, mm) = utc_offset.parse("-08:30")
        self.assertEqual(hh, -8)
        self.assertEqual(mm, -30)

class TestUTCOffsetToString(unittest.TestCase):
    """
    Test capability to return the parsed offset in ISO form
    """

    def test_to_string_001(self):
        result = utc_offset.to_string("08:30")
        self.assertEqual(result, "+08:30")

    def test_to_string_002(self):
        result = utc_offset.to_string("-08:30")
        self.assertEqual(result, "-08:30")

    def test_to_string_003(self):
        result = utc_offset.to_string("0830")
        self.assertEqual(result, "+08:30")

    def test_to_string_004(self):
        result = utc_offset.to_string("-0830")
        self.assertEqual(result, "-08:30")

    def test_to_string_005(self):
        result = utc_offset.to_string("8")
        self.assertEqual(result, "+08:00")

    def test_to_string_006(self):
        result = utc_offset.to_string("-8")
        self.assertEqual(result, "-08:00")


if __name__ == "__main__":
    unittest.main(verbosity=2)

from unittest import TestCase
from datetime import date

import src.data.celendar as lib


class HolidaysTests(TestCase):

    def test_07_03_2022(self):
        actual = lib.is_day_holiday(date(2022, 3, 7))
        expected = 0
        self.assertEqual(expected, actual)

    def test_08_03_2022(self):
        actual = lib.is_day_holiday(date(2022, 3, 8))
        expected = 1
        self.assertEqual(expected, actual)

    def test_09_03_2022(self):
        actual = lib.is_day_holiday(date(2022, 3, 9))
        expected = 1
        self.assertEqual(expected, actual)

    def test_07_03_2023(self):
        actual = lib.is_day_holiday(date(2023, 3, 7))
        expected = 0
        self.assertEqual(expected, actual)

    def test_08_03_2023(self):
        actual = lib.is_day_holiday(date(2023, 3, 8))
        expected = 1
        self.assertEqual(expected, actual)

    def test_09_03_2023(self):
        actual = lib.is_day_holiday(date(2023, 3, 9))
        expected = 1
        self.assertEqual(expected, actual)

    def test_10_03_2023(self):
        actual = lib.is_day_holiday(date(2023, 3, 10))
        expected = 1
        self.assertEqual(expected, actual)

    def test_07_03_2024(self):
        actual = lib.is_day_holiday(date(2024, 3, 7))
        expected = 1
        self.assertEqual(expected, actual)

    def test_08_03_2024(self):
        actual = lib.is_day_holiday(date(2024, 3, 8))
        expected = 1
        self.assertEqual(expected, actual)

    def test_09_03_2024(self):
        actual = lib.is_day_holiday(date(2024, 3, 9))
        expected = 0
        self.assertEqual(expected, actual)

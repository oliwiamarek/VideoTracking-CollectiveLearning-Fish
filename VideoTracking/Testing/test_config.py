import StringIO
import sys
import unittest

import config


class TestConfig(unittest.TestCase):
    def test_log_debugTrue(self):
        config.DEBUG = True
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        test = "test"
        config.log(test)
        result = capturedOutput.getvalue().strip()
        self.assertEqual(result, "test")

    def test_log_debugFalse(self):
        config.DEBUG = False
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        test = "test"
        config.log(test)
        result = capturedOutput.getvalue().strip()
        self.assertEqual(result, "")

    def test_construct_argument_parser_returnsParser(self):
        parser = config.construct_argument_parser()
        self.assertFalse(parser is None)
        self.assertEqual(parser["waiting_frames"], config.WAITING_FRAMES)
        self.assertEqual(parser["threshold"], config.THRESHOLD)
        self.assertEqual(parser["min_area"], config.MIN_AREA_SIZE)

    def test_return_array_returnsRightPartOfArray(self):
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [2, 4, 6, 8, 10]
        result = config.get_array_increments(array, 1, 2)
        self.assertEqual(result, expected)

        expected = [1, 5, 9]
        result = config.get_array_increments(array, 0, 4)
        self.assertEqual(result, expected)

        expected = [3, 2, 1]
        result = config.get_array_increments(array, 2, -1)
        self.assertEqual(expected, result)

    def test_return_array_outOfBoundsReturnsEmptyArray(self):
        array = [1, 2, 3]
        result = config.get_array_increments(array, 3, 6)
        self.assertEqual(result, [])

    def test_return_array_zeroValuesThrowValueError(self):
        array = [1, 2, 3]
        self.assertRaises(ValueError, config.get_array_increments, array, 0, 0)


if __name__ == '__main__':
    unittest.main()

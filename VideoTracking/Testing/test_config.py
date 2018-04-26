#
# This file contains tests for the config file.
#

import StringIO
import sys
import unittest

import config


class TestConfig(unittest.TestCase):
    def test_log_debugTrue(self):
        config.DEBUG = True
        # mock 'print' function
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        test = "test"
        config.log(test)
        result = capturedOutput.getvalue().strip()
        self.assertEqual(result, "test")

    def test_log_debugFalse(self):
        config.DEBUG = False
        # mock 'print' function
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

    def test_get_array_increments_returnsRightPartOfArray(self):
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

    def test_get_array_increments_outOfBoundsReturnsEmptyArray(self):
        array = [1, 2, 3]
        result = config.get_array_increments(array, 3, 6)
        self.assertEqual(result, [])

    def test_get_array_increments_zeroValuesThrowValueError(self):
        array = [1, 2, 3]
        self.assertRaises(ValueError, config.get_array_increments, array, 0, 0)

    def test_is_not_string_returnsRightValues(self):
        self.assertFalse(config.is_not_string(''))
        self.assertFalse(config.is_not_string('foo'))
        self.assertFalse(config.is_not_string('a'))
        self.assertTrue(config.is_not_string(None))
        self.assertTrue(config.is_not_string(True))
        self.assertTrue(config.is_not_string(1))
        self.assertTrue(config.is_not_string(1.01))
        self.assertTrue(config.is_not_string({"object": {}, "name": "foo"}))
        self.assertTrue(config.is_not_string([1, 2, 3]))

    def test_roi_video_setsValuesRight(self):
        mockFrame = type('frame', (object,), {'shape': [4, 9, 16]})()
        expectedWidth = 22
        expectedFirstHeight = 3
        expectedSecondHeight = 6
        config.roi_video(mockFrame)
        resultWidth = config.roi_width
        resultFHight = config.roi_first_height
        resultSHight = config.roi_second_height
        self.assertEqual(expectedWidth, resultWidth)
        self.assertEqual(expectedFirstHeight, resultFHight)
        self.assertEqual(expectedSecondHeight, resultSHight)

    def test_roi_video_incorrectAttributeRaisesAttributeError(self):
        self.assertRaises(AttributeError, config.roi_video, 1)
        self.assertRaises(AttributeError, config.roi_video, type('frame', (object,), {'not-shape': {"name": "foo"}})())
        self.assertRaises(AttributeError, config.roi_video, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()

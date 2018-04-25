import StringIO
import unittest

import sys

import MainProgram as mp


class MainProgramTests(unittest.TestCase):
    def test_print_frame_rate_RaisesErrorWithStringValues(self):
        self.assertRaises(TypeError, mp.print_frame_rate, MockStringCapture)

    def test_print_frame_rate_DoesNotRaiseErrorWithFloatValues(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        mp.print_frame_rate(MockCapture())
        result = capturedOutput.getvalue().strip()
        self.assertTrue("frame rate per second = 5.00\nnumber of frames = 7.00" in result)

    def test_calculate_frames_ReturnsRightValue(self):
        result = mp.calculate_frames(MockCapture(), 5)
        self.assertEqual(result, 25)

    def test_calculate_frames_WrongTypeRaisesTypeError(self):
        self.assertRaises(TypeError, mp.calculate_frames, MockStringCapture, 5)

    def test_calculate_video_duration_setsStopFrameNo(self):
        mp.calculate_video_duration(MockCapture())
        self.assertEqual(mp.stop_frame_no, 7)

    def test_calculate_video_duration_WrongTypeRaisesTypeError(self):
        self.assertRaises(TypeError, mp.calculate_video_duration, MockStringCapture)

    def test_get_name_from_path_returnsPath(self):
        path = "boo/foo"
        expected = "foo"
        self.assertEqual(mp.get_name_from_path(path), expected)

    def test_get_name_from_path_WrongTypeRaisesTypeError(self):
        self.assertRaises(TypeError, mp.get_name_from_path, 123)
        self.assertRaises(TypeError, mp.get_name_from_path, True)


'''
===========================================================================
MOCKS
===========================================================================
'''


class MockStringCapture(object):
    def get(self, integer):
        return str(integer)

    def set(self, integer, startframe):
        print("set")


class MockCapture(object):
    def get(self, integer):
        return float(integer)

    def set(self, integer, startframe):
        print("set")


if __name__ == '__main__':
    unittest.main()

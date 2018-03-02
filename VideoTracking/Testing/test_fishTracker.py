import unittest

import cv2

import FishTracker
from mock import patch, Mock, mock
import sys


class TestFishTracker(unittest.TestCase):
    def setUp(self):
        sys.modules['cv2'] = Mock()
        self.tracker = FishTracker.FishTracker()

    def test_is_not_string(self):
        self.assertTrue(self.tracker.is_not_string(1))
        self.assertFalse(self.tracker.is_not_string("String"))
        self.assertFalse(self.tracker.is_not_string(""))

    def test_draw_point(self):
        patcher = mock.patch.object(cv2, 'circle')
        patched = patcher.start()
        event_left_button_pressed = 1
        event_other = 0
        x, y = 15, 20

        self.tracker.draw_point(event_other, x, y, {}, {})
        self.assertFalse(self.tracker.mouse_x == x)
        self.assertFalse(self.tracker.mouse_y == y)
        self.assertNotEqual(patched.call_count, 1)

        self.tracker.draw_point(event_left_button_pressed, x, y, {}, {})
        self.assertTrue(self.tracker.mouse_x == x)
        self.assertTrue(self.tracker.mouse_y == y)
        self.assertEqual(patched.call_count, 1)
        patched.assert_called_with(self.tracker.current_frame, (x, y), 5, (0, 255, 0), -1)


if __name__ == '__main__':
    unittest.main()

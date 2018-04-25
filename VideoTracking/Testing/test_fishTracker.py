import unittest

import cv2

import FishTracker
from mock import patch, Mock, mock
import sys


class TestFishTracker(unittest.TestCase):
    def setUp(self):
        sys.modules['cv2'] = Mock()
        self.tracker = FishTracker.FishTracker()

    def test_draw_point_setsRightValues(self):
        patcher = mock.patch.object(cv2, 'circle')
        patched = patcher.start()
        event_left_button_pressed = 1
        event_other = 0
        x, y = 15, 20

        self.tracker.draw_point(event_other, x, y, {}, {})
        self.assertNotEqual(patched.call_count, 1)

        self.tracker.draw_point(event_left_button_pressed, x, y, {}, {})
        self.assertEqual(patched.call_count, 1)
        patched.assert_called_with(self.tracker.current_frame, (x, y), 5, (0, 255, 0), -1)

    def test_get_no_fish_for_ROI_createsRightRoi(self):
        with patch('config.roi_width', return_value=4), \
             patch('config.roi_first_height', return_value=2), \
             patch('config.roi_second_height', return_value=4):
            self.tracker.current_frame_fish_coord = [
                "1, 2", "3, 4", "5, 6"
            ]
            expected_x = [1, 3, 5, '']
            expected_y = [2, 4, 6, '']
            expected_roi = [0, 0, 0, 0, 0, 3]

            result = self.tracker.get_no_fish_for_ROI()

            self.assertEqual(expected_x, self.tracker.all_fish_x_coord)
            self.assertEqual(expected_y, self.tracker.all_fish_y_coord)
            self.assertEqual(expected_roi, result)


if __name__ == '__main__':
    unittest.main()

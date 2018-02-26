import unittest
import __builtin__
from mock import patch, mock_open
import MainProgram as tf


class TrackFishTests(unittest.TestCase):

    def is_not_string_TEST(self):
        self.assertTrue(tf.is_not_string(1))
        self.assertFalse(tf.is_not_string("String"))
        self.assertFalse(tf.is_not_string(""))

    # def write_to_output_file_TEST(self):
    #     open_ = mock_open()
    #     with patch.object(__builtin__, "open", open_):
    #         tf.write_to_output_file()
    #     mock_open.assert_called_once()
    #     mock_open.reset_mock()


if __name__ == '__main__':
    unittest.main()

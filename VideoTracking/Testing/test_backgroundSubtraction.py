import unittest

from backgroundSubtr import construct_argument_parser


class BackgroundSubtractionTest(unittest.TestCase):
    def construct_argument_parser(self):
        parser = construct_argument_parser()
        self.assertTrue(parser.long)


if __name__ == '__main__':
    unittest.main()

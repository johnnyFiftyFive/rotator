import unittest

import os
from scratchrotator import remove_oldest


class TestRotator(unittest.TestCase):
    FILES_COUNT = 2
    SURVIVORS = 5

    def setUp(self):
        for i in range(0, self.FILES_COUNT):
            with open('{0}.txt'.format(i), 'w') as f:
                f.write(i.__str__())

    def tearDown(self):
        files = os.listdir('.')
        for f in filter(lambda e: e.endswith('.txt'), files):
            os.remove(f)

    def test_remove_oldest(self):
        remove_oldest('.', self.SURVIVORS)
        files = os.listdir('.')
        for i in files[:self.SURVIVORS]:
            assert '{0}.txt'.format(i) not in files

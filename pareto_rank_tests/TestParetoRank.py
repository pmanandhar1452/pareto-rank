'''
MIT License

Copyright (c) 2020 Prakash Manandhar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pandas
import unittest
import os
from pareto_rank_algos import ParetoRank

class TestParetoRank(unittest.TestCase):
    """
        Tests for pareto_rank_algos.ParetoRank.
    """
    def test_2dminmin_000(self):
        TEMP_FOLDER = 'temp/'
        TEMP_OUT_PATH = TEMP_FOLDER + 'test_data_2d_out.csv'
        TEST_IN_PATH = 'pareto_rank_tests/test_data_2d_minmin000.csv'

        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)

        pr_obj = ParetoRank.ParetoRank(
            TEST_IN_PATH, TEMP_OUT_PATH, 'id', ['v0', 'v1'], [True, True])
        pr_obj.perform_ranking()
        data_out_test = pandas.read_csv(TEMP_OUT_PATH)
        data_out_refr = pandas.read_csv(TEST_IN_PATH)
        self.assertEqual(len(data_out_test), len(data_out_refr), 
            "Output number of rows don't match")
        for i in data_out_test['id'].values:
            row1 = data_out_test[data_out_test['id'] == i]
            row2 = data_out_refr[data_out_refr['id'] == i]
            self.assertEqual(row1['rank'].values[0], row2['manual_rank'].values[0])

if __name__ == '__main__':
    unittest.main()
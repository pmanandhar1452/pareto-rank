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

class ParetoRank:
    """
        Performs Pareto based ranking of given tradespace points.

        Args:
            input_file  (str): 
                path to file that contains the input data. A CSV 
                (comma separated value) file is expected.

            output_file (str): path to file to output data to (existing
                 data will be overwritten). The output file is a CSV file with
                 columnns: "id" and "rank"
            
            id_col (str): name of column containing the unqiue identifier. An 
                integer valued identifier is expected. Please note that column
                names sometimes need to contain spaces if the names are separated
                by spaces after comma in the CSV file.

            utility_cols (str array): array of column names for the utility 
                vector.Please note that column names sometimes need to contain 
                spaces if the names are separated by spaces after comma in the 
                CSV file.

            utility_minmax (bool array): array of True or False values in the same
                order as utility_cols that indicates whether this utility is to
                be minimized or maximmized.
    """
    def __init__(self, 
        input_file, output_file, \
        id_col, utility_cols, utility_min):
        
        self.input_file = input_file
        self.output_file = output_file

        self.id_col = id_col
        self.utility_cols = utility_cols
        self.utility_min = utility_min

    def perform_ranking(self):
        self.data = pandas.read_csv(
            self.input_file, usecols=[self.id_col] + self.utility_cols)
        ofp = open(self.output_file, 'w')
        ofp.write(f'{self.id_col},rank\n')
        ofp.close()

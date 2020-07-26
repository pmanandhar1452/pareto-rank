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

        self.dominates_map = dict()

    """
        returns whether the given id is dominated by the send id

        vector J1 dominates J2 iff 
            J1i <= J2i forall i, and 
            J1i < J2i for at least 1 i
    """
    def dominates(self, id1, id2):
        row1 = self.data[self.data[self.id_col] == id1]
        row2 = self.data[self.data[self.id_col] == id2]
        key = f'{id1}-{id2}'
        if key in self.dominates_map:
             dom = self.dominates_map[key]
        else:
            condition1 = True
            condition2 = False
            for col_i in range(len(self.utility_cols)):
                col_name = self.utility_cols[col_i]
                J1i = row1[col_name].values[0]
                J2i = row2[col_name].values[0]
                
                if J1i > J2i:
                    condition1 = False
                    break
                
                if J1i < J2i:
                    condition2 = True
        
            dom = condition1 and condition2
            self.dominates_map[key] = dom
        return dom

    """
        checks if a given row index is dominated any other datapoint
    """
    def is_dominated(self, i):
        dom = False
        rowi = self.data[self.data[self.id_col] == i]
        idi = rowi[self.id_col].values[0]
        print(f'is_dominated ({i}) with {len(self.data)} rows')
        for j in self.data[self.id_col].values:
            if i == j:
                continue
            rowj = self.data[self.data[self.id_col] == j]
            idj = rowj[self.id_col].values[0]
            if self.dominates(idj, idi):
                dom = True
                break
        return dom

    def perform_ranking(self):
        # load data
        self.data = pandas.read_csv(
            self.input_file, usecols=[self.id_col] + self.utility_cols)

        # if a given column is not to be minimized, invert the data
        for col_i in range(len(self.utility_cols)):
            if not self.utility_min[col_i]:
                self.data[self.utility_cols[col_i]] = -self.data[self.utility_cols[col_i]]
        
        self.data = self.data.sort_values(self.utility_cols, ascending=False)
        self.data_orig = self.data.copy()

        ofp = open(self.output_file, 'w')
        ofp.write(f'{self.id_col},rank\n')
        
        curr_rank = 1
        pareto_front = []
        while (len(self.data > 0)):
            print(f'Running pass {curr_rank}...')
            print(pareto_front)
            self.data = self.data_orig.copy()
            self.data = self.data[~self.data[self.id_col].isin(pareto_front)]
            for i in self.data[self.id_col].values:
                #print(f'Checking {self.id_col} == {i}...')
                if not (self.is_dominated(i)):
                    rowi = self.data[self.data[self.id_col] == i]
                    idi = rowi[self.id_col].values[0]
                    ofp.write(f'{idi}, {curr_rank}\n')
                    pareto_front.append(i)
                else:
                    self.data = self.data.drop(self.data[self.data[self.id_col]==i].index)
            curr_rank += 1
            print('\n')

        ofp.close()

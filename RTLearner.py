"""
Implementation RTLearner
Name: Nam Yoon Kim
GTID: nkim84
"""

import numpy as np

class RTLearner(object):

    def author(self):
        return 'nkim84'

    def __init__(self, leaf_size = 5, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        pass

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        dataY = np.vstack(dataY)
        data = np.concatenate((dataX, dataY), axis = 1)

        # build and save the model
        self.model = self.build_tree(data)

    def correlation(self, dataX, dataY):
        return np.correlate(dataX, dataY)

    def best_feature(self, dataX, dataY):
        colnum = dataX.shape[1]
        index = np.random.randint(colnum)
        return index

    def build_tree(self, data):
        dataX = data[:, 0:-1]
        dataY = data[:, -1]
        if (data.shape[0] <= self.leaf_size) or (np.all(dataY == dataY[0])):
            return np.array([['leaf', np.mean(dataY), np.nan, np.nan]], dtype = object)
        else:
            i = self.best_feature(dataX, dataY)
            random1 = np.random.randint(data.shape[0], dtype = int)
            random2 = np.random.randint(data.shape[0], dtype = int)
            SplitVal = (data[random1, i] + data[random2, i]) / 2
            if np.array_equal(data[data[:, i] <= SplitVal], data) == True:
                return np.array([['leaf', np.mean(dataY), np.nan, np.nan]], dtype = object)
            lefttree = self.build_tree(data[data[:, i] <= SplitVal])
            righttree = self.build_tree(data[data[:, i] > SplitVal])
            root = np.array([[i, SplitVal, 1, lefttree.shape[0] + 1]], dtype = object)
            return (np.concatenate((root, lefttree, righttree), axis = 0))

    def query(self, points):
        query_values = np.empty([points.shape[0], 1])
        for counter, value in enumerate(points):
            index = 0
            factor = self.model[index, 0]
            while(factor != 'leaf'):
                if (value[factor] <= self.model[index, 1]):
                    index += 1
                else:
                    index += self.model[index, 3]
                factor = self.model[index, 0]
            query_values[counter, 0] = self.model[index, 1]
        return np.reshape(query_values, query_values.size)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
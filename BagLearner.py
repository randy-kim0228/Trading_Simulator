"""
Implementation BagLearner
Name: Nam Yoon Kim
GTID: nkim84
"""

import numpy as np
import RTLearner as rt

class BagLearner(object):

    def author(self):
        return 'nkim84'

    def __init__(self, learner = rt.RTLearner, kwargs = {}, bags = 100, boost = False, verbose = False):
        self.learners = []
        self.kwargs = kwargs
        self.bags = bags
        for i in range(self.bags):
            self.learners.append(learner(**kwargs))
        self.boost = boost
        self.verbose = verbose
        pass

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        dataY = np.vstack(dataY)
        data = np.concatenate((dataX, dataY), axis = 1)

        # build and save the model
        nrows, ncols = data.shape[0], data.shape[1]
        dataBag = np.zeros(shape = (0, ncols))
        index = np.random.randint(nrows, size = nrows)
        for i in range(self.bags):
            dataBag = data[index, :]
            dataX = dataBag[:, 0:-1]
            dataY = dataBag[:, -1]
            self.learners[i].addEvidence(dataX, dataY)

    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        val_list = []
        for i in range(self.bags):
            val_list.append(self.learners[i].query(points))
        return np.mean(val_list, axis = 0)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
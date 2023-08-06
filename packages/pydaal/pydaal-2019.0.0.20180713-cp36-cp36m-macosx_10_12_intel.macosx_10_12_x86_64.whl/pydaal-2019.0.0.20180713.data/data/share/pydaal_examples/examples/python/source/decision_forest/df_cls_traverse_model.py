# file: df_cls_traverse_model.py
#===============================================================================
# Copyright 2014-2018 Intel Corporation.
#
# This software and the related documents are Intel copyrighted  materials,  and
# your use of  them is  governed by the  express license  under which  they were
# provided to you (License).  Unless the License provides otherwise, you may not
# use, modify, copy, publish, distribute,  disclose or transmit this software or
# the related documents without Intel's prior written permission.
#
# This software and the related documents  are provided as  is,  with no express
# or implied  warranties,  other  than those  that are  expressly stated  in the
# License.
#===============================================================================

#
# !  Content:
# !    Python example of decision forest classification model traversal.
# !
# !    The program trains the decision forest classification model on a training
# !    datasetFileName and prints the trained model by its depth-first traversing.
# !*****************************************************************************

#
## <a name = "DAAL-EXAMPLE-PY-DF_CLS_TRAVERSE_MODEL"></a>
## \example df_cls_traverse_model.py
#
from __future__ import print_function

from daal.algorithms import classifier
from daal.algorithms import decision_forest
import daal.algorithms.decision_forest.classification
import daal.algorithms.decision_forest.classification.training

from daal.data_management import (
    FileDataSource, HomogenNumericTable, MergedNumericTable, NumericTableIface, DataSourceIface, features
)

# Input data set parameters
trainDatasetFileName = "../data/batch/df_classification_train.csv"
categoricalFeaturesIndices = [2]
nFeatures = 3  # Number of features in training and testing data sets

# Decision forest parameters
nTrees = 2
minObservationsInLeafNode = 8
maxTreeDepth = 15

nClasses = 5  # Number of classes


def trainModel():

    # Create Numeric Tables for training data and dependent variables
    trainData, trainDependentVariable = loadData(trainDatasetFileName)

    # Create an algorithm object to train the decision forest classification model
    algorithm = decision_forest.classification.training.Batch(nClasses)

    # Pass a training data set and dependent values to the algorithm
    algorithm.input.set(classifier.training.data, trainData)
    algorithm.input.set(classifier.training.labels, trainDependentVariable)

    algorithm.parameter.nTrees = nTrees
    algorithm.parameter.featuresPerNode = nFeatures
    algorithm.parameter.minObservationsInLeafNode = minObservationsInLeafNode
    algorithm.parameter.maxTreeDepth = maxTreeDepth

    # Build the decision forest classification model and return the result
    return algorithm.compute()


def loadData(fileName):

    # Initialize FileDataSource<CSVFeatureManager> to retrieve the input data from a .csv file
    trainDataSource = FileDataSource(
        fileName, DataSourceIface.notAllocateNumericTable, DataSourceIface.doDictionaryFromContext
    )

    # Create Numeric Tables for training data and dependent variables
    data = HomogenNumericTable(nFeatures, 0, NumericTableIface.notAllocate)
    dependentVar = HomogenNumericTable(1, 0, NumericTableIface.notAllocate)
    mergedData = MergedNumericTable(data, dependentVar)

    # Retrieve the data from input file
    trainDataSource.loadDataBlock(mergedData)

    dictionary = data.getDictionary()
    for i in range(len(categoricalFeaturesIndices)):
        dictionary[categoricalFeaturesIndices[i]].featureType = features.DAAL_CATEGORICAL

    return data, dependentVar


# Visitor class implementing NodeVisitor interface, prints out tree nodes of the model when it is called back by model traversal method
class PrintNodeVisitor(classifier.TreeNodeVisitor):

    def __init__(self):
        super(PrintNodeVisitor, self).__init__()

    def onLeafNode(self, level, response):

        for i in range(level):
            print("  ", end='')
        print("Level {}, leaf node. Response value = {}".format(level, response))
        return True

    def onSplitNode(self, level, featureIndex, featureValue):

        for i in range(level):
            print("  ", end='')
        print("Level {}, split node. Feature index = {}, feature value = {:.6g}".format(level, featureIndex, featureValue))
        return True


def printModel(m):
    visitor = PrintNodeVisitor()
    print("Number of trees: {}".format(m.numberOfTrees()))
    for i in range(m.numberOfTrees()):
        print("Tree #{}".format(i))
        m.traverseDF(i, visitor)


if __name__ == "__main__":

    trainingResult = trainModel()
    printModel(trainingResult.get(classifier.training.model))

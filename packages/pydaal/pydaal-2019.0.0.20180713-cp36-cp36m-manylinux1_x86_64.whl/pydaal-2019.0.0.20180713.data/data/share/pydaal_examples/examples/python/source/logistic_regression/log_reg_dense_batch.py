# file: log_reg_dense_batch.py
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

## <a name="DAAL-EXAMPLE-PY-LOG_REG_DENSE_BATCH"></a>
## \example log_reg_dense_batch.py

import os
import sys

from daal.algorithms import logistic_regression
from daal.algorithms.logistic_regression import prediction, training
from daal.algorithms import classifier
from daal.data_management import (
    FileDataSource, DataSourceIface, NumericTableIface, HomogenNumericTable,
    MergedNumericTable, features
)

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable, printNumericTables

DAAL_PREFIX = os.path.join('..', 'data')

# Input data set parameters
trainDatasetFileName = os.path.join(DAAL_PREFIX, 'batch', 'logreg_train.csv')
testDatasetFileName = os.path.join(DAAL_PREFIX, 'batch', 'logreg_test.csv')

nFeatures = 6
nClasses = 5

# Model object for the logistic regression algorithm
model = None
predictionResult = None
testGroundTruth = None

def trainModel():
    global model

    # Initialize FileDataSource<CSVFeatureManager> to retrieve the input data from a .csv file
    trainDataSource = FileDataSource(
        trainDatasetFileName,
        DataSourceIface.notAllocateNumericTable,
        DataSourceIface.doDictionaryFromContext
    )

    # Create Numeric Tables for training data and labels
    trainData = HomogenNumericTable(nFeatures, 0, NumericTableIface.notAllocate)
    trainGroundTruth = HomogenNumericTable(1, 0, NumericTableIface.notAllocate)
    mergedData = MergedNumericTable(trainData, trainGroundTruth)

    # Retrieve the data from the input file
    trainDataSource.loadDataBlock(mergedData)

    # Create an algorithm object to train the logistic regression model
    algorithm = training.Batch(nClasses)

    # Pass the training data set and dependent values to the algorithm
    algorithm.input.set(classifier.training.data, trainData)
    algorithm.input.set(classifier.training.labels, trainGroundTruth)
    algorithm.parameter().penaltyL1=0.1;
    algorithm.parameter().penaltyL2=0.1;

    # Train the logistic regression model and retrieve the results of the training algorithm
    trainingResult = algorithm.compute()
    model = trainingResult.get(classifier.training.model)
    printNumericTable(model.getBeta(), "Logistic Regression coefficients:")

def testModel():
    global testGroundTruth, predictionResult

    # Initialize FileDataSource<CSVFeatureManager> to retrieve the test data from a .csv file
    testDataSource = FileDataSource(
        testDatasetFileName,
        DataSourceIface.notAllocateNumericTable,
        DataSourceIface.doDictionaryFromContext
    )

    # Create Numeric Tables for testing data and labels
    testData = HomogenNumericTable(nFeatures, 0, NumericTableIface.notAllocate)
    testGroundTruth = HomogenNumericTable(1, 0, NumericTableIface.notAllocate)
    mergedData = MergedNumericTable(testData, testGroundTruth)

    # Retrieve the data from input file
    testDataSource.loadDataBlock(mergedData)

    # Create algorithm objects for logistic regression prediction with the default method
    algorithm = prediction.Batch(nClasses)

    # Pass the testing data set and trained model to the algorithm
    algorithm.input.setTable(classifier.prediction.data,  testData)
    algorithm.input.setModel(classifier.prediction.model, model)
    algorithm.parameter().resultsToCompute |= logistic_regression.prediction.computeClassesProbabilities | logistic_regression.prediction.computeClassesLogProbabilities

    # Compute prediction results and retrieve algorithm results
    # (Result class from classifier.prediction)
    predictionResult = algorithm.compute()


def printResults():

    printNumericTable(predictionResult.get(classifier.prediction.prediction),"Logistic regression prediction results (first 10 rows):",10)
    printNumericTable(testGroundTruth,"Ground truth (first 10 rows):",10)
    printNumericTable(predictionResult.get(logistic_regression.prediction.probabilities),"Logistic regression prediction probabilities (first 10 rows):",10)
    printNumericTable(predictionResult.get(logistic_regression.prediction.logProbabilities),"Logistic regression prediction log probabilities (first 10 rows):",10)

if __name__ == "__main__":
    trainModel()
    testModel()
    printResults()

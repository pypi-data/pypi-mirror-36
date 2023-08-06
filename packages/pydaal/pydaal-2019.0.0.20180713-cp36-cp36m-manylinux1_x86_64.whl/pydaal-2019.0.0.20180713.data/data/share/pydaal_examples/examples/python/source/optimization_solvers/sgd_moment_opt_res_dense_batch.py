# file: sgd_moment_opt_res_dense_batch.py
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
# !    Python example of the SGD algorithm
# !*****************************************************************************

#
## <a name="DAAL-EXAMPLE-PY-SGD_MOMENT_OPT_RES_DENSE_BATCH"></a>
##  \example sgd_moment_opt_res_dense_batch.py
#

import os
import sys

import numpy as np

import daal.algorithms.optimization_solver as optimization_solver
import daal.algorithms.optimization_solver.mse
import daal.algorithms.optimization_solver.sgd
import daal.algorithms.optimization_solver.iterative_solver

from daal.data_management import (
    DataSourceIface, FileDataSource, HomogenNumericTable, MergedNumericTable, NumericTableIface
)

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable

datasetFileName = os.path.join('..', 'data', 'batch', 'mse.csv')

nFeatures = 3
accuracyThreshold = 0.0000001
halfNIterations = 200
nIterations = halfNIterations * 2
batchSize = 4
learningRate = 0.5

startPoint = np.array([[8], [2], [1], [4]], dtype=np.float64)

if __name__ == "__main__":

    # Initialize FileDataSource<CSVFeatureManager> to retrieve the input data from a .csv file
    dataSource = FileDataSource(datasetFileName,
                                DataSourceIface.notAllocateNumericTable,
                                DataSourceIface.doDictionaryFromContext)

    # Create Numeric Tables for data and values for dependent variable
    data = HomogenNumericTable(nFeatures, 0, NumericTableIface.doNotAllocate)
    dependentVariables = HomogenNumericTable(1, 0, NumericTableIface.doNotAllocate)
    mergedData = MergedNumericTable(data, dependentVariables)

    # Retrieve the data from the input file
    dataSource.loadDataBlock(mergedData)

    nVectors = data.getNumberOfRows()

    mseObjectiveFunction = optimization_solver.mse.Batch(nVectors)
    mseObjectiveFunction.input.set(optimization_solver.mse.data, data)
    mseObjectiveFunction.input.set(optimization_solver.mse.dependentVariables, dependentVariables)

    # Create objects to compute the SGD result using the default method
    sgdAlgorithm = optimization_solver.sgd.Batch(mseObjectiveFunction, method=optimization_solver.sgd.momentum)

    # Set input objects for the the SGD algorithm
    sgdAlgorithm.input.setInput(optimization_solver.iterative_solver.inputArgument, HomogenNumericTable(startPoint))
    sgdAlgorithm.parameter.learningRate = HomogenNumericTable(1, 1, NumericTableIface.doAllocate, learningRate)
    sgdAlgorithm.parameter.nIterations = halfNIterations
    sgdAlgorithm.parameter.accuracyThreshold = accuracyThreshold
    sgdAlgorithm.parameter.batchSize = batchSize
    sgdAlgorithm.parameter.optionalResultRequired = True

    # Compute the SGD result
    # Result class from daal.algorithms.optimization_solver.iterative_solver
    res = sgdAlgorithm.compute()

    # Print computed the SGD result
    printNumericTable(res.getResult(optimization_solver.iterative_solver.minimum), "Minimum after first compute():")
    printNumericTable(res.getResult(optimization_solver.iterative_solver.nIterations), "Number of iterations performed:")

    sgdAlgorithm.input.setInput(optimization_solver.iterative_solver.inputArgument, res.getResult(optimization_solver.iterative_solver.minimum))
    sgdAlgorithm.input.setInput(optimization_solver.iterative_solver.optionalArgument, res.getResult(optimization_solver.iterative_solver.optionalResult))

    res = sgdAlgorithm.compute()

    printNumericTable(res.getResult(optimization_solver.iterative_solver.minimum), "Minimum after second compute():")
    printNumericTable(res.getResult(optimization_solver.iterative_solver.nIterations), "Number of iterations performed:")

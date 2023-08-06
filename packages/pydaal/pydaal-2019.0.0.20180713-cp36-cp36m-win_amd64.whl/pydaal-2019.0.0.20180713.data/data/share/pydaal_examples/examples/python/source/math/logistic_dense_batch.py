# file: logistic_dense_batch.py
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
# !    Python example of Logistic algorithm.
# !
# !*****************************************************************************

#
## <a name="DAAL-EXAMPLE-PY-LOGISTIC_BATCH"></a>
## \example logistic_dense_batch.py
#

import os
import sys

import daal.algorithms.math.logistic as logistic
from daal.data_management import FileDataSource, DataSourceIface

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable

# Input data set parameters
datasetName = os.path.join('..', 'data', 'batch', 'covcormoments_dense.csv')

if __name__ == "__main__":

    # Retrieve the input data
    dataSource = FileDataSource(datasetName,
                                DataSourceIface.doAllocateNumericTable,
                                DataSourceIface.doDictionaryFromContext)
    dataSource.loadDataBlock()

    # Create an algorithm
    algorithm = logistic.Batch()

    # Set an input object for the algorithm
    algorithm.input.set(logistic.data, dataSource.getNumericTable())

    # Compute Logistic function
    res = algorithm.compute()

    # Print the results of the algorithm
    printNumericTable(res.get(logistic.value), "Logistic result (first 5 rows):", 5)

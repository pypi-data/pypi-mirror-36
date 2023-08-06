# file: cor_dense_batch.py
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

## <a name="DAAL-EXAMPLE-PY-CORRELATION_DENSE_BATCH"></a>
## \example cor_dense_batch.py

import os
import sys

from daal.algorithms import covariance
from daal.data_management import FileDataSource, DataSourceIface

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable

DAAL_PREFIX = os.path.join('..', 'data')

#  Input data set parameters
dataFileName = os.path.join(DAAL_PREFIX, 'batch', 'covcormoments_dense.csv')

if __name__ == "__main__":

    # Initialize FileDataSource to retrieve input data from .csv file
    dataSource = FileDataSource(
        dataFileName,
        DataSourceIface.doAllocateNumericTable,
        DataSourceIface.doDictionaryFromContext
    )

    # Retrieve the data from input file
    dataSource.loadDataBlock()

    # Create algorithm to compute dense correlation matrix in batch mode
    algorithm = covariance.Batch()

    # Set input arguments of the algorithm
    algorithm.input.set(covariance.data, dataSource.getNumericTable())

    # Set the parameter to choose the type of the output matrix
    algorithm.parameter.outputMatrixType = covariance.correlationMatrix

    # Get computed correlation matrix
    res = algorithm.compute()

    # Print values
    printNumericTable(res.get(covariance.correlation), "Correlation matrix:")
    printNumericTable(res.get(covariance.mean),        "Mean vector:")

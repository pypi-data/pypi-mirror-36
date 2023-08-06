# file: pca_cor_dense_online.py
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

## <a name="DAAL-EXAMPLE-PY-PCA_CORRELATION_DENSE_ONLINE"></a>
## \example pca_cor_dense_online.py

import os
import sys

import numpy as np

from daal.algorithms import pca
from daal.data_management import FileDataSource, DataSourceIface

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable

DAAL_PREFIX = os.path.join('..', 'data')

# Input data set parameters
nVectorsInBlock = 250
dataFileName = os.path.join(DAAL_PREFIX, 'online', 'pca_normalized.csv')

if __name__ == "__main__":

    # Initialize FileDataSource<CSVFeatureManager> to retrieve the input data from a .csv file
    dataSource = FileDataSource(
        dataFileName, DataSourceIface.doAllocateNumericTable,
        DataSourceIface.doDictionaryFromContext
    )

    # Create an algorithm for principal component analysis using the correlation method
    algorithm = pca.Online(fptype=np.float64)

    while(dataSource.loadDataBlock(nVectorsInBlock) == nVectorsInBlock):
        # Set the input data to the algorithm
        algorithm.input.setDataset(pca.data, dataSource.getNumericTable())

        # Update PCA decomposition
        algorithm.compute()

    result = algorithm.finalizeCompute()

    # Print the results
    printNumericTable(result.get(pca.eigenvalues), "Eigenvalues:")
    printNumericTable(result.get(pca.eigenvectors), "Eigenvectors:")

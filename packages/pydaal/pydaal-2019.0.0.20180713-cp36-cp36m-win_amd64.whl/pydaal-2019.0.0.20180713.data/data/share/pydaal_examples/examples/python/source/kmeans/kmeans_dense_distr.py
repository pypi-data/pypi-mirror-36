# file: kmeans_dense_distr.py
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

## <a name="DAAL-EXAMPLE-PY-KMEANS_DENSE_DISTRIBUTED"></a>
## \example kmeans_dense_distr.py

import os
import sys

import daal.algorithms.kmeans as kmeans
import daal.algorithms.kmeans.init as init
from daal import step1Local, step2Master
from daal.data_management import FileDataSource, DataSourceIface

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable

DAAL_PREFIX = os.path.join('..', 'data')

dataFileNames = [
    os.path.join(DAAL_PREFIX, 'distributed', 'kmeans_dense_1.csv'),
    os.path.join(DAAL_PREFIX, 'distributed', 'kmeans_dense_2.csv'),
    os.path.join(DAAL_PREFIX, 'distributed', 'kmeans_dense_3.csv'),
    os.path.join(DAAL_PREFIX, 'distributed', 'kmeans_dense_4.csv')
]

nClusters = 20
nIterations = 5
nBlocks = 4
nVectorsInBlock = 2500

dataTable = [0] * nBlocks

if __name__ == "__main__":

    masterAlgorithm = kmeans.Distributed(step2Master, nClusters, method=kmeans.lloydDense)

    centroids = None
    assignments = [0] * nBlocks

    masterInitAlgorithm = init.Distributed(step2Master, nClusters, method=init.randomDense)
    for i in range(nBlocks):
        # Initialize FileDataSource<CSVFeatureManager> to retrieve the input data from a .csv file
        dataSource = FileDataSource(
            dataFileNames[i], DataSourceIface.doAllocateNumericTable,
            DataSourceIface.doDictionaryFromContext
        )

        # Retrieve the data from the input file
        dataSource.loadDataBlock()

        dataTable[i] = dataSource.getNumericTable()

        # Create an algorithm object for the K-Means algorithm
        localInit = init.Distributed(step1Local, nClusters, nBlocks * nVectorsInBlock, i * nVectorsInBlock, method=init.randomDense)

        localInit.input.set(init.data, dataTable[i])
        res = localInit.compute()
        masterInitAlgorithm.input.add(init.partialResults, res)

    masterInitAlgorithm.compute()
    res = masterInitAlgorithm.finalizeCompute()
    centroids = res.get(init.centroids)

    for it in range(nIterations):
        for i in range(nBlocks):
            # Create an algorithm object for the K-Means algorithm
            localAlgorithm = kmeans.Distributed(step1Local, nClusters, it == nIterations, method=kmeans.lloydDense)

            # Set the input data to the algorithm
            localAlgorithm.input.set(kmeans.data,           dataTable[i])
            localAlgorithm.input.set(kmeans.inputCentroids, centroids)

            pres = localAlgorithm.compute()

            masterAlgorithm.input.add(kmeans.partialResults, pres)

        masterAlgorithm.compute()
        result = masterAlgorithm.finalizeCompute()

        centroids = result.get(kmeans.centroids)
        goalFunction = result.get(kmeans.goalFunction)

    for i in range(nBlocks):
        # Create an algorithm object for the K-Means algorithm
        localAlgorithm = kmeans.Batch(nClusters, 0, method=kmeans.lloydDense)

        # Set the input data to the algorithm
        localAlgorithm.input.set(kmeans.data,           dataTable[i])
        localAlgorithm.input.set(kmeans.inputCentroids, centroids)

        res = localAlgorithm.compute()

        assignments[i] = res.get(kmeans.assignments)

    # Print the clusterization results
    printNumericTable(assignments[0], "First 10 cluster assignments from 1st node:", 10)
    printNumericTable(centroids, "First 10 dimensions of centroids:", 20, 10)
    printNumericTable(goalFunction,   "Goal function value:")

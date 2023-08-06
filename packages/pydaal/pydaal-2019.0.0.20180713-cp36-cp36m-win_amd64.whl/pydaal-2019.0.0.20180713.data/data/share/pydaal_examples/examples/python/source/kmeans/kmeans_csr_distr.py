# file: kmeans_csr_distr.py
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

## <a name="DAAL-EXAMPLE-PY-KMEANS_CSR_DISTRIBUTED"></a>
## \example kmeans_csr_distr.py

import os
import sys

import daal.algorithms.kmeans as kmeans
import daal.algorithms.kmeans.init as init
from daal import step1Local, step2Master

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printNumericTable, createSparseTable

DAAL_PREFIX = os.path.join('..', 'data')

# K-Means algorithm parameters
nClusters = 20
nIterations = 5
nBlocks = 4
nVectorsInBlock = 8000

dataFileNames = [
    os.path.join(DAAL_PREFIX, 'batch', 'kmeans_csr.csv'),
    os.path.join(DAAL_PREFIX, 'batch', 'kmeans_csr.csv'),
    os.path.join(DAAL_PREFIX, 'batch', 'kmeans_csr.csv'),
    os.path.join(DAAL_PREFIX, 'batch', 'kmeans_csr.csv')
]

dataTable = [0] * nBlocks

if __name__ == "__main__":

    masterAlgorithm = kmeans.Distributed(step2Master, nClusters, method=kmeans.lloydCSR, )

    centroids = None
    assignments = [0] * nBlocks

    masterInitAlgorithm = init.Distributed(step2Master, nClusters, method=init.randomDense)

    for i in range(nBlocks):

        # Read dataFileNames and create a numeric table to store the input data
        dataTable[i] = createSparseTable(dataFileNames[i])

        # Create an algorithm object for the K-Means algorithm
        localInit = init.Distributed(step1Local, nClusters, nBlocks * nVectorsInBlock, i * nVectorsInBlock, method=init.randomDense)

        localInit.input.set(init.data, dataTable[i])
        # compute and add input for next
        masterInitAlgorithm.input.add(init.partialResults, localInit.compute())

    masterInitAlgorithm.compute()
    res = masterInitAlgorithm.finalizeCompute()
    centroids = res.get(init.centroids)

    for it in range(nIterations):
        for i in range(nBlocks):
            # Create an algorithm object for the K-Means algorithm
            localAlgorithm = kmeans.Distributed(step1Local, nClusters, it == nIterations, method=kmeans.lloydCSR)

            # Set the input data to the algorithm
            localAlgorithm.input.set(kmeans.data,           dataTable[i])
            localAlgorithm.input.set(kmeans.inputCentroids, centroids)

            pres = localAlgorithm.compute()

            masterAlgorithm.input.add(kmeans.partialResults, pres)

        masterAlgorithm.compute()
        result = masterAlgorithm.finalizeCompute()

        centroids = result.get(kmeans.centroids)
        objectiveFunction = result.get(kmeans.objectiveFunction)

    for i in range(nBlocks):
        # Create an algorithm object for the K-Means algorithm
        localAlgorithm = kmeans.Batch(nClusters, 0, method=kmeans.lloydCSR)

        # Set the input data to the algorithm
        localAlgorithm.input.set(kmeans.data,           dataTable[i])
        localAlgorithm.input.set(kmeans.inputCentroids, centroids)

        res = localAlgorithm.compute()

        assignments[i] = res.get(kmeans.assignments)

    # Print the clusterization results
    printNumericTable(assignments[0], "First 10 cluster assignments from 1st node:", 10)
    printNumericTable(centroids, "First 10 dimensions of centroids:", 20, 10)
    printNumericTable(objectiveFunction,   "Objective function value:")

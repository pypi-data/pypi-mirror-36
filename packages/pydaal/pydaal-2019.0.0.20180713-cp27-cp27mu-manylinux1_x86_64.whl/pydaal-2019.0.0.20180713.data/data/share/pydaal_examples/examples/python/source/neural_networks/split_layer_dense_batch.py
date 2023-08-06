# file: split_layer_dense_batch.py
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
# !    Python example of forward and backward split layer usage
# !
# !*****************************************************************************

#
## <a name="DAAL-EXAMPLE-PY-SPLIT_LAYER_BATCH"></a>
## \example split_layer_dense_batch.py
#

import os
import sys

from daal.algorithms.neural_networks import layers
from daal.algorithms.neural_networks.layers import split

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printTensor, readTensorFromCSV

# Input data set parameters
datasetName = os.path.join("..", "data", "batch", "layer.csv")
nOutputs = 3
nInputs = 3

if __name__ == "__main__":

    # Read datasetFileName from a file and create a tensor to store input data
    tensorData = readTensorFromCSV(datasetName)

    # Create an algorithm to compute forward split layer results using default method
    splitLayerForward = split.forward.Batch()

    # Set parameters for the forward split layer
    splitLayerForward.parameter.nOutputs = nOutputs
    splitLayerForward.parameter.nInputs = nInputs

    # Set input objects for the forward split layer
    splitLayerForward.input.setInput(layers.forward.data, tensorData)

    printTensor(tensorData, "Split layer input (first 5 rows):", 5)

    # Compute forward split layer results
    forwardResult = splitLayerForward.compute()

    # Print the results of the forward split layer
    for i in range(nOutputs):
        printTensor(forwardResult.getResultLayerData(split.forward.valueCollection, i),
                    "Forward split layer result (first 5 rows):", 5)

    # Create an algorithm to compute backward split layer results using default method
    splitLayerBackward = split.backward.Batch()

    # Set parameters for the backward split layer
    splitLayerBackward.parameter.nOutputs = nOutputs
    splitLayerBackward.parameter.nInputs = nInputs

    # Set input objects for the backward split layer
    splitLayerBackward.input.setInputLayerData(split.backward.inputGradientCollection,
                                               forwardResult.getResultLayerData(split.forward.valueCollection))

    # Compute backward split layer results
    backwardResult = splitLayerBackward.compute()

    # Print the results of the backward split layer
    printTensor(backwardResult.getResult(layers.backward.gradient), "Backward split layer result (first 5 rows):", 5)

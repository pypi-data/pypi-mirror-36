# file: stoch_pool2d_layer_dense_batch.py
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
# !    Python example of neural network forward and backward two-dimensional stochastic pooling layers usage
# !
# !*****************************************************************************

#
## <a name="DAAL-EXAMPLE-PY-STOCHASTIC_POOLING2D_LAYER_BATCH"></a>
## \example stoch_pool2d_layer_dense_batch.py
#

import os
import sys

from daal.algorithms.neural_networks import layers
from daal.algorithms.neural_networks.layers import stochastic_pooling2d

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printTensor, readTensorFromCSV

# Input non-negative data set name
datasetFileName = os.path.join("..", "data", "batch", "layer_non_negative.csv")

if __name__ == "__main__":

    # Read datasetFileName from a file and create a tensor to store input data
    data = readTensorFromCSV(datasetFileName)
    nDim = data.getNumberOfDimensions()
    printTensor(data, "Forward two-dimensional stochastic pooling layer input (first 10 rows):", 10)

    # Create an algorithm to compute forward two-dimensional stochastic pooling layer results using default method
    forwardLayer = stochastic_pooling2d.forward.Batch(nDim)
    forwardLayer.input.setInput(layers.forward.data, data)

    # Compute forward two-dimensional stochastic pooling layer results
    forwardLayer.compute()

    # Get the computed forward two-dimensional stochastic pooling layer results
    forwardResult = forwardLayer.getResult()

    printTensor(forwardResult.getResult(layers.forward.value), "Forward two-dimensional stochastic pooling layer result (first 5 rows):", 5)
    printTensor(forwardResult.getLayerData(layers.stochastic_pooling2d.auxSelectedIndices),
                "Forward two-dimensional stochastic pooling layer selected indices (first 10 rows):", 10)

    # Create an algorithm to compute backward two-dimensional stochastic pooling layer results using default method
    backwardLayer = layers.stochastic_pooling2d.backward.Batch(nDim)
    backwardLayer.input.setInput(layers.backward.inputGradient, forwardResult.getResult(layers.forward.value))
    backwardLayer.input.setInputLayerData(layers.backward.inputFromForward, forwardResult.getResultLayerData(layers.forward.resultForBackward))

    # Compute backward two-dimensional stochastic pooling layer results
    backwardLayer.compute()

    # Get the computed backward two-dimensional stochastic pooling layer results
    backwardResult = backwardLayer.getResult()

    printTensor(backwardResult.getResult(layers.backward.gradient),
                "Backward two-dimensional stochastic pooling layer result (first 10 rows):", 10)

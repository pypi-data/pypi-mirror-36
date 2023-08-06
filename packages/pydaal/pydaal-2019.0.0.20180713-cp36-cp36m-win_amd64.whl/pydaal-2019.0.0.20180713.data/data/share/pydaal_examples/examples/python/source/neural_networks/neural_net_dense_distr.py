# file: neural_net_dense_distr.py
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
# !    Python example of neural network training and scoring in the distributed processing mode
# !*****************************************************************************

#
## <a name="DAAL-EXAMPLE-PY-NEURAL_NET_DENSE_DISTR"></a>
## \example neural_net_dense_distr.py
#

import os
import sys

import numpy as np

from daal import step1Local, step2Master
from daal.algorithms.neural_networks import initializers
from daal.algorithms.neural_networks import layers
from daal.algorithms import optimization_solver
from daal.algorithms.neural_networks import prediction, training
from daal.data_management import NumericTable, HomogenNumericTable, readOnly, SubtensorDescriptor, HomogenTensor

utils_folder = os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if utils_folder not in sys.path:
    sys.path.insert(0, utils_folder)
from utils import printTensors, readTensorFromCSV

# Input data set parameters
trainDatasetFileNames = [
    os.path.join("..", "data", "distributed", "neural_network_train_dense_1.csv"),
    os.path.join("..", "data", "distributed", "neural_network_train_dense_2.csv"),
    os.path.join("..", "data", "distributed", "neural_network_train_dense_3.csv"),
    os.path.join("..", "data", "distributed", "neural_network_train_dense_4.csv")
]
trainGroundTruthFileNames = [
    os.path.join("..", "data", "distributed", "neural_network_train_ground_truth_1.csv"),
    os.path.join("..", "data", "distributed", "neural_network_train_ground_truth_2.csv"),
    os.path.join("..", "data", "distributed", "neural_network_train_ground_truth_3.csv"),
    os.path.join("..", "data", "distributed", "neural_network_train_ground_truth_4.csv")
]

testDatasetFile     = os.path.join("..", "data", "batch", "neural_network_test.csv")
testGroundTruthFile = os.path.join("..", "data", "batch", "neural_network_test_ground_truth.csv")

nNodes = 4
batchSize = 100
batchSizeLocal = int(batchSize / nNodes)


def configureNet():
    m2 = 40
    # Create layers of the neural network
    # Create fully-connected layer and initialize layer parameters
    fullyConnectedLayer1 = layers.fullyconnected.Batch(20)
    fullyConnectedLayer1.parameter.weightsInitializer = initializers.uniform.Batch(-0.001, 0.001)
    fullyConnectedLayer1.parameter.biasesInitializer = initializers.uniform.Batch(0, 0.5)

    # Create fully-connected layer and initialize layer parameters
    fullyConnectedLayer2 = layers.fullyconnected.Batch(m2)
    fullyConnectedLayer2.parameter.weightsInitializer = initializers.uniform.Batch(0.5, 1)
    fullyConnectedLayer2.parameter.biasesInitializer = initializers.uniform.Batch(0.5, 1)

    # Create fully-connected layer and initialize layer parameters
    fullyConnectedLayer3 = layers.fullyconnected.Batch(2)
    fullyConnectedLayer3.parameter.weightsInitializer = initializers.uniform.Batch(-0.005, 0.005)
    fullyConnectedLayer3.parameter.biasesInitializer = initializers.uniform.Batch(0, 1)

    # Create softmax layer and initialize layer parameters
    softmaxCrossEntropyLayer =  layers.loss.softmax_cross.Batch()

    # Create topology of the neural network
    topology = training.Topology()

    # Add layers to the topology of the neural network
    fc1 = topology.add(fullyConnectedLayer1)
    fc2 = topology.add(fullyConnectedLayer2)
    fc3 = topology.add(fullyConnectedLayer3)
    sm  = topology.add(softmaxCrossEntropyLayer)
    topology.get(fc1).addNext(fc2)
    topology.get(fc2).addNext(fc3)
    topology.get(fc3).addNext(sm)

    return topology


def getNextSubtensor(inputTensor, startPos, nElements):
    dims = inputTensor.getDimensions()
    dims[0] = nElements

    subtensorBlock = SubtensorDescriptor(ntype=np.float32)
    inputTensor.getSubtensor([], startPos, nElements, readOnly, subtensorBlock)
    subtensorData = np.array(subtensorBlock.getArray(), dtype=np.float32)
    inputTensor.releaseSubtensor(subtensorBlock)

    return HomogenTensor(subtensorData, ntype=np.float32)


def initializeNetwork():
    trainingData = [None] * nNodes
    trainingGroundTruth = [None] * nNodes
    # Read training data set from a .csv file and create tensors to store input data
    for node in range(nNodes):
        trainingData[node] = readTensorFromCSV(trainDatasetFileNames[node])
        trainingGroundTruth[node] = readTensorFromCSV(trainGroundTruthFileNames[node], True)

    sampleSize = trainingData[0].getDimensions()
    sampleSize[0] = batchSizeLocal

    # Create stochastic gradient descent (SGD) optimization solver algorithm
    sgdAlgorithm = optimization_solver.sgd.Batch(fptype=np.float32)
    sgdAlgorithm.parameter.batchSize = batchSizeLocal

    # Configure the neural network
    topologyMaster = configureNet()
    net = training.Distributed(step2Master, sgdAlgorithm)
    net.parameter.batchSize = batchSizeLocal

    # Initialize the neural network on master node
    net.initialize(sampleSize, topologyMaster)

    topology = [None] * nNodes
    netLocal = [None] * nNodes
    for node in range(nNodes):
        # Configure the neural network
        topology[node] = configureNet()

        # Pass a model from master node to the algorithms on local nodes
        trainingModel = training.Model()
        trainingModel.initialize_Float32(sampleSize, topology[node])

        netLocal[node] = training.Distributed(step1Local)
        netLocal[node].input.setStep1LocalInput(training.inputModel, trainingModel)

        # Set the batch size for the neural network training
        netLocal[node].parameter.batchSize = batchSizeLocal

    return (net, netLocal, trainingData, trainingGroundTruth)


def trainModel(net, netLocal, trainingData, trainingGroundTruth):
    # Create stochastic gradient descent (SGD) optimization solver algorithm
    sgdAlgorithm = optimization_solver.sgd.Batch(fptype=np.float32)

    # Set learning rate for the optimization solver used in the neural network
    learningRate = 0.001
    sgdAlgorithm.parameter.learningRateSequence = HomogenNumericTable(1, 1, NumericTable.doAllocate, learningRate)

    # Set the optimization solver for the neural network training
    net.parameter.optimizationSolver = sgdAlgorithm

    # Run the neural network training
    nSamples = trainingData[0].getDimensions()[0]
    for i in range(0, nSamples - batchSizeLocal + 1, batchSizeLocal):
        # Compute weights and biases for the batch of inputs on local nodes
        for node in range(nNodes):
            # Pass a training data set and dependent values to the algorithm
            netLocal[node].input.setInput(training.data, getNextSubtensor(trainingData[node], i, batchSizeLocal))
            netLocal[node].input.setInput(training.groundTruth, getNextSubtensor(trainingGroundTruth[node], i, batchSizeLocal))

            # Compute weights and biases on local node
            pres = netLocal[node].compute()

            # Pass computed weights and biases to the master algorithm
            net.input.add(training.partialResults, node, pres)

        # Update weights and biases on master node
        net.compute()
        wb = net.getPartialResult().get(training.resultFromMaster).get(training.model).getWeightsAndBiases()

        # Update weights and biases on local nodes
        for node in range(nNodes):
            netLocal[node].input.getStep1LocalInput(training.inputModel).setWeightsAndBiases(wb)

    # Finalize neural network training on the master node
    res = net.finalizeCompute()

    # Retrieve training and prediction models of the neural network
    return res.get(training.model).getPredictionModel_Float32()


def testModel(predictionModel):
    # Read testing data set from a .csv file and create a tensor to store input data
    predictionData = readTensorFromCSV(testDatasetFile)

    # Create an algorithm to compute the neural network predictions
    net = prediction.Batch()

    # Set the batch size for the neural network prediction
    net.parameter.batchSize = predictionData.getDimensionSize(0)

    # Set input objects for the prediction neural network
    net.input.setModelInput(prediction.model, predictionModel)
    net.input.setTensorInput(prediction.data, predictionData)

    # Run the neural network prediction and return result
    return net.compute()


def printResults(testGroundTruthFile, predictionResult):
    # Read testing ground truth from a .csv file and create a tensor to store the data
    predictionGroundTruth = readTensorFromCSV(testGroundTruthFile)

    printTensors(predictionGroundTruth, predictionResult.getResult(prediction.prediction),
                 "Ground truth", "Neural network predictions: each class probability",
                 "Neural network classification results (first 20 observations):", 20)


def main():
    init = initializeNetwork()
    predictionModel = trainModel(*init)
    predictionResult = testModel(predictionModel)
    printResults(testGroundTruthFile, predictionResult)


if __name__ == "__main__":
    main()

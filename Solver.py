# -*- coding: utf-8 -*-

""" AlexNet.
Applying 'Alexnet' to Oxford's 17 Category Flower Dataset classification task.
References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.
    - 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.
Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
    - [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
"""

from __future__ import division, print_function, absolute_import
import pictureslicernew

import tflearn
import numpy as np

from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

newData=True
numofpixels=200
while(numofpixels%4!=0):  #unfortunaly we can't cut pixels in half MUST BE divisble by 4 for my pictureslicer to work
     numofpixels+=1
  #temp=cut.cutter("donaldtrump.jpg", numofpixels)
  #temp.sliceup()
segmentsForTesting=None
segmentsForTraining=None
segmentsForTraining=pictureslicernew.newsegs(numofpixels, "training", True) #this is the size may or may not be a good starting point
segmentsForTesting=pictureslicernew.newsegs(numofpixels, "test", True)
if newData:
   segmentsForTraining.calculatesegments(100,"precalctraining")
   segmentsForTesting.calculatesegments(100,"precalctesting")
matrixsize=numofpixels/2
segmentsForTraining.gatherFiles("precalctraining")
segmentsForTesting.gatherFiles("precalctesting") 
arrayofconnections=[]
while len(segmentsForTraining.files)>0:
  arrayofconnections+=segmentsForTraining.getBatch()
while len(segmentsForTesting.files)>0:
  arrayofconnections+=segmentsForTesting.getBatch()

X=[np.asarray(i[0]) for i in arrayofconnections]# flattern for now will need to convert it to 2d. Just a starting point
Y=[i[1] for i in arrayofconnections]
X=np.asarray(X)
Y=np.asarray(Y)  
print (type(X))
print (type(Y))
print(X.shape)
print(Y.shape)
print (matrixsize)

# Building 'AlexNet'
network = input_data(shape=[None, matrixsize, matrixsize, 3])
network = conv_2d(network, 96, 11, strides=4, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = conv_2d(network, 256, 5, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = conv_2d(network, 384, 3, activation='relu')
network = conv_2d(network, 384, 3, activation='relu')
network = conv_2d(network, 256, 3, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = fully_connected(network, 4096, activation='tanh')
network = dropout(network, 0.5)
network = fully_connected(network, 4096, activation='tanh')
network = dropout(network, 0.5)
network = fully_connected(network, 17, activation='softmax')
network = regression(network, optimizer='momentum',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

# Training
model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                    max_checkpoints=1, tensorboard_verbose=2)
model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
          show_metric=True, batch_size=64, snapshot_step=200,
          snapshot_epoch=False, run_id='alexnet_oxflowers17')

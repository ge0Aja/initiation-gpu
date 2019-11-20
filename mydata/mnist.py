# -*- coding: utf-8 -*-
import os
import gzip

import numpy as np

from .download import maybe_download
from .download import get_data_dir

def _load_mnist_images(filename):
    # Read the inputs in Yann LeCun's binary format.
    with gzip.open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    # The inputs are vectors now, we reshape them to monochrome 2D images,
    # following the shape convention: [batch_size, image_width, image_height, channels]
    data = data.reshape(-1, 28, 28, 1)
    # The inputs come as bytes, we convert them to float32 in range [0,1].
    # (Actually to range [0, 255/256], for compatibility to the version
    # provided at http://deeplearning.net/data/mnist/mnist.pkl.gz.)
    return data / np.float32(256)

def _load_mnist_labels(filename):
    # Read the labels in Yann LeCun's binary format.
    with gzip.open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=8)
    # The labels are vectors of integers now, that's exactly what we want.
    return data

def load_mnist():
    """
    Return
        X [numpy array, (n_sample, 28, 28, 1)] : the image data
        y [numpy array, (n_sample)] : the labels
    """
    source_url = 'http://yann.lecun.com/exdb/mnist/'
    fname_train_images = 'train-images-idx3-ubyte.gz'
    fname_train_labels = 'train-labels-idx1-ubyte.gz'
    fname_test_images = 't10k-images-idx3-ubyte.gz'
    fname_test_labels = 't10k-labels-idx1-ubyte.gz'
    data_dir = get_data_dir()
    maybe_download(os.path.join(data_dir, fname_train_images), source_url+fname_train_images)
    maybe_download(os.path.join(data_dir, fname_train_labels), source_url+fname_train_labels)
    maybe_download(os.path.join(data_dir, fname_test_images), source_url+fname_test_images)
    maybe_download(os.path.join(data_dir, fname_test_labels), source_url+fname_test_labels)

    X_train = _load_mnist_images(os.path.join(data_dir, fname_train_images))
    y_train = _load_mnist_labels(os.path.join(data_dir, fname_train_labels))
    X_test = _load_mnist_images(os.path.join(data_dir, fname_test_images))
    y_test = _load_mnist_labels(os.path.join(data_dir, fname_test_labels))
    X = np.concatenate([X_train, X_test], axis=0)
    y = np.concatenate([y_train, y_test], axis=0)

    return X, y
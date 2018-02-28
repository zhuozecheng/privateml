import keras
import numpy as np
from pond.tensor import NativeTensor, PrivateEncodedTensor, PublicEncodedTensor
from pond.nn import Dense, Sigmoid, ReluExact, Reveal, Diff, Softmax, CrossEntropy, Sequential, DataLoader, Conv2D, AveragePooling2D, Flatten
from keras.utils import to_categorical

_ = np.seterr(over='raise')
_ = np.seterr(under='warn')
_ = np.seterr(invalid='raise')


# read data
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train[:,np.newaxis,:,:] / 255.0
x_test = x_test[:,np.newaxis,:,:] / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)


convnet_deep = Sequential([
    Conv2D((4, 4, 1, 20), strides=2, padding=1, filter_init=lambda shp: np.random.normal(scale=0.1, size=shp)),
    ReluExact(),
    AveragePooling2D(pool_size=(2,2)),
    Conv2D((3, 3, 20, 20), strides=2, padding=1, filter_init=lambda shp: np.random.normal(scale=0.1, size=shp)),
    ReluExact(),
    AveragePooling2D(pool_size=(2,2)),
    Flatten(),
    Dense(10, 80),
    Reveal(),
    Softmax()
])


convnet_deep.initialize()
convnet_deep.fit(
    x_train=DataLoader(x_train, wrapper=NativeTensor),
    y_train=DataLoader(y_train, wrapper=NativeTensor),
    x_valid=DataLoader(x_test, wrapper=NativeTensor),
    y_valid=DataLoader(y_test, wrapper=NativeTensor),
    loss=CrossEntropy(),
    epochs=3,
    batch_size=32,
    verbose=1,
)

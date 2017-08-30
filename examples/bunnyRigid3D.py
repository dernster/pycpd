from functools import partial
from scipy.io import loadmat
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pycpd import rigid_registration
import numpy as np
import time

def rotation_matrix(yaw, pitch, roll):
    X = np.array([[1, 0, 0],
                  [0, np.cos(yaw), - np.sin(yaw)],
                  [0, np.sin(yaw), np.cos(yaw)]])
    Y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                  [0, 1, 0],
                  [- np.sin(pitch), 0, np.cos(pitch)]])
    Z = np.array([[np.cos(roll), - np.sin(roll), 0],
                  [np.sin(roll), np.cos(roll), 0],
                  [0, 0, 1]])
    return Z.dot(Y).dot(X)

def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:,0],  X[:,1], X[:,2], color='red')
    ax.scatter(Y[:,0],  Y[:,1], Y[:,2], color='blue')
    plt.draw()
    print("iteration %d, error %.5f" % (iteration, error))
    plt.pause(0.001)

def main():
    fish = loadmat('./data/bunny.mat')

    R = rotation_matrix(np.pi / 2, np.pi / 4, np.pi / 18)
    # noinspection PyTypeChecker
    np.testing.assert_approx_equal(np.linalg.det(R), 1)
    T = np.array([1, 2, 3])

    X = fish['X']
    # Y = X + 1
    Y = X.dot(R)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    callback = partial(visualize, ax=ax)

    reg = rigid_registration(X, Y, maxIterations=1000)
    reg.register(callback)
    plt.show()


if __name__ == '__main__':
    main()

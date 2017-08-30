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

yaw = 0
pitch = 0
roll = 0
x = 0
y = 0
z = 0
rotation_offset = 0.05
traslation_offset = 0.005

fish = loadmat('./data/bunny.mat')
X = fish['X']

R = rotation_matrix(yaw, 0, 0)
Y = X.dot(R)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def redraw():
    global yaw, pitch, roll
    global X, Y
    global x, y ,z
    global plt, ax
    centroid = np.mean(X, axis=0)
    R = rotation_matrix(yaw, pitch, roll)
    T = np.array([x, y ,z])
    Y = (X - centroid).dot(R) + centroid + T
    plt.cla()
    ax.scatter(X[:,0],  X[:,1], X[:,2], color='red')
    ax.scatter(Y[:,0],  Y[:,1], Y[:,2], color='blue')
    plt.draw()

def manage_key_pressed(event):
    print(event.key)
    global yaw, roll, pitch
    global x, y, z
    global rotation_offset, traslation_offset
    if event.key == "i":
        x += traslation_offset
    elif event.key == "j":
        x -= traslation_offset
    elif event.key == "o":
        y += traslation_offset
    elif event.key == "k":
        y -= traslation_offset
    elif event.key == "p":
        z += traslation_offset
    elif event.key == "l":
        z -= traslation_offset
    if event.key == "I":
        yaw += rotation_offset
    elif event.key == "J":
        yaw -= rotation_offset
    elif event.key == "O":
        roll += rotation_offset
    elif event.key == "K":
        roll -= rotation_offset
    elif event.key == "P":
        pitch += rotation_offset
    elif event.key == "L":
        pitch -= rotation_offset
    redraw()

def main():
    # draw
    plt.cla()
    ax.scatter(X[:,0],  X[:,1], X[:,2], color='red')
    ax.scatter(Y[:,0],  Y[:,1], Y[:,2], color='blue')
    plt.draw()

    cid = plt.gcf().canvas.mpl_connect('key_press_event', manage_key_pressed)


    # callback = partial(visualize, ax=ax)
    # reg = rigid_registration(X, Y, maxIterations=1000)
    # reg.register(callback)

    plt.show()

if __name__ == '__main__':
    main()

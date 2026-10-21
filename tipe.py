
from PIL import Image
import numpy as np
from random import randint

def bottomUp(mat):
    bottom_up_mat = np.copy(mat)
    height, width = mat.shape
    for i in range(1, height):
        bottom_up_mat[i][0] = mat[i][0] + min(bottom_up_mat[i-1][0], bottom_up_mat[i-1][1])
        bottom_up_mat[i][width - 1] = mat[i][width - 1] + min(bottom_up_mat[i-1][width - 2], bottom_up_mat[i-1][width - 1])
        for j in range(1, width - 1):
            bottom_up_mat[i][j] = mat[i][j] + min([bottom_up_mat[i-1][j+k] for k in range(-1, 2)])

    return bottom_up_mat

def path(mat):
    bottom_up_mat = bottomUp(mat)
    height, width = mat.shape
    l = [min(range(width), key=lambda j: bottom_up_mat[height - 1][j])]
    for i in range(height - 2, -1, -1):
        j0 = l[-1]
        if j0 == 0:
            l.append(min(range(0, 2), key=lambda j: bottom_up_mat[i][j]))
        elif j0 == width - 1:
            l.append(min(range(width - 2, width - 1), key=lambda j: bottom_up_mat[i][j]))
        else:
            l.append(min(range(j0 - 1, j0 + 2), key=lambda j: bottom_up_mat[i][j]))
    return l[::-1]
    

"""mat = np.random.random((1000,1000))
print(mat)
print(path(mat))"""

img = Image.open("/home/lactua/Documents/image5.jpg")
size = img.size
color_mat = np.array(img)

kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
])

for i in range(100):

    print("Contouring..")

    l_mat = np.sum(color_mat, axis=2)/3

    grad = np.gradient(l_mat)
    contour_mat = grad[0]**2+grad[1]**2

    print(f"Finding path {i}..")

    points = path(contour_mat)

    print(points)

    print("Deleting path..")

    mask = np.ones(color_mat.shape[:2], dtype=bool)
    mask[np.arange(color_mat.shape[0]), points] = False
    color_mat = color_mat[mask].reshape(color_mat.shape[0], color_mat.shape[1] - 1, 3)

print("Done !")

img = Image.fromarray(color_mat.astype(np.uint8))
img.show()
import cv2
import numpy as np
import random

#A B R
circles = [(100, 100, 60), (150, 450, 35), (300, 100, 80), (200, 250, 50), (400, 400, 50)]
i = 0
points = []
accuracy = 1

for circle in circles:
    for alpha in np.linspace(0, np.pi * 2, 300):
        x = int(circle[0] + circle[2] * np.cos(alpha) + random.randrange(-accuracy, accuracy, 1))
        y = int(circle[1] + circle[2] * np.sin(alpha) + random.randrange(-accuracy, accuracy, 1))
        z = random.randint(20, 40)
        points.append((x, y))


class LidarImage():

    def __init__(self, matrix_shape, points = [ ], number_of_points = 1000, z_max = 100):
        self.points = points
        self.matrix_shape = matrix_shape

        # if not points:
        #     x_max = self.matrix_shape[0] - 1
        #     y_max = self.matrix_shape[1] - 1
        #     for i in range(0,number_of_points):
        #         x = random.randint(0, x_max)
        #         y = random.randint(0, y_max)
        #         z = random.randint(0, z_max)
        #         self.points.append((x,y,z))

    def LIDAR_to_raster(self, z_range = [ ]):
        self.z_range = z_range
        img = np.zeros(self.matrix_shape, np.uint8)
        if z_range:
            for point in self.points:
                img[point[0]][point[1]] = 255 if (point[2] > z_range[0] and point[2] < z_range[1]) else 0
        else:
            for point in self.points:
                img[point[0]][point[1]] = 255
        return img

# matrix_shape = (600,600)
#
# img = LidarImage(matrix_shape, points)
#
# img1 = img.LIDAR_to_raster()
# img2 = img.LIDAR_to_raster([50,100])
#
# cv2.line(img1, (50,50),(100,100),(100,100,100),5)
#
# cv2.imshow('img', img1)
# cv2.imwrite('img1.jpg',img1)
# cv2.imwrite('img2.jpg',img2)
# cv2.waitKey(0)
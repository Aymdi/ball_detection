import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *
import statistics

# img = cv2.imread("../data/log2/"+str(151)+"-rgb.png")
# img2 = cv2.imread("../data/log2/007-rgb.png")
# imgs = [img, img2]

imgslog1 = []

imgslog1.append(cv2.imread("../data/log1/362-rgb.png"))

# for i in range (1,10):
#     imgslog1.append(cv2.imread("../data/log1/00"+str(i)+"-rgb.png"))
# for i in range (10,100):
#     imgslog1.append(cv2.imread("../data/log1/0"+str(i)+"-rgb.png"))
# for i in range (100,375):
#     imgslog1.append(cv2.imread("../data/log1/"+str(i)+"-rgb.png"))


# imgslog2 = []

# for i in range (1,10):
#     imgslog2.append(cv2.imread("../data/log2/00"+str(i)+"-rgb.png"))
# for i in range (10,100):
#     imgslog2.append(cv2.imread("../data/log2/0"+str(i)+"-rgb.png"))
# for i in range (100,340):
#     imgslog2.append(cv2.imread("../data/log2/"+str(i)+"-rgb.png"))


# imgslog3 = []

# for i in range (1,10):
#     imgslog3.append(cv2.imread("../data/log3/00"+str(i)+"-rgb.png"))
# for i in range (10,100):
#     imgslog3.append(cv2.imread("../data/log3/0"+str(i)+"-rgb.png"))
# for i in range (100,265):
#     imgslog3.append(cv2.imread("../data/log3/"+str(i)+"-rgb.png"))

# imgslog4 = []

# for i in range (1,10):
#     imgslog4.append(cv2.imread("../data/log4/00"+str(i)+"-rgb.png"))
# for i in range (10,68):
#     imgslog4.append(cv2.imread("../data/log4/0"+str(i)+"-rgb.png"))

coords_center_algorithm = []
radius_algorithm     = []

coords_center = []
coords_radius = []
radius = []
verification_rates = [0.5]

def onclick_center(event):
    c_x = event.xdata
    c_y = event.ydata
    coords_center.append([c_x,c_y])
    # print (coords_center)
    plt.close()

def onclick_radius(event):
    c_x = event.xdata
    c_y = event.ydata
    coords_radius.append([c_x,c_y])
    # print (coords_radius)
    plt.close()

def in_circle(x, y, x_center, y_center, radius):
    if(sqrt((x_center-x)**2+(y_center-y)**2)<radius):
        return True
    else :
        return False

def compare_cercles(img, center1, radius1, center2, radius2):
    point_intersection = 0
    point_cercle1 = 0
    point_cercle2 = 0
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            if (in_circle(i,j,center1[0], center1[1], radius1)==True and in_circle(i,j,center2[0], center2[1], radius2)==True):
                point_intersection = point_intersection + 1
            elif (in_circle(i,j,center1[0], center1[1], radius1)==True and in_circle(i,j,center2[0], center2[1], radius2)==False):
                point_cercle1 = point_cercle1 + 1 
            elif (in_circle(i,j,center2[0], center2[1], radius2)==True and in_circle(i,j,center1[0], center1[1], radius1)==False):
                point_cercle2 = point_cercle2 + 1
    verification_rate = (point_intersection*2)/(point_intersection*2+point_cercle1+point_cercle2)
    return verification_rate


for i in range (len(imgslog1)) :
    fig = plt.figure()  
    imgplot = plt.imshow(imgslog1[i])
    fig.canvas.mpl_connect('button_press_event', onclick_center)
    plt.show() 
for i in range (len(imgslog1)) :
    fig = plt.figure()  
    imgplot = plt.imshow(imgslog1[i])
    fig.canvas.mpl_connect('button_press_event', onclick_radius)
    plt.show()
for i in range (len(imgslog1)) : 
    radius_calculated = sqrt((coords_center[i][0]-coords_radius[i][0])**2+(coords_center[i][1]-coords_radius[i][1])**2)
    radius.append(radius_calculated)
for i in range (len(imgslog1)) :
    verification_rates.append(compare_cercles(imgslog1[i], coords_center[i], radius[i], [516.25, 98.75], 81.75))
print(verification_rates)
print(statistics.mean(verification_rates))
plt.plot(verification_rates)
plt.show()

# associer image et click

# test
# 362 log1
# radius = 81.75
# center = [516.25, 98.75]
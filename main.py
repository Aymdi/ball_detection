import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

def display(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()

def display_gray(img):
    plt.imshow(img, cmap='gray')
    plt.show()


class model:
    def findBall(img):
        pass

class FirstModel(model):
    def findBall(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(img_hsv)
        seq = cv2.equalizeHist(s)
        hsv_new = cv2.merge([h,seq,v])
        gray = cv2.cvtColor(hsv_new, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 1.5)
        edges = cv2.Canny(blur,150,300)
        kernel = np.ones((3,3))
        dil = cv2.dilate(edges, kernel)
        circles = cv2.HoughCircles(dil, cv2.HOUGH_GRADIENT, 3, 10000, param1=100,param2=80)
        cv2.imshow(path, dil)
        return circles

class SecondModel(model):
    def findBall(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(img_hsv)
        seq = cv2.equalizeHist(s)
        
        h_blur = cv2.GaussianBlur(h, (11,11), 2)
        th, h_tresh = cv2.threshold(h_blur, 30, 1, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(h_tresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2:]
        L=[]
        for cnt in contours:
            x,y,width,height = cv2.boundingRect(cnt)
            L.append((x,y,width,height))
        lbound = sorted(L, key=lambda x: x[-2], reverse=True)[0]

        hsv_new = cv2.merge([h,seq,v])
        
        cropped_image = hsv_new[lbound[1] : lbound[1] + lbound[3], :]

        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        h_blur = cv2.GaussianBlur(gray, (7,7), 3)

        kernel = np.ones((3,3))

        edges = cv2.Canny(h_blur,130,200)
        dil = cv2.dilate(edges, kernel)
        circles = cv2.HoughCircles(dil, cv2.HOUGH_GRADIENT, 3, 10000, param1=1000,param2=90)
        if(circles is None):
            return [[None, None], 0]
        x, y, r = circles[0].reshape(3)
        return [[x, lbound[1] + y], r]

model1 = SecondModel()

path = "../data"
l1 = os.listdir(path + "/log1")

L=[]
for file in l1 :
    img = cv2.imread(path + "/log1/" + file)
    circles = model1.findBall(img)
    L.append(circles)


with open(r'centers.txt', 'w') as fp:
    fp.write("[")
    for v in L:
        # write each item on a new line
        fp.write("[")
        fp.write(str(v[0][0]))
        fp.write(", ")
        fp.write(str(v[0][1]))
        fp.write("],")
    fp.write("]")
    print('Done')

with open(r'radius.txt', 'w') as fp:
    fp.write("[")
    for v in L:
        # write each item on a new line
        fp.write(str(v[1]))
        fp.write(", ")
    fp.write("]")
    print('Done')


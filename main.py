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
        th, h_tresh = cv2.threshold(h_blur, 40, 1, cv2.THRESH_BINARY)


        contours, hierarchy = cv2.findContours(h_tresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2:]
        print(contours)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            im = cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow('img',im)
        cv2.waitKey(0)    


        kernel = np.ones((3,3))
        h_dil = cv2.dilate(h_tresh, kernel, iterations=2)
        h_er = 1 - cv2.erode(h_tresh, kernel, iterations=2)
        h_total = h_dil * h_er
        hsv_new = cv2.merge([h,seq,v])
        gray = cv2.cvtColor(hsv_new, cv2.COLOR_BGR2GRAY)
        h_blur = cv2.GaussianBlur(gray, (7,7), 4)
        edges = cv2.Canny(h_blur,130,100)
        cv2.imshow(path+"a", h_tresh*255)
        cv2.imshow(path+"b", h_total*255)
        dil = cv2.dilate(h_total * edges, kernel)
        circles = cv2.HoughCircles(dil, cv2.HOUGH_GRADIENT, 3, 10000, param1=1000,param2=90)
        cv2.imshow(path, dil)
        if(circles is None):
            return [[None, None], 0]
        x, y, r = circles[0].reshape(3)
        return [[x, y], r]

model1 = SecondModel()

path = "./ball_detection/images"
l1n1 = os.listdir(path + "/log1nv1")
l1n2 = os.listdir(path + "/log1nv2")
l1n3 = os.listdir(path + "/log1nv3")
l1n4 = os.listdir(path + "/log1nv4")

for file in l1n4 :
    img = cv2.imread(path + "/log1nv4/" + file)
    circles = model1.findBall(img)
    output = img.copy()
    if circles[0][0] is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        # loop over the (x, y) coordinates and radius of the circles
        x = int(circles[0][0])
        y = int(circles[0][1])
        r = int(circles[1])
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
    cv2.imshow(file, output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



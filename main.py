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
        circles = cv2.HoughCircles(dil, cv2.HOUGH_GRADIENT, 3, 10000, param1=1000,param2=70)
        if(circles is None):
            return [[None, None], 0]
        x, y, r = circles[0].reshape(3)
        return [[x, lbound[1] + y], r]

model1 = SecondModel()

path = "./ball_detection/images"
l1n1 = os.listdir(path + "/log1nv1")
l1n2 = os.listdir(path + "/log1nv2")
l1n3 = os.listdir(path + "/log1nv3")
l1n4 = os.listdir(path + "/log1nv4")

for file in l1n1 :
    img = cv2.imread(path + "/log1nv1/" + file)
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



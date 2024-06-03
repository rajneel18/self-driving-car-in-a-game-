import pyautogui as pygui
import numpy as np
import cv2
import win32api, win32con
import time

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def accelerate(hold_time):
    start = time.time()
    while time.time()- start <hold_time:
        pygui.keyDown('w')
    pygui.keyUp('w')

def turnLeft(hold_time):
    start = time.time()
    while time.time()- start <hold_time:
        pygui.keyDown('a')
    pygui.keyUp('a')


def turnRight(hold_time):
    start = time.time()
    while time.time()- start <hold_time:
        pygui.keyDown('d')
    pygui.keyUp('d')


click(542,393)
accelerate(0.8)
turnLeft(0.3)
turnRight(0.3)

def takeScreenshot():
    SS = pygui.screenshot("screen.png", region=(143,140,800,450))
    img = np.array(SS)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    return img


def canny(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray,(kernel,kernel),0)
    canny = cv2.Canny(blur,50,150)
    return canny

import numpy as np
import cv2

def roi(img):
    height = img.shape[0]
    width = img.shape[1]
    
    mask = np.zeros_like(img)
    triangle = np.array([[(0, height-2), (width // 2 - 40, height // 2 - 50), (width, height)]], dtype=np.int32)
    car_triangle = np.array([[(width * 1.0 / 4, height), (width // 2, height // 2), (width * 3.0 / 4, height)]], dtype=np.int32)
    cv2.fillPoly(mask, [triangle], 255)
    cv2.fillPoly(mask, [car_triangle], 0)
    masked_image = cv2.bitwise_and(img, mask)
    
    return masked_image



def houghLines(img):
    houghLines = cv2.HoughLinesP(img,2, np.pi/180, 100, np.array([]), minLineLength= 40, maxLineGap= 10 )
    return houghLines

def make_points(img, LineSI):
    slope, intercept = LineSI
    height = img.shape[0]
    y1 = int(height)
    y2 = int(y1*2.5/4)
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return [[x1, y1, x2, y2]]


def avg_slope_intercept(img,lines):
    left_fit = []
    right_fit = []
    for line in lines :
        for x1, y1, x2, y2 in line :
            fit= np.polyfit((x1,x2),(y1,y2),1)
            slope = fit[0]
            intercept = fit[1]

            if slope < 0:
                left_fit.append((slope,intercept))
            else:
                right_fit.append((slope,intercept))
    left_fit_avg=np.average(left_fit,axis=0)
    right_fit_avg=np.average(right_fit,axis=0)
    left_line = make_points(img,left_fit_avg)
    right_line = make_points(img,right_fit_avg)
    average_line = [left_line, right_line]
    return average_line

def display_lines_average(img,lines):
    line_image = np.zeros_like(img)
    if lines is not None :
        for line in lines :
            for x1, y1 , x2, y2 in line:
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),10)
    return img













# frame = takeScreenshot()
# canny_img = canny(frame)
# m_image = roi(canny_img)
# h_lines = houghLines(m_image)
# avg_lines = avg_slope_intercept(frame, h_lines)
# line_img = display_lines_average(frame, avg_lines)

# cv2.imshow("win",line_img)
# cv2.waitKey()
# cv2.destroyAllWindows




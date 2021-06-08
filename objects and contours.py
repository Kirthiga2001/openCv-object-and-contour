import cv2
import numpy as np

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def con(ic):
    c,h=cv2.findContours(ic,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for j in c:
        a=cv2.contourArea(j)
        print("area= ",a,end=", ")
        if a>500:
            cv2.drawContours(icon, j, -1, (0, 0, 0), 4)
            p=cv2.arcLength(j,True) #closed/not
            #print(p,end=" ")
            ap=cv2.approxPolyDP(j,0.02*p,True)
            print("no of corners",len(ap))
            x,y,w,h=cv2.boundingRect(ap)
            sh=len(ap)
            if sh==3:
                sn="Tri"
            elif sh==4:
                if w/float(h)>0.95 and w/float(h)<1.05:
                    sn="sq"
                else:
                    sn="rect"
            else:
                sn="cir"
            cv2.rectangle(icon,(x,y),(x+w,y+h),(255,0,0),3)
            cv2.putText(icon,sn,((x+w//2)-10,(y+h//2)-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

p='shapes.png'
i=cv2.imread(p)
icon=i.copy()

ig=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
ib=cv2.GaussianBlur(ig,(7,7),1)
ic=cv2.Canny(ib,50,50)
con(ic)
ist=stackImages(0.6,([i,ib,ig],[icon,ib,ic]))
cv2.imshow("ori",ist)

cv2.waitKey(0)
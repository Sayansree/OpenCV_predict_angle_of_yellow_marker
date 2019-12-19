import numpy as np
import cv2
import math



r2t=180/np.pi
t2r=np.pi/180
x=0
y=0
font=cv2.FONT_HERSHEY_PLAIN
fourcc=cv2.VideoWriter_fourcc('M','J','P','G')
e=False
t=False
s=False

def f(img):
    blur=cv2.GaussianBlur(img,(9,9),0)
    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    low=np.array([20,80,130])
    high=np.array([39,255,255])
    mask=cv2.inRange(hsv,low,high)
    edges=cv2.Canny(mask,75,150)
   

    lines=cv2.HoughLinesP(edges,1,np.pi/180,40,maxLineGap=30,minLineLength = 10)
    if lines is not None:
        thetas=[]
        x=0
        y=0
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x+=x1+x2
            y+=y1+y2
            if(x2-x1)==0:
                th=np.pi/2
            else:
                th=math.atan((y2-y1)/(x2-x1))*r2t
            thetas.append(th)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)
        M=max(thetas)
        m=min(thetas)
        x=int(.5*x/len(thetas))
        y=int(.5*y/len(thetas))
        if (M-m)>5:
            theta=round(180-(M-m),2)
            cv2.putText(img,"angle = "+str(theta),(x,y+5),font,2,(255,255,0),2,cv2.LINE_AA)
        else:
            cv2.putText(img,"unable to resolve",(x,y+5),font,2,(0,0,255),2,cv2.LINE_AA)
    #else:
        #cv2.putText(img,"unable to resolve",(x,y),font,1,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(img,"Sayansree Paria's Algorithm",(0,15),font,1,(0,255,0),1,cv2.LINE_AA)
    cv2.imshow("lines",img)
    if t:
        cv2.putText(mask,"Sayansree Paria's Algorithm",(0,15),font,1,200,1,cv2.LINE_AA)
        cv2.imshow("thresholding",mask)
        

    
    if e:
        cv2.putText(edges,"Sayansree Paria's Algorithm",(0,15),font,1,200,1,cv2.LINE_AA)
        cv2.imshow("edges detection",edges)
    
    





fram=5#int(input("enter frame rate"))
delay=1000//fram
#path=input("enter file path")
path="robosub_path-1.mp4"
cap=cv2.VideoCapture(path)
key=input("press s if u want to save the results")
print("during video press e to show edge detection and t for thresholding)
out=0
if key=="s":
    s=True
    out=cv2.VideoWriter("output.avi",fourcc,fram,(int(cap.get(3)),int(cap.get(4))))
while(cap.isOpened()):
    ret,img=cap.read()
    if ret:
        f(img)
        if s:
            out.write(img)
        key=cv2.waitKey(delay-15)&0xff
        if(key==27 or key==13):
            break
        elif key==ord('e'):
            e=True
        elif key==ord('t'):
            t=True
    else:
        break
cap.release()
if s:
    out.release()
cv2.destroyAllWindows()
quit()
    

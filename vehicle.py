import numpy as np
import cv2

#for turning on the camera
capture=cv2.VideoCapture('Traffic_video_1.mp4')

#count_line_position=500
min_width_rectangle=80
min_height_rectangle=80



#algo for counting the number of cars
#it subtracts the cars
#pip install opencv-contrib-python
algorithm=cv2.bgsegm.createBackgroundSubtractorMOG()

def centre_handler(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

count_line=550
detect=[]
offset=6 #teh scope of error 
counter=0 

 

while True:
    ret,frame1=capture.read()
    #CONVERT THE FRAME TO GREY IMAGE
    grey=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    #BLUR THE car
    blur=cv2.GaussianBlur(grey,(3,3),5)
    #applying on everry frame
    img_sub = algorithm.apply(blur)
    dilat= cv2.dilate (img_sub,np.ones((5,5)))
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilated= cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilated= cv2.morphologyEx(dilated,cv2.MORPH_CLOSE,kernel)
    counterShape,h = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1,(25,count_line),(1500,count_line),(255,0,0),3)

    #$
        #try code using iou 
    #$

    for i,c in enumerate(counterShape):
        (x,y,w,h) =cv2.boundingRect(c)
        validate_counter=(w>=min_width_rectangle) and (h>=min_height_rectangle)
        if not validate_counter:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        centre=centre_handler(x,y,w,h)
        detect.append(centre)
        cv2.circle(frame1,centre,4,(0,0,255),-1)

        for (x,y) in detect:
            if x<(count_line+offset) and y<(count_line+offset):
                counter+=1
                print("guu")
            cv2.line(frame1,(25,count_line),(1500,count_line),(0,127,255),3)
            detect.remove((x,y))
            print("Vehicle Counter:"+str(counter))
    
    cv2.putText(frame1,"Vehicle Counter:"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)

    #cv2.imshow("detected",dilated)
    cv2.imshow("Traffic",frame1)

    if cv2.waitKey(1)==13:
        break 

cv2.destroyAllWindows()
capture.release()

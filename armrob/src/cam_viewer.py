#! /usr/bin/env python

import cv2
import rospy
from armrob_util.msg import detectedMsgBool
import numpy as np

# opencv2 already has a trained algorithm for detecting humans called getDefaultPeopleDetector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())




CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5

cv2.startWindowThread()
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH,900)
cap.set(CV_CAP_PROP_FRAME_HEIGHT,600)
cap.set(CV_CAP_PROP_FPS,3.0)

print('\n\nPress ''q'' in the display window to quit.\n\n')



def main(): 
    #r = rospy.Rate(10)
    
    # =============================================================================
#   # Publisher for the detected commands. 
# =============================================================================
    pub_detected = rospy.Publisher('/detected',detectedMsgBool, queue_size=10)
#    detected_msg = detectedMsgBool()
    
    msgOut = detectedMsgBool.x
    #msgOut = False
    #pub_detected.publish(msgOut)
    rospy.init_node('talker', anonymous = True)
    
    while not rospy.is_shutdown() :
        # Capture frame-by-frame
        ret, frame = cap.read()

        msgOut = False
        pub_detected.publish(msgOut)
        #r.sleep()
        #rospy.spin()
        
    # resizes frame for better detection
    # frame = cv2.resize(frame, (160, 120)) #optimal frame size for minimal raspberry pi lag
        frame = cv2.resize(frame, (260, 195))  # minimum frame size for frame detection to still work
    
       # detects people in the image
    # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16))

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
    #    # Our operations on the frame come here
    #    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    #    # Display the resulting frame
    #    cv2.imshow('frame',gray)
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        break
        for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)    
            #if (np.size(abs(xB-xA)) >= 40) and (np.size(abs(yB-yA)) >= 40):
            msgOut = True
            print("detected")
            pub_detected.publish(msgOut)                
            # trigger publisher for boxes big enough

   
            
        # Display the resulting frame
        resizeFrame = cv2.resize(frame, (640, 480))  # makes the frame bigger again for human viewing.
        cv2.imshow('frame', resizeFrame)
    # to exit the code
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
  #      r.sleep
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    try: 
        main()
    except: 
        pass
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
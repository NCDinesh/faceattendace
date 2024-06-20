import cv2
import pickle
import face_recognition
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

file = open('faceattendace/FeatureFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown , studentIds = encodeListKnownWithIds
#print(studentIds)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),fx=0.25,fy=0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceInCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS,faceInCurrentFrame)

    for encodeFace, faceLocation in zip(encodeCurrentFrame , faceInCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print("matches",matches)
        #print("faceDist",faceDist)
        
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex] and faceDist[matchIndex]<=0.5:
            name = studentIds[matchIndex].upper()
            #print("Known Face")
            y1,x2,y2,x1 = faceLocation
            y1,x2,y2,x1 = y1*4 , x2*4 , y2*4 , x1*4  
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(img, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        elif faceDist[matchIndex]>0.5:
            #print("Unknown Face")
            name = "Unknown"
            y1,x2,y2,x1 = faceLocation
            y1,x2,y2,x1 = y1*4 , x2*4 , y2*4 , x1*4  
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(img, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow("Face Attendance",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
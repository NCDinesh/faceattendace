from django.shortcuts import render
from rest_framework import viewsets
from api.serializer import CourseSerializer
from api.models import Course
from django.http import StreamingHttpResponse
import cv2
import pickle
import face_recognition
import numpy as np

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Create your views here.
def index(request):
    return render(request, "index.html")

file = open('./FeatureFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

# Video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


def face_recognition_stream():
    global stop_streaming
    while True:
        if stop_streaming:
            break

        success, img = cap.read()
        if not success:
            break

        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceInCurrentFrame = face_recognition.face_locations(imgS)
        encodeCurrentFrame = face_recognition.face_encodings(imgS, faceInCurrentFrame)

        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceInCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDist)

            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            if matches[matchIndex] and faceDist[matchIndex] <= 0.5:
                name = studentIds[matchIndex].upper()
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            else:
                name = "Unknown"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()
    cv2.destroyAllWindows()

def index(request):
    return render(request, 'index.html')

def video_feed(request):
    global stop_streaming
    stop_streaming = False
    return StreamingHttpResponse(face_recognition_stream(),
                                content_type='multipart/x-mixed-replace; boundary=frame')

def stop_feed(request):
    global stop_streaming
    stop_streaming = True
    return StreamingHttpResponse("Camera stopped")
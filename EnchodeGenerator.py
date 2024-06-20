import cv2
import face_recognition
import pickle
import os 

folderPath = 'Project/Images'
pathList = os.listdir(folderPath)
print(pathList)

imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    print()
    print(path)
    print(os.path.splitext(path))
    print(os.path.splitext(path)[0])
    print()
    studentIds.append(os.path.splitext(path)[0])
print(len(imgList))
print(studentIds)
print()


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
print(encodeListKnown)
print("Encoding Complete")

encodeListKnownWithIds = [encodeListKnown , studentIds]

file = open("Project/FeatureFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File saved as FeatureFile.p")






from datetime import datetime
import cv2
import numpy as np
import face_recognition
import os

from collegegatepass import constants

def capture_img(userid):

    try:
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(constants.path + 'haarcascade_frontalface_default.xml')
        sampleNum = 0

        while (True):

            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # incrementing sample number
                sampleNum = sampleNum + 1

                imgloc=constants.dataset_path+"images/"+userid + '.' + str(sampleNum) + ".jpg"

                 # saving the captured face in the dataset folder

                cv2.imwrite(imgloc,gray[y:y + h, x:x + w])
                cv2.imshow('Frame', img)

            # wait for 100 miliseconds
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 10:
                break

        cam.release()
        cv2.destroyAllWindows()

    except Exception as e:
            print(e)
    return

def finduser():

    path = constants.dataset_path
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        Id = os.path.split(path+"/"+cl)[-1].split(".")[0]
        classNames.append(Id)
    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    print("images:",images, "type:",type(images))
    print("Classes:",classNames,"type:",type(classNames))
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:

        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            print(matches,matchIndex)
            if matches[matchIndex]:
                Id = classNames[matchIndex]

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(Id), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        # wait for 100 miliseconds
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
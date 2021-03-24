import numpy as np
import face_recognition
import cv2
import os
import database


path = 'imageAttendance'
my_list = os.listdir(path)
class_names = [os.path.splitext(cls)[0] for cls in my_list]
print(class_names)
print(my_list)


def student_images():
    images = []
    try:
        for cls in my_list:
            images.append(cv2.imread(f'{path}/{cls}'))
        print("Fetched all images!!!")
        return images
    except cv2.error as Error:
        print("Failed to fetch the image")
        return -1


def find_encoding(images):
    encode_list = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encode_list.append(encode)

    print("Encoding completed!!!")
    return encode_list


def recognize_face(images_encoded):
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        print(img)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        face_cur_frame = face_recognition.face_locations(imgS)
        encode_cur_frame = face_recognition.face_encodings(imgS)

        for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(images_encoded, encode_face)
            face_dis = face_recognition.face_distance(images_encoded, encode_face)

            match_index = np.argmin(face_dis)
            if matches[match_index]:
                name = class_names[match_index].upper()
                database.mark_attendance(name)
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1,y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x2+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('WebCam', img)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

        cap.release()
        cv2.destroyAllWindows()

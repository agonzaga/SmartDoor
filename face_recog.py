import cv2
import sys
import os
import numpy
import train_model


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    # just making a copy of image passed, so that passed image is not changed
    img_copy = colored_img.copy()

    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);

    # go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img_copy




def main():
    casc_type = os.path.abspath('./data/lbpcascade_frontalface.xml')
    # casc_type = os.path.abspath('./data/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(casc_type)


    # Training data
    folder_path = os.path.abspath('./training_sets')

    print("Preparing data...")
    faces, labels, names = train_model.prepare_training_data(face_cascade, folder_path)
    print("Data prepared")

    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    print(names)

    face_recog = train_model.recognizer(faces, labels)


    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        image = train_model.predict(face_cascade, frame, face_recog, names)

        if image is not None:
            cv2.imshow("Faces found", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

import cv2
import sys
import os
import numpy
import train_model
import argparse

parser = argparse.ArgumentParser(description='Facial recognition door unlocker.')
parser.add_argument('-t', '--train', action='store_true', help="Retrains the facial recognizer on the images in training_set.")

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


def getNamesMap(folder_path):
    dirs = os.listdir(folder_path)

    names = {}
    count = 0

    for dir in dirs:
        names[count] = dir
        count += 1

    return names


def main():
    args = parser.parse_args()
    casc_type = os.path.abspath('./data/lbpcascade_frontalface.xml')
    # casc_type = os.path.abspath('./data/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(casc_type)


    # Training data
    # face_recognizer = cv2.face.createLBPHFaceRecognizer()
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # or use EigenFaceRecognizer by replacing above line with
    # face_recognizer = cv2.face.createEigenFaceRecognizer()
    # face_recognizer = cv2.face.EigenFaceRecognizer_create()

    # or use FisherFaceRecognizer by replacing above line with
    # face_recog = cv2.face.createFisherFaceRecognizer()
    face_recog = cv2.face.FisherFaceRecognizer_create()
    folder_path = os.path.abspath('./training_sets')
    if args.train:
        print("Preparing data...")
        faces, labels, names = train_model.prepare_training_data(face_cascade, folder_path)
        print("Data prepared")

        # print total faces and labels
        print("Total faces: ", len(faces))
        print("Total labels: ", len(labels))
        print(names)

        face_recog = train_model.recognizer(faces, labels)
    else:
        face_recog.load('model.yaml')
        names = getNamesMap(folder_path)



    vid = cv2.VideoCapture(0)
    in_row_count = 0
    while True:
        ret, frame = vid.read()
        image, conf, name = train_model.predict(face_cascade, frame, face_recog, names)

        if image is not None:
            cv2.imshow("Faces found", image)

        if conf < 350:
            in_row_count += 1
        else:
            in_row_count = 0

        if in_row_count > 10:
            print("Unlocked user %s!" % name)
            in_row_count = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

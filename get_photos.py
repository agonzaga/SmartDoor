import cv2
import os
import sys
import time


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    # just making a copy of image passed, so that passed image is not changed
    img_copy = colored_img.copy()

    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);

    return len(faces)


def main(num=250):
    # casc_type = os.path.abspath('./data/lbpcascade_frontalface.xml')
    casc_type = os.path.abspath('./data/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(casc_type)


    # Training data
    folder_path = os.path.abspath('./training_sets')

    name = input("What is your name? ")
    name_path = folder_path + '/' + name

    if not os.path.exists(name_path):
        os.mkdir(name_path)


    vid = cv2.VideoCapture(0)
    time.sleep(2)
    count = 0
    while count < num:
        ret, frame = vid.read()
        num_faces = detect_faces(face_cascade, frame)

        if num_faces == 1:
            cv2.imwrite(name_path + '/' + name + str(count) + '.jpg', frame)
            cv2.imshow("Faces found", frame)
            count += 1


    vid.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

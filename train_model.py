import cv2
import os
import sys
import numpy


# function to detect face using OpenCV
def detect_face_trim(f_cascade, img):
    # convert the test image to gray scale as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale images(some images may be closer to camera than others)
    # result is a list of faces
    faces = f_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    # if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    # under the assumption that there will be only one face,
    # extract the face area
    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return gray[y:y + w, x:x + h], faces[0]


def prepare_training_data(folder_path):
    dirs = os.listdir(folder_path)

    faces = []
    labels = []

    casc_type = os.path.abspath('./data/lbpcascade_frontalface.xml')
    # casc_type = os.path.abspath('./data/haarcascade_frontalface_default.xml')

    face_cascade = cv2.CascadeClassifier(casc_type)

    for dir in dirs:
        label = dir
        subdir_path = folder_path + "/" + dir

        subdirs = os.listdir(subdir_path)

        for image in subdirs:
            # build image path
            # sample image path = training-data/s1/1.pgm
            image_path = subdir_path + "/" + image

            # read image
            img = cv2.imread(face_cascade, image_path)

            detect_face_trim(img)

            # display an image window to show the image
            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)

            # detect face
            face, rect = detect_face(image)

            if face is not None:
                faces.append(face)
                labels.append(label)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels



def main():
    folder_path = os.path.abspath('./training_sets')

    print("Preparing data...")
    faces, labels = prepare_training_data(folder_path)
    print("Data prepared")

    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

if __name__ == '__main__':
    main()
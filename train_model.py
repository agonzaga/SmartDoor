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


def prepare_training_data(face_cascade, folder_path):
    dirs = os.listdir(folder_path)

    faces = []
    labels = []


    for dir in dirs:
        label = dir
        subdir_path = folder_path + "/" + dir

        subdirs = os.listdir(subdir_path)

        for image in subdirs:
            # build image path
            # sample image path = training-data/s1/1.pgm
            image_path = subdir_path + "/" + image

            # read image
            img = cv2.imread(image_path)

            if img is None:
                continue

            # display an image window to show the image
            cv2.imshow("Training on image...", img)
            cv2.waitKey(100)

            # detect face
            face, rect = detect_face_trim(face_cascade, img)

            if face is not None:
                faces.append(face)
                # labels.append(label)
                labels.append(1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels


def recognizer(faces, labels):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # or use EigenFaceRecognizer by replacing above line with
    # face_recognizer = cv2.face.createEigenFaceRecognizer()

    # or use FisherFaceRecognizer by replacing above line with
    # face_recognizer = cv2.face.createFisherFaceRecognizer()
    print(labels)

    # train our face recognizer of our training faces
    face_recognizer.train(faces, numpy.array(labels))
    return face_recognizer


def predict(face_cascade, test_img, face_recognizer):
    # according to given (x, y) coordinates and
    # given width and heigh
    def draw_rectangle(img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # function to draw text on give image starting from
    # passed (x, y) coordinates.
    def draw_text(img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    # detect face from the image
    face, rect = detect_face_trim(face_cascade, img)

    # predict the image using our face recognizer
    if face is None:
        return img

    label = face_recognizer.predict(face)

    # draw a rectangle around face detected
    draw_rectangle(img, rect)
    # draw name of predicted person
    draw_text(img, str(label), rect[0], rect[1] - 5)

    return img


def main():
    folder_path = os.path.abspath('./training_sets')

    print("Preparing data...")
    faces, labels = prepare_training_data(folder_path)
    print("Data prepared")

    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    print(labels)

    face_recog = recognizer(faces, labels)
    #predict(test_img, face_recog)

if __name__ == '__main__':
    main()
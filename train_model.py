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
    faces = f_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5);

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
    names = {}

    count = 0

    for dir in dirs:
        label = dir
        subdir_path = folder_path + "/" + dir
        if label == ".DS_Store":
            continue

        subdirs = os.listdir(subdir_path)

        for image in subdirs:
            # build image path
            # sample image path = training-data/s1/1.pgm
            image_path = subdir_path + "/" + image

            # read image
            img = cv2.imread(image_path)

            if img is None:
                continue

            # detect face
            face, rect = detect_face_trim(face_cascade, img)
            # display an image window to show the image

            if face is not None:
                cv2.imshow("Training on image...", face)
                # print(image)
                cv2.waitKey(100)



            if face is not None:
                faces.append(cv2.resize(face, (280, 280)))
                labels.append(count)
                names[count] = label
        count += 1

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()


    return faces, labels, names


def recognizer(faces, labels):
    # face_recognizer = cv2.face.createLBPHFaceRecognizer()
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # or use EigenFaceRecognizer by replacing above line with
    # face_recognizer = cv2.face.createEigenFaceRecognizer()
    # face_recognizer = cv2.face.EigenFaceRecognizer_create()

    # or use FisherFaceRecognizer by replacing above line with
    face_recognizer = cv2.face.createFisherFaceRecognizer()

    print("Training...")

    # train our face recognizer of our training faces
    face_recognizer.train(faces, numpy.array(labels))
    face_recognizer.save("model.yaml")
    return face_recognizer


def predict(face_cascade, test_img, face_recognizer, name_map):
    # according to given (x, y) coordinates and
    # given width and height
    def draw_rectangle(img, rect, color):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    # function to draw text on give image starting from
    # passed (x, y) coordinates.
    def draw_text(img, text, x, y, color):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, color, 2)


    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    # detect face from the image
    face, rect = detect_face_trim(face_cascade, img)

    # predict the image using our face recognizer
    if face is None:
        return img, 1000, "Unknown"

    label, conf = face_recognizer.predict(cv2.resize(face, (280, 280)))
    color = (0, 255, 0) if int(conf) < 350 else (0, 0, 255)
    # draw a rectangle around face detected
    draw_rectangle(img, rect, color)
    # draw name of predicted person
    draw_text(img, name_map[label], rect[0], rect[1] - 5, color)

    return img, conf, name_map[label]


def main():
    folder_path = os.path.abspath('./training_sets')

    print("Preparing data...")
    trained_set = prepare_training_data(folder_path)
    print("Data prepared")

    for label, faces in trained_set.items():
        print('{0}: {1}'.format(label, len(faces)))

    face_recog = recognizer(faces, labels)
    #predict(test_img, face_recog)

if __name__ == '__main__':
    main()



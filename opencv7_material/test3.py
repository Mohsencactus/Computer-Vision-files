import cv2 as cv

while True:
    webcam.release()
    if cv.waitKey(1) == ord("q"):
        cv.destroyAllWindows()
        break
    
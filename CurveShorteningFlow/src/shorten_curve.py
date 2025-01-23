import sys
import os
import math
import cv2
import numpy as np
import geometry as geom
import CurveExtractor as ce
import CurveShortener as cs
import ImageSupport

# callback function returns True to terminate flow, False otherwise
def myCallBack(curve, curvature, iter, obj):
    print("iter=", iter, " curve arclength=", geom.get_curve_length(curve))
    color = ImageSupport.getSignalColor()
    if obj is not None:
        img = np.zeros((obj[0], obj[1]), np.uint8)
        ImageSupport.drawCurveLines(img, curve, color)
        cv2.floodFill(img, None, (0, 0), color)
        fillCurveInterior(img, 100)
        path = obj[2]
        cv2.imwrite(os.path.join(path, 'image' + (str(iter)).zfill(5) + '.png'), img)
        xmin = min([p[0] for p in curve])
        xmax = max([p[0] for p in curve])
        ymin = min([p[1] for p in curve])
        ymax = max([p[1] for p in curve])
        iterations = obj[3]
        # terminate flow if number of iterations is exhausted or curve size in horizontal and vertical directions is small
        if (iterations>0 and iter==iterations) or (max(xmax - xmin, ymax - ymin) < 10):
            print("Curve horiz size=", xmax-xmin, " vert size=", ymax - ymin)
            return True
        else:
            return False
    return True


def fillCurveInterior(img, color):
    rows, cols = img.shape
    for row in range(0,rows):
        for col in range(0, cols):
            if img[row,col] == 0:
                cv2.floodFill(img, None, (col, row), color)
                return

#
# reads image from png file and runs curve shortening flow for it
# at every iteration curve is saved in folder as png file.
# Then those images are used to create movie.
#
def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("python shorten_curve.py inputImagePath outputFolderPath [number_of_iterations]")
        return

    if not os.path.exists(args[0]):
        print("File '", args[0], "' doesn't exist!")
        return

    imagePath = args[0]

    # load original image
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    
    if not os.path.isdir(args[1]):
        print("Folder '", args[1], "' doesn't exist!")
        return

    image_folder = args[1]
    
    # number of iterations
    iterations = -1
    if len(args) >= 2: iterations = int(args[2])
    
    # perform median filtering with window 3x3
    median_img = cv2.medianBlur(img, 3)
    cv2.imwrite(imagePath.replace(".png", "_median.png"), median_img)
    
    # perform curve thinning
    thinned_img = cv2.ximgproc.thinning(median_img)
    cv2.imwrite(imagePath.replace(".png", "_thinned.png"), thinned_img)
    
    # extract curve from image
    signalColor = ImageSupport.getSignalColor()
    curveExtractor = ce.CurveExtractor()
    curve = curveExtractor.extract(thinned_img, signalColor)
    if len(curve) == 0:
        print("curveExtractor.extract returned empty curve")
        return

    rows, cols = img.shape
    curve_img = np.zeros((rows, cols), np.uint8)
    ImageSupport.drawCurvePoints(curve_img, curve, signalColor)
    cv2.imwrite(imagePath.replace(".png", "_extracted.png"), curve_img)

    # perform smoothing of extracted curve
    smoothed_curve = geom.smooth(curve, 3, 1, 100)

    flow = cs.CurveShortener()
    flow.setCallBack(myCallBack, (rows, cols, image_folder, iterations))
    flow.run(smoothed_curve)
   

if __name__ == "__main__":
    main()
import cv2

def getSignalColor():
    return 255

def getBackgroundColor():
    return 0

def drawCurvePoints(img, curve, value=getSignalColor()):
    rows,cols = img.shape
    for p in curve:
        x = int(p[0])
        y = int(p[1])
        if x >=0 and x < cols and y >=0 and y < rows:
            img[y,x] = value
                    
def drawCurveLines(img, curve, value=getSignalColor()):
    rows,cols = img.shape
    p1 = curve[0]
    for i in range(1,len(curve)):
        p2 = curve[i]
        cv2.line(img, (int(p1[0]),int(p1[1])), (int(p2[0]),int(p2[1])), value, 1)
        p1 = p2

def displayVectorField(img, curve, vectorField, color):
    N = len(curve)
    i = 0
    while i < N:
        p = curve[i]
        v = vectorField[i]
        cv2.line(img, (int(p[0]),int(p[1])), (int(p[0]-1000*v[0]),int(p[1]-1000*v[1])), color, 1)
        i += 5
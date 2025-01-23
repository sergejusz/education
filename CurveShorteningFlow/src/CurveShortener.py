import math
import cv2
import geometry as geom
import ImageSupport


class CurveShortener():
    
    def __init__(self):
        self.iter = 0
        self.callBack = None
        self.callBackObj = None
        self.maxIterations = None
        self.threshold = 50

    def setMaxIterations(self, iterations):
        self.maxIterations = iterations

    def setCallBack(self, callBackFcn, obj=None):
        self.callBack = callBackFcn
        self.callBackObj = obj
        
    def run(self, source_curve):
        curve = []
        curve.extend(source_curve)
        
        numSource = len(source_curve)
        lenSource = geom.get_curve_length(source_curve)
        
        iter = 0
        finished = False
        while not finished:
            smoothed_curve = geom.smooth(curve, 3, 1, 50)
            curvature = geom.get_curvature([p[0] for p in smoothed_curve], [p[1] for p in smoothed_curve])
            # user supplied callback function is called if set
            if self.callBack is not None:
                finished = self.callBack(smoothed_curve, curvature, iter, self.callBackObj)
            else:
                if self.maxIterations is not None:
                    finished = iter >= self.maxIterations
            normal_field = geom.get_normal_field([p[0] for p in smoothed_curve], [p[1] for p in smoothed_curve])
            normal_unit_field = geom.normalize(normal_field)
            curve = self.getNextCurve(smoothed_curve, normal_unit_field, curvature)
            iter += 1
            if not finished:
                numCurve = len(curve)
                lenCurve  = geom.get_curve_length(curve)
                # if arc length of current curve becomes shorter - perform decimation of curve points
                if (100.0*lenCurve)/lenSource < self.threshold:
                    curve = self.downsample(curve)
                    numSource = len(curve)
                    lenSource = geom.get_curve_length(curve)
                    print("Downsampled  to ", len(curve), " curveLength=", lenSource)

        print("iterations=", iter)


    def getNextCurve(self, curve, normal_field, curvature):
        next_curve = []
        kabs = max([math.fabs(k) for k in curvature])
        normalized_curvature = [k/kabs for k in curvature]
        for i in range(0, len(curve)):
            p = curve[i]
            n = normal_field[i]
            x = p[0] - normalized_curvature[i]*n[0]
            y = p[1] - normalized_curvature[i]*n[1]
            next_curve.append((x, y))
        return next_curve

    def downsample(self, curve):
        # primitive decimation procedure - remove all even point of curve
        decimated_curve = []
        for i in range(0, len(curve)):
            if i % 2 == 0:
                decimated_curve.append(curve[i])
        return decimated_curve
    

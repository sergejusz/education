import math
import numpy as np
from scipy import signal


def get_curvature(x, y):
    x_der1 = signal.savgol_filter(x, window_length=5, polyorder=3, deriv=1, mode="wrap")
    y_der1 = signal.savgol_filter(y, window_length=5, polyorder=3, deriv=1, mode="wrap")
    x_der2 = signal.savgol_filter(x, window_length=5, polyorder=3, deriv=2, mode="wrap")
    y_der2 = signal.savgol_filter(y, window_length=5, polyorder=3, deriv=2, mode="wrap")
    a = [y_der2[i]*x_der1[i]-x_der2[i]*y_der1[i] for i in range(0, len(x_der1))]
    b = [(math.hypot(x_der1[i], y_der1[i]))**3 for i in range(0, len(x_der1))]
    return [a[i]/b[i] for i in range(0, len(a))]
    
def get_tangent_field(x, y, w=3, porder=2):
    x_der1 = signal.savgol_filter(x, window_length=w, polyorder=porder, deriv=1, mode="wrap")
    y_der1 = signal.savgol_filter(y, window_length=w, polyorder=porder, deriv=1, mode="wrap")
    return [(x_der1[i],y_der1[i]) for i in range(0, len(x_der1))]

def get_normal_field(x, y, w=3, porder=2):
    x_der2 = signal.savgol_filter(x, window_length=w, polyorder=porder, deriv=2, mode="wrap")
    y_der2 = signal.savgol_filter(y, window_length=w, polyorder=porder, deriv=2, mode="wrap")
    return [(x_der2[i],y_der2[i]) for i in range(0, len(x_der2))]

def normalize(vectors):
    normalized = []
    for i in range(0, len(vectors)):
        v = vectors[i]
        l = math.hypot(v[0], v[1])
        if l > 0.0:
            f = 1.0/l
            normalized.append((v[0]*f, v[1]*f))
        else:
            normalized.append((0.0, 0.0))
    return normalized

def smooth(curve, w=3, p=2, iter=1):
    x = [p[0] for p in curve]
    y = [p[1] for p in curve]
    while iter > 0:
        x1 = signal.savgol_filter(x, window_length=w, polyorder=p, mode="wrap")
        y1 = signal.savgol_filter(y, window_length=w, polyorder=p, mode="wrap")
        iter -= 1
        if iter > 0:
            x.clear()
            x.extend(x1)
            y.clear()
            y.extend(y1)
            
    return [(x1[i], y1[i]) for i in range(0, len(curve))]

def translate(curve, p):
    x = [p[0] for p in curve]
    y = [p[1] for p in curve]
    return [(x[i] + p[0], y[i] + p[1]) for i in range(0, len(curve))]
    
def get_curve_length(curve):
    if len(curve) == 0: return 0.0
    l = 0
    p1 = curve[0]
    for i in range(1, len(curve)):
        p2 = curve[i]
        l += math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        p1 = p2
    return l
    
def get_mean_curvature(curve, curvature):
    if len(curve) == 0: return 0.0
    sumc = 0
    L = 0
    p1 = curve[0]
    for i in range(1, len(curve)):
        p2 = curve[i]
        ds = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        sumc += ds*curvature[i-1]
        L += ds
        p1 = p2
    return sumc/L

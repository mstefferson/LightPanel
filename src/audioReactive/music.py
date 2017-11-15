from __future__ import print_function
from __future__ import division
import time
import sys
import numpy as np
from numpy import *
from scipy.ndimage.filters import gaussian_filter1d
import config




class ExpFilter:
    """Simple exponential smoothing filter"""
    def __init__(self, val=0.0, alpha_decay=0.5, alpha_rise=0.5):
        """Small rise / decay factors = more smoothing"""
        self.alpha_decay = alpha_decay
        self.alpha_rise = alpha_rise
        self.value = val
    def update(self, value):
        if isinstance(self.value, (list, np.ndarray, tuple)):
            alpha = value - self.value
            alpha[alpha > 0.0] = self.alpha_rise
            alpha[alpha <= 0.0] = self.alpha_decay
        else:
            alpha = self.alpha_rise if value > self.value else self.alpha_decay
        self.value = alpha * value + (1.0 - alpha) * self.value
        return self.value
        
        
        

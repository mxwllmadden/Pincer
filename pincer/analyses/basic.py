# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:16:45 2024

@author: mbmad
"""

import pincer.analysis_base as ban
import pincer.analyses.utils as util
import statistics as sts
import numpy as np

class PeakMagnitude(ban.PincerAnalysis):
    def __init__(self,baseline = (), region : tuple= (), direction : int = -1, binning : int = 0):
        self.baseline = baseline
        self.regions = regions
        self.direction = direction
        self.binning = binning
    def run(self,abf):
        #Create Results Dict and working variables
        results = {}
        peaks = []
        
        #iterate across each sweep, baselining then finding the magnitude
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepY
            #baseline the trace
            util.baseline(trace, self.baseline)
        
class AreaUnderCurve(ban.PincerAnalysis):
    def __init__(self, baseline = (), region : tuple = (), binning : int = 0):
        
class SealTest(ban.PincerAnalysis):
    def __init__(self, baseline = (), stepregion : tuple = (), binning : int = 0)



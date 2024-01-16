# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:14:59 2024

@author: mbmad
"""

from pincer import ROI
import pincer.analysis_base as ban
import pincer.analyses.basic as base
import pincer.analyses.utils as util
import statistics as sts
import numpy as np

class CRACM_Current_LightPulse(ban.PincerAnalysis):
    def __init__(self, baseline, lightpulsespertrace = 3):
        self.baseline = baseline
        self.lightpulsespertrace =lightpulsespertrace
        self.an_apperlp = base.CountThresholdEvents(threshold = -20, direction = 1, binning = 0)
        self.an_auc = base.AreaUnderCurve(baseline=baseline,direction=1,binning=0)
    def run(self,abf):
        AUCResults = self.an_auc.run(abf)
        APLP = self.an_apperlp.run(abf)
        APLP = {k:(v/(abf.sweepNumber*self.lightpulsespertrace)) for k, v in APLP.items()}
        return AUCResults | APLP
    
class CRACM_
    
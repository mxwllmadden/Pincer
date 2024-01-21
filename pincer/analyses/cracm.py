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
    """
    CRACM Analysis: Used on Lightpulse Traces
    """
    def __init__(self, baseline, lightpulsespertrace = 3):
        """
        Lightpulse analysis for CRACM ephys protocols. Reports AUC and action
        potentials per lightpulse.

        Parameters
        ----------
        baseline : ROI
            ROI defining baseline region.
        lightpulsespertrace : TYPE, optional
            Number of lightpulses per sweep. Used for AP/LP calculation.
            The default is 3.

        Returns
        -------
        None.

        """
        self.baseline = baseline
        self.lightpulsespertrace =lightpulsespertrace
        self.an_apperlp = base.CountThresholdEvents(threshold = -20, direction = 1, binning = 0)
        self.an_auc = base.AreaUnderCurve(baseline=baseline,direction=1,binning=0)
    def run(self,abf):
        """
        Takes an abf file and finds AUC and APs/LP within the trace.

        Parameters
        ----------
        abf : PincerABF
            File to be analyzed.

        Returns
        -------
        results : dict
            Dictionary containing results values.

        """
        AUCResults = self.an_auc.run(abf)
        APLP = self.an_apperlp.run(abf)
        APLP = {k:(v/(abf.sweepNumber*self.lightpulsespertrace)) for k, v in APLP.items()}
        return AUCResults | APLP
    

    
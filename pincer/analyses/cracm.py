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
    def __init__(self, baseline, lightpulsespertrace = 3, stimregions : tuple[ROI] = None):
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
        self.an_apperlp = base.CountThresholdEvents(
            threshold = -20, 
            direction = 1, 
            binning = 0,
            binfnc=sum)
        self.an_auc = base.AreaUnderCurve(
            baseline=baseline,
            direction=1,
            binning=0)
        self.an_stimregion = []
        for stimreg in stimregions:
            self.an_stimregion.append(base.CountThresholdEvents(
                threshold = -20,
                direction = 1,
                binning = 0,
                binfnc = lambda arg : np.mean([int(bool(a)) for a in arg]),
                region = stimreg))
        self.an_stimregionburst = []
        for stimreg in stimregions:
            self.an_stimregionburst.append(base.CountThresholdEvents(
                threshold = -20,
                direction = 1,
                binning = 0,
                binfnc = lambda arg : np.mean([int(a >= 2) for a in arg]),
                region = stimreg))

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
        APLP = {k:(v/(abf.sweepCount*self.lightpulsespertrace)) for k, v in APLP.items()}
        
        APFidelity = []
        for stim_analysis in self.an_stimregion:
            APFidelity += list(stim_analysis.run(abf).values())
        APFidelityResults = {'AP Fidelity' : np.mean(APFidelity)}
        
        BurstFidelity = []
        for stim_analysis in self.an_stimregionburst:
            BurstFidelity += list(stim_analysis.run(abf).values())
        BurstFidelityResults = {'Burst Fidelity' : np.mean(BurstFidelity)}
        
            
        return AUCResults | APLP | APFidelityResults | BurstFidelityResults
    

    
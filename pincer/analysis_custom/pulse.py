# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:01:46 2024

@author: mbmad
"""
import pincer.analysis_base as ban
import statistics as sts
import numpy as np

class Peaks(ban.PincerAnalysis):    
    def __init__(self,baseline : tuple = (1,2000), ranges : list = [(2400,3000)]):
        """
        Find peak magnitude over specified regions with baselining

        Parameters
        ----------
        baseline : tuple, optional
            Region of trace to use as baseline. The default is (1,2000).
        ranges : list of tuples, optional
            Regions of trace to take magnitude. The default is [(2400,3000)].

        Returns
        -------
        None.

        """
        self.baseline = baseline
        self.ranges = ranges
        
    def run(self,abf):
        #Create results and define working variables
        results = {}
        rangemaxs = []
        
        #Iterate across each range
        for r in range(len(self.ranges)):
            for i in range(abf.sweepCount):
                #required to include
                abf.setSweep(i)
                trace = abf.sweepY
                
                #perform required calculations
                bl_trace, bl = ban.baseline(trace, self.baseline)
                
                #generate results
                results['Peak ' + str(r) + ' sweep ' + str(i)] = np.max(bl_trace[self.ranges[r][0]:self.ranges[r][1]])
        return results
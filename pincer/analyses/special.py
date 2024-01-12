# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:09:24 2024

@author: mbmad
"""

import pincer.analysis_base as ban
import pincer.analyses.utils as util
import statistics as sts
import numpy as np

class Current_Basic_Rheoramp(ban.PincerAnalysis):
    def __init__(self, apthreshold = -20, binning = 0):
        self.baseline = baseline
        self.apthreshold = apthreshold
    def run (self,abf):
        #Create results and define working variables
        results = {}
        apthresh = []
        apthresh_binned = []
        
        #iterate across each sweep
        for i in range(abf.sweepCount):
            #required to include
            abf.setSweep(i)
            trace = abf.sweepY
            
            #perform required calculations
            apindexs = ban.detectAP(trace)
            if len(apindexs) > 0:
                apindexs = list(apindexs)
                apindexs.sort()
                trunc_trace = trace[0:apindexs[0]+1]
                trunc_trace_jerk = np.gradient(np.gradient(trunc_trace))
                indx = int(np.argmax(trunc_trace_jerk))
                #calculate apthresh
                apthresh.append(int(trace[indx]))
            
            #handling binning of peaks
            apthresh = util.binning(apthresh, self.binning, sts.mean)
           
            #setup results dictionary and return
            results = {'AP Threshold '+str(i)+' (mV)':apthresh[i] for i in range(len(apthresh))}
            return results
        
class Current_Steps_MaxFiring(ban.PincerAnalysis):
    def __init__(self, stepregion, binning = 0):
        self.stepregion = stepregion
    def run(self, abf):
        #Create results and define working variables
        results = {}
        apcount = []
        
        #Convert all ROI to sample units
        hz = abf.sampleRate
        self.stepregion.samplcnv(hz)
        
        #Iterate across each sweep, filtering only the stepregion
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepY
            #filter the trace
            trace = self.stepregion.filt(trace)
            #Identify all action potentials
            aplist = util.detectEvents(trace,threshold = -10, minlength= (hz/1000))
            #produce final sweep results
            apcount = len(aplist)
        
        #bin values
        apcount = util.binning(apcount, self.binning, sts.mean)
        
        #create results dict
        results = {'Mean AP Count, Bin:'+str(i)+' (mV)':apcount[i] for i in range(len(apcount))}
        return results
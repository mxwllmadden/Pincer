# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:16:45 2024

@author: mbmad
"""

from pincer import ROI
import pincer.analysis_base as ban
import pincer.analyses.utils as util
import statistics as sts
import numpy as np

class PeakMagnitude(ban.PincerAnalysis):
    def __init__(self, region = None, baseline = None, direction : int = -1, binning : int = 0):
        assert type(region) == ROI or type(region) == type(None), 'region must be pincer.ROI'
        assert type(baseline) == type(None) or type(baseline) == ROI, 'baseline must be None or Pincer.ROI'
        assert direction == 1 or direction == -1, 'direction must be 1 or -1'
        assert type(binning) == int and binning >= 0, 'binning must be int equal or greater to zero'
        self.baseline = baseline
        self.region = region
        self.direction = direction
        self.binning = binning
        
    def run(self,abf):
        #Create Results Dict and working variables
        results = {}
        peaksbysweep = []
        peaksbinned = []
        
        #Convert all ROI to sample units
        hz = abf.sampleRate
        if self.baseline != None: self.baseline.samplcnv(hz)
        if self.region != None: self.region.samplcnv(hz)
        
        #iterate across each sweep, baselining then finding the magnitude
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepY
            #baseline the trace
            if self.baseline != None: trace, bl = util.baseline(trace, self.baseline)
            trace = trace * self.direction
            if self.region != None: trace = self.region.filt(trace)
            peaksbysweep.append(np.max(trace))
        
        #handling binning of peaks
        peaksbinned = util.binning(peaksbysweep, self.binning, sts.mean)
        
        #setup results dictionary and return
        results = {'Peak '+str(i)+' Magnitude':peaksbinned[i] for i in range(len(peaksbinned))}
        return results
        
class AreaUnderCurve(ban.PincerAnalysis):
    def __init__(self, region = None, baseline = None, direction : int = -1, binning : int = 0):
        assert type(region) == ROI or type(region) == type(None), 'region must be pincer.ROI'
        assert type(baseline) == type(None) or type(baseline) == ROI, 'baseline must be None or Pincer.ROI'
        assert direction == 1 or direction == -1, 'direction must be 1 or -1'
        assert type(binning) == int and binning >= 0, 'binning must be int equal or greater to zero'
        self.baseline = baseline
        self.region = region
        self.direction = direction
        self.binning = binning
        
    def run(self,abf):
        #Create Results Dict and working variables
        results = {}
        aucs = []
        
        #Convert all ROI to sample units
        hz = abf.sampleRate
        if self.baseline != None: self.baseline.samplcnv(hz)
        if self.region != None: self.region.samplcnv(hz)
        
        #iterate across each sweep, baselining then finding the magnitude
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepY
            #baseline the trace
            if self.baseline != None: trace, bl = util.baseline(trace, self.baseline)
            trace = trace * self.direction
            if self.region != None: trace = self.region.filt(trace)
            aucs.append(np.sum(trace))
        
        #handling binning of peaks
        aucs = util.binning(aucs, self.binning, sum)
        
        #convert units from sample*units to ms*units
        aucs = [i/(hz/1000) for i in aucs]
        
        #setup results dictionary and return
        results = {'Sum AUC '+str(i)+' ms*units':aucs[i] for i in range(len(aucs))}
        return results
    
class CountThresholdEvents(ban.PincerAnalysis):
    def __init__(self, region = None, baseline = None, threshold = 0, direction : int = -1, binning : int = 0, min_eventwidth_ms = 1):
        assert type(region) == ROI or type(region) == type(None), 'region must be pincer.ROI'
        assert type(baseline) == type(None) or type(baseline) == ROI, 'baseline must be None or Pincer.ROI'
        assert type(threshold) == int or type(threshold) == float, 'threshold must be int or float'
        assert type(binning) == int or binning >= 0, 'Binning must be int >= 0'
        self.baseline = baseline
        self.region = region
        self.direction = direction
        self.binning = binning
        self.threshold = threshold
        self.min_eventwidth_ms = min_eventwidth_ms
        
    def run(self,abf):
        #Create Results Dict and working variables
        results = {}
        peaksbysweep = []
        peaksbinned = []
        
        #Convert all ROI/time units to sample units
        hz = abf.sampleRate
        if self.baseline != None: self.baseline.samplcnv(hz)
        if self.region != None: self.region.samplcnv(hz)
        min_eventwidth = self.min_eventwidth_ms*(hz/1000)
        
        #iterate across each sweep, baselining then finding the magnitude
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepY
            #baseline the trace
            if self.baseline != None: trace, bl = util.baseline(trace, self.baseline)
            trace = trace * self.direction
            if self.region != None: trace = self.region.filt(trace)
            peaksbysweep.append(len(util.detectEvents(trace, threshold=self.threshold, minlength = min_eventwidth)))
        
        #handling binning of peaks
        peaksbinned = util.binning(peaksbysweep, self.binning, sum)
        
        #setup results dictionary and return
        results = {'Sum Events in Bin '+str(i):peaksbinned[i] for i in range(len(peaksbinned))}
        return results
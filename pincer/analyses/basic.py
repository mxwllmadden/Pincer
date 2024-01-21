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
    """
    Basic Analysis: Peak Magnitude
    """
    def __init__(self, region = None, baseline = None, direction : int = -1, binning : int = 0, binfnc = sts.mean):
        """
        Create a Peak Magnitude analysis according to parameters. Peak Magnitude
        finds the maximum value within a given region with optional baselining.

        Parameters
        ----------
        region : ROI, optional
            Pincer ROI defining the region to inspect. The default is None.
            If None, then the region is defined as the complete trace.
        baseline : ROI, optional
            Pincer ROI defining a baseline region. The default is None.
            If None, then no baselining is performed and raw values are reported.
        direction : int, optional
            Direction of peak, must be 1 or -1, indicating upwards or downwards
            peaks respectively. The default is -1.
        binning : int, optional
            Define a number of sweeps to average across. The default is 0.
            If binning is zero, then all sweeps will be placed in the same bin.
            Note that the binning function is sts.mean
        binfnc : func, optional
            Define the function to run across binned values. Default is sts.mean.
            Another commonly used function is sum.

        Returns
        -------
        None.

        """
        assert type(region) == ROI or type(region) == type(None), 'region must be pincer.ROI'
        assert type(baseline) == type(None) or type(baseline) == ROI, 'baseline must be None or Pincer.ROI'
        assert direction == 1 or direction == -1, 'direction must be 1 or -1'
        assert type(binning) == int and binning >= 0, 'binning must be int equal or greater to zero'
        self.baseline = util.confirmROI(baseline)
        self.region = util.confirmROI(region)
        self.direction = direction
        self.binning = binning
        self.binfnc = binfnc
    
    def run(self,abf):
        """
        Takes an abf file and finds the peak value in a specified region.

        Parameters
        ----------
        abf : PincerABF
            File to be analyzed.

        Returns
        -------
        results : dict
            Dictionary containing results values.

        """
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
        peaksbinned = util.binning(peaksbysweep, self.binning, self.binfnc)
        
        #setup results dictionary and return
        results = {'Peak '+str(i)+' Magnitude':peaksbinned[i] for i in range(len(peaksbinned))}
        return results
        
class AreaUnderCurve(ban.PincerAnalysis):
    """
    Basic Analysis: Area Under Curve
    """
    def __init__(self, region = None, baseline = None, direction : int = -1, binning : int = 0, binfnc = sts.mean):
        """
        Create an Area Under Curve analysis customized to parameters. AreaUnderCurve
        finds the area under the curve of a region of a trace, with optional
        baselining.

        Parameters
        ----------
        region : ROI, optional
            Pincer ROI defining the region to inspect. The default is None.
            If None, then the region is defined as the complete trace.
        baseline : ROI, optional
            Pincer ROI defining a baseline region. The default is None.
            If None, then no baselining is performed and raw values are reported.
        direction : int, optional
            Direction of activity, must be 1 or -1, indicating upwards or downwards
            AUC respectively. The default is -1.
        binning : int, optional
            Define a number of sweeps to average across. The default is 0.
            If binning is zero, then all sweeps will be placed in the same bin.
            Note that the binning function is sts.mean
        binfnc : func, optional
            Define the function to run across binned values. Default is sts.mean.
            Another commonly used function is sum.

        Returns
        -------
        None.

        """
        assert type(region) == ROI or type(region) == type(None), 'region must be pincer.ROI'
        assert type(baseline) == type(None) or type(baseline) == ROI, 'baseline must be None or Pincer.ROI'
        assert direction == 1 or direction == -1, 'direction must be 1 or -1'
        assert type(binning) == int and binning >= 0, 'binning must be int equal or greater to zero'
        self.baseline = util.confirmROI(baseline)
        self.region = util.confirmROI(region)
        self.direction = direction
        self.binning = binning
        self.binfnc = binfnc
        
    def run(self,abf):
        """
        Takes an abf file and finds the peak value in a specified region.

        Parameters
        ----------
        abf : PincerABF
            File to be analyzed.

        Returns
        -------
        results : dict
            Dictionary containing results values.

        """
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
        aucs = util.binning(aucs, self.binning, self.binfnc)
        
        #convert units from sample*units to ms*units
        aucs = [i/(hz/1000) for i in aucs]
        
        #setup results dictionary and return
        results = {'Sum AUC '+str(i)+' ms*units':aucs[i] for i in range(len(aucs))}
        return results
    
class CountThresholdEvents(ban.PincerAnalysis):
    """
    Basic Analysis: Count Events Over Threshold
    """
    def __init__(self, region = None, baseline = None, threshold = 0, direction : int = -1, binning : int = 0, binfnc = sts.mean, min_eventwidth_ms = 1):
        """
        Create CountThresholdEvents analysis according to specified parameters.
        This analysis searches for events that exceed a threshold value in a 
        specified direction. It ignores events that exceed the threshold for less
        than a specified minimum event width, this prevents excessive event labeling
        due to noise. This analysis has optional baselining and binning.

        Parameters
        ----------
        region : ROI, optional
            Pincer ROI defining the region to inspect for events. 
            The default is None. if None, then the region is the complete trace.
        baseline : TYPE, optional
            Pincer ROI defining a baseline region. The default is None.
            If None, then no baselining is performed.
        threshold : TYPE, optional
            Threshold value for events. The default is 0. Keep in mind that
            thresholding is applied AFTER baselining occurs if it is used.
        direction : int, optional
            Direction of activity, must be 1 or -1, indicating upwards or downwards
            AUC respectively. The default is -1.
        binning : int, optional
            Define a number of sweeps to average across. The default is 0.
            If binning is zero, then all sweeps will be placed in the same bin.
            Note that the binning function is sts.mean. The default is 0.
        binfnc : TYPE, optional
            Define the function to run across binned values. Default is sts.mean.
            Another commonly used function is sum.. The default is sts.mean.
        min_eventwidth_ms : TYPE, optional
            Minimum width of an event to be counted in milliseconds. 
            The default is 1.

        Returns
        -------
        None.

        """
        assert type(region) == ROI or type(region) == type(None), 'region must be pincer.ROI'
        assert type(baseline) == type(None) or type(baseline) == ROI, 'baseline must be None or Pincer.ROI'
        assert type(threshold) == int or type(threshold) == float, 'threshold must be int or float'
        assert type(binning) == int or binning >= 0, 'Binning must be int >= 0'
        self.baseline = util.confirmROI(baseline)
        self.region = util.confirmROI(region)
        self.direction = direction
        self.binning = binning
        self.threshold = threshold
        self.binfnc = binfnc
        self.min_eventwidth_ms = min_eventwidth_ms
        
    def run(self,abf):
        """
        Takes an abf file and finds the peak value in a specified region.

        Parameters
        ----------
        abf : PincerABF
            File to be analyzed.

        Returns
        -------
        results : dict
            Dictionary containing results values.

        """
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
        peaksbinned = util.binning(peaksbysweep, self.binning, self.binfnc)
        
        #setup results dictionary and return
        results = {'Sum Events in Bin '+str(i):peaksbinned[i] for i in range(len(peaksbinned))}
        return results
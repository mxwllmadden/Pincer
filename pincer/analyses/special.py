# -*- coding: utf-8 -*-
"""
Contains commonly used analyses that are not generalizable across many different
contexts. These analyses are usually not utilized by other analysis classes.
"""

import pincer.analysis_base as ban
import pincer.analyses.utils as util
import statistics as sts
import numpy as np
import scipy.optimize

class Current_Basic_Rheoramp(ban.PincerAnalysis):
    def __init__(self, apthreshold = -20, binning = 0):
        assert type(apthreshold) == float or type(apthreshold) == int, 'apthreshold must be int or float'
        assert type(binning) == int and binning >= 0, 'binning must be int >= 0'
        self.apthreshold = apthreshold
        self.binning = binning
    def run (self,abf):
        #Create results and define working variables
        results = {}
        apthresh = []
        
        #iterate across each sweep
        for i in range(abf.sweepCount):
            #required to include
            abf.setSweep(i)
            trace = abf.sweepY
            
            #perform required calculations
            apindexs = util.detectEvents(trace)
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
    
class Voltage_Step_CheckSeal(ban.PincerAnalysis):
    def __init__(self,baseline,region,stepsize_mV = 5,mode='curvefit', binning = 0):
        self.baseline = util.confirmROI(baseline)
        self.region = util.confirmROI(region)
        self.stepsize_mV = stepsize_mV
        self.mode = mode
        self.binning = binning
        self.binfnc = sts.mean
        assert type(stepsize_mV) == int, 'stepsize_mV must be int'
        
    def run(self, abf):
        #create results and define working variables
        results = {}
        l_cm = []
        l_rm = []
        l_ra = []
        l_hold = []
        l_rsqaure = []
        
        #convert all ROI to sample units
        hz = abf.sampleRate
        if self.baseline != None: self.baseline.samplcnv(hz)
        if self.region != None: self.baseline.samplcnv(hz)
        
        #Iterate across each sweep
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepY
            """
            This section of code below the fitted curve method for determining
            cell properties. It is largely based upon the information contained
            in this blog article 
            https://swharden.com/blog/2020-10-11-model-neuron-ltspice/
            """
            if self.mode == 'curvefit': 
                cm, rm, ra, hold, r2 = self._curvefit(trace, hz)
            l_cm.append(cm)
            l_rm.append(rm)
            l_ra.append(ra)
            l_hold.append(hold)
            l_rsqaure.append(r2)
        #binning
        l_cm = util.binning(l_cm, self.binning, self.binfnc)
        l_rm = util.binning(l_rm, self.binning, self.binfnc)
        l_ra = util.binning(l_ra, self.binning, self.binfnc)
        l_hold = util.binning(l_hold, self.binning, self.binfnc)
        l_rsqaure = util.binning(l_rsqaure, self.binning, self.binfnc)
        
        #setup results dictionary and return
        """NOT FINISHED ADD MORE HERE"""
                

    def _curvefit(self,trace, hz):
        #create an inner function to describe the exponential curve to be fit
        curve = lambda x, m, t: m * np.exp(-t*x)
        
        orig_trace = trace
        
        #filtering the trace should isolate a fittable curve
        trace = self.region.filt(trace) #Filter region
        trace = trace[np.argmax(trace):] #remove beginning rising phase
        
        #Baseline the trace to the last 20% of the step region.
        trace, Iss = util.baseline(trace, trace[-len(trace)//5:])
        #note that Iss will be useful later on. It is the steady state current
        #after the step is applied.
        
        #Filter to include only data between the 10%-80% ordinates, 
        #this removes potential distortion of the peak due to hardware filtering.
        thresh80 = np.max(trace)*0.8
        thresh10 = np.max(trace)*0.1
        index80 = np.argwhere(trace<=thresh80)[0][0]
        index10 = np.argwhere(trace<=thresh10)[0][0]
        
        trace = trace[index80:index10]
        
        #generate time values for the trace in sample units
        timefrompeak = np.arange(index80,index10)
        
        #Perform Fit
        param0 = (2000,0.1)
        params, cv = scipy.optimize.curve_fit(curve,timefrompeak,trace,param0)
        f_m, f_t = params
        tauSec = f_t / hz #convert tau from sample units to seconds
        
        #Determine quality of the fit
        squaredDiffs = np.square(trace - curve(timefrompeak,f_m,f_t))
        squaredDiffsFromMean = np.square(trace - np.mean(trace))
        rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
        
        #Calculate our baseline value
        bl = np.mean(self.baseline.filt(orig_trace))
        """
        Calculation of Ra.
        
        Ra can be determined from the peak transient current. We expect that the
        peak is distorted due to hardware filtering and we therefore use the 
        fitted curve to determine the peak value.
        """
        Id = curve(0,*params) #because we baselined the curve, we don't have to subtrace here.
        gO_Ra = self.stepsize_mV / Id
        mO_Ra = gO_Ra * 1000 #mV/pA = GOhm. Thus we multiply by 1000 to get MOhms
        
        """
        Calculation of Rm
        
        The steady state current during the step is limited by the sum of Rm and Ra. 
        Now that we know Ra, we can determine Rm by subtracting it out.
        
        Make sure to note units. gO_Ra is in gigaohms, which is more convenient here
        
        1 GOhm * 1 pA is a mV, which matches stepsize
        mV / pA is a gigaohm again, so we do the same conversion as we did for Ra
        """
        gO_Rm = (self.stepsize_mV - (mO_Ra * Iss)) / Iss
        mO_Rm = gO_Rm * 1000 #Convert Gigaohm to Megaohms
        
        """
        Calculation of Cm from Ra Rm and Tau.
        
        """
        effectiveR = 1/((1/gO_Ra) + (1/gO_Rm))
        pF_Cm = (tauSec / effectiveR)*1000 #conversion factor to get pF instead of kpF
        
        """
        Leak Correction.
        """
        correction = 1 + (mO_Ra/mO_Rm)
        mO_Ra = mO_Ra * correction
        mO_Rm = mO_Rm * correction
        pF_Cm = pF_Cm / (correction**2)
        
        return pF_Cm, mO_Rm, mO_Ra, bl, rSquared
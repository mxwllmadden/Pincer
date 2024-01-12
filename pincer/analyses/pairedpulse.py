# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 15:47:54 2024

@author: mbmad
"""

from pincer import ROI
import pincer.analysis_base as ban
import pincer.analyses.basic as base
import pincer.analyses.utils as util
import statistics as sts
import numpy as np

class PairedPulse(ban.PincerAnalysis):
    def __init__(self, baseline1, pulseregion1, pulseregion2, baseline2, sealtestregion, binsize = 1):
        self.an_pulse1 = base.PeakMagnitude(region=pulseregion1,baseline=baseline1,direction=-1,binning=1)
        self.an_pulse2 = base.PeakMagnitude(region=pulseregion2,baseline=baseline1,direction=-1,binning=1)
        self.an_seal = base.PeakMagnitude(region=sealtestregion,baseline=baseline2,direction=-1,binning=1)
        self.binning = binsize
    def run(self,abf):
        p1res = self.an_pulse1.run(abf)
        p2res = self.an_pulse2.run(abf)
        sealres = self.an_seal.run(abf)
        
        peak1 = list(p1res.values())
        peak2 = list(p2res.values())
        ppr = list(np.divide(np.array(peak2),np.array(peak1)))
        seal = list(sealres.values())
        
        #binning
        peak1 = util.binning(peak1, self.binning, sts.mean)
        ppr = util.binning(ppr, self.binning, sts.mean)
        seal = util.binning(seal, self.binning, sts.mean)
        
        #Results matricies
        r1 = {'First Peak Mag, Bin '+str(i) + ' (pA)':peak1[i] for i in range(len(peak1))}
        r2 = {'PPR, Bin '+str(i):ppr[i] for i in range(len(ppr))}
        r3 = {'SealTest, Bin '+str(i)+ ' (pA)':seal[i] for i in range(len(seal))}
        return r1 | r2 | r3
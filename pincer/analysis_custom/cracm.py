import pincer.analysis_base as ban
import numpy as np

class CurrentInducedAP(ban.PincerAnalysis):    
    def __init__(self,baseline : tuple = (1,2000)):
        """
        Define analysis for a current induced action potential.
        Assumes single action potential.

        Parameters
        ----------
        baseline : tuple, optional
            DESCRIPTION. The default is (1:2000).

        Returns
        -------
        None.

        """
        self.baseline = baseline
        
    def run(self,abf):
        #Create results and define working variables
        results = {}
        rmp = None
        appeak = None
        apheight = None
        apnumber = None
        
        #Iterate across each sweep
        for i in range(abf.sweepCount):
            abf.setSweep(i)
            trace = abf.sweepX
            apindexs = ban.detectAP(trace)
            trace = ban.baseline(trace, self.baseline)
            
        results['Resting Membrane Potential'] = rmp
        results['Action Potential Count'] = apnumber
        results['First Action Potential Peak'] = appeak
        results['First Action Potential Height'] = apheight
        results['Time of Day'] = abf.timeofday
        results['Time of Day (str)'] = abf.timeofday_str
        
        return results
        

class CRACM(ban.PincerAnalysis):
    pass
    
class Rheoramp(ban.PincerAnalysis):
    pass
    
class CheckSealStep(ban.PincerAnalysis):
    def __init__(self,baseline : tuple = (1,2000)):
        pass
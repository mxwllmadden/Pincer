import pincer.analysis_base as ban
import statistics as sts
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
        rmp = []
        appeak = []
        apheight = []
        apnumber = []
        
        #Iterate across each sweep
        for i in range(abf.sweepCount):
            #required to include
            abf.setSweep(i)
            trace = abf.sweepY
            
            #perform required calculations
            apindexs = ban.detectAP(trace)
            bl_trace, bl = ban.baseline(trace, self.baseline)
            
            #generate results
            rmp.append(float(bl))
            appeak.append(float(trace[apindexs[0]]))
            apheight.append(float(bl_trace[apindexs[0]]))
            apnumber.append(int(len(apindexs)))
            
        #compile dictionary to return to CellDex
        results['Resting Membrane Potential'] = sts.mean(rmp)
        results['Action Potential Count'] = sts.mean(apnumber)
        results['First Action Potential Peak'] = sts.mean(appeak)
        results['First Action Potential Height'] = sts.mean(apheight)
        return results
        

class CRACM(ban.PincerAnalysis):
    def __init__(self,baseline : tuple = (1,2000), pulsesPerTrace : int = 3):
        self.baseline = baseline
        self.pulsesPerTrace = pulsesPerTrace
        
    def run(self,abf):
        #Create results and define working variables
        results = {}
        apsPerLP = []
        auc = []
        #iterate across each sweep
        for i in range(abf.sweepCount):
            #required to include
            abf.setSweep(i)
            trace = abf.sweepY
            
            #perform required calculations
            apindexs = ban.detectAP(trace)
            bl_trace, bl = ban.baseline(trace,self.baseline)
            
            #generate results
            apsPerLP.append(len(apindexs))
            auc.append(float(np.trapz(bl_trace,dx = 1)))#URGENT I need to change dx to match the unit calculation (base off sampling rate)
        
        #compile dictionary to return to CellDex
        results['Action Potentials per Light Pulse'] = sts.mean(apsPerLP)/self.pulsesPerTrace
        results['Area Under the Curve UNITS'] = sts.mean(auc)
        return results
    
class Rheoramp(ban.PincerAnalysis):
    def __init__(self, baseline: tuple = (1,200), ramptimepoints = (800,8800), rampmaxcurr_pA = 25):
        self.baseline = baseline
        self.ramptimepoints = ramptimepoints
        self.rampmaxcurr_pA = rampmaxcurr_pA
    
    def run (self,abf):
        #Create results and define working variables
        results = {}
        rheobase = []
        apthresh = []
        rheobase = []
        
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
                #calculate rheobase and apthresh
                apthresh.append(int(trace[indx]))
                rheo = (indx-self.ramptimepoints[0]) * \
                    (self.rampmaxcurr_pA / (self.ramptimepoints[1] - \
                                            self.ramptimepoints[0]))
                rheobase.append(int(rheo))
            results['AP Threshold'] = sts.mean(apthresh)
            results['Rheobase (pA)'] = sts.mean(rheobase)
            return results                
    
class CheckSealStep(ban.PincerAnalysis):
    def __init__(self,baseline : tuple = (1,500)):
        pass
    
    def run(self, abf):
        # Create results and define working variables
        results = {}
        results['Time of Day'] = abf.timeofday
        results['Time of Day (str)'] = abf.timeofday_str
        return {}
        
        
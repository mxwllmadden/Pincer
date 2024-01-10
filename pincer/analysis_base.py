# -*- coding: utf-8 -*-
"""
Contains the analysis for each protocol, outputs can be suppressed if needed

"""
import numpy as np

class StatsManager():
    _registry = {}
    def __init__(self):
        pass
    
    def make(self,name,**kwargs):
        return self._registry[name](**kwargs)
    
    def report(self):
        print('Available Comparisons:')
        print('-------------------')
        for i in self._registry:
            print(i)

class AnalysisManager():
    _registry = {}
    def __init__(self):
        pass
    
    def make(self,name,**kwargs):
        return self._registry[name](**kwargs)
    
    def report(self):
        print('Available Analyses:')
        print('-------------------')
        for i in self._registry:
            print(i)
            
class PincerComparison():
    def __init_subclass__(cls,**kwargs):
        super().__init_subclass__(**kwargs)
        StatsManager._registry[cls.__name__] = cls
        
    def run(self, *series):
        print('Warning! Missing Run Method!')
        return {'ERROR1':1,'ERROR2':2}
    
class PincerAnalysis():
    def __init_subclass__(cls,**kwargs):
        super().__init_subclass__(**kwargs)
        AnalysisManager._registry[cls.__name__] = cls
        
    def run(self, ABF):
        print('Warning! Missing Run Method!')
        return {'ERROR1':1,'ERROR2':2}

class Template(PincerAnalysis):
    def __init__(self, **kwargs):
        pass
    
    def run(self, ABF):
        pass
    
def detectAP(sweep, threshold: int = -20):
    aps = []
    #detect every region where
    regions = reglabel(sweep>=threshold)
    apcount = np.amax(regions)
    for i in range(int(apcount)):
        #index of maximum value within region of interest
        apindex = np.argmax(sweep[regions==(i+1)])
        apindex = apindex + np.min(np.where(regions==(i+1)))
        aps.append(apindex)
    return tuple(aps)

def detectAPonset(sweep : np.ndarray, ap_index : int):
    onset_index = 1
    return onset_index

def baseline(sweep,baseline : tuple):
    """
    Simple utility function for baselining ephys traces.

    Parameters
    ----------
    sweep : numpy.ndarray
        1-Dimensional numpy array with numerical data to baseline.
    baseline : tuple
        Indexes at start and end of the baseline region.

    Returns
    -------
    sweep : numpy.ndarray
        Newly baselined 1-Dimensional numpy array with numerical data.
    base : int
        The average value of the baseline region in the original sweep.

    """
    assert isinstance(sweep, np.ndarray) and sweep.ndim == 1, 'sweep is not a 1-d numpy array'
    assert isinstance(baseline, tuple) and len(baseline) == 2, 'baseline is not a length 2 tuple'
    assert all([x<=len(sweep) and x >= 0 for x in baseline]), 'baseline indexes not contained in sweep'
    assert baseline[0] <= baseline[1], 'baseline indexes in incorrect order'
    base = np.average(sweep[baseline[0]:baseline[1]])
    sweep = np.subtract(sweep, base)
    return sweep, int(base)

def reglabel(sweep):
    """
    

    Parameters
    ----------
    sweep : TYPE
        DESCRIPTION.

    Returns
    -------
    sweepout : TYPE
        DESCRIPTION.

    """
    assert isinstance(sweep, np.ndarray) and sweep.ndim == 1, 'sweep is not a 1-d numpy array'
    assert sweep.dtype == bool, 'sweep dtype is not boolean'
    count = 0
    state = False
    sweepout = np.empty(len(sweep))
    for x in range(len(sweep)):
        if sweep[x] == True and state == False:
            count += 1
            state = True
            sweepout[x] = count
        if sweep[x] == False:
            state = False
            sweepout[x] = 0
        if sweep[x] == True and state == True:
            sweepout[x] = count
    return sweepout
        
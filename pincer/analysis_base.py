# -*- coding: utf-8 -*-
"""
Contains the analysis for each protocol, outputs can be suppressed if needed

"""
import numpy as np

class AnalysisManager():
    _registry = {}
    def __init__(self):
        print('Available Analyses:')
        print('-------------------')
        for i in self._registry:
            print(i)
    
    def get(self,name,**kwargs):
        return self._registry[name](**kwargs)
    
class PincerAnalysis():
    def __init_subclass__(cls,**kwargs):
        super().__init_subclass__(**kwargs)
        AnalysisManager._registry[cls.__name__] = cls
        
    def run(self, ABF):
        print('Warning! Missing Run Method!')
        return {'ERROR':1,'ERROR':2}

class Template(PincerAnalysis):
    def __init__(self, **kwargs):
        pass
    
    def run(self, ABF):
        pass
    
class CurrentInducedAP(PincerAnalysis):
    def __init__(self, **kwargs):
        pass
    
    def run(self, ABF):
        pass
    
def detectAP(sweep):
    aps = []
    threshold = -20
    #detect every region where trace exceeds threshold
    regions = bwlabel(sweep>=threshold)
    return aps

def baseline(sweep,baseline : tuple):
    sweep = np.subtract(sweep, np.average(sweep[baseline[0],baseline[1]]))
    return sweep

def bwlabel(sweep):
    count = 0
    state = False
    sweepout = np.empty(len(sweep),dtype=int)
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
        
# -*- coding: utf-8 -*-
"""
Contains various managers and parent classes for expandable plugin system.

"""

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
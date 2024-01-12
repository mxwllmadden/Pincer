# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 21:30:15 2024

@author: Maxwell Madden
"""

class ROI():
    _defaultunits = {'us': 1,'ms':1000,'s':1000000,'sec':1000000,'min':60000000}
    def __init__(self,region,unit = 'ms'):
        self._units = self._defaultunits
        assert unit in self._units.keys(), 'invalid unit, use one of: '+', '.join(list(self._units.keys()))
        assert type(region) == tuple or type(region) == list, 'regions must be defined as a tuple or list of tuples'
        if type(region) == tuple: region = [region]
        
        assert all([type(x) == tuple for x in region]), 'ranges must be tuples'
        for i in region:
            assert all([type(x) == int for x in i]), 'start and end of range must be int'
            assert len(i) == 2, 'ranges may only be defined as (start,end)'
            
        self.region = region
        self._mergeranges()
        self.unit = unit
        
    def _mergeranges(self):
        result = []
        for i in sorted(self.region):
            result = result or [i]
            if i[0] >= result[-1][1]:
                result.append(i)
            else:
                old = result[-1]
                result[-1] = (old[0], max(old[1], i[1]))
        self.region = result
    
    def convertunit(self,unit):
        assert unit in self._units.keys(), 'invalid unit, use one of: '+', '.join(list(self._units.keys())) 
        self.region = [tuple([i*self._units[self.unit]//self._units[unit] for i in y]) for y in self.region]
        self.unit = unit
        
    def _makefriendlywith(self,new):
        newunit = min(self._units[self.unit],new._units[new.unit])
        x = self._units | new._units
        lookup = {v:k for k,v in x.items()}
        if self._units[self.unit] != newunit: self.convertunit(lookup[newunit])
        if new._units[new.unit] != newunit: new.convertunit(lookup[newunit])
    
    def __add__(self, new):
        self._makefriendlywith(new)
        result = self.region + new.region
        return ROI(result, unit = self.unit)
    
    def __sub__(self,new):
        pass
    
    def __iter__(self):
        self._itcurr = -1
        self._itmax = len(self.region)
        return self
    
    def __next__(self):
        if self._itcurr < self._itmax-1:
            self._itcurr += 1
            return self.region[self._itcurr]
        else:
            raise StopIteration
    
    def __repr__(self):
        return 'Pincer Range of Interest (ROI) including ' + ' '.join(str(x) for x in self.region).replace('(','[') + ' in unit (' + self.unit + ')'
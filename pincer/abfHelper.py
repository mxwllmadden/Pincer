# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:42:56 2023

@author: mbmad
"""
import pyabf

class PincerABF(pyabf.ABF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
        #Determine Header Properties
        head_spl = self.headerText.split('\n') #seperate by newline
        head_spl = [x for x in head_spl if '=' in x and 'strings' not in x] #filter
        head_spl = [x.split('=') for x in head_spl] #split key from value
        head_spl = {key.strip() : value.strip() for [key, value] in head_spl}
        for i in head_spl.keys():
            if '[' in head_spl[i] and ']' in head_spl[i]:
                head_spl[i] = strlist2list(head_spl[i])
        self.headerProp = head_spl
        
        #Create additional properties for ease of access
        self.timeofday = self.abfDateTime.time()
        self.timeofday_str = self.abfDateTime.strftime('%H:%M')

def strlist2list(f_string : str):
    assert '[' in f_string and ']' in f_string
    f_string = f_string[f_string.index('[')+1:f_string.index(']')]
    outlist = f_string.split(',')
    outlist = [x.strip() for x in outlist]
    return outlist
        
if __name__ == '__main__':
    x = PincerABF(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data\23n17080.abf')
    z = x.headerProp
    print(z)
    
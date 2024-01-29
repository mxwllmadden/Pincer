# -*- coding: utf-8 -*-
"""
This module contains the PincerABF class, which inherits from and adds some
additional functionality to pyabf.ABF. It also contains some minor functions
to aid organization and processing of ABF file headers.
"""
import pyabf

class PincerABF(pyabf.ABF):
    def __init__(self, *args, epochcompensation : bool = True, **kwargs):
        self.epochcompensation = epochcompensation
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
        
    def setSweep(self, sweepNumber):
        """
        pClamp has a nasty habit of adding extra samples prior to initiating an
        Epoch, this removes those samples, aligning the beginning of the sweep
        to the beginning of the Epoch.
        
        You can access the unaltered sweep by using the setSweepFull method.
        """
        super().setSweep(sweepNumber)
        if self.epochcompensation == True:
            self.sweepY = self.sweepY[len(self.sweepY)//64:]
    
    def setSweepFull(self, sweepNumber):
        super().setSweep(sweepNumber)
        

def strlist2list(f_string : str):
    assert '[' in f_string and ']' in f_string
    f_string = f_string[f_string.index('[')+1:f_string.index(']')]
    outlist = f_string.split(',')
    outlist = [x.strip() for x in outlist]
    return outlist
        
if __name__ == '__main__':
    x = PincerABF(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data\23n17080.abf')
    z = x.head
    print(z)
    
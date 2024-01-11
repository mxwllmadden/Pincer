# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:52:40 2024

@author: mbmad
"""

import pincer
import pincer.analysis_custom.cracm

class AWCellDex(pincer.CellDex):
    def cmbABFnm(self,daycode,index):
        d = str(daycode)
        i = str(index)
        i = i.partition('.')[0]
        i = i.rjust(4,'0')
        return d + i.zfill(4) + '.abf'

mydata = pincer.CellDex(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data')
mydata.import_formattedexcel(r'celldex_24hr_1mgkg_psilo_inj (2).xlsx')

analysis = pincer.AnalysisManager()
rheo = analysis.make('Rheoramp')

mydata.queue_analysis(1, rheo)

mydata.process(report=True)

mydata.export_formattedexcel(r'celldex_postprocess_24hr_1mgkg_psilo_inj.xlsx')
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:02:36 2024

@author: mbmad
"""

import pincer
import pincer.analysis_custom.pulse

mydata = pincer.CellDex(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\DataAlli')
mydata.import_formattedexcel('celldex_Alli_MRK.xlsx')

analysis = pincer.AnalysisManager()
pairedpulse = analysis.make('Peaks', baseline = (0,1000), ranges = [(1100,1550),(165,2300)], peakdir = -1)
sealtest = analysis.make('Peaks', baseline = (4500,4800), ranges = [(4850,4950)], peakdir = -1)

mydata.queue_analysis(0, pairedpulse)
mydata.queue_analysis(1, sealtest)

mydata.process(report = True, check = True)

mydata.export_formattedexcel(r'celldex_postprocess_Alli_MRK.xlsx')
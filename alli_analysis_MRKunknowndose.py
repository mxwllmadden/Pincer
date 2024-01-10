# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:02:36 2024

@author: mbmad
"""

import pincer
import pincer.analysis_custom.pulse

mydata = pincer.CellDex(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\DataAlli')
mydata.import_formattedexcel('celldex_AlliMRexample.xlsx')

analysis = pincer.AnalysisManager()
pairedpulse = analysis.make('Peaks', baseline = (0,100), ranges = [(110,155),(165,230)])
sealtest = analysis.make('Peaks', baseline = (450,480), ranges = [(485,495)])

mydata.queue_analysis(0, pairedpulse)
mydata.queue_analysis(1, sealtest)

mydata.process(report = True)

mydata.export_formattedexcel(r'celldex_postprocess_alliMRKexample.xlsx')
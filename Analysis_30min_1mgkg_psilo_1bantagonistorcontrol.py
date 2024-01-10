# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:49:56 2023

@author: mbmad
"""

import pincer
import pincer.analysis_custom.cracm

mydata = pincer.CellDex(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data')
mydata.import_formattedexcel('celldex_30min_1mgkg_psilo_1bantagonistorcontrol.xlsx')

analysis = pincer.AnalysisManager()
ap1 = analysis.make('CurrentInducedAP')
cracm = analysis.make('CRACM')
rheo = analysis.make('Rheoramp')
check = analysis.make('CheckSealStep')

mydata.queue_analysis(1, cracm)
mydata.queue_analysis(0, ap1)
mydata.queue_analysis(2, rheo)
mydata.queue_analysis(9, check)

tname = ['100%','80%','60%','40%','20%','0%']
idents = [[x, 'Action Potentials per Light Pulse'] for x in tname]
mydata.queue_secondary_measure('Average APs/LP',idents)
idents = [[x, 'Area Under the Curve UNITS'] for x in tname]
mydata.queue_secondary_measure('Average Area Under the Curve UNITS',idents)

mydata.process(report = True)

mydata.export_formattedexcel(r'celldex_postprocess_30min_1mgkg_psilo_1bantagonistorcontrol.xlsx')
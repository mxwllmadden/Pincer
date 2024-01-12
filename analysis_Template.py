# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 16:40:33 2024

@author: mbmad
"""

# import pincer, as well as the specific analysis we want to use
import pincer
import pincer.analyses.pairedpulse as ppan

# Create a "Pincer" object. Specify the folder containing all ABF files
mydata = pincer.Pincer(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\DataAlli')

# Import your formatted CellDex from an excel file.
# This file contains all information about your recordings
mydata.import_formattedexcel(r'celldex_Template.xlsx')

# Create analyses by defining your regions of interest then passing them
# to your new analysis object

#Regions for first analysis. pincer.ROI takes milliseconds by default
firstbaseline = pincer.ROI((0,100))
firstpeak = pincer.ROI((110,155))
secondpeak = pincer.ROI((165,230))
secondbaseline = pincer.ROI((450,480))
sealtestregion = pincer.ROI((485,495))

pairedpulse = ppan.PairedPulse(firstbaseline, firstpeak, secondpeak, secondbaseline, sealtestregion, binsize=1)

#Now you must queue the analysis and tell it which analysis code you want it
#to run on

mydata.queue_analysis(0, pairedpulse)

#Now you can run the analysis

mydata.process(report=True,check=False)

#and export to the same or a different file

mydata.export_formattedexcel(r'celldex_post_Template.xlsx')
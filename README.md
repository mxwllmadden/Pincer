# Pincer: Automated Whole-Cell Patch-Clamp Analysis Utility
_Maxwell Madden_

Utilizes pyABF to automate patch analysis. Is written to be both expandable and flexible

## Creating an Analysis Script

You can use a provided example script to structure your own analysis. Alternatively, follow the workflow written out below in pseudocode.

'''
import pincer
import pincer.analysis_custom.cracm #optional, import analyses relevant to you
import mycustomanalysis #optional, import an analysis from another file

mydata = pincer.CellDex(r'c:/path/to/files')

'''
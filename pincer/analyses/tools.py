# -*- coding: utf-8 -*-
"""
Contains Wrapper Classes for Analyses

These classes purposefully do not inherit from pincer.analysis_base.PincerAnalysis
so as not to be listed in the analysis roster. Use these classes to alter the
outputs of an Analysis without changing the analysis's internal logic.
"""

class MultiAnalysis:
    """
    MultiAnalysis allows for the combination of multiple analysis objects. This
    is one of three ways to run multiple analyses on the same abf file, the other
    two being writing custom analyses, or by putting the file in the celldex
    twice and listing two different analysis indexes.
    """
    def __init__(self, analyses : dict):
        """
        Combine multiple analyses.

        Parameters
        ----------
        analyses : dict
            DESCRIPTION.

        Returns
        -------
        None.

        """
        pass
    
    def run(self,abf):
        pass
    
class SuppressOutput:
    """
    SuppressOutput allows for the removal of specific results from an analysis
    Report. These suppressed analyses are identified by searching for specific
    keywords.
    """
    def __init__(self):
        pass
    def run(self,abf):
        pass
# -*- coding: utf-8 -*-
"""
Contains various managers and parent classes for Pincer's expandable plugin 
system. While this is less useful when manually writing scripts or performing
operations via CLI, it sets the groundwork for a future GUI interface for Pincer.
"""

import numpy as np
from dataclasses import dataclass

class MissingAnalysisMethodError(Exception):
    pass

class PincerAnalysis():
    """
    Manager/parent class for all pincer analyses. Records all subclasses in
    _registry. Contains class methods for reporting subclasses (specific analyses).
    """
    _registry = {}
    def __init_subclass__(cls,**kwargs):
        """
        DO NOT EDIT. Registers every instance of a subclass in _registry.
        This allows for dynamic registering of analyses for an eventual GUI.

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
        
    def run(self, ABF):
        """
        This method should be overwritten in all subclasses. Is called by
        pincer.main.Pincer when processing abf files.

        Parameters
        ----------
        ABF : PincerABF
            DESCRIPTION.

        Returns
        -------
        dict
            Dictionary of results where all keys are result labels and values are
            the result value.

        """
        raise MissingAnalysisMethodError(f'"{self.__class__.__name__}.run(ABF)" is missing')
    
    @classmethod
    def make(cls,name,**kwargs):
        """
        Create an instance of the subclass with a given set of keyword arguments

        Parameters
        ----------
        name : str
            name of the analysis function.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        object
            Instance of an analysis class.

        """
        return cls._registry[name](**kwargs)
    
    @classmethod
    def report(cls):
        """Simple reporter of all analyses within _registry"""
        print('Available Analyses:')
        print('-------------------')
        for i in cls._registry:
            print(i)
        
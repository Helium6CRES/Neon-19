from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scipy as sp
import math
import random
from scipy.optimize import curve_fit,minimize
from numpy.linalg import inv
from tqdm import tqdm as tqdm


class Run: 
    """
    Description of the class with Attributes and Method's described briefly. 
    """
  
            
    def __init__(self, Date, Run):
        
        """
        __init__ (Method): 
            Desription: Creates class attributes based on Date, Cycle. 
            Arguments: Date (str): mmddyyyy , Cycle (int): #
            Returns: NA 
            Attributes Created: 
                * self.Data: A list of pandas df's consisting of [dfCh0,dfCh1,dfCh2] respectively.
                * self.DataCycles: A list consisting of [Ch0Cycles,Ch1Cycles], where each is a list
                of df's corresponding to each cycle. 
            Notes: 
                * Need to stick to run naming convention when taking data. runTESTmmddyyyy_#
                * Need to keep data in directory Data/Ne19Run_mmddyyyy
            
        """
        
        Path0 = Path().absolute() / 'Data/Ne19Run_{}/CH0@DT5725_1146_Data_runTEST{}_{}.csv'.format(Date, Date, Run)
        Path1 = Path().absolute() / 'Data/Ne19Run_{}/CH1@DT5725_1146_Data_runTEST{}_{}.csv'.format(Date, Date, Run)
        Path2 = Path().absolute() / 'Data/Ne19Run_{}/CH2@DT5725_1146_Data_runTEST{}_{}.csv'.format(Date, Date, Run)
        dfCh0 = pd.read_csv(Path0,sep=';')
        dfCh1 = pd.read_csv(Path1,sep=';')
        dfCh2 = pd.read_csv(Path2,sep=';')
        
        self.Data = [dfCh0,dfCh1,dfCh2]
        
#         self.DataCycles = self.CycleSplit(self.Data,TimeInterval) # Commenting this out for now to save time on certain things...
        
        
    def CycleSplit(self, TimeInterval):
        """ 
        CycleSplit (Method): 
            Desription: Splits attribute self.Data into cycles for both Ch0 and Ch1 data. 
            Arguments: 
                * Data: A list of pandas df's consisting of [dfCh0,dfCh1,dfCh2] respectively.
                * TimeInterval: A tuple representing the time interval relative to t=0 that defines each cycle. 
            Returns: 
                *DataCycles: A list consisting of [Ch0Cycles,Ch1Cycles], where each is a list
                of df's corresponding to each cycle. 
            Notes: 
                * As an example: Run_1[0][5] is a df that corresponds to Ch0, Cycle 5 of Run_1. 
         """
        
        self.TimeInterval = TimeInterval  
        
        Data = self.Data
        Ch0Cycles  = []
        Ch1Cycles  = []
        
        # Iterating through the number of times Ch2 recieved a signal.
        for i in np.arange(0,len(Data[2])):
            
            # Creating a temporary df for the events within the TimeInterval for each cycle (i). 
            df0Temp = Data[0][(Data[0]['TIMETAG'] > Data[2]['TIMETAG'][i]+self.TimeInterval[0]*10**12) & (Data[0]['TIMETAG'] < Data[2]['TIMETAG'][i]+self.TimeInterval[1]*10**12)]
            df1Temp = Data[1][(Data[1]['TIMETAG'] > Data[2]['TIMETAG'][i]+self.TimeInterval[0]*10**12) & (Data[1]['TIMETAG'] < Data[2]['TIMETAG'][i]+self.TimeInterval[1]*10**12)]
            
            
            # Reset 'TIMETAG' so that all cycles start at t = 0. This throws a warning but I am getting nowhere! Ask Kris maybe. 

            df0Temp.loc[:,'TIMETAG'] = df0Temp.loc[:,'TIMETAG'] - (Data[2].loc[:,'TIMETAG'][i]+self.TimeInterval[0]*10**12)
            df1Temp.loc[:,'TIMETAG'] = df1Temp.loc[:,'TIMETAG'] - (Data[2].loc[:,'TIMETAG'][i]+self.TimeInterval[0]*10**12)
            
            # Reset the index.
            
            df0Temp = df0Temp.reset_index()
            df1Temp = df1Temp.reset_index()
            
            # Drop 'FLAGS' Column for ease, so all entries are floats.
            
            df0Temp = df0Temp.drop(['FLAGS'], axis=1)
            df1Temp = df1Temp.drop(['FLAGS'], axis=1)
            
            Ch0Cycles.extend([df0Temp])
            Ch1Cycles.extend([df1Temp])
            
            
        # Create a list of lists of dfs. 
        DataCycles = [Ch0Cycles,Ch1Cycles]
        
        self.Cycles = DataCycles
        
        return None  
        
        
#     def CountRate(self, BinSizeSeconds): 
        
#         BinSize = BinSizeSeconds*10**12
        
        
        
        
#         self.CountRate = BlAH
        
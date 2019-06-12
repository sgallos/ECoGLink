# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:28:52 2019

@author: charl
"""

#Continuous state
class Continuous_Condition():
    
    
    def __init__(self):
        return
    
    def process(self, BMI_input):
        if BMI_input:
            Hardware_output = 1
        else:
            Hardware_output = 0        
        return Hardware_output
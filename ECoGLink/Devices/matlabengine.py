# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:00:05 2019

@author: charl

Code starts the opening of matlab engine in python
Opens Nexus Device channel lines
"""

# add pathway
import matlab.engine
eng = matlab.engine.start_matlab()
eng.javaaddpath('C:\\Users\\charl\\Documents\\Python Scripts\\Prasad Lab\\Jar_Nexus\\nexus.jar', nargout =0)
eng.javaaddpath('C:\\Users\\charl\\Documents\\Python Scripts\\Prasad Lab\\Jar_Nexus\\jssc.jar', nargout =0)
# call matlabengine.workspace['variable'] = matlabengine.function/object to set within matlab workspace
eng.workspace['inst']=eng.mdt.neuro.nexus.NexusInstrument(nargout = 1)
eng.workspace['s2'] = eng.mdt.neuro.nexus.SerialConnection('COM5')
# matlabengine.eval('runs this line directly in matlab')
eng.eval('inst.connect(s2)')
eng.workspace['provider']=eng.mdt.neuro.nexus.ThreadedNexusInstrument(eng.eval('inst'))
eng.eval('inst.getNexusStatus', nargout = 0)
eng.eval('inst.setNexusConfiguration(30,15)')
eng.eval('inst.startDataSession')
eng.eval('inst.getDataPacket',nargout = 0)
eng.eval('inst.stopDataSession')

## code to check the value into a string for python to read
eng.workspace["curState"] = eng.eval("inst.getNexusStatus.get('State')")
eng.eval("strcmp(curState, 'INS_CONNECTED')")
State = "INS_CONNECTED"
eng.eval(f"strcmp(curState, '{State}')")
eng.eval("char(curState)")

## run getting a packet
## cd into location of matlab files

eng.grab_data_pkts(1, nargout = 1)
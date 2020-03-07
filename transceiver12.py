# -*- coding: cp1251 -*-
#===Transceiver_for_blocking_noise_module_by_panda===
#=_Use this module at your own risk, author has no responsibility
#_________Version 1.3__________________________
#=import math module, or just pow, pi, and log10 if errors

import math

class radio(object):
	def __init__(self,Ftr):
		self.freq=Ftr
		self.power=40
		self.antennaGain=0
		self.alpha=3
		self.Qfactor=100
		self.Kfactor=0
		self.radius=1
		self.selfactor=70
		self.wl=300/self.freq
		self.hant=0.25*self.wl
		self.harmonic=1
		self.deltaF=1.0
		self.cntN=1
		self.B=10*self.cntN*math.log10(1+math.pow(self.Qfactor,2)* math.pow(((self.freq+self.deltaF)/self.freq-(self.freq-self.deltaF)/self.freq),2))
		self.LR=20*math.log10(4*math.pi*self.radius/self.wl)
		
	
	
	def rebuild(self):
		self.wl=300/self.freq
		self.B=10*math.log10(1+math.pow(self.Qfactor,2)* math.pow(((self.freq+self.deltaF)/self.freq-(self.freq-self.deltaF)/self.freq),2))
		self.LR=20*math.log10(4*math.pi*self.radius/self.wl)
		self.hant=0.25*self.wl

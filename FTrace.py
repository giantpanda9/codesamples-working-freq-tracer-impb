#-*-coding: utf-8 -*-
from Tkinter import *
from Tix import *
from tkMessageBox import *
import math
from transceiver13 import radio
import string
import datetime
import os
import win32api
import threading


defcol="#d4cfc7"

rangeTLST={}
FtHhLST={}
FtHVarLST={}
FtFrmLST={}
FtBoldLST={}
iTFrms=0

rangeRLST={}
FrHhLST={}
FrHVarLST={}
FrFrmLST={}
FrBoldLST={}
iRFrms=0

Rng=0


Counted=0




Cube=unicode(' █','utf-8')

def dummy():
	return 0
	
def FreqTagT(ev):	
	tmp=ev.widget.cget('font')
	tmp=tmp.replace("}","")
	tmp=tmp.replace("{","")
	tmp=tmp.replace("8","")
	ev.widget.configure(font=(tmp,8,"bold"))
	FtBoldLST[ev.widget.cget('text')]="bold"
	

def FreqTagOutT(ev):
	tmp=ev.widget.cget('font')
	tmp=tmp.replace("}","")
	tmp=tmp.replace("{","")
	tmp=tmp.replace("8","")
	ev.widget.configure(font=(tmp,8, "normal"))
	FtBoldLST[ev.widget.cget('text')]="normal"
	
	
def FreqTagR(ev):	
	tmp=ev.widget.cget('font')
	tmp=tmp.replace("}","")
	tmp=tmp.replace("{","")
	tmp=tmp.replace("8","")
	ev.widget.configure(font=(tmp,8,"bold"))
	FrBoldLST[ev.widget.cget('text')]="bold"
	

def FreqTagOutR(ev):
	tmp=ev.widget.cget('font')
	tmp=tmp.replace("}","")
	tmp=tmp.replace("{","")
	tmp=tmp.replace("8","")
	ev.widget.configure(font=(tmp,8, "normal"))
	FrBoldLST[ev.widget.cget('text')]="normal"

def ReturnYellow(ev):
	
	for i in range(0, len(FtHhLST)):
		if FtHhLST[i]['bg']=="yellow" or FtHhLST[i]['bg']=="green":
			FtHhLST[i].configure(bg="cyan")
	for i in range(0, len(FrHhLST)):
		if FrHhLST[i]['bg']=="yellow" or FrHhLST[i]['bg']=="green":
			FrHhLST[i].configure(bg="cyan")


def CheckYellow(ev):
	widtext=""
	
	global Counted
	
	if Counted == 1:
		pass
			
def ClearAll():
	
	RepVar1.set('')
	for i in range(0, len(FtHhLST)):
		FtHVarLST.pop(i)
		FtHhLST[i].destroy()
		FtHhLST.pop(i)
		
	for i in range(0,len(FtFrmLST)):
		FtFrmLST[i].destroy()
		FtFrmLST.pop(i)
		
	for i in range(0, len(FrHhLST)):
		FrHVarLST.pop(i)
		FrHhLST[i].destroy()
		FrHhLST.pop(i)

	for i in range(0,len(FrFrmLST)):
		FrFrmLST[i].destroy()
		FrFrmLST.pop(i)	
		
		
	
	
	
		
	global iTFrms
	iTFrms=0
	global iRFrms
	iRFrms=0
	global ib
	ib=0
	global ib1
	ib1=0
	global Counted
	Counted=0

	return 0
	
def addTR():
	RepVar1.set('')
	global Counted
	Counted=0
			
	startTF=transEntry.get()
	startTF=startTF.replace(',','.')
	endTF=transEntry1.get()
	endTF=endTF.replace(',','.')
	
	startRF=recvEntry.get()
	startRF=startRF.replace(',','.')
	endRF=recvEntry1.get()
	endRF=endRF.replace(',','.')
	
	try:
		a=float(startTF)/3
		a=float(endTF)/3
	except:
		showerror("Ошибка!", "Диапазон частот передатчиков введен неверено!")
		transEntry.insert(0,'450.0000')
		transEntry.delete ('8',END)
	
		transEntry1.insert(0,'453.0000')
		transEntry1.delete ('8',END)
		return 0
				
	try:
		a=float(startRF)/3
		a=float(endRF)/3
	except:
		showerror("Ошибка!", "Диапазон частот приёмников введен неверено!")
		recvEntry.insert(0,'460.0000')
		recvEntry.delete ('8',END)
	
		recvEntry1.insert(0,'463.0000')
		recvEntry1.delete ('8',END)
		return 0

	startTF=float(startTF)
	endTF=float(endTF)
	startRF=float(startRF)
	endRF=float(endRF)
		
	if endTF <= startTF:
		showerror("Ошибка!", "Диапазон частот передатчиков введен неверено!")
		return 0
	
	if endRF <= startRF:
		showerror("Ошибка!", "Диапазон частот приёмников введен неверено!")	
		return 0
		
	ClearAll()
	
	
	stepFi=0
	transF1=startTF
	stepF=0.0125
	xs=[0,70,140,210,280]
	while transF1 <= endTF:
		
		rangeTLST[stepFi]=transF1
		FtBoldLST["%3.4f" % float(transF1)]="normal"
		transF1=transF1+stepF
		
		stepFi=stepFi+1
		
	#print len(rangeTLST)
	ib=0
	global iTFrms
	
	for i in range(4, len(rangeTLST),5):
		
		tmp1=Frame(Twin, width=349,height=19,bg=defcol)
		tmp1.pack()
		FtFrmLST[iTFrms]=tmp1
		iTFrms=iTFrms+1		
		
		FtHVarLST[i-4]=DoubleVar()		
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeTLST[i-4]), onvalue=rangeTLST[i-4], offvalue=0.0, variable=FtHVarLST[i-4],bg=defcol,fg='black', font=(Font1,8,"normal"))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagT)
		tmp.bind('<Double-Button-3>', FreqTagOutT)
		tmp.place(x=0,y=0)
		FtHhLST[i-4]=tmp
		
		FtHVarLST[i-3]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeTLST[i-3]), onvalue=rangeTLST[i-3], offvalue=0.0, variable=FtHVarLST[i-3],bg=defcol,fg='black', font=(Font1,8,"normal"))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagT)
		tmp.bind('<Double-Button-3>', FreqTagOutT)
		tmp.place(x=70,y=0)
		FtHhLST[i-3]=tmp
		
		FtHVarLST[i-2]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeTLST[i-2]), onvalue=rangeTLST[i-2], offvalue=0.0, variable=FtHVarLST[i-2],bg=defcol,fg='black', font=(Font1,8,"normal"))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagT)
		tmp.bind('<Double-Button-3>', FreqTagOutT)
		tmp.place(x=140,y=0)
		FtHhLST[i-2]=tmp
		
		FtHVarLST[i-1]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeTLST[i-1]), onvalue=rangeTLST[i-1], offvalue=0.0, variable=FtHVarLST[i-1],bg=defcol,fg='black', font=(Font1,8,"normal"))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagT)
		tmp.bind('<Double-Button-3>', FreqTagOutT)
		tmp.place(x=210,y=0)
		FtHhLST[i-1]=tmp
		
		FtHVarLST[i]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeTLST[i]), onvalue=rangeTLST[i], offvalue=0.0, variable=FtHVarLST[i],bg=defcol,fg='black', font=(Font1,8,"normal"))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagT)
		tmp.bind('<Double-Button-3>', FreqTagOutT)
		tmp.place(x=280,y=0)
		FtHhLST[i]=tmp
		
		ib=i
	#print ib
	ib=ib+1
	tmp1=Frame(Twin, width=349,height=19,bg=defcol)
	tmp1.pack()
	
	
	FtFrmLST[iTFrms]=tmp1

	
				
	FtHVarLST[ib]=DoubleVar()
	tmp=Checkbutton(tmp1, text="%3.4f" % (endTF), onvalue=endTF, offvalue=0.0, variable=FtHVarLST[ib],bg=defcol,fg='black', font=(Font1,8,"normal"))
	tmp.bind('<Motion>', CheckYellow)
	tmp.bind('<Leave>', ReturnYellow)
	tmp.bind('<Button-3>', FreqTagT)
	tmp.bind('<Double-Button-3>', FreqTagOutT)
	tmp.place(x=0,y=0)
	FtHhLST[ib]=tmp
		
	
	
	stepFi=0
	transF2=startRF
	stepF=0.0125
	xs=[0,70,140,210,280]
	while transF2 <= endRF:
		rangeRLST[stepFi]=transF2
		FrBoldLST["%3.4f" % float(transF2)]="normal"
		transF2=transF2+stepF
		stepFi=stepFi+1
		
	#print len(rangeTLST)
	ib1=0
	global iRFrms
	for i in range(4, len(rangeRLST),5):
		
		tmp1=Frame(Rwin, width=349,height=19,bg=defcol)
		tmp1.pack()
		FrFrmLST[iRFrms]=tmp1
		iRFrms=iRFrms+1
		
		FrHVarLST[i-4]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeRLST[i-4]), onvalue=rangeRLST[i-4], offvalue=0.0, variable=FrHVarLST[i-4],bg=defcol,fg='black', font=(Font1,8,"normal"))
		#FrHVarLST[i-4].set("%3.4f" % (rangeRLST[i-4]))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagR)
		tmp.bind('<Double-Button-3>', FreqTagOutR)
		tmp.place(x=0,y=0)
		FrHhLST[i-4]=tmp
		
		FrHVarLST[i-3]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeRLST[i-3]), onvalue=rangeRLST[i-3], offvalue=0.0, variable=FrHVarLST[i-3],bg=defcol,fg='black', font=(Font1,8,"normal"))
		#FrHVarLST[i-3].set("%3.4f" % (rangeRLST[i-3]))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagR)
		tmp.bind('<Double-Button-3>', FreqTagOutR)
		tmp.place(x=70,y=0)
		FrHhLST[i-3]=tmp
		
		FrHVarLST[i-2]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeRLST[i-2]), onvalue=rangeRLST[i-2], offvalue=0.0, variable=FrHVarLST[i-2],bg=defcol,fg='black', font=(Font1,8,"normal"))
		#FrHVarLST[i-2].set("%3.4f" % (rangeRLST[i-2]))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagR)
		tmp.bind('<Double-Button-3>', FreqTagOutR)
		tmp.place(x=140,y=0)
		FrHhLST[i-2]=tmp
		
		FrHVarLST[i-1]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeRLST[i-1]), onvalue=rangeRLST[i-1], offvalue=0.0, variable=FrHVarLST[i-1],bg=defcol,fg='black', font=(Font1,8,"normal"))
		#FrHVarLST[i-1].set("%3.4f" % (rangeRLST[i-1]))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagR)
		tmp.bind('<Double-Button-3>', FreqTagOutR)
		tmp.place(x=210,y=0)
		FrHhLST[i-1]=tmp
		
		FrHVarLST[i]=DoubleVar()
		tmp=Checkbutton(tmp1, text="%3.4f" % (rangeRLST[i]), onvalue=rangeRLST[i], offvalue=0.0, variable=FrHVarLST[i],bg=defcol,fg='black', font=(Font1,8,"normal"))
		#FrHVarLST[i].set("%3.4f" % (rangeRLST[i]))
		tmp.bind('<Motion>', CheckYellow)
		tmp.bind('<Leave>', ReturnYellow)
		tmp.bind('<Button-3>', FreqTagR)
		tmp.bind('<Double-Button-3>', FreqTagOutR)
		tmp.place(x=280,y=0)
		FrHhLST[i]=tmp
		
		ib1=i
	#print ib
	ib1=ib1+1
	tmp1=Frame(Rwin, width=349,height=19,bg=defcol)
	tmp1.pack()
	FrFrmLST[iRFrms]=tmp1
	
	
				
	FrHVarLST[ib1]=DoubleVar()
	tmp=Checkbutton(tmp1, text="%3.4f" % (endRF), onvalue=endRF, offvalue=0.0, variable=FrHVarLST[ib1],bg=defcol,fg='black', font=(Font1,8,"normal"))
	#FrHVarLST[ib1].set("%3.4f" % (endRF))
	tmp.bind('<Motion>', CheckYellow)
	tmp.bind('<Leave>', ReturnYellow)
	tmp.bind('<Button-3>', FreqTagR)
	tmp.bind('<Double-Button-3>', FreqTagOutR)
	tmp.place(x=0,y=0)
	FrHhLST[ib1]=tmp
		
def swapTR(ev):
	tmp=transEntry.get()+"000"
	tmp1=transEntry1.get()+"000"
		
	transEntry.insert(0,recvEntry.get()+"000")
	transEntry.delete ('8',END)
	transEntry1.insert(0,recvEntry1.get()+"000")
	transEntry1.delete ('8',END)
		
	recvEntry.insert(0,tmp)
	recvEntry.delete ('8',END)
	recvEntry1.insert(0,tmp1)
	recvEntry1.delete ('8',END)
	
	return 0	

def checkF(ev):
	ev.widget.delete ('8',END)
	
def Quit():
	global root
	root.destroy()
	
def halfTproc1(*outFA):
	print "halfTproc1 started\n"
	

	global Rng
	global Cube
	RepVar1.set(RepVar1.get()+Cube)
	
	for i in range(0,len(outFA)):
		for j in range(0,(len(rangeTLST)/2)):
			if ("%3.4f" % (outFA[i]))==("%3.4f" % (rangeTLST[j])):
				
				try:
					if float(outFA[i]) - float(FtHVarLST[j].get())!=Rng:
						FtHhLST[j].configure(bg="red")	
					print outFA[i]
				
				except:
					pass
		
			
				
	global Counted
	Counted=1
	RepVar1.set(RepVar1.get()+Cube)
	
	print "halfTproc1 ended\n"


def halfTproc2(*outFA):
	print "halfTproc2 started\n"


	global Rng
	global Cube
	RepVar1.set(RepVar1.get()+Cube)
	
	for i in range(0,len(outFA)):
		for j in range((len(rangeTLST)/2),len(rangeTLST)):
			if ("%3.4f" % (outFA[i]))==("%3.4f" % (rangeTLST[j])):
				
				try:
					if float(outFA[i]) - float(FtHVarLST[j].get())!=Rng:
						FtHhLST[j].configure(bg="red")	
					
					
				
				except:
					pass
		
			
	global Counted
	Counted=1
	RepVar1.set(RepVar1.get()+Cube)
	
	print "halfTproc2 ended\n"

					
def halfRproc1(*outFA):
	print "halfRproc1 started\n"
	
	global Rng
	print Rng
	global Cube
	RepVar1.set(RepVar1.get()+Cube)
	
	for i in range(0,len(outFA)):
		for j in range(0,(len(rangeRLST)/2)):
			if ("%3.4f" % (outFA[i]))==("%3.4f" % (rangeRLST[j])):
				
				try:
					if float(outFA[i]) - float(FrHVarLST[j].get())!=Rng:
						FrHhLST[j].configure(bg="red")
					
				

				
				except:
					pass

			
	global Counted
	Counted=1
	RepVar1.set(RepVar1.get()+Cube)
	
	print "halfRproc1 ended\n"
	
	
def halfRproc2(*outFA):
	print "halfRproc2 started\n"
	global Rng
	global Cube

	
	
	RepVar1.set(RepVar1.get()+Cube)
	
	for i in range(0,len(outFA)):
		for j in range((len(rangeRLST)/2),len(rangeRLST)):
			if ("%3.4f" % (outFA[i]))==("%3.4f" % (rangeRLST[j])):
				
				try:
					if float(outFA[i]) - float(FrHVarLST[j].get())!=Rng:
						FrHhLST[j].configure(bg="red")
			
				except:
					pass
			
			
					
	global Counted
	Counted=1
	
	RepVar1.set(RepVar1.get()+Cube)
	
	print "halfRproc2 ended\n"
	
def Watcher(*p):
	print "Watching..."
	p[0].join()
	p[1].join()
	p[2].join()
	p[3].join()
	
	
	while len(RepVar1.get())<=15:
		RepVar1.set(RepVar1.get()+Cube)
		
	print "Watch is ended."
	

	
	
def CountIt():
	RepVar1.set('')	
	#Input array of frequencies
	InputFreqArray=[]
		
	#Output array of combined frequencies
	OutputFreqArray=[]
	
	startTF=transEntry.get()
	startTF=startTF.replace(',','.')
	endTF=transEntry1.get()
	endTF=endTF.replace(',','.')
	
	startRF=recvEntry.get()
	startRF=startRF.replace(',','.')
	endRF=recvEntry1.get()
	endRF=endRF.replace(',','.')
	
	global Rng
	
	Rng=abs(float(startTF)-float(startRF))

	
	#Fill up the array with the values of user selected frequencies
	
	for i in range(0, len(FtHhLST)):
		if FtHVarLST[i].get()!=0.0:
			InputFreqArray.append(FtHVarLST[i].get())
			
	for i in range(0, len(FrHhLST)):
		if FrHVarLST[i].get()!=0.0:
			InputFreqArray.append(FrHVarLST[i].get())
	
	for i in range(0, len(FrHhLST)):
		if FrHVarLST[i].get()!=0.0:
			InputFreqArray.append(FrHVarLST[i].get())
		
	for i in range(0, len(FtHhLST)):
		if FtHVarLST[i].get()!=0.0:
			InputFreqArray.append(FtHVarLST[i].get())
		


			
					
	#If user inputs nothing or doesn't even generate a freqency list say him about it	
	if len(InputFreqArray)<2:
		showerror("Ошибка!", "Определите миниум две входных частоты или произведите генерацию частот по диапазону!")
		return 0
	
	for i in range(0, len(FtHhLST)):
		FtHhLST[i].configure(bg=defcol)
			
	for i in range(0, len(FrHhLST)):
		FrHhLST[i].configure(bg=defcol)
		
		
	
	for i in range(0,len(InputFreqArray)):
		f1=InputFreqArray[i]
		tmp=InputFreqArray
		#tmp[i]=0.0
		for j in range(0,len(tmp)):
			f2=tmp[j]			
			tmp1=tmp
			#tmp1[j]=0.0
							
			for k in range(0,len(tmp1)):
				f3=tmp1[k]
				
				if ((float(startTF)<=abs(float(f1-f2+f3))<=float(endTF)) or (float(startRF)<=abs(float(f1-f2+f3))<=float(endRF))) and (abs(f1)!=abs(f2))  and (abs(f1)!=abs(f3)) and (abs(f1)!=abs(f2)!=abs(f3)): 
					if float(f1-f2+f3) not in OutputFreqArray:
						OutputFreqArray.append(abs(f1-f2+f3))		
				if ((float(startTF)<=abs(float(f1+f2-f3))<=float(endTF)) or (float(startRF)<=abs(float(f1+f2-f3))<=float(endRF))) and (abs(f1)!=abs(f2)) and (abs(f1)!=abs(f3)) and (abs(f1)!=abs(f2)!=abs(f3)): 
					if float(f1+f2-f3) not in OutputFreqArray:
						OutputFreqArray.append(abs(f1+f2-f3))
				if ((float(startTF)<=abs(float(2*f1-f2))<=float(endTF)) or (float(startRF)<=abs(float(2*f1-f2))<=float(endRF))) and (abs(f1)!=abs(f2)): 
					if float(2*f1-f2) not in OutputFreqArray:
						OutputFreqArray.append(abs(2*f1-f2))	
	
	
	ps=[]
	p1 = threading.Thread(target=halfTproc1, name="halfTproc1", args=OutputFreqArray)
	ps.append(p1)
	p2 = threading.Thread(target=halfTproc2, name="halfTproc2", args=OutputFreqArray)
	ps.append(p2)
	p3 = threading.Thread(target=halfRproc1, name="halfRproc1", args=OutputFreqArray)
	ps.append(p3)
	p4 = threading.Thread(target=halfRproc2, name="halfRproc2", args=OutputFreqArray)
	ps.append(p4)
	p5 = threading.Thread(target=Watcher, name="Watcher",args=ps)
	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p5.start()
	

	global CountEnd				
	CountEnd=0


	
def expSel():
	#Input array of frequencies
	tExpFreqArray=[]
	
	#Output array of combined frequencies
	rExpFreqArray=[]
	
	#Fill up the array with the values of user selected frequencies
	for i in range(0, len(FtHhLST)):
		if FtHVarLST[i].get()!=0.0:
			tExpFreqArray.append(FtHVarLST[i].get())
	
	for i in range(0, len(FrHhLST)):
		if FrHVarLST[i].get()!=0.0:
			rExpFreqArray.append(FrHVarLST[i].get())
				
	#If user inputs nothing or doesn't even generate a freqency list say him about it	
	if len(tExpFreqArray)==0 and len(rExpFreqArray)==0:
		showerror("Ошибка!", "Определите по одной экспортируемой частоте в левом и правом блоках или произведите генерацию частот по диапазону!")
		
		return 0	
		
	tExpF=""
	rExpF=""
	
	for i in range(0, len(tExpFreqArray)):
		tExpF=tExpF+str(tExpFreqArray[i])+","
	
	tExpF=tExpF[:-1]
	
	for i in range(0, len(rExpFreqArray)):
		rExpF=rExpF+str(rExpFreqArray[i])+","	
	
	rExpF=rExpF[:-1]
	
	
	trExpF=tExpF + " " + rExpF
		
	strPath=str(os.getcwd())
	strPath=strPath+"\RTCalc.exe"
	
	if os.path.isfile(strPath.decode('utf-8').encode('cp1251')):
		win32api.ShellExecute(0, "open", strPath.decode('utf-8').encode('cp1251'),trExpF,"",1)
	else:
		showerror("Ошибка!", "Исполняемый файл ИМПБ не найден!")
		
def expRed():
	#Input array of frequencies
	tRedFreqs=[]
	
	#Output array of combined frequencies
	rRedFreqs=[]
	
	#Fill up the array with the values of user selected frequencies
	for i in range(0, len(FtHhLST)):
		if FtHhLST[i]['bg']=="red":
			tRedFreqs.append(rangeTLST[i])
	
	for i in range(0, len(FrHhLST)):
		if FrHhLST[i]['bg']=="red":
			rRedFreqs.append(rangeRLST[i])
				
	
	
	if len(tRedFreqs)==0 and len(rRedFreqs)==0:
		showerror("Ошибка!", "Расчёт модели поражённых частот не произведён, список поражённых частот пуст!")
		return 0
	
	tExpF=""
	rExpF=""
	
	for i in range(0, len(tRedFreqs)):
		tExpF=tExpF+str(tRedFreqs[i])+","
	
	tExpF=tExpF[:-1]
	
	for i in range(0, len(rRedFreqs)):
		rExpF=rExpF+str(rRedFreqs[i])+","	
	
	rExpF=rExpF[:-1]
	
	
	trExpF=tExpF + " " + rExpF
	
	strPath=str(os.getcwd())
	strPath=strPath+"\RTCalc.exe"
	
	if os.path.isfile(strPath.decode('utf-8').encode('cp1251')):
		win32api.ShellExecute(0, "open", strPath.decode('utf-8').encode('cp1251'),trExpF,"",1)
	else:
		showerror("Ошибка!", "Исполняемый файл ИМПБ не найден!")
		
def GenRep():
	if len(rangeTLST)!=0 and len(rangeRLST)!=0:
		
		dtt = datetime.datetime.now()
		dtt = str(dtt.strftime('%d.%m.%Y - %H:%M:%S'))
		reportData='<html><head><title>Отчёт о работе программы трассировки комбинаций рабочих частот</title></head><body><right>Дата и время создания отчёта: '+dtt+'</right><br><center><u>Отчёт о работе программы трассировки комбинаций рабочих частот по диапазонам<br>%3.4f - %3.4f и %3.4f - %3.4f МГц</u></center><br>'% (rangeTLST[0], rangeTLST[len(rangeTLST)-1], rangeRLST[0], rangeRLST[len(rangeRLST)-1])
		reportData=reportData+"<table border=1 width=\"49%\" align=LEFT>"
		#reportData=reportData+"<TR><TD>Диапазон:%3.4f - %3.4f</TD></TR>" % (rangeTLST[0], rangeTLST[len(rangeTLST)-1], rangeRLST[0], rangeRLST[len(rangeRLST)-1])
		ib=0
		for i in range(4, len(rangeTLST),5):
			reportData=reportData + "<TR>"
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FtHhLST[i-4]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-4]], float(rangeTLST[i-4]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FtHhLST[i-3]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-3]], float(rangeTLST[i-3]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FtHhLST[i-2]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-2]], float(rangeTLST[i-2]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FtHhLST[i-1]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-1]], float(rangeTLST[i-1]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FtHhLST[i]['bg']), FtBoldLST["%3.4f" % rangeTLST[i]], float(rangeTLST[i]))
			reportData=reportData + "</TR>"
			ib=i
	
		ib=ib+1
		
	
		
		reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD></table>" % (str(FtHhLST[ib]['bg']), FtBoldLST["%3.4f" % rangeTLST[ib]],float(rangeTLST[len(rangeTLST)-1]))
		
		reportData=reportData+"<table border=1 width=\"49%\" align=RIGHT>"
		#reportData=reportData+"<TH>Диапазон: %3.4f - %3.4f</TH>" % (rangeRLST[0], rangeRLST[len(rangeRLST)-1])
		
		ib=0
		for i in range(4, len(rangeRLST),5):
			
			reportData=reportData + "<TR>"
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FrHhLST[i-4]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-4]], float(rangeRLST[i-4]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FrHhLST[i-3]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-3]],float(rangeRLST[i-3]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FrHhLST[i-2]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-2]],float(rangeRLST[i-2]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FrHhLST[i-1]['bg']), FtBoldLST["%3.4f" % rangeTLST[i-1]],float(rangeRLST[i-1]))
			reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD>" % (str(FrHhLST[i]['bg']), FtBoldLST["%3.4f" % rangeTLST[i]],float(rangeRLST[i]))
			reportData=reportData + "</TR>"
			ib=i
	
		ib=ib+1
		reportData=reportData + "<TD BGCOLOR=%s><p style=\"font-weight:%s;\">%3.4f</p></TD></table>" % (str(FrHhLST[ib]['bg']), FtBoldLST["%3.4f" % rangeTLST[ib]],float(rangeRLST[len(rangeRLST)-1]))
	
	
	
		reportData=reportData+"</html>"

		strPath=str(os.getcwd())
		strPath=strPath.replace('Data','')
		strPath=strPath+"ftrace-report.htm"
		open(strPath.decode('utf-8').encode('cp1251'), "w").write(reportData.decode('utf-8').encode('cp1251'))
	
	strPath=str(os.getcwd())
	strPath=strPath.replace('Data','')
	strPath=strPath+"ftrace-report.htm"
	if os.path.isfile(strPath.decode('utf-8').encode('cp1251')):
		win32api.ShellExecute(0, "open", strPath.decode('utf-8').encode('cp1251'),None,"",1)
	else:
		showerror("Ошибка!", "Файл отчёта не найден!")

def ViewRep():
	strPath=str(os.getcwd())
	strPath=strPath.replace('Data','')
	strPath=strPath+"ftrace-report.htm"
	if os.path.isfile(strPath.decode('utf-8').encode('cp1251')):
		win32api.ShellExecute(0, "open", strPath.decode('utf-8').encode('cp1251'),None,"",1)
	else:
		showerror("Ошибка!", "Файл отчёта не найден!")
		

def aboutMe():
	showinfo(" О программе:", "Программист: Чегодаев Н.И.")

root = Tk()

root.wm_title("Программа трассировки комбинаций рабочих частот")

root.wm_minsize(width=root.winfo_screenwidth(),height=root.winfo_screenheight())
root.wm_maxsize(width=root.winfo_screenwidth(),height=root.winfo_screenheight())

imm = Menu(root)
root.config(menu=imm)

fm = Menu(imm, tearoff=0)
imm.add_cascade(label="Файл",menu=fm)
fm.add_command(label="Новый расчёт", command=ClearAll)
fm.add_command(label="Выход",command=Quit)

Counted=IntVar()

cm = Menu(imm, tearoff=0)
imm.add_cascade(label="Модель",menu=cm)
cm.add_command(label="Генерация сетки частот", command=addTR)
cm.add_command(label="Вычислить поражённые частоты", command=CountIt)
cm.add_command(label="Генерация отчёта", command=GenRep)
cm.add_command(label="Просмотр отчёта", command=ViewRep)

em = Menu(imm, tearoff=0)
imm.add_cascade(label="Экспорт",menu=em)
em.add_command(label="Экспортировать выделенные", command=expSel)
em.add_command(label="Экспортировать поражённые",command=expRed)

am = Menu(imm, tearoff=0)
imm.add_cascade(label="Информация",menu=am)
am.add_command(label="О программе", command=aboutMe)

freqFrame = Frame(width = 500, height = 60)
#freqFrame.place(x=0, y=0)
freqFrame.pack(side=TOP, fill="x")



TLbl=Label(freqFrame, text='Передатчики. Укажите диапазон:')
TLbl.place(x=10, y=10)

TLbl=Label(freqFrame, text='Приёмники. Укажите диапазон:')
TLbl.place(x=220, y=10)

transEntry=Entry(freqFrame,width=8)
transEntry.insert(0,'450,0000')
transEntry.bind('<KeyRelease>', checkF)
transEntry.place(x=10, y=40)

Font1=transEntry.cget('font')
Font1=Font1.replace("}","")
Font1=Font1.replace("{","")
Font1=Font1.replace("8","")


transLbl=Label(freqFrame, text='-')
transLbl.place(x=65, y=40)

transEntry1=Entry(freqFrame,width=8)
transEntry1.insert(0,'453,0000')
transEntry1.bind('<KeyRelease>', checkF)
transEntry1.place(x=75, y=40)

swapUS=Button(freqFrame, text='Обменять')
swapUS.bind("<Button-1>", swapTR)
swapUS.place(x=150,y=35)
#--------------------------------------------------------------------------------------
recvEntry=Entry(freqFrame,width=8,)
recvEntry.insert(0,'460,0000')
recvEntry.bind('<KeyRelease>', checkF)
recvEntry.place(x=230, y=40)

recvLbl=Label(freqFrame, text='-')
recvLbl.place(x=280, y=40)

recvEntry1=Entry(freqFrame,width=8)
recvEntry1.insert(0,'463,0000')
recvEntry1.bind('<KeyRelease>', checkF)
recvEntry1.place(x=290, y=40)

transGen=Button(freqFrame, text='Генерировать', command=addTR)
transGen.place(x=350,y=35)

ReportFrame=Frame(freqFrame, width = (((root.winfo_screenwidth()/2))), height = 30)
ReportFrame.place(x=((root.winfo_screenwidth()/2)-20),y=35)


ReportLbl=Label(ReportFrame, text='Завершено:')
ReportLbl.place(x=0,y=0)



RepVar1=StringVar()

ReportLb = Label(ReportFrame,textvariable=RepVar1, bg='white', fg='blue', relief='groove')
ReportLb.place(x=70,y=0, width=95,height=23)

RepVar1.set('')



FtFrame = Frame(width=((root.winfo_screenwidth()/2)),height=root.winfo_screenheight()-148)
FtFrame.place(x=10, y=70)
FtWin = ScrolledWindow(FtFrame, width=((root.winfo_screenwidth()/2)-50), height=root.winfo_screenheight()-148)
FtWin.place(x=0,y=0)
Twin = FtWin.window
Twin.config(bg=defcol)

FrFrame = Frame(width=((root.winfo_screenwidth()/2)),height=root.winfo_screenheight()-148)
FrFrame.place(x=((root.winfo_screenwidth()/2)-20), y=70)
FrWin = ScrolledWindow(FrFrame, width=((root.winfo_screenwidth()/2)), height=root.winfo_screenheight()-148)
FrWin.place(x=0,y=0)
Rwin = FrWin.window
Rwin.config(bg=defcol)

root.mainloop() 

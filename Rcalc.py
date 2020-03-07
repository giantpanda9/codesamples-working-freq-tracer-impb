#-*-coding: utf-8 -*-
from Tkinter import *
from Tix import *
from tkMessageBox import *
import math
from transceiver12 import radio
import string
import datetime

FtEntryLST = {}
FtPWLST = {}
FtNLST ={}
FtdFLST={}
FtFrmLST={}
deltaFT=[1.0,4.5,5.4,33]
deltaFR=[1.0,5.3,6.7,6.5,7.2]
ib=0

def Quit():
    global root
    root.destroy()
    
def printme(ev):
	print ev.widget

def addF(ev):
	global ib
	ib=ib+1	
	qtyTRvar.set(str(ib))
	tmp1=Frame(win,width=210,height=20)
	tmp1.pack()
	FtFrmLST[ib]=tmp1
	tmp = Spinbox(tmp1,width=8,format="%3.4f",from_=000.0003, to=999.9999, increment=0.0125)
	tmp.bind('<KeyRelease>', maxsym)
	tmp.place(x=0,y=0)
	FtEntryLST[ib] = tmp
	tmp = Spinbox(tmp1,width=3, state="readonly",from_=40,to=60)
	tmp.place(x=80,y=0)
	FtPWLST[ib] = tmp
	tmp = Spinbox(tmp1,width=3,state="readonly", from_=1,to=5)
	tmp.insert(0,'1')
	tmp.place(x=120,y=0)
	FtNLST[ib] = tmp
	tmp = Spinbox(tmp1,width=3,state="readonly", from_=1,to=4)
	tmp.place(x=160,y=0)
	FtdFLST[ib] = tmp
	
def CountIt():
	
	if ib <=0:
		showerror("Ошибка!", "Не указаны мешающие передатчики!")
		return 0
	startRF=recvEntry.get()
	startRF=startRF.replace(',','.')
	endRF=recvEntry1.get()
	endRF=endRF.replace(',','.')
	try:
		a=float(startRF)/3
		a=float(endRF)/3
	except:
		showerror("Ошибка!", "Диапазон частот передатчика введен неверено!")
		recvEntry.insert(0,'000.0003')
		recvEntry.delete ('8',END)
		recvEntry1.insert(0,'000.0125')
		recvEntry1.delete ('8',END)
		return 0
	

	if endRF <= startRF:
		showerror("Ошибка!", "Диапазон частот передатчика введен неверено!")
		return 0
	qTrans=0
	tLST = ["Transceiver List",]
	for i in range(1,len(FtEntryLST)+1):
		tmp = FtEntryLST[i].get()
		tmp=tmp.replace(',','.')
		try:
			
			a=float(tmp)/3
			tLST.append(radio(float(tmp)))
			qTrans=qTrans+1
		except:
			print "Error!"
	
	
	goodRLST ={}
	badRLST = ['',]	
	goodFLST = ['WorkF',]
	badFLST = {}
	badFLST1 = {}
	rangeRLST={}
	subPP={}
	subPPsorted=[]
	freqTUP={}
	stepF=0.0125
	stepFi=0
	blfLb.delete(0,END)
	startRF=float(startRF)
	endRF=float(endRF)	
	recvF1=startRF
	#harmonic=1

	while recvF1 <= endRF:
		rangeRLST[stepFi]=recvF1
		badFLST[recvF1]=''
		stepFi=stepFi+1
		recvF1=recvF1+stepF
	
	for recvFs in range (0,len(rangeRLST)):
		recv1=radio(float(rangeRLST[recvFs]))
		if StdVar.get() != 1:
			recv1.harmonic=int(RdfVar.get())
			recv1.deltaF=deltaFR[recv1.harmonic-1]
			recv1.cntN=int(RNVar.get())
			recv1.power=int(RpowVar.get())
			recv1.antennaGain=int(GVar.get())
			recv1.Qfactor=int(QVar.get())
			recv1.rebuild()
		
		#harmonic=recv1.harmonic
		for i in range(1,len(tLST)):
			if StdVar.get() !=1:
				r1=i*int(deltaRVar.get())
				tLST[i].harmonic=int(FtdFLST[i].get())
				tLST[i].deltaF=deltaFT[tLST[i].harmonic-1]
				tLST[i].cntN=int(FtNLST[i].get())
				tLST[i].power=int(FtPWLST[i].get())
				tLST[i].radius=r1
				tLST[i].rebuild()
				recv1.radius=r1
				recv1.rebuild()
		
			Pt1=10*math.log10(tLST[i].power)
	
			
			Pn=Pt1+tLST[i].antennaGain+recv1.antennaGain+tLST[i].Kfactor-tLST[i].alpha-recv1.alpha-tLST[i].LR-tLST[i].B
			Pr1=10*math.log10(recv1.power)
			Pnr=Pr1+tLST[i].antennaGain+recv1.antennaGain+tLST[i].Kfactor-tLST[i].alpha-recv1.alpha-tLST[i].LR-recv1.B
			
			
			#print 'Без учёта положения: Pпрм' + str(i) + ':Pпрд' + str(recvFs) + '<=>' + str(Pn) + ':' + str(Pnr)	
			if LRSVar.get()==1:
				if recv1.freq>tLST[i].freq:

						if Pn > Pnr:
							badFLST[recv1.freq]=str(badFLST[recv1.freq])+str(tLST[i].freq)+'<br>'
							badFLST1[recv1.freq]=tLST[i].freq
							subPP[recv1.freq]=(abs(Pnr-Pn))
							subPPsorted.append(abs(Pnr-Pn))
							freqTUP[recv1.freq]=tLST[i].freq
							
						else:	
							if str(tLST[i].freq) not in goodFLST:
								goodFLST.append(str(tLST[i].freq))
				else:

						if abs(Pn) > abs(Pnr):
							badFLST[recv1.freq]=str(badFLST[recv1.freq])+str(tLST[i].freq)+'<br>'
							badFLST1[recv1.freq]=tLST[i].freq
							subPP[recv1.freq]=(abs(Pnr-Pn))
							subPPsorted.append(abs(Pnr-Pn))
							freqTUP[recv1.freq]=tLST[i].freq
					
						else:	
							if str(tLST[i].freq) not in goodFLST:
								goodFLST.append(str(tLST[i].freq))
			else:	
				
				if Pn > Pnr:
					badFLST[recv1.freq]=str(badFLST[recv1.freq])+str(tLST[i].freq)+'<br>'
					badFLST1[recv1.freq]=tLST[i].freq
					subPP[recv1.freq]=(abs(Pnr-Pn))
					subPPsorted.append(abs(Pnr-Pn))
					freqTUP[recv1.freq]=tLST[i].freq
					
				else:	
					if str(tLST[i].freq) not in goodFLST:
						goodFLST.append(str(tLST[i].freq))
	tmpTRvar=int(qtyTRvar.get())
	if (SubSpVar.get())==1 and tmpTRvar>=2:			
		subPPsorted.sort()
		#print harmonic
		subPPcut=subPPsorted[0:tmpTRvar:1]
	
		for i in subPPcut:
			for key,val in subPP.items():
				#print str(key) + ',' + str(val)
				if i != val:
					if str(badFLST1[key]) not in goodFLST:
						goodFLST.append(str(badFLST1[key]))
					for key1 in badFLST.keys():
						badFLST[key1]=badFLST[key1].replace(str(badFLST1[key]),'')
					
				
	
	for i in range(1,len(goodFLST)):			
		blfLb.insert(END, goodFLST[i])

	dtt = datetime.datetime.now()
	dtt = str(dtt.strftime('%d.%m.%Y - %H:%M:%S'))
	reportData='<html><head><title>Отчёт о работе программы расчёта интермодуляционных помех блокирования по диапазону частот приёмника</title></head><body><right>Дата и время создания отчёта: '+dtt+'</right><br><center><a name="#menu"><u>Оглавление:</u></a><br><br><a href="#blockF">Блокирующие частоты</a><br><a href="#workF">Рабочие частоты</a><br></center><br><a name="blockF"><center><u>Блокирующие частоты:</u></center></a><br><br><a href="#menu">Вернуться к оглавлению</a><br><br>'
	
	
	reportData=reportData+'<table border=0>'

	for key, val in badFLST.items():
		
		if val!='':
			reportData=reportData+'<tr><th>'+str(key)+'</th</tr><tr><td></td><td>'+str(val)+'</td></tr>'
			
		
	reportData=reportData+'</table><br><br><a href="#menu">Вернуться к оглавлению</a><br><br><a name="workF"><center><u>Рабочие частоты:</center></u></a><br><br><a href="#menu">Вернуться к оглавлению</a><br><br>'

	
	reportData=reportData+'<table border=0>'
	reportData=reportData+'<tr><th>'+str(startRF)+'</tr></th>'
	for i in range(1,len(goodFLST)):
		reportData=reportData+'<tr><th></th><th></th></tr><tr><td></td><td>'
		reportData=reportData+goodFLST[i]+'</td></tr>'
	reportData=reportData+'<tr><th>'+str(endRF)+'</tr></th>'	
	reportData=reportData+'</td></tr></table><br><br><a href="#menu">Вернуться к оглавлению</a><br><br></body></html>'
	
	open("report-range.htm", "w").write(reportData.decode('utf-8').encode('cp1251'))


def ClearAll():
	
	global ib
	ib=0
	for i in  range(1, len(FtEntryLST)+1):
		FtEntryLST[i].destroy()
		FtEntryLST.pop(i)
		FtPWLST[i].destroy()
		FtPWLST.pop(i)
		FtNLST[i].destroy()
		FtNLST.pop(i)
		FtdFLST[i].destroy()
		FtdFLST.pop(i)
		FtFrmLST[i].destroy()
		FtFrmLST.pop(i)
	recvEntry.insert(0,'000.0003')
	recvEntry.delete ('8',END)
	blfLb.delete(0,END)
 	qtyTRvar.set(str(ib))

def maxsym(ev):
	ev.widget.delete ('8',END)

def maxsyment(ev):
	recvEntry.delete ('8',END)
	recvEntry1.delete ('8',END)
	
def subF(ev):
	try:
		global ib
		FtEntryLST[ib].destroy()
		FtEntryLST.pop(ib)
		FtPWLST[ib].destroy()
		FtPWLST.pop(ib)
		FtNLST[ib].destroy()
		FtNLST.pop(ib)
		FtdFLST[ib].destroy()
		FtdFLST.pop(ib)
		FtFrmLST[ib].destroy()
		FtFrmLST.pop(ib)
		ib=ib-1
		qtyTRvar.set(str(ib))
	except:
		return 0

def aboutMe():
	showinfo(" О программе:", "Программист: Чегодаев Н.И.   \n-------------------------------------\nПрограмма основана\nна положениях\nинтерполяции Окамуры-Хата")

root = Tk()

root.wm_title("Многофакторная иммитационная модель ИМПБ")
root.wm_minsize(width=390,height=570)
root.wm_maxsize(width=390,height=570)

imm = Menu(root)
root.config(menu=imm)
fm = Menu(imm)
imm.add_cascade(label="Файл",menu=fm)
fm.add_command(label="Новый расчёт", command=ClearAll)
fm.add_command(label="Выход",command=Quit)

cm = Menu(imm)
imm.add_cascade(label="Модель",menu=cm)
cm.add_command(label="Рассчитать", command=CountIt)

am = Menu(imm)
imm.add_cascade(label="Информация",menu=am)
am.add_command(label="О программе", command=aboutMe)

recvFrame = Frame(width = 370, height = 50)
recvFrame.place(x=0, y=10)

recvLbl=Label(recvFrame, text='Диапазон\nчастот приёмника:')
recvLbl.place(x=15, y=7)

recvEntry=Entry(recvFrame,width=8)
recvEntry.insert(0,'000.0003')
recvEntry.bind('<KeyRelease>', maxsyment)
recvEntry.place(x=150, y=10)

recvLbl=Label(recvFrame, text='-')
recvLbl.place(x=200, y=10)

recvEntry1=Entry(recvFrame,width=8)
recvEntry1.insert(0,'000.0125')
recvEntry1.bind('<KeyRelease>', maxsyment)
recvEntry1.place(x=210, y=10)

freqFrame = Frame(width = 390, height = 50)
freqFrame.place(x=0, y=50)

freqLbl=Label(freqFrame, text='Мешающие\nпередатчики:')
freqLbl.place(x=19, y=7)

blfLbl=Label(freqFrame, text="Рабочие\nчастоты:")
blfLbl.place(x=270,y=7)

addBtn = Button(freqFrame, text = '+', width=3)
addBtn.bind("<Button-1>", addF)
addBtn.place(x=100, y=10)

subBtn = Button(freqFrame, text = '-',width=3)
subBtn.bind("<Button-1>", subF)
subBtn.place(x=130, y=10)

qtyTRvar=StringVar()
qtyTRvar.set('0')
qtyTRLbl=Label(freqFrame, text='0', textvariable=qtyTRvar)
qtyTRLbl.place(x=230, y=25)

FtFrame = Frame(width=230,height=160)
FtFrame.place(x=10, y=100)
FtWin = ScrolledWindow(FtFrame, width=230, height=160)
FtWin.place(x=0,y=0)
win = FtWin.window

blfFrame=Frame(width=110, height=160)
blfFrame.place(x=250,y=100)

blfLb = Listbox(blfFrame,selectmode=SINGLE)
blfLb.place(x=0,y=0,width=110,height=160)
scrollbar = Scrollbar(blfLb)

scrollbar['command'] = blfLb .yview
blfLb ['yscrollcommand'] = scrollbar.set
scrollbar.pack(side = 'right', fill = 'y')

optFrame=Frame(width=390,height=300)
optFrame.place(x=0, y=270)

RoptLbl=Label(optFrame, text='Параметры ПРМ:')
RoptLbl.place(x=0,y=0)

RpowVar = IntVar()
Rpow = Scale(optFrame, variable = RpowVar, orient=HORIZONTAL, label='Pполезное:',from_=30,to=60)
Rpow.place(x=0,y=20)

RNVar = IntVar()
RN = Scale(optFrame, variable = RNVar, orient=HORIZONTAL, label='N-каскадное:',from_=1, to=5)
RN.place(x=0,y=80)

RdfVar = IntVar()
Rdf = Scale(optFrame, variable = RdfVar, orient=HORIZONTAL, label='Дельта-F:', from_=1, to=5)
Rdf.place(x=0,y=140)

#--------------------------------------------------------------

RoptLbl=Label(optFrame, text='Общие параметры ПРМ-ПРД:')
RoptLbl.place(x=210,y=0)

deltaRVar = IntVar()
deltaR = Scale(optFrame, variable = deltaRVar, orient=HORIZONTAL, label='Дельта-R:',from_=1,to=10)
deltaR.place(x=210,y=20)

GVar = IntVar()
G = Scale(optFrame, variable = GVar, orient=HORIZONTAL, label='G-антенны:',from_=0, to=3)
G.place(x=210,y=80)

QVar = IntVar()
Q = Scale(optFrame, variable = QVar, orient=HORIZONTAL, label='Q-контура:', from_=10, to=300)
Q.place(x=210,y=140)

addLbl=Label(optFrame, text='Дополнительные условия:')
addLbl.place(x=0,y=210)

LRSVar=IntVar()
LRSCheck=Checkbutton(optFrame, text="Учитывать взаиморасположение частот ПРМ-ПРД", onvalue=1, offvalue=0, variable=LRSVar)
LRSCheck.place(x=0,y=230)

SubSpVar=IntVar()
SubSpCheck=Checkbutton(optFrame, text="Произвести разностное уточнение результатов бинарного поиска", onvalue=1, offvalue=0, variable=SubSpVar)
SubSpCheck.place(x=0,y=250)

StdVar=IntVar()
SubSpCheck=Checkbutton(optFrame, text="Использовать стандартные значения параметров ПРМ-ПРД", onvalue=1, offvalue=0, variable=StdVar)
SubSpCheck.place(x=0,y=270)
root.mainloop() 
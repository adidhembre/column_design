from tkinter import *
from engine import Execute
from template import RectBiaxialReport
import datetime
import time
from tkinter import messagebox
import os
window = Tk()
window.title("Column Design")
window.geometry("500x350")
window.resizable(width=False, height=False)
Copyright = PanedWindow(window)
#Copyright.pack(side = "bottom",fill = 'x')
Inputmaster = PanedWindow(window,orient = "vertical")
#Inputmaster.pack(side = "left",fill='y')
Reportmaster = PanedWindow(window,orient = "vertical")
#Reportmaster.pack(side = "top")
Outputmaster = PanedWindow(window,orient = "vertical")
#Outputmaster.pack(side = "top")
Inputmaster.grid(row=0,column=0,rowspan=2,stick='nw')
Reportmaster.grid(row=0,column=1,stick='nw',padx=20)
Outputmaster.grid(row=1,column=1,stick='w',padx=20)
Copyright.grid(row=2,columnspan=2)

Lbl1 = StringVar(Inputmaster)
Lbl1.set("")
Lbl2 = StringVar(Inputmaster)
Lbl2.set("")
Lbl3 = StringVar(Inputmaster)
Lbl3.set("")
def preExecute(b,d,c,L,kx,kz,Fy_type,Fck,p,Mx,Mz,reinf_type,desgn_type):
    if float(b)==0 or float(d)==0 or float(Fck)==0:
        messagebox.showerror("Input Error", "B , D, Fck cannot be zero")
        return(None)
    global gettedvalue
    gettedvalue = Execute(b,d,c,L,kx,kz,Fy_type,Fck,p,Mx,Mz,reinf_type,desgn_type)
    if gettedvalue != None:
        Lbl1.set(gettedvalue[0])
        Lbl2.set(gettedvalue[1])
        Lbl3.set(gettedvalue[2])
        Lbl4 = gettedvalue[3]
        l1.config(fg=Lbl4)
        l2.config(fg=Lbl4)
        l3.config(fg=Lbl4)
def GetReport(b,D,c,L,kx,kz,Fy_type,Fck,p,Mx,Mz,reinf_type,desgn_1):
    preExecute(b,D,c,L,kx,kz,Fy_type,Fck,p,Mx,Mz,reinf_type,desgn_1)
    global Report
    if gettedvalue[4] != None:
        desgn = desgn_type.get()
        print(desgn)
        com = Com_N.get()
        pro = Pro_N.get()
        cli = Cli_N.get()
        col = Col_N.get()
        sldx = round(float(kx)*float(L)/float(D),2)
        sldz = round(float(kz)*float(L)/float(b),2)
        ex = max(round(float(L)/500+float(D)/30,2),20)
        ez = max(round(float(L)/500+float(b)/30,2),20)
        Mxe = round(float(p) * ex,2)/1000
        Mze = round(float(p) * ez,2)/1000
        FMx = max(float(Mx),Mxe)
        FMz = max(float(Mz),Mze)
        Ast = float(gettedvalue[4][0]) * float(b) * float(D) / 100
        xr = float(gettedvalue[4][2]) * float(b) * float(Fck) * float(D)**2 / 10**6
        zr = float(gettedvalue[4][3]) * float(D) * float(Fck) * float(b)**2 / 10**6
        Mxr = round(xr,2)
        Mzr = round(zr,2)
        intr = float(gettedvalue[4][2])
    if gettedvalue[4] != None:
        if desgn == "Biaxial":
            Report = RectBiaxialReport(com,pro,cli,col,b,D,c,L,kx,kz,
                                       p,Mx,Mz,Fck,Fy_type,reinf_type,
                                       desgn,sldx,sldz,ex,ez,Mxe,
                                       Mze,FMx,FMz,p,Ast,Mxr,Mzr,intr,Ast)
        elif desgn == "Uniaxial" and float(Mx) == 0:
            Report = RectBiaxialReport(com,pro,cli,col,b,D,c,L,kx,kz,
                                       p,Mx,Mz,Fck,Fy_type,reinf_type,
                                       desgn,sldx,sldz,"N.A",ez,"N.A",
                                       Mze,"N.A",FMz,p,Ast,"N.A",Mzr,"N.A",Ast)
        elif desgn == "Uniaxial" and float(Mz) == 0:
            Report = RectBiaxialReport(com,pro,cli,col,b,D,c,L,kx,kz,
                                       p,Mx,Mz,Fck,Fy_type,reinf_type,
                                       desgn,sldx,sldz,ex,"N.A",Mxe,
                                       "N.A",FMx,"N.A",p,Ast,Mxr,"N.A","N.A",Ast)
        elif desgn == "Axial":
            Report = RectBiaxialReport(com,pro,cli,col,b,D,c,L,kx,kz,
                                       p,Mx,Mz,Fck,Fy_type,reinf_type,
                                       desgn,sldx,sldz,"N.A","N.A","N.A",
                                       "N.A","N.A","N.A",p,Ast,Mxr,Mzr,"N.A",Ast)
        else:
            Report = None
    if Report != None:
        dirpath = os.getcwd()
        FMT = "%d %b, %Y-%H:%M:%S"
        time1 = datetime.datetime.now()
        file1 = open('Column Design.txt',"w")
        file1.write("Printing Report - {}\n".format(time1.strftime(FMT)))
        file1.write(Report)
        file1.close()
        os.startfile('{}\Column Design.txt'.format(dirpath), "print")
        time.sleep(1)
        os.remove('Column Design.txt')
    pass
Label(Inputmaster, text="B").grid(row=0,column=0)
b = Entry(Inputmaster,width=10)
b.insert(END,300)
b.grid(row=0,column=1)
Label(Inputmaster, text="mm").grid(row=0,column=2)
Label(Inputmaster, text="D").grid(row=1,column=0)
d = Entry(Inputmaster,width=10)
d.insert(END,600)
d.grid(row=1,column=1)
Label(Inputmaster, text="mm").grid(row=1,column=2)
Label(Inputmaster, text="d'").grid(row=2,column=0)
c = Entry(Inputmaster,width=10)
c.insert(END,50)
c.grid(row=2,column=1)
Label(Inputmaster, text="KN").grid(row=2,column=2)
Label(Inputmaster, text="L").grid(row=3,column=0)
L = Entry(Inputmaster,width=10)
L.insert(END,3000)
L.grid(row=3,column=1)
Label(Inputmaster, text="mm").grid(row=3,column=2)
Label(Inputmaster, text="kx").grid(row=4,column=0)
kx = Entry(Inputmaster,width=10)
kx.insert(END,1)
kx.grid(row=4,column=1)
Label(Inputmaster, text="kz").grid(row=5,column=0)
kz = Entry(Inputmaster,width=10)
kz.insert(END,1)
kz.grid(row=5,column=1)
Label(Inputmaster, text="Pu").grid(row=6,column=0)
p = Entry(Inputmaster,width=10)
p.insert(END,1000)
p.grid(row=6,column=1)
Label(Inputmaster, text="KN").grid(row=6,column=2)
Label(Inputmaster, text="Mux").grid(row=7,column=0)
Mx = Entry(Inputmaster,width=10)
Mx.insert(END,0)
Mx.grid(row=7,column=1)
Label(Inputmaster, text="KN.m").grid(row=7,column=2)
Label(Inputmaster, text="Muz").grid(row=8,column=0)
Mz = Entry(Inputmaster,width=10)
Mz.insert(END,0)
Mz.grid(row=8,column=1)
Label(Inputmaster, text="KN.m").grid(row=8,column=2)
Label(Inputmaster, text="Fck").grid(row=9,column=0)
Fck = Entry(Inputmaster,width=10)
Fck.insert(END,30)
Fck.grid(row=9,column=1)
Label(Inputmaster, text="N/Sq.mm").grid(row=9,column=2)
Fy_type = StringVar(Inputmaster)
Fy_list = (250, 415, 500)
Fy_type.set(415)
FyMenu = OptionMenu(Inputmaster, Fy_type, *Fy_list)
Label(Inputmaster, text="Fy").grid(row=10,column=0)
FyMenu.grid(row=10,column=1,sticky='w')
Label(Inputmaster, text="N/Sq.mm").grid(row=10,column=2)
reinf_type = StringVar(Inputmaster)
reinf_list = ("Equally Dist.", "Along B", "Along D")
reinf_type.set("Equally Dist.")
popupMenu = OptionMenu(Inputmaster, reinf_type, *reinf_list)
Label(Inputmaster, text="Reinf.").grid(row=11,column=0)
popupMenu.grid(row=11,column=1,sticky='w',columnspan=5)
desgn_type = StringVar(Inputmaster)
desgn_list = ("Axial", "Uniaxial", "Biaxial")
desgn_type.set("Biaxial")
desgnMenu = OptionMenu(Inputmaster, desgn_type, *desgn_list)
Label(Inputmaster, text="Design").grid(row=12,column=0)
desgnMenu.grid(row=12,column=1,sticky='w',columnspan=5)
x = Button(Inputmaster, text="Submit",
               command = lambda: preExecute(b.get(),d.get(),c.get(),L.get(),kx.get(),kz.get(),Fy_type.get(),Fck.get(),p.get(),Mx.get(),Mz.get(),reinf_type.get(),desgn_type.get()))
x.grid(row=13,columnspan=5)
b.focus()
l = Label(Outputmaster,text="Output Data :-")
l.grid(row=0,sticky='w')
l1 = Label(Outputmaster,textvariable=Lbl1)
l1.grid(row=1,sticky='w')
l2 = Label(Outputmaster,textvariable=Lbl2)
l2.grid(row=2,sticky='w')
l3 = Label(Outputmaster, textvariable=Lbl3)
l3.grid(row=3,sticky='w')
l4 = Label(Copyright, text="© Aditya Dhembre")
l4.pack(side="left")
Label(Reportmaster,text="Compony Name").grid(row=0,column=0,sticky='w')
Com_N = Entry(Reportmaster,width=30)
Com_N.grid(row=0,column=1,sticky='w')
Com_N.insert(END,"My Company")
Label(Reportmaster,text="Project Name").grid(row=1,column=0,sticky='w')
Pro_N = Entry(Reportmaster,width=30)
Pro_N.grid(row=1,column=1,sticky='w')
Label(Reportmaster,text="Client Name").grid(row=2,column=0,sticky='w')
Cli_N = Entry(Reportmaster,width=30)
Cli_N.grid(row=2,column=1,sticky='w')
Label(Reportmaster,text="Column Name").grid(row=3,column=0,sticky='w')
Col_N = Entry(Reportmaster,width=30)
Col_N.grid(row=3,column=1,sticky='w')
z = Button(Reportmaster, text="Print Report",
               command = lambda: GetReport(b.get(),d.get(),c.get(),L.get(),kx.get(),kz.get(),Fy_type.get(),Fck.get(),p.get(),Mx.get(),Mz.get(),reinf_type.get(),desgn_type.get()))
z.grid(row=4,columnspan=5)

window.mainloop()

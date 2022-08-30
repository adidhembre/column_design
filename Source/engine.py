import datetime
from tkinter import messagebox

###########   Stress Calculation   ###########
def GetSteelContribution(k,cover_coef,Fy,Fck):
    de = (1-2*cover_coef)
    s1 = 0.0035/k*(k-cover_coef)
    s2 = 0.0035/k*(k-cover_coef-de)
    y1 = 0.5-cover_coef
    y2 = 0.5-cover_coef-de
    fs1 = GetStreesInSteel(s1,Fy)
    fs2 = GetStreesInSteel(s2,Fy)
    fc1 = GetStreesInConc(s1,Fck)
    fc2 = GetStreesInConc(s2,Fck)
    fsc1 = fs1 - fc1
    fsc2 = fs2 - fc2
    fscy1 = fsc1 * y1
    fscy2 = fsc2 * y2
    x=GetAvgStressInSteel(k,cover_coef,Fy,Fck)
    fsc = x[0]
    fscy = x[1]
    return(fsc,fscy,fsc1,fscy1,fsc2,fscy2)
def GetStreesInConc(s,Fck):
    s = round(float(s),5)
    if s < 0:
        fc = 0
    if s >= 0.002:
        fc = 0.446 * Fck
    else:
        fc = 0.446 * Fck * (2*(s/0.002)-(s/0.002)**2)
    return(fc)
def GetAvgStressInSteel(k,cover_coef,Fy,Fck):
    de = (1-2*cover_coef)/10
    add_fsc = 0
    add_fscy = 0
    for i in range(0,11,1):
        s = 0.0035/k*(k-cover_coef-de*i)
        y = 0.5-cover_coef-de*i
        fs = GetStreesInSteel(s,Fy)
        fc = GetStreesInConc(s,Fck)
        fsc = fs - fc
        fscy = fsc*y
        add_fsc = add_fsc + fsc
        add_fscy = add_fscy + fsc*y
        if i == 10:
            avg_fsc = add_fsc/11
            avg_fscy = add_fscy/11
            return(avg_fsc,avg_fscy)
def GetStreesInSteel(s,Fy):
    s = float(s)
    if s == 0:
        fs1 = 0
        return(fs1)
    if Fy == 250:
        fs1 = s * 2*10**5
        if abs(fs1) < (0.87*Fy):
            return(fs1)
        if abs(fs1) >= (0.87*Fy):
            if s > 0:
                return(0.87*Fy)
            if s < 0:
                return(-0.87*Fy)
    if s < 0:
        fs1 = s * 2*10**5
        if abs(fs1) < (0.87*Fy):
            return(fs1)
        if abs(fs1) >= (0.87*Fy):
            return(-0.87*Fy)
    if s>0 and Fy != 250:
        if Fy == 415:
            if s < 0.00144:
                fs1 = s * 2*10**5
                return(fs1)
            elif s < 0.00163:
                fs1 = 306.7 - (0.00163-s)/0.00019 * 18.0
                return(fs1)
            elif s < 0.00192:
                fs1 = 324.8 - (0.00192-s)/0.00029 * 18.1
                return(fs1)
            elif s < 0.00241:
                fs1 = 342.8 - (0.00241-s)/0.00049 * 18.0
                return(fs1)
            elif  s <= 0.0038:
                fs1 = 360.9 - (0.0038-s)/0.00139 * 18.1
                return(fs1)
            else:
                print("DATA not found")
        elif Fy == 500:
            if s < 0.00174:
                fs1 = s * 2*10**5
                return(fs1)
            elif s < 0.00195:
                fs1 = 369.6 - (0.00195-s)/0.00021 * 21.8
                return(fs1)
            elif s < 0.00226:
                fs1 = 391.3 - (0.00226-s)/0.00031 * 21.7
                return(fs1)
            elif s <= 0.00277:
                fs1 = 413.0 - (0.00277-s)/0.00051 * 21.7
                return(fs1)
            elif  s <= 0.00417:
                fs1 = 434.8 - (0.00417-s)/0.0014 * 21.8
                return(fs1)
            else:
                print("DATA not found")
        else:
            print("This Grade of Reinforcement is not Included")
    else:
        print("Error Occured")

def GetSteelFactor(k,cover_coef,Fy,Fck,pt,Shape):
    x = GetSteelContribution(k,cover_coef,Fy,Fck)
    if Shape == "Equally Dist.":
        Cs = pt / Fck / 4 / 100 * (2*x[0]+x[2]+x[4])
        Csy = pt / Fck / 4 / 100 * (2*x[1]+x[3]+x[5])
        return(Cs,Csy)
    if Shape == "Along B":
        Cs = pt / Fck / 2 / 100 * (x[2]+x[4])
        Csy = pt / Fck / 2 / 100 * (x[3]+x[5])
        return(Cs,Csy)
    if Shape == "Along D":
        Cs = pt / Fck / 2 / 100 * (2*x[0])
        Csy = pt / Fck / 2 / 100 * (2*x[1])
        return(Cs,Csy)
def GetConcFactor(k,cover_coef):
    if k > 1:
        Cc = 0.446*(1-(4/21)*(4/(7*k-3))**2)
        Const = (0.5-8/49*(4/(7*k-3))**2)/(1-4/21*(4/(7*k-3))**2)
        Ccy = Cc * (0.5 - Const)
        return(Cc,Ccy)
    else:
        Cc = 0.36*k
        Ccy = Cc*(0.5-0.42*k)
        return(Cc,Ccy)

###########   Calculating Factors   ###########
def GetFactors(k,kcritical,cover_coef,Fy,Fck,pt,Shape):  
    if kcritical < k < 1.2:
        S = GetSteelFactor(k,cover_coef,Fy,Fck,pt,Shape)
        C = GetConcFactor(k,cover_coef)
        pfactor = C[0] + S[0]
        mfactor = C[1] + S[1]
        return(pfactor,mfactor)
def GetAxialFactors(Fy,Fck,pt):
    pfactor = 0.4 + pt/Fck/100*(0.67*Fy-0.4*Fck)
    mfactor = 0.02 + 0.05 * pt/Fck/100*(0.67*Fy-0.4*Fck)
    return(pfactor,mfactor)

###########   Calculating Time   ###########
def GetTimeLag(StartTime,EndTime):
    FMT = "%H:%M:%S:%f"
    StartTimeH = StartTime.strftime(FMT)
    EndTimeH = EndTime.strftime(FMT)
    TimeLag = EndTime.strptime(EndTimeH,FMT) - StartTime.strptime(StartTimeH,FMT)
    return("Time taken = {}".format(TimeLag))

###########   Perform Calculations   ###########
def GetActualFactors(kcr,c,Fy,Fck,pt,Shape,Preq,Mreq):
    start = int(round(kcr*100,0))
    inc = int(round((120-start)/100))
    end = start + inc * 100
    for i in range (start,end,inc):
        k = i / 100
        f = GetFactors(k,kcr,c,Fy,Fck,pt,Shape)
        if f != None:
            if Preq <= f[0] and Mreq <= f[1]:
                return(f)
def GetAlpha(Preq,Fy,Fck,pt):
    Puz = 0.45+pt/Fck/100*(0.75*Fy-0.45*Fck)
    a = Preq/Puz
    if a <= 0.2:
        return(1.0)
    elif a >= 0.8:
        return(2.0)
    else:
        return(2-(0.8-a)/(0.8-0.2))
    
def Design(b,D,c,L,kx,kz,Fy,Fck,Pu,Mux,Muz,Shapex,Shapez):
    cx = c / D
    cz = c / b
    kxcr = (1-cx)/((0.002+0.87*Fy/2/10**5)/0.0035+1)
    kzcr = (1-cz)/((0.002+0.87*Fy/2/10**5)/0.0035+1)
    Kxeff = (1-cx)/((0.87*Fy/2/10**5)/0.0035+1)
    Kzeff = (1-cz)/((0.87*Fy/2/10**5)/0.0035+1)
    Preq = Pu/Fck/b/D * 1000
    Mxreq = Mux/Fck/b/D**2*1000000
    Mzreq = Muz/Fck/D/b**2*1000000       
    for i in range (80, 600):
        pt = i/100
        Axial = GetAxialFactors(Fy,Fck,pt)
        if Preq > Axial[0]:
            continue
        else:
            if Mxreq <= Axial[1] and Mzreq <= Axial[1]:
                a = GetAlpha(Preq,Fy,Fck,pt)
                const = (Mxreq/Axial[1])**a + (Mzreq/Axial[1])**a
                if const <= 1.0:
                    return(pt,const,Axial[1],Axial[1])
                else:
                    continue
            else:
                Mxf = GetFactors(Kxeff,kxcr,cx,Fy,Fck,pt,Shapex)
                Mzf = GetFactors(Kzeff,kzcr,cz,Fy,Fck,pt,Shapez)
                if Mxreq > Mxf[1] or Mzreq > Mzf[1]:
                    continue
                else:
                    x = GetActualFactors(kxcr,
                                         cx,Fy,Fck,pt,Shapex,Preq,Mxreq)
                    z = GetActualFactors(kzcr,
                                         cz,Fy,Fck,pt,Shapez,Preq,Mzreq)
                    if x == None or z == None:
                        continue
                    else:
                        if Mxreq == 0 or Mzreq == 0:
                            a = 1
                        else:
                            a = GetAlpha(Preq,Fy,Fck,pt)
                        const = (Mxreq/x[1])**a + (Mzreq/z[1])**a
                        if const <=1.0:
                            return(pt,const,x[1],z[1])
                        else:
                            continue
    
def PerformDesign(b,D,c,L,kx,kz,Fy,Fck,Pu,Mux,Muz,Shape,desgn):
    if Shape == "Equally Dist.":
        Shapex = Shape
        Shapez = Shape
    elif Shape == "Along B":
        Shapex = Shape
        Shapez = "Along D"
    elif Shape == "Along D":
        Shapex = Shape
        Shapez = Shape
    sldx = kx * L / D
    sldz = kz * L / b
    if sldx > 12 or sldz > 12:
        messagebox.showinfo("Section is Slender", "Sorry but I am Unable to design Slender Column")
        return(None)
    if desgn == "Axial":
        if Mux > 0 or Muz > 0:
            messagebox.showerror("Only Axial Forces Allowed", "Please Check Moments")
            return(None)
        else:
            return(Design(b,D,c,L,kx,kz,Fy,Fck,Pu,0,0,Shapex,Shapez))
    if desgn == "Uniaxial":
        if Mux == 0 and Muz > 0:
            ezmin = max(L / 500 + b / 30,20)
            M_for_ez = Pu * ezmin / 1000
            Mz_max = max(M_for_ez,Muz)
            return(Design(b,D,c,L,kx,kz,Fy,Fck,Pu,0,Mz_max,Shapex,Shapez))
        if Muz == 0 and Mux > 0:
            exmin = max(L / 500 + D / 30,20)
            M_for_ex = Pu * exmin / 1000
            Mx_max = max(M_for_ex,Mux)
            return(Design(b,D,c,L,kx,kz,Fy,Fck,Pu,Mx_max,0,Shapex,Shapez))
        if Mux == 0 and Muz == 0:
            messagebox.showerror("Uniaxial Moment", "All Moment Cannot be zero")
            return(None)
        else:
            messagebox.showerror("Uniaxial Moment", "Please Make 1 moment as zero")
            return(None)
    if desgn == "Biaxial":
        ezmin = max(L / 500 + b / 30,20)
        M_for_ez = Pu * ezmin / 1000
        Mz_max = max(M_for_ez,Muz)
        exmin = max(L / 500 + D / 30,20)
        M_for_ex = Pu * exmin / 1000
        Mx_max = max(M_for_ex,Mux)
        return(Design(b,D,c,L,kx,kz,Fy,Fck,Pu,Mx_max,Mz_max,Shapex,Shapez))
    else:
        messagebox.showerror("Undefined Error", "Please contact designer")
        return(None) 

###########   Execution   ###########
def display(Inputmaster):
    Label(Inputmaster,text=Lbl1.get()).grid(row=14,columnspan=5)
    Label(Inputmaster,text=Lbl2.get()).grid(row=15,columnspan=5)
def Execute(b,d,c,l,klx,klz,Fy,Fck,p,Mx,Mz,reinf_type,design_type):
    try:
        b = float(b)
        d = float(d)
        c = float(c)
        L = float(l)
        kx = float(klx)
        kz = float(klz)
        Fy = int(Fy)
        Fck = float(Fck)
        p = float(p)
        Mx = float(Mx)
        Mz = float(Mz)
        Shape = reinf_type
        desgn = design_type
        chkd = True
    except ValueError:
        chkd = False
        messagebox.showerror("Value Error", "Please Check Input Data")
        return(None)
    if chkd == True:
        global Lbl1 , Lbl2 , Lbl3
        StartTime = datetime.datetime.now()
        x = PerformDesign(b,d,c,L,kx,kz,Fy,Fck,p,Mx,Mz,Shape,desgn)
        if x != None:
            Lbl1=("Required Reinforcement is {}%".format(x[0]))
            Lbl2=("Interaction ratio is {}".format(round(x[1],2)))
            Lbl3 = "Green"
        else:
            Lbl1 = ("Redesign Section")
            Lbl2 = ("Or Check Input Data")
            Lbl3 = "Red"
        EndTime = datetime.datetime.now()
        time = (GetTimeLag(StartTime,EndTime))
        return(Lbl1,Lbl2,str(time),Lbl3,x)
    
        


def RectBiaxialReport(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,
                      v11,v12,v13,v14,v15,v16,v17,v18,
                      v19,v20,v21,v22,v23,v24,v25,v26,
                      v27,v28,v29,v30,v31):
    x = '''************************************************
**************   Column  Design   **************
************************************************

Basic Info >>>

Compony Name	=	{}
Project Name	=	{}
Client Name	=	{}
Column Name	=	{}

Input...

width		=	{}	mm
Depth		=	{}	mm
Eff. Cover	=	{}	mm
Uns. Length	=	{}	mm
Kx		=	{}	
kz		=	{}
Axial Force	=	{}	KN
Moment in x	=	{}	KN.m
Moment in z	=	{}	KN.m
Conc. Grade	=	M{}
Steel Grade	=	Fe{}
Reinf. Type	=	{}
Design as	=	{}

Solution >>>

1) Check for Slender
	Le/D = {} < 12
	Le/b = {} < 12
	Hence Column is Short

2) Minimum Eccenrticity
	emin = max(L/500 + D/30,20) mm
	ex,min = {} mm
	ez,min = {} mm
	Mx_for_ex = {} KN.m
	Mz_for_ez = {} KN.m

3) Final Forces
	M 	= max(M_for_e, Mu)
	Mx 	= {} KN.m
	Mz	= {} KN.m
	P	= {} KN
	
4) Area of Steel required
	Ast = max(Ast.req , Ast.min) < Ast,max
	Ast = {} Sq.mm

5) Check
	Mxr 	= {} KN.m > Mux...Ok
	Mzr 	= {} KN.m > Muz...Ok
	Interaction ratio

	(Mxu/Mxr)^a + (Mzu/Mzr)^a = {} <= 1
	
	Hence OK.

Output >>>

Provide {} Sq.mm Reinforcement.

************************************************
© RANCON Consultants'''.format(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,
                                          v11,v12,v13,v14,v15,v16,v17,v18,
                                          v19,v20,v21,v22,v23,v24,v25,v26,
                                          v27,v28,v29,v30,v31)

    return(x)

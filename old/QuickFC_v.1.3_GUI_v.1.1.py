
import customtkinter as ctk
import math
from tkinter import messagebox

ctk.set_appearance_mode('dark')

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('QuickFC v1.3')
        self.geometry('600x400')

        tabs = ctk.CTkTabview(self)
        tabs.pack(fill='both', expand=True, padx=10, pady=10)

        # Eluent predictor
        t1 = tabs.add('Eluent Predictor')
        self.ep_r1=ctk.CTkEntry(t1,placeholder_text='Current Rf')
        self.ep_p=ctk.CTkEntry(t1,placeholder_text='Pentane parts')
        self.ep_e=ctk.CTkEntry(t1,placeholder_text='EA parts')
        self.ep_r2=ctk.CTkEntry(t1,placeholder_text='Target Rf')
        for w in (self.ep_r1,self.ep_p,self.ep_e,self.ep_r2): w.pack(fill='x',padx=10,pady=4)
        self.ep_out=ctk.CTkTextbox(t1,height=100); self.ep_out.pack(fill='both',expand=True,padx=10,pady=5)
        ctk.CTkButton(t1,text='Calculate',command=self.eluent_predictor).pack(pady=5)

        # Flash column
        t2=tabs.add('Flash Column')
        self.fc_mode=ctk.StringVar(value='known')
        ctk.CTkRadioButton(t2,text='Known column size',variable=self.fc_mode,value='known').pack(anchor='w')
        ctk.CTkRadioButton(t2,text='Unknown column size',variable=self.fc_mode,value='unknown').pack(anchor='w')
        self.fc_m=ctk.CTkEntry(t2,placeholder_text='Sample mass (mg)')
        self.fc_rf=ctk.CTkEntry(t2,placeholder_text='Lowest Rf')
        self.fc_d=ctk.CTkEntry(t2,placeholder_text='Diameter mm (known mode)')
        self.fc_drf=ctk.CTkEntry(t2,placeholder_text='dRf (unknown mode)')
        self.fc_l=ctk.CTkEntry(t2,placeholder_text='Length cm')
        for w in (self.fc_m,self.fc_rf,self.fc_d,self.fc_drf,self.fc_l): w.pack(fill='x',padx=10,pady=3)
        self.fc_out=ctk.CTkTextbox(t2,height=120); self.fc_out.pack(fill='both',expand=True,padx=10,pady=5)
        ctk.CTkButton(t2,text='Calculate',command=self.flash_column).pack()

        # Prepare eluent
        t3=tabs.add('Prepare Eluent')
        self.pe_mode=ctk.StringVar(value='regular')
        ctk.CTkRadioButton(t3,text='Pentane / EA',variable=self.pe_mode,value='regular').pack(anchor='w')
        ctk.CTkRadioButton(t3,text='Custom mixture',variable=self.pe_mode,value='custom').pack(anchor='w')
        self.pe_p=ctk.CTkEntry(t3,placeholder_text='Pentane parts')
        self.pe_e=ctk.CTkEntry(t3,placeholder_text='EA parts')
        self.pe_v=ctk.CTkEntry(t3,placeholder_text='Volume')
        self.pe_custom=ctk.CTkTextbox(t3,height=80)
        self.pe_custom.insert('1.0','Pentane,7\nEthylacetate,3')
        for w in (self.pe_p,self.pe_e,self.pe_v): w.pack(fill='x',padx=10,pady=3)
        self.pe_custom.pack(fill='x',padx=10,pady=3)
        self.pe_out=ctk.CTkTextbox(t3,height=110); self.pe_out.pack(fill='both',expand=True,padx=10,pady=5)
        ctk.CTkButton(t3,text='Calculate',command=self.prepare_eluent).pack()

        # Change polarity
        t4=tabs.add('Change Polarity')
        self.cp_v1=ctk.CTkEntry(t4,placeholder_text='Current volume')
        self.cp_p1=ctk.CTkEntry(t4,placeholder_text='Current pentane parts')
        self.cp_e1=ctk.CTkEntry(t4,placeholder_text='Current EA parts')
        self.cp_p2=ctk.CTkEntry(t4,placeholder_text='Target pentane parts')
        self.cp_e2=ctk.CTkEntry(t4,placeholder_text='Target EA parts')
        self.cp_v2=ctk.CTkEntry(t4,placeholder_text='Target volume or min')
        for w in (self.cp_v1,self.cp_p1,self.cp_e1,self.cp_p2,self.cp_e2,self.cp_v2): w.pack(fill='x',padx=10,pady=2)
        self.cp_out=ctk.CTkTextbox(t4,height=120); self.cp_out.pack(fill='both',expand=True,padx=10,pady=5)
        ctk.CTkButton(t4,text='Calculate',command=self.change_polarity).pack()

        t5=tabs.add('About')
        ctk.CTkLabel(t5,text='QuickFC v1.3\nFlash Column Chromatography Calculator\n© Dmitrii Ladan').pack(pady=20)

    def eluent_predictor(self):
        r1=float(self.ep_r1.get()); p1=float(self.ep_p.get()); e1=float(self.ep_e.get()); r2=float(self.ep_r2.get())
        x=-e1/((e1+p1)*math.log(1-r1)); u2=-x*math.log(1-r2)
        if u2<=0.5:
            p=1/u2-1; e=1
        else:
            x=-p1/((e1+p1)*math.exp(1-r1)); u2=-x*math.exp(1-r2); p=1; e=1/u2-1
        self.ep_out.delete('1.0','end'); self.ep_out.insert('end',f'Use ratio:\nPentane {p:.0f}\nEA {e:.0f}')

    def flash_column(self):
        rf=float(self.fc_rf.get()); L=float(self.fc_l.get())
        if self.fc_mode.get()=='known':
            D=float(self.fc_d.get())
        else:
            m=float(self.fc_m.get()); drf=float(self.fc_drf.get())
            D=m/(2*math.sqrt(m/10))*0.1/(drf**(1+1.5*(drf-0.1)))
        ms=((D/20)**2)*3.14*L*0.5
        vd=((1-0.5/2.5)*((D/20)**2)*3.14*L)*1.5/rf
        self.fc_out.delete('1.0','end'); self.fc_out.insert('end',f'Diameter: {D:.0f} mm\nSilica: {ms:.0f} g\nEluent: {vd:.0f} ml')

    def prepare_eluent(self):
        self.pe_out.delete('1.0','end')
        v=float(self.pe_v.get())
        if self.pe_mode.get()=='regular':
            p=float(self.pe_p.get()); e=float(self.pe_e.get())
            self.pe_out.insert('end',f'Pentane: {v*p/(p+e):.0f}\nEA: {v*e/(p+e):.0f}')
        else:
            rows=[x for x in self.pe_custom.get('1.0','end').splitlines() if x.strip()]
            vals=[]; names=[]
            for r in rows:
                n,p=r.split(',')
                names.append(n); vals.append(float(p))
            total=sum(vals)
            for n,p in zip(names,vals):
                self.pe_out.insert('end',f'{n}: {v*p/total:.0f}\n')

    def change_polarity(self):
        v1=float(self.cp_v1.get()); p1=float(self.cp_p1.get()); e1=float(self.cp_e1.get())
        p2=float(self.cp_p2.get()); e2=float(self.cp_e2.get())
        v2=self.cp_v2.get().strip()
        if v2.lower()=='min':
            pent=((v1*p2/(p2+e2)-v1*p1/(p1+e1))/(1-p2/(p2+e2))) if e2/(e2+p2)<e1/(e1+p1) else 0
            ea=((v1*e2/(p2+e2)-v1*e1/(p1+e1))/(1-e2/(p2+e2))) if e2/(e2+p2)>e1/(e1+p1) else 0
            total=v1+pent+ea
        else:
            v2=float(v2)
            pent=v2*p2/(p2+e2)-v1*p1/(p1+e1)
            ea=v2*e2/(p2+e2)-v1*e1/(p1+e1)
            total=v1+pent+ea
        self.cp_out.delete('1.0','end')
        self.cp_out.insert('end',f'Add Pentane: {pent:.0f}\nAdd EA: {ea:.0f}\nFinal Volume: {total:.0f}')

QuickFC().mainloop()

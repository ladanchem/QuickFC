import customtkinter as ctk, math
from tkinter import messagebox

ctk.set_appearance_mode('dark')

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('QuickFC GUI')
        self.geometry('950x750')
        tabs=ctk.CTkTabview(self)
        tabs.pack(fill='both',expand=True,padx=10,pady=10)

        t1=tabs.add('Eluent Predictor')
        self.r1=ctk.CTkEntry(t1,placeholder_text='Current Rf')
        self.p1=ctk.CTkEntry(t1,placeholder_text='Pentane parts')
        self.e1=ctk.CTkEntry(t1,placeholder_text='EA parts')
        self.r2=ctk.CTkEntry(t1,placeholder_text='Target Rf')
        [w.pack(fill='x',padx=20,pady=5) for w in (self.r1,self.p1,self.e1,self.r2)]
        out1=ctk.CTkTextbox(t1,height=120); out1.pack(fill='both',expand=True,padx=20,pady=10)
        def calc1():
            r1=float(self.r1.get()); p1=float(self.p1.get()); e1=float(self.e1.get()); r2=float(self.r2.get())
            x=-e1/((e1+p1)*math.log(1-r1)); u2=-x*math.log(1-r2)
            if u2<=0.5: p=1/u2-1; e=1
            else: x=-p1/((e1+p1)*math.exp(1-r1)); u2=-x*math.exp(1-r2); p=1; e=1/u2-1
            out1.delete('1.0','end'); out1.insert('end',f'Pentane: {p:.0f}\nEA: {e:.0f}')
        ctk.CTkButton(t1,text='Calculate',command=calc1).pack()

        t2=tabs.add('Flash Column')
        self.m=ctk.CTkEntry(t2,placeholder_text='Sample mass mg')
        self.rf=ctk.CTkEntry(t2,placeholder_text='Lowest Rf')
        self.d=ctk.CTkEntry(t2,placeholder_text='Diameter mm')
        self.l=ctk.CTkEntry(t2,placeholder_text='Length cm')
        [w.pack(fill='x',padx=20,pady=5) for w in (self.m,self.rf,self.d,self.l)]
        out2=ctk.CTkTextbox(t2,height=180); out2.pack(fill='both',expand=True,padx=20,pady=10)
        def calc2():
            R=float(self.rf.get()); D=float(self.d.get()); L=float(self.l.get())
            ms=((D/20)**2)*3.14*L*0.5
            vd=((1-0.5/2.5)*((D/20)**2)*3.14*L)*1.5/R
            out2.delete('1.0','end'); out2.insert('end',f'Silica mass: {ms:.0f} g\nEluent volume: {vd:.0f} ml')
        ctk.CTkButton(t2,text='Calculate',command=calc2).pack()

        t3=tabs.add('Prepare Eluent')
        self.pp=ctk.CTkEntry(t3,placeholder_text='Pentane parts'); self.pp.pack(fill='x',padx=20,pady=5)
        self.ee=ctk.CTkEntry(t3,placeholder_text='EA parts'); self.ee.pack(fill='x',padx=20,pady=5)
        self.v=ctk.CTkEntry(t3,placeholder_text='Volume'); self.v.pack(fill='x',padx=20,pady=5)
        out3=ctk.CTkTextbox(t3,height=120); out3.pack(fill='both',expand=True,padx=20,pady=10)
        def calc3():
            p=float(self.pp.get()); e=float(self.ee.get()); v=float(self.v.get())
            out3.delete('1.0','end'); out3.insert('end',f'Pentane: {v*p/(p+e):.0f}\nEA: {v*e/(p+e):.0f}')
        ctk.CTkButton(t3,text='Calculate',command=calc3).pack()

if __name__=='__main__': QuickFC().mainloop()

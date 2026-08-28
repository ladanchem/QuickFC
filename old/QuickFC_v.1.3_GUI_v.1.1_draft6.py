import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickFC v.1.31")
        self.geometry("600x425")

        top=ctk.CTkFrame(self)
        top.pack(fill='x',padx=5,pady=5)
        self.content=ctk.CTkFrame(self)
        self.content.pack(fill='both',expand=True,padx=5,pady=5)
        self.pages={}
        names=['Eluent predictor (demo)','Running a flash column','Prepare eluent','About']
        for n in names:
            ctk.CTkButton(top,text=n,command=lambda x=n:self.show(x)).pack(side='left',padx=2)
            self.pages[n]=ctk.CTkFrame(self.content)

        self.build_predictor(); self.build_flash(); self.build_prepare(); self.build_about()
        self.show(names[0])

    def show(self,n):
        for p in self.pages.values(): p.pack_forget()
        self.pages[n].pack(fill='both',expand=True)

    def split(self,p):
        l=ctk.CTkFrame(p); r=ctk.CTkFrame(p)
        l.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        r.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        return l,r

    def build_predictor(self):
        l,r=self.split(self.pages['Eluent predictor (demo)'])
        self.ep=[]
        for t in ['Current Rf','Pentane parts','EA parts','Target Rf']:
            e=ctk.CTkEntry(l,placeholder_text=t); e.pack(fill='x',pady=2); self.ep.append(e)
        self.ep_out=ctk.CTkTextbox(r); self.ep_out.pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate',command=self.calc_ep).pack(side='bottom')

    def calc_ep(self):
        r1,p1,e1,r2=[float(x.get()) for x in self.ep]
        x=-e1/((e1+p1)*math.log(1-r1)); u2=-x*math.log(1-r2)
        if u2<=0.5: p=1/u2-1; e=1
        else: p=1; e=max(1/u2-1,1)
        self.ep_out.delete('1.0','end'); self.ep_out.insert('end',f'Pentane: {p:.0f}\nEA: {e:.0f}')

    def build_flash(self):
        l,r=self.split(self.pages['Running a flash column'])
        self.flash_mode=ctk.StringVar(value='known')
        ctk.CTkRadioButton(l,text='Known size',variable=self.flash_mode,value='known',command=self.flash_redraw).pack(anchor='w')
        ctk.CTkRadioButton(l,text='Unknown size',variable=self.flash_mode,value='unknown',command=self.flash_redraw).pack(anchor='w')
        ctk.CTkLabel(l,text='').pack()
        self.flash_body=ctk.CTkFrame(l); self.flash_body.pack(fill='both',expand=True)
        self.flash_entries={}
        self.flash_redraw()
        self.flash_out=ctk.CTkTextbox(r); self.flash_out.pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate',command=self.calc_flash).pack(side='bottom')

    def flash_redraw(self):
        for w in self.flash_body.winfo_children(): w.destroy()
        self.flash_entries={}
        fields=['Lowest Rf','Diameter','Length'] if self.flash_mode.get()=='known' else ['Sample mass','dRf','Lowest Rf','Length']
        for f in fields:
            e=ctk.CTkEntry(self.flash_body,placeholder_text=f); e.pack(fill='x',pady=2)
            self.flash_entries[f]=e

    def calc_flash(self):
        rf=float(self.flash_entries['Lowest Rf'].get())
        L=float(self.flash_entries['Length'].get())
        if self.flash_mode.get()=='known':
            D=float(self.flash_entries['Diameter'].get())
        else:
            m=float(self.flash_entries['Sample mass'].get())
            drf=float(self.flash_entries['dRf'].get())
            D=m/(2*math.sqrt(m/10))*0.1/(drf**(1+1.5*(drf-0.1)))
        ms=((D/20)**2)*3.14*L*0.5
        vd=((1-0.5/2.5)*((D/20)**2)*3.14*L)*1.5/rf
        self.flash_out.delete('1.0','end'); self.flash_out.insert('end',f'Diameter: {D:.0f} mm\nSilica: {ms:.0f} g\nEluent: {vd:.0f} ml')

    def build_prepare(self):
        l,r=self.split(self.pages['Prepare eluent'])
        self.major=ctk.StringVar(value='new')
        self.minor=ctk.StringVar(value='pea')

        # choice boxes at very top
        ctk.CTkRadioButton(l,text='Prepare from the beginning',variable=self.major,value='new',command=self.prepare_redraw).pack(anchor='w')
        ctk.CTkRadioButton(l,text='I already have eluent with the same components',variable=self.major,value='existing',command=self.prepare_redraw).pack(anchor='w')
        ctk.CTkLabel(l,text='').pack(pady=4)

        self.prepare_body=ctk.CTkFrame(l); self.prepare_body.pack(fill='both',expand=True)
        self.prepare_redraw()

        self.prepare_out=ctk.CTkTextbox(r); self.prepare_out.pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate',command=self.calc_prepare).pack(side='bottom')

    def prepare_redraw(self):
        for w in self.prepare_body.winfo_children(): w.destroy()
        self.custom_rows=[]
        if self.major.get()=='new':
            ctk.CTkRadioButton(self.prepare_body,text='Pentane / EA',variable=self.minor,value='pea',command=self.prepare_redraw).pack(anchor='w')
            ctk.CTkRadioButton(self.prepare_body,text='Custom mixture',variable=self.minor,value='custom',command=self.prepare_redraw).pack(anchor='w')
            ctk.CTkLabel(self.prepare_body,text='').pack(pady=4)
            if self.minor.get()=='pea':
                self.p=ctk.CTkEntry(self.prepare_body,placeholder_text='Pentane parts'); self.p.pack(fill='x')
                self.e=ctk.CTkEntry(self.prepare_body,placeholder_text='EA parts'); self.e.pack(fill='x')
                self.v=ctk.CTkEntry(self.prepare_body,placeholder_text='Volume'); self.v.pack(fill='x')
            else:
                self.rows_frame=ctk.CTkFrame(self.prepare_body); self.rows_frame.pack(fill='x')
                for _ in range(2): self.add_row()
                ctk.CTkButton(self.prepare_body,text='Add',command=self.add_row).pack()
                self.cv=ctk.CTkEntry(self.prepare_body,placeholder_text='Volume'); self.cv.pack(fill='x')
        else:
            self.ev1=ctk.CTkEntry(self.prepare_body,placeholder_text='Current volume'); self.ev1.pack(fill='x')
            self.ep1=ctk.CTkEntry(self.prepare_body,placeholder_text='Current Pentane'); self.ep1.pack(fill='x')
            self.ee1=ctk.CTkEntry(self.prepare_body,placeholder_text='Current EA'); self.ee1.pack(fill='x')
            self.ep2=ctk.CTkEntry(self.prepare_body,placeholder_text='Target Pentane'); self.ep2.pack(fill='x')
            self.ee2=ctk.CTkEntry(self.prepare_body,placeholder_text='Target EA'); self.ee2.pack(fill='x')
            row=ctk.CTkFrame(self.prepare_body); row.pack(fill='x')
            self.vol=ctk.CTkEntry(row,placeholder_text='Target volume'); self.vol.pack(side='left',fill='x',expand=True)
            self.minv=ctk.BooleanVar()
            def tgl():
                if self.minv.get(): self.vol.pack_forget()
                else: self.vol.pack(side='left',fill='x',expand=True)
            ctk.CTkCheckBox(row,text='Minimum',variable=self.minv,command=tgl).pack(side='left')

    def add_row(self):
        if len(self.custom_rows)>=5:return
        r=ctk.CTkFrame(self.rows_frame); r.pack(fill='x')
        n=ctk.CTkEntry(r,placeholder_text='Name'); n.pack(side='left',fill='x',expand=True)
        p=ctk.CTkEntry(r,placeholder_text='Parts',width=70); p.pack(side='left')
        self.custom_rows.append((n,p))

    def calc_prepare(self):
        self.prepare_out.delete('1.0','end')
        if self.major.get()=='new':
            if self.minor.get()=='pea':
                p=float(self.p.get()); e=float(self.e.get()); v=float(self.v.get())
                self.prepare_out.insert('end',f'Pentane: {v*p/(p+e):.0f}\nEA: {v*e/(p+e):.0f}')
            else:
                vol=float(self.cv.get()); total=sum(float(p.get()) for _,p in self.custom_rows if p.get())
                for n,p in self.custom_rows:
                    if n.get() and p.get():
                        self.prepare_out.insert('end',f'{n.get()}: {vol*float(p.get())/total:.0f}\n')
        else:
            v1=float(self.ev1.get()); p1=float(self.ep1.get()); e1=float(self.ee1.get())
            p2=float(self.ep2.get()); e2=float(self.ee2.get())
            if self.minv.get():
                pent=((v1*p2/(p2+e2)-v1*p1/(p1+e1))/(1-p2/(p2+e2))) if e2/(e2+p2)<e1/(e1+p1) else 0
                ea=((v1*e2/(p2+e2)-v1*e1/(p1+e1))/(1-e2/(p2+e2))) if e2/(e2+p2)>e1/(e1+p1) else 0
            else:
                v2=float(self.vol.get()); pent=v2*p2/(p2+e2)-v1*p1/(p1+e1); ea=v2*e2/(p2+e2)-v1*e1/(p1+e1)
            self.prepare_out.insert('end',f'Add Pentane: {pent:.0f}\nAdd EA: {ea:.0f}')

    def build_about(self):
        p=self.pages['About']
        ctk.CTkLabel(p,text='QuickFC v.1.31',font=('Arial',20,'bold')).pack(pady=10)
        ctk.CTkLabel(p,text='Flash Column Chromatography Calculator').pack()
        ctk.CTkLabel(p,text='© 2024-2026 Dmitrii Ladan\nAll rights reserved.').pack(pady=10)

QuickFC().mainloop()

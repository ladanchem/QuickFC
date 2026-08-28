import customtkinter as ctk
import math
from CTkToolTip import CTkToolTip

ctk.set_appearance_mode("dark")


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        background="transparent", relief="solid", borderwidth=1)
        label.pack()
    
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickFC v.1.41")
        self.geometry("600x470Calculate")
        self.resizable(False, False)

        top=ctk.CTkFrame(self)
        top.pack(fill='x',padx=5,pady=5)
        self.content=ctk.CTkFrame(self)
        self.content.pack(fill='both',expand=True,padx=5,pady=5)
        self.pages={}
        names=['Eluent prediction (demo)','Running a flash column','Prepare eluent','About']
        for n in names:
            ctk.CTkButton(top,text=n,command=lambda x=n:self.show(x)).pack(side='left',padx=2)
            self.pages[n]=ctk.CTkFrame(self.content)

        self.build_prediction(); self.build_flash(); self.build_prepare(); self.build_about()
        self.show(names[0])

    def show(self,n):
        for p in self.pages.values(): p.pack_forget()
        self.pages[n].pack(fill='both',expand=True)

    def split(self,p):
        l=ctk.CTkFrame(p); r=ctk.CTkFrame(p)
        l.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        r.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        l.configure(width=280)
        r.configure(width=320)
        l.pack_propagate(False)
        r.pack_propagate(False)
        return l,r








    def build_prediction(self):
        l, r = self.split(self.pages['Eluent prediction (demo)'])
        self.prediction_mode=ctk.StringVar(value='Eluent')
        ctk.CTkLabel(l,text='Eluent mixture').pack(pady=0)
        ctk.CTkRadioButton(l,text='Pentane / Ethylacetate',variable=self.prediction_mode,value='Eluent').pack(anchor='w',padx=(20,0),pady=(0,20))
        def add_field(name, description): 
            row=ctk.CTkFrame(l, fg_color='transparent')
            row.pack(fill='x', pady=2)
            e=ctk.CTkEntry(row, placeholder_text=name)
            e.pack(side='left', fill='x', expand=True, padx=(6,0))
            info=ctk.CTkButton(row, text='ⓘ', width=25, height=25, corner_radius=15)
            info.pack(side='right', padx=5)
            CTkToolTip(info, message=description, delay=0.1)
            e.bind('<Return>', lambda event: self.calc_ep())
            return e

        self.Rf = add_field('Rf', 'Rf, the Rf value of the purifying compound based on TLC (between 0.01 and 0.99)')
        self.Pentane = add_field('Pentane parts', 'Pentane parts, the number of pentane parts in the eluent which has been used')
        self.EA = add_field('Ethylacetate parts', 'Ethylacetate parts, the number of ethylacetate parts in the eluent which has been used')
        self.TargetRf = add_field('Target Rf', 'Target Rf, the desired Rf value (between 0.01 and 0.99)')
        self.ep_out = ctk.CTkTextbox(r)
        self.ep_out.pack(fill='both', expand=True)
        ctk.CTkButton(r, text='Calculate', command=self.calc_ep).pack(side='bottom', pady=(10,10))

    def calc_ep(self):
        Rf = float(self.Rf.get())
        P = float(self.Pentane.get())
        E = float(self.EA.get())
        tRf = float(self.TargetRf.get())
        self.ep_out.configure(font=("Arial", 15)); self.ep_out.delete('1.0','end');
        self.ep_out.insert('end', f'\nEntered data:\n\nRf = {Rf}\nPentane parts = {P}\nEthylacetate parts = {E}\nTarget Rf = {tRf}\n\n_________________________________')

        x = -E / ((E + P) * math.log(1 - Rf))
        U2 = -x * math.log(1 - tRf)
        if U2 <= 0.5:
            P2 = 1 / U2 - 1
            E2 = 1
            self.ep_out.insert('end', f'\n\n\n\nRecommended eluent:\n \nPentane: {P2:.0f}\nEthylacetate: {E2:.0f}')
        else:
            x = -P / ((E + P) * math.exp(1 - Rf))
            U2 = -x * math.exp(1 - tRf)
            P2 = 1
            E2 = 1 / U2 - 1
            self.ep_out.insert('end', f'\nRecommended eluent:\n \nPentane: {P2:.0f}\nEthylacetate: {E2:.1f}')







    def build_flash(self):
        l,r=self.split(self.pages['Running a flash column'])
        self.flash = []
        self.flash_mode=ctk.StringVar(value='known')
        ctk.CTkLabel(l,text='The column size is').pack(pady=0)
        ctk.CTkRadioButton(l,text='Known',variable=self.flash_mode,value='known',command=self.flash_redraw).pack(anchor='w',padx=(20,0),pady=(0,10))
        ctk.CTkRadioButton(l,text='Unknown',variable=self.flash_mode,value='unknown',command=self.flash_redraw).pack(anchor='w',padx=(20,0),pady=(0,20))
        self.flash_body=ctk.CTkFrame(l, fg_color="transparent"); self.flash_body.pack(fill='both',expand=True)
        self.flash_entries={}
        self.flash_redraw()
        self.flash_out=ctk.CTkTextbox(r); self.flash_out.pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate',command=self.calc_flash).pack(side='bottom',pady=(10,10))

    def flash_redraw(self):
        for w in self.flash_body.winfo_children(): w.destroy()
        def add_field(name, description, unit=""):
            row = ctk.CTkFrame(self.flash_body, fg_color="transparent")
            row.pack(fill='x', pady=2)
            e = ctk.CTkEntry(row, placeholder_text=name)
            e.pack(side='left', fill='x', expand=True, padx=(6,0))
            if unit:
                ctk.CTkLabel(row, text=unit, width=35).pack(side="left", padx=(0,5))
            info = ctk.CTkButton(row, text='ⓘ', width=25, height=25, corner_radius=15)
            info.pack(side='right', padx=5)
            CTkToolTip(info, message=description, delay=0.1)
            e.bind('<Return>', lambda event: self.calc_flash())
            return e
        if self.flash_mode.get() == 'known':
            self.Rfmin = add_field('Rfmin', 'Rfmin, the lowest Rf value of the purifying compound based on TLC (between 0.01 and 0.99)')
            self.D = add_field('Diameter', 'Diameter, the inner diameter of the column', 'mm')
            self.L = add_field('Length', 'Length, the length of the packed silica / the length of the column', 'cm')
        else:
            self.m = add_field('mass', 'mass, the mass of the crude sample to be purified', 'mg')
            self.dRf = add_field('dRf', 'dRf, the difference between the Rf values of the purifying compound and and nearest one')
            self.Rfmin = add_field('Rfmin', 'Rfmin, the lowest Rf value of the purifying compound based on TLC (between 0.01 and 0.99)')
            self.L = add_field('Length', 'Length, the length of the packed silica / the length of the column (if unknown, enter average value ≈25)', 'cm')

    def calc_flash(self):
        if self.flash_mode.get()=='known':
            Rfmin = float(self.Rfmin.get())
            D = float(self.D.get())
            L = float(self.L.get())
            self.flash_out.configure(font=("Arial", 15)); self.flash_out.delete('1.0','end');
            self.flash_out.insert('end', f'Entered data:\nRfmin = {Rfmin:.2f}\nDiameter = {D:.0f}mm\nLength = {L:.0f}cm\n_________________________________\n')
            Vc = math.pow((D / 20), 2) * 3.14 * L
            ms = Vc * 0.5
            Vsl = 2 * (1 - 0.5 / 2.5) * Vc
            Vd = ((1 - 0.5 / 2.5) * Vc) * 40 / (D * Rfmin) + Vsl
            Vw = ((1 - 0.5 / 2.5) * Vc) * 40 / (D * Rfmin)
            n1 = Vw / 10
            n2 = Vw / 20
            self.flash_out.insert('end',f'\nRecommended parameters:\n\nMass of silica: {ms:.0f}g\n\nDry silica loading:\nVolume of eluent for colomning: {Vd:.0f}ml\n\nWet silica loading:\nVolume of eluent for loading: {Vsl:.0f}ml\nVolume of eluent for colomning: {Vw:.0f}ml\n\nNumber of 10ml test tubes (small): {n1:.0f}pcs\nNumber of 20ml test tubes (large): {n2:.0f}pcs')
        else:
            m = float(self.m.get())
            dRf = float(self.dRf.get())
            Rfmin = float(self.Rfmin.get())
            L = float(self.L.get())
            self.flash_out.configure(font=ctk.CTkFont(family="Arial", size=15)); self.flash_out.delete('1.0','end');
            self.flash_out.insert('end', f'Entered data:\nm = {m:.0f}mg,  dRf = {dRf:.2f},  Rfmin = {Rfmin:.2f}\nL = {L:.0f}cm\n_________________________________\n')
            ms = m * 7/math.pow(dRf, 1.2) / 1000
            D = 20 * math.sqrt(ms / (0.5 * L * 3.14))
            Vc = math.pow((D / 20), 2) * 3.14 * L
            Vsl = 2 * (1 - 0.5 / 2.5) * Vc
            Vd = (1 - 0.5 / 2.5) * Vc * 40 / (D * Rfmin) + Vsl
            Vw = (1 - 0.5 / 2.5) * Vc * 40 / (D * Rfmin)
            n1 = Vw / 10
            n2 = Vw / 20
            self.flash_out.insert('end',f'\nRecommended parameters:\nDiameter (internal) = {D:.0f}mm\n\nMass of silica: {ms:.0f}g\n\nDry silica loading:\nVolume of eluent for colomning: {Vd:.0f}ml\n\nWet silica loading:\nVolume of eluent for loading: {Vsl:.0f}ml\nVolume of eluent for colomning: {Vw:.0f}ml\n\nNumber of 10ml test tubes (small): {n1:.0f}\nNumber of 20ml test tubes (large): {n2:.0f}')









    def build_prepare(self):
        l,r=self.split(self.pages['Prepare eluent'])
        self.major=ctk.StringVar(value='new')
        self.minor=ctk.StringVar(value='pea')
        # choice boxes at very top
        ctk.CTkRadioButton(l,text='Prepare new eluent',variable=self.major,value='new',command=self.prepare_redraw).pack(anchor='w',padx=(20,0),pady=(10,10))
        ctk.CTkRadioButton(l,text='Change polarity of the existing eluent',variable=self.major,value='existing',command=self.prepare_redraw).pack(anchor='w',padx=(20,0),pady=(0,20))
        self.prepare_body=ctk.CTkFrame(l, fg_color="transparent"); self.prepare_body.pack(fill='both',expand=True)
        self.prepare_redraw()
        self.prepare_out=ctk.CTkTextbox(r); self.prepare_out.pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate',command=self.calc_prepare).pack(side='bottom',pady=(10,10))
    def prepare_redraw(self):
        for w in self.prepare_body.winfo_children(): w.destroy()
        self.custom_rows = []
        def add_field(name, description, unit=""):
            row = ctk.CTkFrame(self.prepare_body, fg_color="transparent")
            row.pack(fill='x', pady=2)
            e = ctk.CTkEntry(row, placeholder_text=name)
            e.pack(side='left', fill='x', expand=True, padx=(6,0))
            if unit:
                ctk.CTkLabel(row, text=unit, width=35).pack(side="left", padx=(0,5))
            info = ctk.CTkButton(row,text='ⓘ',width=25,height=25,corner_radius=15)
            info.pack(side='right', padx=5)
            CTkToolTip(info, message=description, delay=0.1)
            e.bind('<Return>', lambda event: self.calc_prepare())
            return e
        if self.major.get() == 'new':
            ctk.CTkLabel(self.prepare_body, text='Eluent mixture').pack(pady=0)
            ctk.CTkRadioButton(self.prepare_body,text='Pentane / Ethylacetate',variable=self.minor,value='pea',command=self.prepare_redraw).pack(anchor='w', padx=(10,0), pady=(0,10))
            ctk.CTkRadioButton(self.prepare_body,text='Custom mixture',variable=self.minor,value='custom',command=self.prepare_redraw).pack(anchor='w', padx=(10,0), pady=(0,20))
            if self.minor.get() == 'pea':
                self.p = add_field('Pentane parts','Pentane parts, the desired number of pentane parts in the preparing eluent')
                self.e = add_field('Ethylacetate parts','Ethylacetate parts, the desired number of ethylacetate parts in the preparing eluent')
                self.v = add_field('Target Volume','Target Volume, total volume of the preparing eluent', 'ml')
            else:
                self.rows_frame = ctk.CTkFrame(self.prepare_body,fg_color="transparent")
                self.rows_frame.pack(fill='x')
                for _ in range(2):
                    self.add_row()
                ctk.CTkButton(self.prepare_body,text='Add',command=self.add_row).pack(pady=(7,10))
                self.cv = add_field('Target Volume','Volume, total volume of the preparing eluent', 'ml')
        else:
            self.prepare_mode=ctk.StringVar(value='Eluent')
            ctk.CTkLabel(self.prepare_body,text='Eluent mixture').pack(pady=0)
            ctk.CTkRadioButton(self.prepare_body,text='Pentane / Ethylacetate',variable=self.prepare_mode,value='Eluent').pack(anchor='w',padx=(20,0),pady=(0,20))
            self.ev1 = add_field('Volume','Volume, the volume of the existing eluent', 'ml')
            self.ep1 = add_field('Pentane parts','Pentane parts, the number of pentane parts in the existing eluent')
            self.ee1 = add_field('Ethylacetate parts','Ethylacetate parts, the number of ethylacetate parts in the existing eluent')
            self.ep2 = add_field('Target Pentane parts','Target Pentane parts, the number of pentane parts in the preparing eluent')
            self.ee2 = add_field('Target Ethylacetate parts','Target Ethylacetate parts, the number of ethylacetate parts in the preparing eluent')
            row = ctk.CTkFrame(self.prepare_body, fg_color="transparent")
            row.pack(fill='x', pady=2)

            # Left side: Target V + ml
            self.vol_row = ctk.CTkFrame(row, fg_color="transparent")
            self.vol_row.pack(side='left', fill='x', expand=True)
            self.vol = ctk.CTkEntry(self.vol_row, placeholder_text='Target V', width=80)
            self.vol.pack(side='left', padx=(6,0))
            ctk.CTkLabel(self.vol_row, text='ml', width=35).pack(side='left', padx=(0,5))

            # Right side: Minimum + info
            right_frame = ctk.CTkFrame(row, fg_color="transparent")
            right_frame.pack(side='right')
            self.minv = ctk.BooleanVar(value=False)
            def tgl():
                if self.minv.get():
                    self.vol_row.pack_forget()
                else:
                    self.vol_row.pack(side='left', fill='x', expand=True)
            ctk.CTkCheckBox(right_frame, text='Minimum', variable=self.minv, onvalue=True, offvalue=False, command=tgl).pack(side='left', padx=(5,0), pady=(4,0))
            info = ctk.CTkButton(right_frame, text='ⓘ', width=25, height=25, corner_radius=15)
            info.pack(side='left', padx=5)
            CTkToolTip(info, message='Target Volume, the volume of the preparing eluent (ml)', delay=0.1)

    def add_row(self):
        if len(self.custom_rows)>=5:return
        r=ctk.CTkFrame(self.rows_frame); r.pack(fill='x')
        n=ctk.CTkEntry(r,placeholder_text='Name'); n.pack(side='left',fill='x',expand=True,padx=(6,3),pady=(0,3))
        p=ctk.CTkEntry(r,placeholder_text='Parts',width=70); p.pack(side='left',padx=(3,6),pady=(0,3))
        n.bind('<Return>', lambda event: self.calc_prepare())
        p.bind('<Return>', lambda event: self.calc_prepare())
        self.custom_rows.append((n,p))

    def calc_prepare(self):
        self.prepare_out.delete('1.0','end')
        if self.major.get()=='new':
            if self.minor.get()=='pea':
                p=float(self.p.get())
                e=float(self.e.get())
                v=float(self.v.get())
                self.prepare_out.configure(font=ctk.CTkFont(family="Arial", size=15)); self.flash_out.delete('1.0','end');
                self.prepare_out.insert('end', f'\nEntered data:\n\nPentane parts = {p:.0f}\nEthylacetate parts = {e:.0f}\nVolume = {v:.0f}ml\n\n_________________________________\n')
                pentane_result=v*p/(p+e)
                ea_result=v*e/(p+e)
                self.prepare_out.insert('end',f'\n\nRecommended parameters:\n\nPentane: {pentane_result:.0f}ml\nEthylacetate: {ea_result:.0f}ml')
            else:
                v=float(self.cv.get())
                total=sum(float(p.get()) for _, p in self.custom_rows if p.get())
                self.prepare_out.configure(font=ctk.CTkFont(family="Arial", size=15));
                self.prepare_out.delete('1.0','end');
                self.prepare_out.insert('end', f'\nEntered data:\n\n')
                for n,p in self.custom_rows:
                    if n.get() and p.get():
                        self.prepare_out.insert('end', f'{n.get()} parts = {float(p.get()):.0f}\n')
                self.prepare_out.insert('end', f'\nTarget Volume = {v:.0f}ml' f'\n\n_________________________________\n')
                for n,p in self.custom_rows:
                    if n.get() and p.get():
                        tv = v*float(p.get())/total
                        self.prepare_out.insert('end', f'\n\nRecommended parameters:{n.get()} = {tv:.0f}ml\n')
                        
# --- calc_prepare(), the "existing" branch ---
        else:
            v1 = float(self.ev1.get())
            p1 = float(self.ep1.get())
            e1 = float(self.ee1.get())
            p2 = float(self.ep2.get())
            e2 = float(self.ee2.get())
            self.prepare_out.configure(font=ctk.CTkFont(family="Arial", size=15)); self.flash_out.delete('1.0','end');
            if self.minv.get():
                pent = ((v1*p2/(p2+e2) - v1*p1/(p1+e1)) / (1 - p2/(p2+e2))) if e2/(e2+p2) < e1/(e1+p1) else 0
                ea   = ((v1*e2/(p2+e2) - v1*e1/(p1+e1)) / (1 - e2/(p2+e2))) if e2/(e2+p2) > e1/(e1+p1) else 0
                tv = "Minimum"
                t = v1 + pent + ea
                total = f'Total Volume: {t:.0f}ml'
            else:
                v2 = float(self.vol.get())
                tv = f'{v2:.0f}ml'
                pent = v2*p2/(p2+e2) - v1*p1/(p1+e1)
                ea   = v2*e2/(p2+e2) - v1*e1/(p1+e1)
                total = ''
            self.prepare_out.configure(font=ctk.CTkFont(family="Arial", size=15))
            self.prepare_out.delete('1.0', 'end')
            self.prepare_out.insert('end', f'\nEntered data:\n\nVolume = {v1:.0f}ml\nPentane parts = {p1:.0f}\nEthylacetate parts = {e1:.0f}\nTarget Pentane parts = {p2:.0f}\nTarget Ethylacetate parts = {e2:.0f}\nTarget Volume = {tv}\n\n__________________________________\n')
            self.prepare_out.insert('end', f'\n\nRecommended parameters:\n\nAdd:     Pentane: {pent:.0f}ml\n             EA: {ea:.0f}ml\n             {total}')









    def build_about(self):
        p=self.pages['About']
        ctk.CTkLabel(p,text='The program provides rough calculations.').pack(pady=(50,0))
        ctk.CTkLabel(p,text='We recommend to double check all the generated data!').pack(pady=0)
        ctk.CTkLabel(p,text='QuickFC v.1.41',font=('Arial',20,'bold')).pack(pady=(100,0))
        ctk.CTkLabel(p,text='Flash Column Chromatography Calculator').pack()
        ctk.CTkLabel(p,text='© 2024-2026 Dmitrii Ladan\nAll rights reserved').pack(pady=10)

QuickFC().mainloop()

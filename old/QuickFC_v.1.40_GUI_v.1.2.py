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
        self.geometry("600x490Calculate")
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
        self.ep = []
        self.prediction_mode=ctk.StringVar(value='Eluent')
        ctk.CTkLabel(l,text='Eluent mixture').pack(pady=0)
        ctk.CTkRadioButton(l,text='Pentane / Ethylacetate',variable=self.prediction_mode,value='Eluent').pack(anchor='w',padx=(20,0),pady=(0,20))
        fields = [
            ('Rf', 'The Rf value of the product based on TLC (between 0.01 and 0.99)'),
            ('Pentane parts', 'The number of pentane parts in the eluent'),
            ('Ethylacetate parts', 'The number of ethyl acetate parts in the eluent mixture.'),
            ('Target Rf', 'The desired Rf value you want to achieve (between 0.01 and 0.99).')
            ]
        for name, description in fields:
            row=ctk.CTkFrame(l, fg_color='transparent')
            row.pack(fill='x', pady=2)
            # Short name
            e=ctk.CTkEntry(row, placeholder_text=name)
            e.pack(side='left', fill='x', expand=True,padx=(6,0))
            self.ep.append(e)
            #button
            info_button=ctk.CTkButton(row, text='ⓘ', width=25, height=25, corner_radius=15)
            info_button.pack(side='right', padx=5)
            # Hover
            CTkToolTip(info_button, message=description, delay=0.1)
            e.bind('<Return>', lambda event: self.calc_ep())
        self.ep_out = ctk.CTkTextbox(r)
        self.ep_out.pack(fill='both', expand=True)
        self.ep_button = ctk.CTkButton(r,text='Calculate',command=self.calc_ep).pack(side='bottom',pady=(10,10))


    def calc_ep(self):
        r1,p1,e1,r2=[float(x.get()) for x in self.ep]
        x = -e1 / ((e1 + p1) * math.log(1 - r1))
        u2 = -x * math.log(1 - r2)
        if u2 <= 0.5:
            p=1/u2-1
            e=1
        else:
            x = -p1 / ((e1 + p1) * math.exp(1 - r1))
            u2 = -x * math.exp(1 - r2)
            p=1; e=1/u2-1
        self.ep_out.configure(font=("Arial", 15)); self.ep_out.delete('1.0','end');
        self.ep_out.insert('end',f'\n\n\n\n\nRecommended eluent:\n \nPentane: {p:.0f}\nEthylacetate: {e:.0f}')







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
        for w in self.flash_body.winfo_children():
            w.destroy()
        self.flash_entries = {}
        if self.flash_mode.get() == 'known':
            fields = [
                ('Rfmin', 'The lowest Rf value of the compound to be separated'),
                ('D', 'The inner diameter of the column (mm)'),
                ('L', 'The length of the packed silica / the length of the column (cm)')
            ]
        else:
            fields = [
                ('m', 'The mass of the crude sample to be purified (mg).'),
                ('dRf', 'The difference between the Rf values of the product and closest compound'),
                ('Rfmin', 'The lowest Rf value of the compound to be separated'),
                ('L', 'The length of the packed silica / the length of the column (cm)')
            ]
        for name, description in fields:
            row = ctk.CTkFrame(self.flash_body, fg_color="transparent")
            row.pack(fill='x', pady=2)
            e = ctk.CTkEntry(row, placeholder_text=name)
            e.pack(side='left', fill='x', expand=True,padx=(6,0))
            self.flash_entries[name] = e
            info = ctk.CTkButton(row, text='ⓘ', width=25, height=25, corner_radius=15)
            info.pack(side='right', padx=5)
            CTkToolTip(info, message=description, delay=0.1)
            e.bind('<Return>', lambda event: self.calc_flash())

    def calc_flash(self):
        values = {name: float(entry.get()) for name, entry in self.flash_entries.items()}
        if self.flash_mode.get()=='known':
            Rfmin = values['Rfmin']
            D = values['D']
            L = values['L']
            ms=math.pow((D/20),2)*3.14*L*0.5
            Vd=((1-0.5/2.5)*math.pow((D/20),2)*3.14*L)*1.5/Rfmin
            Vsl=((1-0.5/2.5)*math.pow((D/20),2)*3.14*L)*0.8
            Vw=((1-0.5/2.5)*math.pow((D/20),2)*3.14*L)*1.5/Rfmin-Vsl
            n1=Vw/10
            n2=Vw/20
            self.flash_out.configure(font=("Arial", 15)); self.flash_out.delete('1.0','end');
            self.flash_out.insert('end',f'\nFor the chosen column of:\ninternal diameter D = {D:.0f}mm\nlength L = {L:.0f}cm:\n\n\nMass of silica: {ms:.0f}g\n\n\nDry silica loading:\nVolume of eluent for colomning: {Vd:.0f}ml\n\nWet silica loading:\nVolume of eluent for loading: {Vsl:.0f}ml\nVolume of eluent for colomning: {Vw:.0f}ml\n\n\nNumber of 10ml test tubes (small): {n1:.0f}pcs\nNumber of 20ml test tubes (large): {n2:.0f}pcs')
        else:
            m = values['m']
            dRf = values['dRf']
            Rfmin = values['Rfmin']
            L = values['L']
            D = m / (2 * math.sqrt(m / 10)) * 0.1 / math.pow(dRf, (1 + 1.5 * (dRf - 0.1)))
            ms = math.pow((D / 20), 2) * 3.14 * L * 0.5
            Vd = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 1.5 / Rfmin
            Vsl = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 0.8
            Vw = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 1.5 / Rfmin - Vsl
            n1 = Vw/10
            n2 = Vw/20
            self.flash_out.configure(font=ctk.CTkFont(family="Arial", size=15)); self.flash_out.delete('1.0','end');
            self.flash_out.insert('end',f'\nRecommended column:\ninternal diameter D = {D:.0f}mm\nlength L = {L:.0f}cm\n\n\nMass of silica: {ms:.0f}g\n\n\nDry silica loading:\nVolume of eluent for colomning: {Vd:.0f}ml\n\nWet silica loading:\nVolume of eluent for loading: {Vsl:.0f}ml\nVolume of eluent for colomning: {Vw:.0f}ml\n\n\nNumber of 10ml test tubes (small): {n1:.0f}\nNumber of 20ml test tubes (large): {n2:.0f}')









    def build_prepare(self):
        l,r=self.split(self.pages['Prepare eluent'])
        self.major=ctk.StringVar(value='new')
        self.minor=ctk.StringVar(value='pea')

        # choice boxes at very top
        ctk.CTkLabel(l,text='Prepare from').pack(pady=0)
        ctk.CTkRadioButton(l,text='the beginning',variable=self.major,value='new',command=self.prepare_redraw).pack(anchor='w',padx=(10,0),pady=(0,10))
        ctk.CTkRadioButton(l,text='another eluent (the same components)',variable=self.major,value='existing',command=self.prepare_redraw).pack(anchor='w',padx=(10,0),pady=(0,20))


        self.prepare_body=ctk.CTkFrame(l, fg_color="transparent"); self.prepare_body.pack(fill='both',expand=True)
        self.prepare_redraw()

        self.prepare_out=ctk.CTkTextbox(r); self.prepare_out.pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate',command=self.calc_prepare).pack(side='bottom',pady=(10,10))

    def prepare_redraw(self):
        for w in self.prepare_body.winfo_children(): w.destroy()
        self.custom_rows = []
        def add_field(name, description):
            row = ctk.CTkFrame(self.prepare_body, fg_color="transparent")
            row.pack(fill='x', pady=2)
            e = ctk.CTkEntry(row, placeholder_text=name)
            e.pack(side='left', fill='x', expand=True, padx=(6,0))
            info = ctk.CTkButton(row,text='ⓘ',width=25,height=25,corner_radius=15)
            info.pack(side='right', padx=5)
            CTkToolTip(info, message=description, delay=0.1)
            return e
        if self.major.get() == 'new':
            ctk.CTkLabel(self.prepare_body, text='Eluent mixture').pack(pady=0)
            ctk.CTkRadioButton(self.prepare_body,text='Pentane / EA',variable=self.minor,value='pea',command=self.prepare_redraw).pack(anchor='w', padx=(10,0), pady=(0,10))
            ctk.CTkRadioButton(self.prepare_body,text='Custom mixture',variable=self.minor,value='custom',command=self.prepare_redraw).pack(anchor='w', padx=(10,0), pady=(0,20))
            if self.minor.get() == 'pea':
                self.p = add_field('Pentane parts','Number of pentane parts in the eluent mixture.')
                self.e = add_field('EA parts','Number of ethyl acetate parts in the eluent mixture.')
                self.v = add_field('Volume','Total volume of eluent to prepare (mL).')
            else:
                self.rows_frame = ctk.CTkFrame(self.prepare_body,fg_color="transparent")
                self.rows_frame.pack(fill='x')
                for _ in range(2):
                    self.add_row()
                ctk.CTkButton(self.prepare_body,text='Add',command=self.add_row).pack(pady=(7,10))
                self.cv = add_field('Volume','Total final volume of the custom eluent mixture (mL).')
        else:
            self.prepare_mode=ctk.StringVar(value='Eluent')
            ctk.CTkLabel(self.prepare_body,text='Eluent mixture').pack(pady=0)
            ctk.CTkRadioButton(self.prepare_body,text='Pentane / Ethylacetate',variable=self.prepare_mode,value='Eluent').pack(anchor='w',padx=(20,0),pady=(0,20))
            self.ev1 = add_field('V','V, the volume of the existing eluent', 'ml')
            self.ep1 = add_field('Pentane parts','Pentane parts, the number of pentane parts in the existing eluent')
            self.ee1 = add_field('Ethylacetate parts','Ethylacetate parts, the number of ethylacetate parts in the existing eluent')
            self.ep2 = add_field('Target Pentane','Target Pentane, the number of pentane parts in the preparing eluent')
            self.ee2 = add_field('Target Ethylacetate','Target Ethylacetate, the number of ethylacetate parts in the preparing eluent')
            row = ctk.CTkFrame(self.prepare_body, fg_color="transparent")
            row.pack(fill='x', pady=2)

            # Left side: Target V + ml
            self.vol_row = ctk.CTkFrame(row, fg_color="transparent")
            self.vol_row.pack(side='left', fill='x', expand=True)

            self.vol = ctk.CTkEntry(self.vol_row, placeholder_text='Target V', width=80)
            self.vol.pack(side='left', padx=(6,0))

            ctk.CTkLabel(
                self.vol_row,
                text='ml',
                width=35
            ).pack(side='left', padx=(0,5))


            # Right side: Minimum + info
            right_frame = ctk.CTkFrame(row, fg_color="transparent")
            right_frame.pack(side='right')

            self.minv = ctk.BooleanVar()

            def tgl():
                if self.minv.get():
                    self.vol_row.pack_forget()
                else:
                    self.vol_row.pack(side='left', fill='x', expand=True)

            ctk.CTkCheckBox(
                right_frame,
                text='Minimum',
                variable=self.minv,
                command=tgl
            ).pack(side='left', padx=(5,0), pady=(4,0))

            info = ctk.CTkButton(
                right_frame,
                text='ⓘ',
                width=25,
                height=25,
                corner_radius=15
            )
            info.pack(side='left', padx=5)

            CTkToolTip(
                info,
                message='Target V, the volume of the preparing eluent (ml)',
                delay=0.1
            )

    def add_row(self):
        if len(self.custom_rows)>=5:return
        r=ctk.CTkFrame(self.rows_frame); r.pack(fill='x')
        n=ctk.CTkEntry(r,placeholder_text='Name'); n.pack(side='left',fill='x',expand=True,padx=(6,3),pady=(0,3))
        p=ctk.CTkEntry(r,placeholder_text='Parts',width=70); p.pack(side='left',padx=(3,6),pady=(0,3))
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
        ctk.CTkLabel(p,text='The program can provide rough calculations.').pack(pady=(50,0))
        ctk.CTkLabel(p,text='We recommend to double check all the generated data!').pack(pady=0)
        ctk.CTkLabel(p,text='QuickFC v.1.41',font=('Arial',20,'bold')).pack(pady=(100,0))
        ctk.CTkLabel(p,text='Flash Column Chromatography Calculator').pack()
        ctk.CTkLabel(p,text='© 2024-2026 Dmitrii Ladan\nAll rights reserved').pack(pady=10)

QuickFC().mainloop()

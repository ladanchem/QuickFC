import customtkinter as ctk
ctk.set_appearance_mode("dark")

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickFC v.1.31")
        self.geometry("760x400")

        top=ctk.CTkFrame(self)
        top.pack(fill="x",padx=5,pady=5)

        self.pages={}
        self.content=ctk.CTkFrame(self)
        self.content.pack(fill='both',expand=True,padx=5,pady=5)

        pages=['Eluent predictor (demo)','Running a flash column','Prepare eluent','About']
        for p in pages:
            ctk.CTkButton(top,text=p,command=lambda x=p:self.show(x)).pack(side='left',padx=2)
            self.pages[p]=ctk.CTkFrame(self.content)

        self.build_predictor(); self.build_flash(); self.build_prepare(); self.build_about()
        self.show(pages[0])

    def show(self,n):
        for p in self.pages.values(): p.pack_forget()
        self.pages[n].pack(fill='both',expand=True)

    def split(self,page):
        l=ctk.CTkFrame(page); r=ctk.CTkFrame(page)
        l.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        r.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        return l,r

    def build_predictor(self):
        l,r=self.split(self.pages['Eluent predictor (demo)'])
        for t in ['Current Rf','Pentane parts','EA parts','Target Rf']:
            ctk.CTkEntry(l,placeholder_text=t).pack(fill='x',pady=2)
        ctk.CTkTextbox(r).pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate (disabled)').pack(side='bottom',pady=5)

    def build_flash(self):
        l,r=self.split(self.pages['Running a flash column'])
        mode=ctk.StringVar(value='known')
        ctk.CTkRadioButton(l,text='Known size',variable=mode,value='known').pack(anchor='w')
        ctk.CTkRadioButton(l,text='Unknown size',variable=mode,value='unknown').pack(anchor='w')
        ctk.CTkLabel(l,text='').pack(pady=6)
        body=ctk.CTkFrame(l); body.pack(fill='both',expand=True)
        def redraw(*_):
            for w in body.winfo_children(): w.destroy()
            items=['Lowest Rf','Diameter','Length'] if mode.get()=='known' else ['Sample mass','dRf','Lowest Rf','Length']
            for i in items: ctk.CTkEntry(body,placeholder_text=i).pack(fill='x',pady=2)
        mode.trace_add('write',redraw); redraw()
        ctk.CTkTextbox(r).pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate (disabled)').pack(side='bottom',pady=5)

    def build_prepare(self):
        l,r=self.split(self.pages['Prepare eluent'])
        major=ctk.StringVar(value='new')
        minor=ctk.StringVar(value='pea')
        body=ctk.CTkFrame(l); body.pack(fill='both',expand=True)

        ctk.CTkRadioButton(l,text='Prepare from the beginning',variable=major,value='new').pack(anchor='w')
        ctk.CTkRadioButton(l,text='I already have eluent with the same components',variable=major,value='existing').pack(anchor='w')

        def redraw(*_):
            for w in body.winfo_children(): w.destroy()
            if major.get()=='new':
                ctk.CTkLabel(body,text='').pack(pady=5)
                ctk.CTkRadioButton(body,text='Pentane / EA',variable=minor,value='pea').pack(anchor='w')
                ctk.CTkRadioButton(body,text='Custom mixture',variable=minor,value='custom').pack(anchor='w')
                ctk.CTkLabel(body,text='').pack(pady=5)
                area=ctk.CTkFrame(body); area.pack(fill='both',expand=True)

                def draw_inner(*a):
                    for w in area.winfo_children(): w.destroy()
                    if minor.get()=='pea':
                        for t in ['Pentane parts','EA parts','Volume']:
                            ctk.CTkEntry(area,placeholder_text=t).pack(fill='x',pady=2)
                    else:
                        for _i in range(2):
                            row=ctk.CTkFrame(area); row.pack(fill='x',pady=1)
                            ctk.CTkEntry(row,placeholder_text='Name').pack(side='left',expand=True,fill='x',padx=1)
                            ctk.CTkEntry(row,placeholder_text='Parts',width=80).pack(side='left',padx=1)
                        ctk.CTkButton(area,text='Add (disabled)').pack(pady=3)
                        ctk.CTkEntry(area,placeholder_text='Volume').pack(fill='x',pady=4)
                minor.trace_add('write',draw_inner)
                draw_inner()
            else:
                for t in ['Current volume','Current Pentane','Current EA','Target Pentane','Target EA']:
                    ctk.CTkEntry(body,placeholder_text=t).pack(fill='x',pady=2)
                row=ctk.CTkFrame(body); row.pack(fill='x',pady=2)
                flag=ctk.BooleanVar()
                vol=ctk.CTkEntry(row,placeholder_text='Target volume')
                vol.pack(side='left',fill='x',expand=True)
                def toggle():
                    if flag.get():
                        vol.pack_forget()
                    else:
                        vol.pack(side='left',fill='x',expand=True)
                ctk.CTkCheckBox(row,text='Minimum',variable=flag,command=toggle).pack(side='left',padx=5)

        major.trace_add('write',redraw); redraw()
        ctk.CTkTextbox(r).pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate (disabled)').pack(side='bottom',pady=5)

    def build_about(self):
        p=self.pages['About']
        ctk.CTkLabel(p,text='QuickFC v.1.31',font=('Arial',20,'bold')).pack(pady=10)
        ctk.CTkLabel(p,text='Flash Column Chromatography Calculator').pack()
        ctk.CTkLabel(p,text='© 2024-2026 Dmitrii Ladan, All rights reserved.').pack(pady=10)

QuickFC().mainloop()

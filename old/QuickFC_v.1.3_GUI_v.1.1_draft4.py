import customtkinter as ctk

ctk.set_appearance_mode("dark")

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickFC v.1.31")
        self.geometry("700x400")

        top=ctk.CTkFrame(self)
        top.pack(fill="x",padx=5,pady=5)

        self.pages={}
        self.content=ctk.CTkFrame(self)
        self.content.pack(fill="both",expand=True,padx=5,pady=5)

        pages=["Eluent predictor (demo)","Running a flash column","Prepare eluent","About"]
        for p in pages:
            ctk.CTkButton(top,text=p,command=lambda x=p:self.show(x)).pack(side="left",padx=2)
            self.pages[p]=ctk.CTkFrame(self.content)

        self.build_predictor()
        self.build_flash()
        self.build_prepare()
        self.build_about()
        self.show(pages[0])

    def show(self,name):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[name].pack(fill='both',expand=True)

    def split(self,page):
        l=ctk.CTkFrame(page)
        r=ctk.CTkFrame(page)
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
        body=ctk.CTkFrame(l); body.pack(fill='both',expand=True)
        def redraw(*a):
            for w in body.winfo_children(): w.destroy()
            if mode.get()=='known':
                items=['Lowest Rf','Diameter','Length']
            else:
                items=['Sample mass','dRf','Lowest Rf','Length']
            for i in items:
                ctk.CTkEntry(body,placeholder_text=i).pack(fill='x',pady=2)
        mode.trace_add('write',redraw)
        redraw()
        ctk.CTkTextbox(r).pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate (disabled)').pack(side='bottom',pady=5)

    def build_prepare(self):
        l,r=self.split(self.pages['Prepare eluent'])

        major=ctk.StringVar(value='new')
        minor=ctk.StringVar(value='pea')
        body=ctk.CTkFrame(l)

        ctk.CTkRadioButton(l,text='Prepare from the beginning',variable=major,value='new').pack(anchor='w')
        ctk.CTkRadioButton(l,text='I already have eluent with the same components',variable=major,value='existing').pack(anchor='w')
        body.pack(fill='both',expand=True,pady=5)

        def redraw(*a):
            for w in body.winfo_children(): w.destroy()

            if major.get()=='new':
                ctk.CTkRadioButton(body,text='Pentane / EA',variable=minor,value='pea').pack(anchor='w')
                ctk.CTkRadioButton(body,text='Custom mixture',variable=minor,value='custom').pack(anchor='w')

                area=ctk.CTkFrame(body)
                area.pack(fill='both',expand=True)

                def draw_inner(*b):
                    for w in area.winfo_children(): w.destroy()
                    if minor.get()=='pea':
                        for t in ['Pentane parts','EA parts','Volume']:
                            ctk.CTkEntry(area,placeholder_text=t).pack(fill='x',pady=2)
                    else:
                        holder=ctk.CTkFrame(area)
                        holder.pack(fill='x')
                        rows=[]
                        def add_row():
                            if len(rows)>=5:return
                            row=ctk.CTkFrame(holder)
                            row.pack(fill='x',pady=1)
                            ctk.CTkEntry(row,placeholder_text='Name').pack(side='left',fill='x',expand=True,padx=1)
                            ctk.CTkEntry(row,placeholder_text='Parts',width=80).pack(side='left',padx=1)
                            rows.append(row)
                        add_row();add_row()
                        ctk.CTkButton(area,text='Add').pack(pady=3)
                minor.trace_add('write',draw_inner)
                draw_inner()

            else:
                for t in ['Current volume','Current Pentane','Current EA','Target Pentane','Target EA']:
                    ctk.CTkEntry(body,placeholder_text=t).pack(fill='x',pady=2)
                row=ctk.CTkFrame(body); row.pack(fill='x')
                vol=ctk.CTkEntry(row,placeholder_text='Target volume')
                vol.pack(side='left',fill='x',expand=True)
                flag=ctk.BooleanVar()
                def toggle():
                    if flag.get():
                        vol.configure(state='disabled',fg_color='#333333')
                    else:
                        vol.configure(state='normal')
                ctk.CTkCheckBox(row,text='Minimum',variable=flag,command=toggle).pack(side='left',padx=5)

        major.trace_add('write',redraw)
        redraw()
        ctk.CTkTextbox(r).pack(fill='both',expand=True)
        ctk.CTkButton(r,text='Calculate (disabled)').pack(side='bottom',pady=5)

    def build_about(self):
        p=self.pages['About']
        ctk.CTkLabel(p,text='QuickFC v.1.31',font=('Arial',18,'bold')).pack(pady=10)
        ctk.CTkLabel(p,text='Flash Column Chromatography Calculator').pack()

QuickFC().mainloop()

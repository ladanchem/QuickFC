
import customtkinter as ctk

ctk.set_appearance_mode('dark')

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('QuickFC v.1.31')
        self.geometry('850x450')

        top=ctk.CTkFrame(self)
        top.pack(fill='x',padx=5,pady=5)

        self.container=ctk.CTkFrame(self)
        self.container.pack(fill='both',expand=True,padx=5,pady=5)

        self.pages={}
        names=['Eluent predictor (demo)','Running a flash column','Prepare eluent','Change polarity','About']
        for n in names:
            ctk.CTkButton(top,text=n,command=lambda x=n:self.show(x)).pack(side='left',padx=2)
            p=ctk.CTkFrame(self.container)
            self.pages[n]=p

        self.build_predictor()
        self.build_flash()
        self.build_prepare()
        self.build_polarity()
        self.build_about()
        self.show(names[0])

    def show(self,n):
        for p in self.pages.values(): p.pack_forget()
        self.pages[n].pack(fill='both',expand=True)

    def lr(self,page):
        l=ctk.CTkFrame(page)
        r=ctk.CTkFrame(page)
        l.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        r.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        return l,r

    def build_predictor(self):
        l,r=self.lr(self.pages['Eluent predictor (demo)'])
        for t in ['Current Rf','Pentane parts','EA parts','Target Rf']:
            ctk.CTkEntry(l,placeholder_text=t).pack(fill='x',pady=4)
        ctk.CTkTextbox(r).pack(fill='both',expand=True,pady=5)
        ctk.CTkButton(r,text='Calculate').pack(side='bottom',pady=5)

    def build_flash(self):
        l,r=self.lr(self.pages['Running a flash column'])
        mode=ctk.StringVar(value='known')
        fields={}
        body=ctk.CTkFrame(l); body.pack(fill='both',expand=True)

        def redraw():
            for w in body.winfo_children(): w.destroy()
            show=['Lowest Rf','Length']
            if mode.get()=='known': show+=['Diameter']
            else: show+=['Sample mass','dRf']
            for s in show:
                fields[s]=ctk.CTkEntry(body,placeholder_text=s)
                fields[s].pack(fill='x',pady=3)

        ctk.CTkRadioButton(l,text='Known size',variable=mode,value='known',command=redraw).pack(anchor='w')
        ctk.CTkRadioButton(l,text='Unknown size',variable=mode,value='unknown',command=redraw).pack(anchor='w')
        redraw()
        ctk.CTkTextbox(r).pack(fill='both',expand=True,pady=5)
        ctk.CTkButton(r,text='Calculate').pack(side='bottom',pady=5)

    def build_prepare(self):
        l,r=self.lr(self.pages['Prepare eluent'])
        mode=ctk.StringVar(value='regular')
        body=ctk.CTkFrame(l)
        body.pack(fill='both',expand=True)

        def render():
            for w in body.winfo_children(): w.destroy()
            if mode.get()=='regular':
                for t in ['Pentane parts','EA parts','Volume']:
                    ctk.CTkEntry(body,placeholder_text=t).pack(fill='x',pady=3)
            else:
                rows=[]
                holder=ctk.CTkFrame(body)
                holder.pack(fill='x')
                def add_row():
                    if len(rows)>=5: return
                    row=ctk.CTkFrame(holder)
                    row.pack(fill='x',pady=2)
                    ctk.CTkEntry(row,placeholder_text='Compound name').pack(side='left',expand=True,fill='x',padx=2)
                    ctk.CTkEntry(row,placeholder_text='Parts',width=100).pack(side='left',padx=2)
                    rows.append(row)
                add_row(); add_row()
                ctk.CTkButton(body,text='Add',command=add_row).pack(pady=4)

        ctk.CTkRadioButton(l,text='Pentane / EA',variable=mode,value='regular',command=render).pack(anchor='w')
        ctk.CTkRadioButton(l,text='Custom mixture',variable=mode,value='custom',command=render).pack(anchor='w')
        render()
        ctk.CTkTextbox(r).pack(fill='both',expand=True,pady=5)
        ctk.CTkButton(r,text='Calculate').pack(side='bottom',pady=5)

    def build_polarity(self):
        l,r=self.lr(self.pages['Change polarity'])
        for t in ['Current volume','Current Pentane','Current EA','Target Pentane','Target EA']:
            ctk.CTkEntry(l,placeholder_text=t).pack(fill='x',pady=3)

        row=ctk.CTkFrame(l); row.pack(fill='x',pady=3)
        vol=ctk.CTkEntry(row,placeholder_text='Target volume')
        vol.pack(side='left',fill='x',expand=True)
        minvar=ctk.BooleanVar()
        def toggle():
            vol.configure(state='disabled' if minvar.get() else 'normal')
        ctk.CTkCheckBox(row,text='Minimum',variable=minvar,command=toggle).pack(side='left',padx=5)

        ctk.CTkTextbox(r).pack(fill='both',expand=True,pady=5)
        ctk.CTkButton(r,text='Calculate').pack(side='bottom',pady=5)

    def build_about(self):
        p=self.pages['About']
        ctk.CTkLabel(p,text='QuickFC v.1.31',font=('Arial',20,'bold')).pack(pady=10)
        ctk.CTkLabel(p,text='Flash Column Chromatography Calculator').pack()
        ctk.CTkLabel(p,text='© 2024-2026 Dmitrii Ladan\nAll rights reserved.').pack(pady=10)

QuickFC().mainloop()

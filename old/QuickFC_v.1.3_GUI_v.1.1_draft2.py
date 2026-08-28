
import customtkinter as ctk

ctk.set_appearance_mode("dark")

class QuickFC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickFC v.1.31")
        self.geometry("600x400")

        nav = ctk.CTkFrame(self, width=170)
        nav.pack(side="left", fill="y", padx=(5,2), pady=5)

        content = ctk.CTkFrame(self)
        content.pack(side="right", fill="both", expand=True, padx=(2,5), pady=5)

        self.pages = {}

        buttons = [
            "Eluent predictor (demo)",
            "Running a flash column",
            "Prepare eluent",
            "Change polarity",
            "About"
        ]

        for name in buttons:
            ctk.CTkButton(nav, text=name,
                          command=lambda n=name:self.show(n)).pack(fill='x', padx=5, pady=3)

        for name in buttons:
            page = ctk.CTkFrame(content)
            self.pages[name] = page

        self.build_predictor()
        self.build_flash()
        self.build_prepare()
        self.build_polarity()
        self.build_about()

        self.show("Eluent predictor (demo)")

    def show(self, name):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[name].pack(fill='both', expand=True)

    def build_predictor(self):
        p=self.pages["Eluent predictor (demo)"]
        left=ctk.CTkFrame(p); left.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        right=ctk.CTkFrame(p); right.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        for txt in ['Current Rf','Pentane parts','EA parts','Target Rf']:
            ctk.CTkEntry(left,placeholder_text=txt).pack(fill='x',pady=3)
        ctk.CTkButton(right,text='Calculate (disabled)').pack(pady=5)
        ctk.CTkTextbox(right).pack(fill='both',expand=True)

    def build_flash(self):
        p=self.pages['Running a flash column']
        left=ctk.CTkFrame(p); left.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        right=ctk.CTkFrame(p); right.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        ctk.CTkRadioButton(left,text='Known size').pack(anchor='w')
        ctk.CTkRadioButton(left,text='Unknown size').pack(anchor='w')
        for txt in ['Sample mass','dRf','Lowest Rf','Diameter','Length']:
            ctk.CTkEntry(left,placeholder_text=txt).pack(fill='x',pady=3)
        ctk.CTkButton(right,text='Calculate (disabled)').pack(pady=5)
        ctk.CTkTextbox(right).pack(fill='both',expand=True)

    def build_prepare(self):
        p=self.pages['Prepare eluent']
        left=ctk.CTkFrame(p); left.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        right=ctk.CTkFrame(p); right.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        ctk.CTkRadioButton(left,text='Pentane / EA').pack(anchor='w')
        ctk.CTkRadioButton(left,text='Custom mixture').pack(anchor='w')
        for txt in ['Pentane parts','EA parts','Volume']:
            ctk.CTkEntry(left,placeholder_text=txt).pack(fill='x',pady=3)
        ctk.CTkButton(left,text='Add').pack(pady=3)
        ctk.CTkButton(right,text='Calculate (disabled)').pack(pady=5)
        ctk.CTkTextbox(right).pack(fill='both',expand=True)

    def build_polarity(self):
        p=self.pages['Change polarity']
        left=ctk.CTkFrame(p); left.pack(side='left',fill='both',expand=True,padx=5,pady=5)
        right=ctk.CTkFrame(p); right.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        for txt in ['Current volume','Current Pentane','Current EA','Target Pentane','Target EA','Target volume/min']:
            ctk.CTkEntry(left,placeholder_text=txt).pack(fill='x',pady=3)
        ctk.CTkButton(right,text='Calculate (disabled)').pack(pady=5)
        ctk.CTkTextbox(right).pack(fill='both',expand=True)

    def build_about(self):
        p=self.pages['About']
        ctk.CTkLabel(p,text='QuickFC v.1.31').pack(pady=10)
        ctk.CTkLabel(p,text='UI Preview Only').pack()

QuickFC().mainloop()

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EluCalcApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EluCalc GUI")
        self.geometry("800x700")

        title = ctk.CTkLabel(self, text="EluCalc", font=("Arial", 24, "bold"))
        title.pack(pady=10)

        self.tabview = ctk.CTkTabview(self, width=750)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.prepare_regular_tab()
        self.prepare_custom_tab()
        self.change_regular_tab()

    def prepare_regular_tab(self):
        tab = self.tabview.add("Prepare P:EA")
        self.p = ctk.CTkEntry(tab, placeholder_text="Pentane parts")
        self.e = ctk.CTkEntry(tab, placeholder_text="Ethylacetate parts")
        self.v = ctk.CTkEntry(tab, placeholder_text="Required volume")
        for w in (self.p, self.e, self.v):
            w.pack(pady=8, padx=20, fill='x')

        ctk.CTkButton(tab, text="Calculate", command=self.calc_regular).pack(pady=10)
        self.reg_result = ctk.CTkTextbox(tab, height=120)
        self.reg_result.pack(fill='both', padx=20, pady=10)

    def calc_regular(self):
        try:
            p=float(self.p.get()); e=float(self.e.get()); v=float(self.v.get())
            pent=v*p/(p+e)
            ea=v*e/(p+e)
            self.reg_result.delete('1.0','end')
            self.reg_result.insert('end',f'Pentane: {pent:.0f}\nEthylacetate: {ea:.0f}')
        except Exception as ex:
            messagebox.showerror('Error', str(ex))

    def prepare_custom_tab(self):
        tab = self.tabview.add("Prepare Custom")
        self.comp_box = ctk.CTkTextbox(tab, height=180)
        self.comp_box.pack(fill='x', padx=20, pady=10)
        self.comp_box.insert('1.0','Pentane,7\nEthylacetate,3')

        self.custom_vol = ctk.CTkEntry(tab, placeholder_text='Required volume')
        self.custom_vol.pack(fill='x', padx=20, pady=8)

        ctk.CTkButton(tab, text='Calculate', command=self.calc_custom).pack(pady=10)
        self.custom_result = ctk.CTkTextbox(tab, height=200)
        self.custom_result.pack(fill='both', padx=20, pady=10)

    def calc_custom(self):
        try:
            volume=float(self.custom_vol.get())
            rows=[r.strip() for r in self.comp_box.get('1.0','end').splitlines() if r.strip()]
            names=[]; parts=[]
            for r in rows:
                n,p=r.split(',')
                names.append(n.strip())
                parts.append(float(p))
            total=sum(parts)
            self.custom_result.delete('1.0','end')
            for n,p in zip(names,parts):
                self.custom_result.insert('end',f'{n}: {volume*p/total:.0f}\n')
        except Exception as ex:
            messagebox.showerror('Error', str(ex))

    def change_regular_tab(self):
        tab = self.tabview.add('Change P:EA')
        fields = [
            ('Current volume','v1'),('Current Pentane parts','p1'),('Current EA parts','e1'),
            ('Target Pentane parts','p2'),('Target EA parts','e2'),('Target volume (number or min)','v2')]
        self.entries={}
        for label,key in fields:
            ctk.CTkLabel(tab,text=label).pack(anchor='w',padx=20)
            ent=ctk.CTkEntry(tab)
            ent.pack(fill='x',padx=20,pady=3)
            self.entries[key]=ent
        ctk.CTkButton(tab,text='Calculate',command=self.change_regular).pack(pady=10)
        self.change_result=ctk.CTkTextbox(tab,height=180)
        self.change_result.pack(fill='both',padx=20,pady=10)

    def change_regular(self):
        try:
            v1=float(self.entries['v1'].get())
            p1=float(self.entries['p1'].get())
            e1=float(self.entries['e1'].get())
            p2=float(self.entries['p2'].get())
            e2=float(self.entries['e2'].get())
            v2=self.entries['v2'].get().strip()

            if v2.lower()=='min':
                pent=((v1*p2/(p2+e2)-v1*p1/(p1+e1))/(1-p2/(p2+e2))) if e2/(e2+p2)<e1/(e1+p1) else 0
                ea=((v1*e2/(p2+e2)-v1*e1/(p1+e1))/(1-e2/(p2+e2))) if e2/(e2+p2)>e1/(e1+p1) else 0
                total=v1+pent+ea
            else:
                v2=float(v2)
                pent=v2*p2/(p2+e2)-v1*p1/(p1+e1)
                ea=v2*e2/(p2+e2)-v1*e1/(p1+e1)
                total=v1+pent+ea

            self.change_result.delete('1.0','end')
            self.change_result.insert('end',f'Add Pentane: {pent:.0f}\nAdd Ethylacetate: {ea:.0f}\nTotal Volume: {total:.0f}')
        except Exception as ex:
            messagebox.showerror('Error', str(ex))

if __name__ == '__main__':
    app = EluCalcApp()
    app.mainloop()

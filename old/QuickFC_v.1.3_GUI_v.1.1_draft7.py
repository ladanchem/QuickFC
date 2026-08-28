# QuickFC_tooltip_patch.py
# Add this code to QuickFC_v.1.3_GUI_v.1.1_draft6.py

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        self.after_id = None

        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)

    def schedule(self, event=None):
        self.after_id = self.widget.after(2000, self.show)

    def show(self):
        if self.tip:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        import customtkinter as ctk
        self.tip = ctk.CTkToplevel(self.widget)
        self.tip.overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(self.tip, text=self.text)
        label.pack(padx=5, pady=5)

    def hide(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tip:
            self.tip.destroy()
            self.tip = None

# Replace the field creation loop in build_predictor() with:

DESCRIPTIONS = {
    "Current Rf": "Rf value from TLC (0.01-0.99)",
    "Pentane parts": "Pentane ratio in the current eluent",
    "EA parts": "Ethyl acetate ratio in the current eluent",
    "Target Rf": "Desired Rf value after optimization"
}

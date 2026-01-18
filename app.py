import customtkinter as ctk
from ui.layout import AppLayout

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = AppLayout()
    app.mainloop()

if __name__ == "__main__":
    main()

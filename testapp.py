import customtkinter as ctk
from chat import get_response, bot_name
from PIL import Image


import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

intents_path = os.path.join(BASE_DIR, "intents.json")
data_path = os.path.join(BASE_DIR, "data.pth")
logo_path = os.path.join(BASE_DIR, "logo.png")


BG_COLOR = "#FFFFFF"
BG_BLUE = "#0096FF"
TEXT_COLOR = "#000000"

FONT = ("Helvetica", 14)
FONT_BOLD = ("Helvetica", 15, "bold")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.intro()

    def run(self):
        self.mainloop()

    def intro(self):
        self.title("HappyMind")
        self.geometry("600x750")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=BG_BLUE,)

        #Header
        self.header_frame = ctk.CTkFrame(self, fg_color=BG_BLUE)
        self.header_frame.pack(fill="x", pady=(10, 0), padx=10)

        #Image
        img = ctk.CTkImage(light_image=Image.open(logo_path), size=(150,150))

        my_label = ctk.CTkLabel(self.header_frame, text="", image=img)
        my_label.pack(pady=7, padx=7, side="top")

        #Text
        self.head_label = ctk.CTkLabel( self.header_frame, text="Víta vás HappyMind\n\nVáš poradca duševného zdravia",font=("Helvetica", 30), text_color="#FFFFFF", pady=20)
        self.head_label.pack(pady=15, padx=15)

        #Name entry
        self.entry_name = ctk.CTkEntry(self, font=FONT, placeholder_text="Zadaj svoje meno...", width=400, border_color="#000000")
        self.entry_name.pack(pady=20)
        self.entry_name.bind("<Return>", self.start_chat_key)

        #Start button
        self.start_button = ctk.CTkButton(self, text="Štart", font=FONT_BOLD, text_color=BG_COLOR, border_color="#000000", border_width=2, command=self.start_chat)
        self.start_button.pack(pady=10)

        # ABOUT
        self.about_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=10, border_width=2, border_color="#000000")
        self.about_frame.pack(pady=15, padx=20, fill="both")

        self.about_title = ctk.CTkLabel(self.about_frame, text="O projekte", font= FONT_BOLD)  # Zvýraznený nadpis
        self.about_title.pack(pady=10)

        self.about_label = ctk.CTkLabel(self.about_frame, text="Tento ChatBot bol vytvorený ako ročníkový projekt na odbornú maturitnú skúšku.\n\nZ dôvodu zlej podpory knižnice NLTK pre slovenský jazyk som sa rozhodol že ChatBot bude v anglickom jazyku.\n\nChatBot je vytvorený tak aby používateľovi odpovedal na otázky o duševnom zdraví.\n\n ChatBot nie je určený na zdĺhavú komunikáciu, ale je trénovaný tak aby používateľovi odporúčil rôzne techniky na zvládnutie určitých situácii.\n\nPo kliknutí na tlačidlo Štart bude celá aplikácia už len v anglickom jazyku.\n", font=FONT, text_color=TEXT_COLOR, wraplength=550, justify="center")
        self.about_label.pack(pady=10, padx=10)

    def start_chat(self):
        user_name = self.entry_name.get()
        if user_name:
            self.user_name = user_name
            self._setup_main_window()

    def start_chat_key(self, event=None):
        self.start_chat()

    def _setup_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.title("HappyMind")
        self.geometry("600x750")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=BG_COLOR)

        #Header
        self.header_frame = ctk.CTkFrame(self, fg_color=BG_BLUE, corner_radius=15)
        self.header_frame.pack(fill="x", pady=(10, 0), padx=10)

        img = ctk.CTkImage(light_image=Image.open(logo_path),
	    size=(70,70))

        my_label = ctk.CTkLabel(self.header_frame, text="", image=img)
        my_label.pack(pady=7, padx=7, side="left")

        self.head_label = ctk.CTkLabel( self.header_frame, text="Chat with\nHappyMind",font=FONT, text_color="#FFFFFF", pady=10, justify="left")
        self.head_label.pack(pady=10, padx=10, side="left")
        
        self.button = ctk.CTkButton(self.header_frame, text="•\n•\n•", corner_radius=30, fg_color="transparent", text_color=BG_COLOR, font=("Helvetica", 12, "bold"), width= 10, height= 10, hover= None)
        self.button.pack(pady=0, padx=15, side="right")
        
        #Text-field
        self.text_widget = ctk.CTkTextbox(self, width=600, height=550, font=FONT, wrap="word", state="disabled", border_color=TEXT_COLOR, border_width=1)
        self.text_widget.pack(pady=10, padx=10, fill="both", expand=True)
        
        #Bottom-frame
        self.bottom_frame = ctk.CTkFrame(self, height=90, fg_color=BG_BLUE)
        self.bottom_frame.pack(fill="x", side="bottom")

        #Message-entry
        self.msg_entry = ctk.CTkEntry(self.bottom_frame, font=FONT, width=400, border_color= "#000000")
        self.msg_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.msg_entry.bind("<Return>", self.enter)

        # Example
        self.msg_entry.insert(0, "Type your message here...")  

        # Example clear and restore
        self.msg_entry.bind("<FocusIn>", self.clear_placeholder)
        self.msg_entry.bind("<FocusOut>", self.restore_placeholder)

        #Button
        self.send_button = ctk.CTkButton(self.bottom_frame, text="Send", font=FONT_BOLD, text_color= BG_COLOR, border_color= TEXT_COLOR, 
                                         border_width=2, command=lambda: self.enter(None))
        self.send_button.grid(row=0, column=1, padx=10, pady=10)

        self.bottom_frame.columnconfigure(0, weight=1)
        #First msg
        self._insert_message(f"{bot_name}: Hi there, I am HappyMind. I am here to explain anything you need to know about mental health.\n\n", bot=True)

    def enter(self, event):
        msg = self.msg_entry.get()
        if msg and msg != "Type your message here...":
            self.msg_entry.delete(0, "end")
            self._insert_message(f"{self.user_name}: {msg}\n\n")
            response = get_response(msg)
            self._insert_message(f"{bot_name}: {response}\n\n", bot=True)

    def _insert_message(self, msg, bot=False):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", msg,)
        self.text_widget.configure(state="disabled")
        self.text_widget.see("end")

    def clear_placeholder(self, event):
        if self.msg_entry.get() == "Type your message here...":
            self.msg_entry.delete(0, "end")

    def restore_placeholder(self, event):
        if not self.msg_entry.get():
            self.msg_entry.insert(0, "Type your message here...")

if __name__ == "__main__":
    app = App()
    app.run()
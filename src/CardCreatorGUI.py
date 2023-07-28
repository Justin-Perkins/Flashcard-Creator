import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
import CreatePDF as cp

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Flashcard Creator")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Flashcard Creator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.add_card_button = customtkinter.CTkButton(self.sidebar_frame, command=self.add_card_button_event, text="Add Card")
        self.add_card_button.grid(row=1, column=0, padx=20, pady=10)

        self.translate_mode_switch = customtkinter.CTkSwitch(self.sidebar_frame, text="Translate Mode", command=self.translate_mode_switch_event)
        self.translate_mode_switch.grid(row=2, column=0, padx=20, pady=10)
        
        self.start_language_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["English"], state="disabled")
        self.start_language_menu.grid(row=3, column=0, padx=20, pady=10)

        self.end_language_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Japanese"], state="disabled")
        self.end_language_menu.grid(row=4, column=0, padx=20, pady=10)

        # Create card entry frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=1, columnspan=3, rowspan=3, padx=20, pady=(20, 0), sticky="nsew")

        # Create main entry and button
        self.filename_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Filename...")
        self.filename_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.finished_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Finish Cards", command=self.finish_card_button_event)
        self.finished_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Variables for storing card entries and number of cards
        self.num_cards = 0
        self.card_entries = []

    def add_card_button_event(self):
        self.num_cards += 1
        
        new_card_frame = customtkinter.CTkFrame(self.scrollable_frame, width=300, height=100, corner_radius=5, border_width=2, fg_color='#404040')
        new_card_frame.pack(pady=10, fill="x")

        labels = ["Front:", "Front Subtext:", "Back:", "Back Subtext:"]

        # Create row number
        row_number_label = customtkinter.CTkLabel(new_card_frame, text=str(self.num_cards))
        row_number_label.grid(row=0, column=0, pady=5, padx=5)

        # Create a vertical divider frame
        divider_frame = customtkinter.CTkFrame(new_card_frame, width=2, height= 30, border_color='#2b2b2b')
        divider_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        # Create a grid with 1 row and 4 columns
        for col, label_text in enumerate(labels):
            label = customtkinter.CTkLabel(new_card_frame, text=label_text)
            label.grid(row=0, column=col * 2 + 2, padx=5, pady=5, sticky="e")

            entry = customtkinter.CTkEntry(new_card_frame)
            entry.grid(row=0, column=col * 2 + 3, padx=5, pady=5)

            # Add entry to the list of card entries
            self.card_entries.append(entry)

            # Set uniform weight to ensure equal spacing
            new_card_frame.grid_columnconfigure(col * 2 + 3, weight=1)

    def finish_card_button_event(self):
        file_name = self.filename_entry.get()

        folder_path = filedialog.askdirectory()

        # Check if there if a folder has been selected and a filename has been entered
        if not file_name:
            tkinter.messagebox.showinfo("Warning", "Please enter a file name before exporting the flash cards.")
        # Both file name and folder path have been selected
        elif folder_path: 
            pdf = cp.Pdf(file_name)

            for count, card in enumerate(self.card_entries):
                if count % 4 == 0:
                    front_text = card.get()
                elif count % 4 == 1:
                    if card.get() != "":
                        front_subtext = f"({card.get()})"
                    else:
                        front_subtext = ""
                elif count % 4 == 2:
                    back_text = card.get()
                elif count % 4 == 3:
                    if card.get() != "":
                        back_subtext = f"({card.get()})"
                    else:
                        back_subtext = ""

                    # Add completed card to pdf
                    pdf.addCard(front_text, front_subtext, back_text, back_subtext)
            
            # Export Pdf
            pdf.exportPdf()
        else:
            print("Exporting process canceled.")

    def translate_mode_switch_event(self):
        state = self.translate_mode_switch.get()

        if(state == 1):
            self.start_language_menu.configure(state='normal')
            self.end_language_menu.configure(state='normal')
        else:
            self.start_language_menu.configure(state='disabled')
            self.end_language_menu.configure(state='disabled')


if __name__ == "__main__":
    app = App()
    app.mainloop()
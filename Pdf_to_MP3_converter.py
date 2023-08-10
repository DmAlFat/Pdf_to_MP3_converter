from tkinter import *
from tkinter import ttk, filedialog
from gtts import gTTS
import pdfplumber
from pathlib import Path
from tkinter.messagebox import showerror, showinfo

root = Tk()
root.geometry("477x80+750+400")
root.title("PDF to MP3 converter")
icon = PhotoImage(file="icon.png")
root.iconphoto(False, icon)

label = ttk.Label(text="This program is developed to convert PDF file to MP3 file.\nAttention! An Internet connection is required for the correct operation of the program.")
label.pack(anchor=N, padx=10, pady=10)

language_input = 'en'


def dismiss(window):
    window.grab_release()
    window.destroy()


def click():
    window = Toplevel()
    window.title("PDF to MP3 converter")
    window.geometry("285x195+840+400")
    window.iconphoto(False, icon)
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    label = ttk.Label(window, text="1) Select language | Default: en")
    label.pack(anchor=N)


    def selected(event):
        global language_input
        language_input = combobox.get()
        label3["text"] = f"Selected language: {language_input}"

    languages = ["en", "ru"]

    label3 = ttk.Label(window)
    label3.pack(anchor=N, fill=X, padx=5, pady=5)
    combobox = ttk.Combobox(window, values=languages, state="readonly")
    combobox.pack(anchor=N, fill=X, padx=5, pady=5)
    combobox.bind("<<ComboboxSelected>>", selected)
    label4 = ttk.Label(window, text="2) Select pdf file and save file path\n3) Wait for the conversion to complete")
    label4.pack(anchor=N, padx=10, pady=10)

    def open_info():
        showinfo(title="Done", message=f'Mp3 saved successfully!')

    def open_error():
        showerror(title="Error", message="Wrong file's format, check the file's format!")

    def Pdf_to_MP3_converter():
        filepath = filedialog.askopenfilename()
        if Path(filepath).is_file() and Path(filepath).suffix == '.pdf':

            with pdfplumber.PDF(open(file=filepath, mode='rb')) as pdf:
                pages = [page.extract_text() for page in pdf.pages]

            text = ''.join(pages)
            text = text.replace('\n', '')

            mp3 = gTTS(text=text, lang=language_input.strip())
            file_name = Path(filepath).stem
            file_directory = filedialog.askdirectory()
            mp3.save(f'{file_directory}\{file_name}.mp3')

            return open_info()
        else:
            return open_error()

    close_button = ttk.Button(window, text="Select pdf file and save file path", command=Pdf_to_MP3_converter)
    close_button.pack(anchor="center", expand=1)
    label2 = ttk.Label(window, text="v.2.0")
    label2.pack(anchor=SW, expand=1)
    label1 = ttk.Label(window, text="Developed by DmAlFat")
    label1.pack(anchor=SE)
    window.grab_set()


open_button = ttk.Button(text="Start", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()


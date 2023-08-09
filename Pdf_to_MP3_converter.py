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
    window.geometry("340x180+820+400")
    window.iconphoto(False, icon)
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    editor = Text(window, height=1)
    editor.pack(anchor=N, fill=X)
    label = ttk.Label(window, text="1) Enter language ('en' or 'ru') and click apply (Default: en)\n2) Select pdf file and save file path\n3) Wait for the conversion to complete")
    label.pack(anchor=N, padx=10, pady=10)


    def get_text():
        global language_input
        language_input = editor.get("1.0", "2.0")

    close_button1 = ttk.Button(window, text="Apply language", command=get_text)
    close_button1.pack(anchor="s", expand=1)

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
    label2 = ttk.Label(window, text="v.1.3")
    label2.pack(anchor=SW, expand=1)
    label1 = ttk.Label(window, text="Developed by DmAlFat")
    label1.pack(anchor=SE)
    window.grab_set()


open_button = ttk.Button(text="Start", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()


from tkinter import *
from tkinter import ttk, filedialog
from gtts import gTTS
import pdfplumber
from pathlib import Path
from tkinter.messagebox import showerror, showinfo
from threading import Thread

root = Tk()
root.geometry("477x80+750+400")
root.title("PDF to MP3 converter")
icon = PhotoImage(file="icon.png")
root.iconphoto(False, icon)

label = ttk.Label(
    text="This program is developed to convert PDF file to MP3 file.\n"
         "Attention! An Internet connection is required for the correct operation of the program.")
label.pack(anchor=N, padx=10, pady=10)

language_input = 'en'  # create a global variable to display the default language


def dismiss(window):  # Definition of a function to intercept the closing of the launch window
    window.grab_release()
    window.destroy()


def click():
    window = Toplevel()
    window.title("PDF to MP3 converter")
    window.geometry("290x250+840+400")
    window.iconphoto(False, icon)
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    label0 = ttk.Label(window, text="1) Select language | Default: English")
    label0.pack(anchor=N)

    def selected(event):  # defining the language selection function from combox and changing the global variable
        global language_input
        language_input = languages[combobox.get()]
        label3["text"] = f"Selected language: {combobox.get()}"

    # dictionary to select value
    languages = {'English': "en", 'Русский': "ru", 'French': 'fr', 'Portuguese': 'pt', 'Spanish': 'es'}
    # reverse dictionary for key selection
    inverse_languages = {v: k for k, v in languages.items()}

    label3 = ttk.Label(window, text=f"Selected language: {inverse_languages[language_input]}")
    label3.pack(anchor=N, fill=X, padx=5, pady=5)
    combobox = ttk.Combobox(window, values=list(languages), state="readonly")
    combobox.pack(anchor=N, fill=X, padx=5, pady=5)
    combobox.bind("<<ComboboxSelected>>", selected)
    label4 = ttk.Label(window,
                       text="2) Select pdf file and the path to the saving file\n"
                            "      The conversion will start automatically")
    label4.pack(anchor=N, padx=5, pady=5)

    def open_info():
        showinfo(title="Done", message=f'Mp3 saved successfully!')

    def open_error():
        showerror(title="Error", message="Wrong file's format, check the file's format!")

    def Pdf_to_MP3_converter():
        filepath = filedialog.askopenfilename()  # file path selection
        if Path(filepath).is_file() and Path(filepath).suffix == '.pdf':  # Test file selection and format

            with pdfplumber.PDF(open(file=filepath, mode='rb')) as pdf:
                pages = [page.extract_text() for page in pdf.pages]

            text = ''.join(pages)
            text = text.replace('\n', '')

            mp3 = gTTS(text=text, lang=language_input)  # resort to API google
            file_name = Path(filepath).stem
            file_directory = filedialog.askdirectory()  # saving file path selection
            mp3.save(f'{file_directory}\{file_name}.mp3')
            progressbar.stop()
            return open_info()
        else:
            progressbar.stop()
            return open_error()

    def start():
        progressbar.start(25)

    def merge():  # create function to execute threads
        thread1 = Thread(target=start)  # creating a class Thread with a called function
        thread2 = Thread(target=Pdf_to_MP3_converter)
        thread1.start()  # method call for stream start
        thread2.start()

    close_button = ttk.Button(window, text="Select...", command=merge)
    close_button.pack(anchor="center", expand=1)
    progressbar = ttk.Progressbar(window, orient="horizontal", mode="indeterminate")
    progressbar.pack(fill=X, padx=5, pady=5)
    label5 = ttk.Label(window, text="3) Wait for the conversion to complete...")
    label5.pack(anchor=N, padx=5, pady=5)
    label2 = ttk.Label(window, text="v.2.2")
    label2.pack(anchor=SW)
    label1 = ttk.Label(window, text="Developed by DmAlFat")
    label1.pack(anchor=SE)
    window.grab_set()


open_button = ttk.Button(text="Start", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()

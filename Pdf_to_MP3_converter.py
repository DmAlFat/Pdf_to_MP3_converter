from gtts import gTTS
import pdfplumber
from pathlib import Path


def Pdf_to_MP3(file_path='test.pdf', language='en'):

    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':

        print(f'-> Input file: {Path(file_path).name}')
        print(f'-> Converting...')

        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]

        text = ''.join(pages)
        text = text.replace('\n', '')

        mp3 = gTTS(text=text, lang=language)
        file_name = Path(file_path).stem
        mp3.save(f'{file_name}.mp3')

        return f'-> {file_name}.mp3 saved successfully!'

    else:
        return 'File not found, check the file path!'


def main():
    file_path = input("Enter a file's path: ")
    language = input("Choose language ('en' or 'ru')")
    print(Pdf_to_MP3(file_path=file_path, language=language))


if __name__ == '__main__':
    main()
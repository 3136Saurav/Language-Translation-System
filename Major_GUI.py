import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from langdetect import detect
from PIL import Image, ImageTk
import speech_recognition as sr
from gtts import gTTS
import os
import smtplib
import webbrowser
import tempfile
import subprocess
import textract
from googletrans import Translator
from fpdf import FPDF

LARGE_FONT = {"Verdana", 12}


def finalTranslation(text_inp, get_lang):
    translator = Translator()
    translated_text = translator.translate(text_inp, dest=get_lang).text

    return translated_text

def docTextExtract(docfilename):
    str1 = str(textract.process(docfilename))
    str2 = str1.replace('b\'', ' ').replace('\\n', ' ').replace('\\b', '').replace('\\r', '').replace('\\x0c', '')\
           .replace('\\b','').replace('\'', '').replace('b\"', '').replace('\"', '').replace('■', ' ').replace('\\xc3\\xa2TM', '\'')
    return str2

def docInputOutput(extracted_text, lang_inp):
    return finalTranslation(extracted_text, lang_inp)

def ocr(path):
    temp = tempfile.NamedTemporaryFile(delete=False)

    process = subprocess.Popen(['tesseract', path, temp.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()

    with open(temp.name + '.txt', 'r') as handle:
        contents = handle.read()

    #os.remove(temp.name + '.txt')
     #os.remove(temp.name)

    return contents

def imageInputOutput(inputVar, lang_inp):
    return finalTranslation(inputVar, lang_inp)

def speechInputOutput(inputVar, lang_inp):
    modifiedInput = ''
    if detect(inputVar) != 'en':
        modifiedInput = finalTranslation(inputVar, 'English')
        print(modifiedInput)

    return finalTranslation(modifiedInput, lang_inp)

def textInputOutput(inputVar, lang_inp):
    text_inp = inputVar
    lang_inp = lang_inp.get()

    print(text_inp)
    print(lang_inp)

    return finalTranslation(text_inp, lang_inp)

def speechtoText():
    global spokenText
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            spokenText = r.recognize_google(audio)
            print("You said : {}".format(spokenText))
            return spokenText
            # print("You said : {}".format(text))
        except:
            print("Sorry could not recognize what you said")

def quit():  #Close the Window
    app.destroy()

class Welcome(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="light-bulb.ico")
        tk.Tk.wm_title(self, "Language Translation System")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, InputPageOne, ImageInputPage, TextInputPage, SpeechInputPage, DocumentInputPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="WELCOME TO LANGUAGE TRANSLATION SYSTEM", font=LARGE_FONT, fg="blue", bg="white")
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Next", width=25, command=lambda: controller.show_frame(InputPageOne))
        button1.pack()

        Close_button = ttk.Button(self, text="Close", width=25, command=quit)
        Close_button.pack()


class InputPageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Type of Input", font=LARGE_FONT, fg='blue', bg='white')
        label.pack(pady=10, padx=10)

        text_button = ttk.Button(self, text="TEXT", width=25, command=lambda: controller.show_frame(TextInputPage))
        text_button.pack()

        image_button = ttk.Button(self, text="IMAGE", width=25, command=lambda: controller.show_frame(ImageInputPage))
        image_button.pack()

        pdf_button = ttk.Button(self, text="DOC", width=25, command=lambda: controller.show_frame(DocumentInputPage))
        pdf_button.pack()

        speech_button = ttk.Button(self, text="SPEECH", width=25, command=lambda: controller.show_frame(SpeechInputPage))
        speech_button.pack()

        back_button = ttk.Button(self, text="Back to Homepage", width=25, command=lambda: controller.show_frame(StartPage))
        back_button.pack(pady=10, padx=10)

        Close_button = ttk.Button(self, text="Close", width=25, command=quit)
        Close_button.pack()


class TextInputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Enter Input Text", font=8)
        label1.pack(padx=10, pady=10)

        inputVar = tk.StringVar()
        print(type(inputVar))

        inputText = tk.Text(self, height=10, width=100)
        inputText.pack(padx=10, pady=10, expand=1)

        label2 = tk.Label(self, text="Translated Text", font=8)
        label2.pack(padx=10, pady=10)

        translatedText = tk.Text(self, height=10, width=100)
        translatedText.pack(padx=10, pady=10)

        inputText.delete('1.0',tk.END)
        translatedText.delete('1.0', tk.END)

        tkvar = tk.StringVar()
        choices = {'English', 'Hindi', 'Punjabi', 'Tamil', 'Sindhi', 'Malayalam', 'Marathi', 'Bengali', 'French',
                   'Spanish', 'Japanese'}
        tkvar.set('English')  # set the default option

        popupMenu = OptionMenu(self, tkvar, *choices)
        popupMenu.pack(padx=10, pady=10)

        convert_button = ttk.Button(self, text="Translate", command=lambda: translated_text(tkvar))
        convert_button.pack()

        def translated_text(tkvar):
            label1.config(text='Input', fg='blue')
            label2.config(fg='green')
            inputVar=inputText.get('1.0',tk.END)
            resulted_text = textInputOutput(inputVar, tkvar)
            print(resulted_text)
            translatedText.pack()
            translatedText.delete('1.0', tk.END)
            translatedText.insert('1.0', resulted_text)

        menu_button = ttk.Button(self, text="Back to Menu", width=25, command=lambda: controller.show_frame(InputPageOne))
        menu_button.pack()

        Close_button = ttk.Button(self, text="Close", width=25, command=quit)
        Close_button.pack()


class ImageInputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        uploadImageButton = ttk.Button(self, text="Upload Image", command=lambda: openFile())
        uploadImageButton.pack(padx=10, pady=10)

        l1 = tk.Label(self)
        l1.pack()

        def openFile():
            global filename
            filename = askopenfilename()
            l1.config(text='Uploaded')
            l1.config(fg='green', bg='white')

        label1 = tk.Label(self, text="Extracted Text", font=8)
        label1.pack(padx=10, pady=10)

        inputText = tk.Text(self, height=10, width=100)
        inputText.pack(padx=10, pady=10, expand=1)

        label2 = tk.Label(self, text="Translated Text", font=8)
        label2.pack(padx=10, pady=10)

        translatedText = tk.Text(self, height=10, width=100)
        translatedText.pack(padx=10, pady=10)

        tkvar = tk.StringVar()
        choices = {'English', 'Hindi', 'Punjabi', 'Tamil', 'Sindhi', 'Malayalam', 'Marathi', 'Bengali', 'French',
                   'Spanish', 'Japanese'}
        tkvar.set('English')  # set the default option

        popupMenu = OptionMenu(self, tkvar, *choices)
        popupMenu.pack(padx=10, pady=10)

        convert_button = ttk.Button(self, text="Translate", command=lambda: imageTranslateText(tkvar))
        convert_button.pack()

        #global text
            #return imageTranslateText(text, tkvar)

        def imageTranslateText(tkvar):
            label1.config(fg='blue')
            label2.config(fg='green')
            text = ocr(filename)
            print(tkvar.get())
            #inputText = tk.Text(self, height=10, width=100)
            #inputText.pack(padx=10, pady=10, expand=1)
            inputText.delete('1.0', tk.END)
            inputText.insert('1.0', text)
            resultedText = imageInputOutput(text, tkvar.get())
            translatedText.pack()
            translatedText.delete('1.0', tk.END)
            translatedText.insert('1.0', resultedText)

        menu_button = ttk.Button(self, text="Back to Menu", width=25, command=lambda: controller.show_frame(InputPageOne))
        menu_button.pack()

        Close_button = ttk.Button(self, text="Close", width=25, command=quit)
        Close_button.pack()

class DocumentInputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        uploadDocButton = ttk.Button(self, text="Upload Document", command=lambda : openFile())
        uploadDocButton.pack(padx=10, pady=10)

        l1 = tk.Label(self)
        l1.pack()

        def openFile():
            global docfilename
            docfilename = askopenfilename()
            l1.config(text='Uploaded')
            l1.config(fg='green', bg='white')

        label1 = tk.Label(self, text="Extracted Text", font=8)
        label1.pack(padx=10, pady=10)

        inputText = tk.Text(self, height=10, width=100)
        inputText.pack(padx=10, pady=10, expand=1)

        label2 = tk.Label(self, text="Translated Text", font=8)
        label2.pack(padx=10, pady=10)

        translatedText = tk.Text(self, height=10, width=100)
        translatedText.pack(padx=10, pady=10)

        tkvar = tk.StringVar()
        choices = {'English', 'Hindi', 'Punjabi', 'Tamil', 'Sindhi', 'Malayalam', 'Marathi', 'Bengali', 'French',
                   'Spanish', 'Japanese'}
        tkvar.set('English')  # set the default option

        popupMenu = OptionMenu(self, tkvar, *choices)
        popupMenu.pack(padx=10, pady=10)

        convert_button = ttk.Button(self, text="Translate", command=lambda: docTranslateText(tkvar))
        convert_button.pack()

        def docTranslateText(tkvar):
            label1.config(fg='blue')
            label2.config(fg='green')
            docText = docTextExtract(docfilename)
            print(tkvar.get())
            inputText.delete('1.0', tk.END)
            inputText.insert('1.0', docText)
            resultedText = docInputOutput(docText, tkvar.get())
            translatedText.pack()
            translatedText.delete('1.0', tk.END)
            translatedText.insert('1.0', resultedText)

        menu_button = ttk.Button(self, text="Back to Menu", width=25, command=lambda: controller.show_frame(InputPageOne))
        menu_button.pack()

        Close_button = ttk.Button(self, text="Close", width=25, command=quit)
        Close_button.pack()

class SpeechInputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        speechButton = ttk.Button(self, text="Input Speech", command=lambda:speechtoText())
        speechButton.pack(padx=10, pady=10)

        label1 = tk.Label(self, text="Extracted Text",font=8)
        label1.pack(padx=10, pady=10)

        inputText = tk.Text(self, height=10, width=100)
        inputText.pack(padx=10, pady=10, expand=1)

        label2 = tk.Label(self, text="Translated Text", font=8)
        label2.pack(padx=10, pady=10)

        translatedText = tk.Text(self, height=10, width=100)
        translatedText.pack(padx=10, pady=10)

        tkvar = tk.StringVar()
        choices = {'English', 'Hindi', 'Punjabi', 'Tamil', 'Sindhi', 'Malayalam', 'Marathi', 'Bengali', 'French',
                   'Spanish', 'Japanese'}
        tkvar.set('English')  # set the default option

        popupMenu = OptionMenu(self, tkvar, *choices)
        popupMenu.pack(padx=10, pady=10)

        convert_button = ttk.Button(self, text="Translate", command=lambda : translateText(tkvar))
        convert_button.pack()

        def translateText(tkvar):
            #speechText = speechtoText()
            label1.config(fg='blue')
            label2.config(fg='green')
            #speechInputOutput(spokenText, tkvar.get())
            inputText.delete('1.0', tk.END)
            inputText.insert('1.0', spokenText)
            resultedText = speechInputOutput(spokenText, tkvar.get())
            translatedText.pack()
            translatedText.delete('1.0', tk.END)
            translatedText.insert('1.0', resultedText)

            print(tkvar.get())
            print(spokenText)

        menu_button = ttk.Button(self, text="Back to Menu", width=25, command=lambda: controller.show_frame(InputPageOne))
        menu_button.pack()

        Close_button = ttk.Button(self, text="Close", width=25, command=quit)
        Close_button.pack()

app = Welcome()
app.mainloop()
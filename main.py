from tkinter import *
from PIL import Image, ImageTk
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3
import os

def speak_text(text):
    if text.strip() == "":
        return

    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Female
    else:
        engine.setProperty('voice', voices[0].id)

    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def search():
    textarea.delete(1.0, END)

    try:
        with open(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\data.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Dictionary data.json not found!")
        return

    word = enterwordEntry.get().strip().lower()

    if word == "":
        messagebox.showwarning("Warning", "Please enter a word!")
        return

    if word in data:
        show_meaning(data[word])
    else:
        matches = get_close_matches(word, data.keys())
        if matches:
            close = matches[0]
            res = messagebox.askyesno("Did you mean?", f"Did you mean '{close}'?")
            if res:
                enterwordEntry.delete(0, END)
                enterwordEntry.insert(END, close)
                show_meaning(data[close])
            else:
                textarea.insert(END, "No meaning found.\n")
        else:
            textarea.insert(END, "No meaning found.\n")

def show_meaning(data_value):
    textarea.delete(1.0, END)

    if isinstance(data_value, list):
        for meaning in data_value:
            textarea.insert(END, u'\u2022 ' + meaning + '\n\n')
    else:
        textarea.insert(END, u'\u2022 ' + data_value + '\n\n')


def clear():
    enterwordEntry.delete(0, END)
    textarea.delete(1.0, END)


def iexit():
    if messagebox.askyesno("Exit", "Do you really want to exit?"):
        root.destroy()


def wordaudio():
    speak_text(enterwordEntry.get())


def meaningaudio():
    speak_text(textarea.get(1.0, END))


def load_image(path):
    if os.path.exists(path):
        return ImageTk.PhotoImage(Image.open(path))
    else:
        messagebox.showerror("Image Error", f"Image not found:\n{path}")
        return None


root = Tk()
root.geometry("1000x626+100+30")
root.title("Talking Dictionary - By RAMU CHIKKA")
root.resizable(False, False)

# Background
bg_img = load_image(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\back.jpg")
if bg_img:
    Label(root, image=bg_img).place(x=0, y=0)

Label(root, text="Enter the Word", font=("castellar", 25, "bold"),bg="whitesmoke").place(x=520, y=20)

enterwordEntry = Entry(root, font=("arial", 23, "bold"), justify=CENTER, bd=8)
enterwordEntry.place(x=520, y=90)

# Buttons
search_img = load_image(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\search.png")
Button(root, image=search_img, bd=0, bg="darkgreen",activebackground="darkgreen", cursor="hand2",command=search).place(x=620, y=150)

mic_img = load_image(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\microphone.png")
Button(root, image=mic_img, bd=0, bg="green",activebackground="darkgreen", cursor="hand2",command=wordaudio).place(x=710, y=150)

Label(root, text="Meaning", font=("castellar", 25, "bold"),bg="whitesmoke").place(x=580, y=240)

textarea = Text(root, width=34, height=8, font=("arial", 18, "bold"), bd=8)
textarea.place(x=460, y=300)

audio_img = load_image(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\mic.png")
Button(root, image=audio_img, bd=0, bg="whitesmoke",cursor="hand2", activebackground="whitesmoke",command=meaningaudio).place(x=530, y=555)

clear_img = load_image(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\clear.png")
Button(root, image=clear_img, bd=0, bg="whitesmoke",cursor="hand2", activebackground="whitesmoke",command=clear).place(x=650, y=555)

exit_img = load_image(r"C:\Users\ADMIN\Desktop\Python_Projects\Talking_Dictonary\exit.png")
Button(root, image=exit_img, bd=0, bg="whitesmoke",cursor="hand2", activebackground="whitesmoke",command=iexit).place(x=780, y=555)


root.bind("<Return>", lambda e: search())

root.mainloop()

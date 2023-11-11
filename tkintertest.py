import tkinter as tk
import time
import itertools
from PIL import Image, ImageTk

class TypewriterLabel(tk.Label):
    def animate_text(self, text):
        self.displayed_text = ''
        self.full_text = text
        self.after(100, self.add_character)

    def add_character(self):
        if len(self.displayed_text) < len(self.full_text):
            self.displayed_text += self.full_text[len(self.displayed_text)]
            self.config(text=self.displayed_text)
            self.after(100, self.add_character)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.photos = self.load_gif("img/anim.gif")
        self.label = TypewriterLabel(self)
        self.label.pack(side="right")

        self.image_label = tk.Label(self)
        self.image_label.pack(side="left")
        self.animate(0)

        self.button = tk.Button(self)
        self.button["text"] = "Change Text"
        self.button["command"] = self.change_text
        self.button.pack(side="bottom")

    def load_gif(self, path):
        gif = Image.open(path)
        frames = []
        try:
            for i in itertools.count(1):
                gif.seek(i)
                frame = ImageTk.PhotoImage(gif.convert('RGBA'))
                frames.append(frame)
        except EOFError:
            pass
        return frames

    def animate(self, counter):
        self.image_label.config(image=self.photos[counter])
        self.master.after(20, self.animate, (counter+1) % len(self.photos))

    def change_text(self):
        self.label.animate_text('Lorem ipsum dolor sit amet')

root = tk.Tk()
root.geometry("1000x600")  # Set the window size
root.resizable(False, False)  # Make the window non-resizable
app = Application(master=root)
app.mainloop()
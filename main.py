"""
A flash card application that shows a user a word and allows a user to guess the definition of the word then shows them
the word after 5 seconds. They select whether they got it right and based on this, the word is removed from the list of
words. after the first round of words, the user is shown the words they got wrong and can guess again. This continues
until the user gets all the words correct.
"""

import random
import tkinter as tk
from tkinter import messagebox
import json
WORDS_FILE = "frequent-words-kiswahili.json"


# Create a class to hold the flash card
class FlashCard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.word_dict = None
        self.word_dict_index = None
        self.title("Flash Card")
        self.geometry("800x600")
        self.config(padx=50, pady=50, bg="#222222")
        self.words_data = self.load_data(words_file=WORDS_FILE)

        # Create a canvas to hold the flash card
        self.canvas = tk.Canvas(width=700, height=500, bg="white", highlightthickness=0)
        self.card_front = tk.PhotoImage(file="images/card_front.png")
        self.card_back = tk.PhotoImage(file="images/card_back.png")
        self.canvas_image = self.canvas.create_image(400, 263, image=self.card_front)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.get_word()

    def get_word(self):
        if len(self.words_data) == 0:
            messagebox.showinfo(title="Congratulations", message="You have completed the flash card game!")
            self.destroy()
        self.clear_old_labels()
        self.canvas.itemconfig(self.canvas_image, image=self.card_front)
        # select a random word from the dictionary
        self.word_dict_index = random.choice(list(self.words_data))
        self.word_dict = self.words_data[self.word_dict_index]

        # Create a label to hold the word
        self.word_label = tk.Label(text="", font=("Arial", 40, "bold"))
        self.word_label.config(bg="#F5D88B", fg="black", highlightthickness=0, text=self.word_dict["Kiswahili"])
        self.word_label.place(x=350, y=250, anchor="center")
        # flip the card after 3 seconds
        self.after(3000, self.flip_card)


    def flip_card(self):
        self.canvas.itemconfig(self.canvas_image, image=self.card_back)
        self.word_label.config(text=self.word_dict["English"], bg="#D2E4C7")
        # Create a button to indicate that the user failed to remember the meaning of the word
        self.wrong_button = tk.Button(text="𝘅", font=("Arial", 20, "bold"))
        self.wrong_button.config(bg="white", fg="black", highlightthickness=0, width=6,
                                 height=2, command=self.get_word)

        # Create a button to indicate that the user correctly remembered the meaning of the word
        self.right_button = tk.Button(text="✓", font=("Arial", 20, "bold"))
        self.right_button.config(bg="white", fg="black", highlightthickness=0, width=6,
                                 height=2, command=self.remove_word)
        self.right_button.place(x=200, y=450, anchor="center")
        self.wrong_button.place(x=600, y=450, anchor="center")

    def remove_word(self):
        self.words_data.pop(self.word_dict_index)
        self.get_word()

    def clear_old_labels(self):
        try:
            self.word_label.destroy()
            self.right_button.destroy()
            self.wrong_button.destroy()
        except AttributeError:
            pass

    def load_data(self, words_file) -> dict:
        try:
            with open(words_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror(title="File not found", message="The file containing the words was not found.")
            self.destroy()
flip_card = FlashCard()

flip_card.mainloop()

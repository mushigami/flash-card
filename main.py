import tkinter as tk
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
title_font = ("Ariel", 30, "italic")
word_font = ("Ariel", 60, "bold")

# ---------------------------- Card Funcs ------------------------------- #
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/dutch-frequency-dict-3000.csv")
word_dict = data.to_dict(orient="records")
print(len(word_dict))
current_word = {}


def next_card():
    global current_word
    global flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(word_dict)
    canvas.itemconfig(title_text, text="NL", fill="black")
    canvas.itemconfig(word_text, text=current_word["NL"], fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    flip_timer = window.after(3000, show_backside)


def show_backside():
    canvas.itemconfig(title_text, text="EN", fill="white")
    canvas.itemconfig(word_text, text=current_word["EN"], fill="white")
    canvas.itemconfig(canvas_image, image=back_img)


def is_known():
    word_dict.remove(current_word)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
# window
window = tk.Tk()
window.title("Flashy")
window.config(padx=30, pady=30, highlightthickness=0, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=next_card)

back_img = tk.PhotoImage(file="./images/card_back.png")
front_img = tk.PhotoImage(file="./images/card_front.png")

yes_button_img = tk.PhotoImage(file="./images/right.png")
no_button_img = tk.PhotoImage(file="./images/wrong.png")

canvas = tk.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
flash_card_img = tk.PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=flash_card_img)
title_text = canvas.create_text(400, 150, text="NL", font=title_font)
word_text = canvas.create_text(400, 263, text="word", font=word_font)
canvas.grid(row=0, column=0, columnspan=2)

# buttons
yes_button = tk.Button(image=yes_button_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0,
                       command=is_known)
yes_button.grid(row=1, column=1)

no_button = tk.Button(image=no_button_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0,
                      command=next_card)
no_button.grid(row=1, column=0)

next_card()  # To show a card in the beginning.

window.mainloop()

# ---------------------------- Save Data ------------------------------- #
print(len(word_dict))
new_data = pandas.DataFrame(word_dict)
new_data.to_csv("./data/words_to_learn.csv", index=False)

from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
rand_word = {}
data_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


# ------------------------------Random English Word--------------------------------

def random_english_word():
    canvas.itemconfig(front_card, image=card_back_img)
    canvas.itemconfig(lang_word, fill="white", text="English")
    canvas.itemconfig(fr_word, fill="white", text=rand_word["English"])


# ------------------------------Random French Word--------------------------------


def random_french_word():
    global rand_word, flip_timer
    window.after_cancel(flip_timer)
    rand_word = random.choice(data_dict)
    canvas.itemconfig(front_card, image=card_front_img)
    canvas.itemconfig(lang_word, fill="black", text="French")
    canvas.itemconfig(fr_word, fill="black", text=rand_word["French"])
    flip_timer = window.after(3000, func=random_english_word)


def know_word():
    data_dict.remove(rand_word)
    words_to_learn = pandas.DataFrame(data_dict)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    random_french_word()


# ------------------------------UI SECTION--------------------------------

window = Tk()

window.title("Flashy")
window.minsize(width=800, height=800)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=random_english_word)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)  # pixels
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
front_card = canvas.create_image(400, 263, image=card_front_img)
lang_word = canvas.create_text(400, 150, text="", fill="black", font=(FONT_NAME, 30, "italic"))
fr_word = canvas.create_text(400, 263, text="", fill="black", font=(FONT_NAME, 50, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, width=100, height=100, command=know_word)
right_btn.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, width=100, height=100, command=random_french_word)
wrong_btn.grid(column=0, row=1)

random_french_word()

window.mainloop()

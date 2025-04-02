import time
import customtkinter as ctk
import pyglet
import random
from itertools import cycle
import json

ctk.set_appearance_mode("dark")

#Hello

gradient_colors = cycle([ 
    "#ff0000", "#ff4000", "#ff8000", "#ffbf00", "#ffff00", 
    "#bfff00", "#80ff00", "#40ff00", "#00ff00", "#00ff40", 
    "#00ff80", "#00ffbf", "#00ffff", "#00bfff", "#0080ff", 
    "#0040ff", "#0000ff", "#4000ff", "#8000ff", "#bf00ff", 
    "#ff00ff", "#ff00bf", "#ff0080", "#ff0040" 
])

time_left = 30
correct_chars = 0  # Количество правильных символов
total_chars = 0  # Общее количество символов (включая ошибочные)
start_time = None  # Время начала игры
random_sentence = ""
letters = "FGHJ"
random_letter1 = random.choice(letters)

pyglet.font.add_file('Kanit-Medium.ttf')

score = 0
timer = 0
levels = {"Easy": "FGHJ",
          "Medium": "ASDFGHJKL",
          "Hard": "QWERTYUIOPASDFGHJKLZXCVBNM"}

with open("Sentences.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def get_new_sentence():
    return random.choice(data["sentences"])

random_sentence = get_new_sentence()

def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        time_widget.configure(text=format_time(time_left))
        root.after(1000, update_timer)
    else:
        end_screen()

def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"Timer : {minutes:02}:{secs:02}"

def animate_text(widgets):
    widgets.configure(text_color=next(gradient_colors))
    root.after(500, lambda: animate_text(widgets))

def end_screen():
    global correct_chars, total_chars, start_time
    for widget in root.winfo_children():
        widget.pack_forget()

    # Рассчитываем скорость печати и точность
    end_time = time.time() - start_time  # Время игры
    speed = (correct_chars / end_time) * 12  # Скорость печати в словах в минуту
    accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0  # Точность

    # Отображаем статистику
    stats = f"Speed: {speed:.2f} WPM\nAccuracy: {accuracy:.2f}%"
    stat_widget = ctk.CTkLabel(root, text=stats, font=("Kanit Medium", 20))
    stat_widget.pack()

def on_key(event):
    global random_sentence, score, correct_chars, total_chars, random_letter1
    print(f"Вы нажали: {event.char}")
    difficulty = optionmenu.get()
    mode = mode_menu.get()
    print(difficulty)
    
    if mode == "Sentences":
        if event.char == random_sentence[0]:
            random_sentence = random_sentence[1:]
            letter_widget.configure(text=random_sentence[0] if random_sentence else "")
            word_widget.configure(text=random_sentence[1:11] if random_sentence else "")
            score += 1
            correct_chars += 1  # Правильный символ
        total_chars += 1  # Все символы (включая ошибочные)
        score_widget.configure(text=f"Score : {score}")
        
        # Если пользователь ввел все символы в предложении, показываем новое предложение
        if not random_sentence:  # Если предложение пустое (все символы введены)
            random_sentence = get_new_sentence()  # Выбираем новое случайное предложение
            letter_widget.configure(text=random_sentence[0])
            word_widget.configure(text=random_sentence[1:11])

    if mode == "Letters":
        if event.char == random_letter1:
            random_letter1 = random.choice(levels[difficulty])
            letter_widget.configure(text=random_letter1)
            score += 1
            correct_chars += 1  # Правильный символ
        total_chars += 1  # Все символы (включая ошибочные)
        score_widget.configure(text=f"Score : {score}")

root = ctk.CTk()
root.geometry("400x400")
root.bind("<KeyPress>", on_key)

letter_widget = ctk.CTkLabel(root, text="A", font=("Kanit Medium", 60))
word_widget = ctk.CTkLabel(root, text="A", font=("Kanit Medium", 60), text_color="#696969")
score_widget = ctk.CTkLabel(root, text=f"Score : {score}", font=("Kanit Medium", 30))
time_widget = ctk.CTkLabel(root, text=f"Time : {timer}", font=("Kanit Medium", 30))

def game():
    global time_left, start_time, random_sentence
    start_time = time.time()  # Начинаем отсчет времени
    update_timer()
    mode = mode_menu.get()
    if mode == "Sentences":
        for widget in root.winfo_children():
            widget.pack_forget()
        score_widget.pack()
        time_widget.pack()

        letter_widget.pack(side="left", padx=(20, 0))
        letter_widget.configure(text=random_sentence[0])

        word_widget.pack(side="left")
        word_widget.configure(text=random_sentence[1:11])

        animate_text(letter_widget)
    else:
        for widget in root.winfo_children():
            widget.pack_forget()
        score_widget.pack()
        time_widget.pack()
        letter_widget.pack()
        letter_widget.configure(text=random_letter1)

        animate_text(letter_widget)

        if time_left == 0:
            end_screen()

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

optionmenu = ctk.CTkOptionMenu(root, values=["Easy", "Medium", "Hard"], command=optionmenu_callback, anchor="center")
mode_menu = ctk.CTkOptionMenu(root, values=["Sentences", "Letters"], command=optionmenu_callback, anchor="center")

optionmenu.set("Difficulty level")
optionmenu.pack(pady=10)
mode_menu.set("Mode")
mode_menu.pack(pady=10)

button_widget = ctk.CTkButton(root, command=game, text="Start")
button_widget.pack(pady=10)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import math
import os


class StanfordBinetTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест Стэнфорд-Бине")
        self.window.state('zoomed')

        # Цветовая схема
        self.colors = {
            "bg": "#faf0e6",
            "card": "#fff5e6",
            "primary": "#e6d5c0",
            "secondary": "#d4b8b0",
            "accent": "#c5b9b0",
            "text": "#5d5d5d",
            "light_text": "#8a8a8a",
            "correct": "#c1d5c7",
            "wrong": "#f0cfcf",
            "pattern": "#d9c9c0"
        }

        self.window.configure(bg=self.colors["bg"])

        # Данные пользователя
        self.user_data = {
            "name": "",
            "age": 0,
            "test_date": datetime.now().strftime("%d.%m.%Y"),
            "chronological_age_months": 0
        }

        # Состояние теста
        self.all_questions = []
        self.current_question_index = 0
        self.score = 0
        self.questions_answered = []
        self.start_time = None
        self.mental_age_months = 0
        self.timer_running = True
        self.total_questions = 60
        self.test_active = False
        self.answer_selected = False

        # Переменные для полей ввода
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()

        # Папка для сохранения результатов
        self.results_dir = "test_results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        # Показываем главное меню
        self.show_main_menu()

    def show_main_menu(self):
        """Показывает главное меню"""
        for widget in self.window.winfo_children():
            widget.destroy()

        main = tk.Frame(self.window, bg=self.colors["bg"])
        main.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        tk.Label(main, text="🧠 Тест Стэнфорд-Бине",
                 font=("Arial", 32, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=30)
        tk.Label(main, text="Пятая редакция",
                 font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["light_text"]).pack(pady=10)
        tk.Label(main, text="", bg=self.colors["bg"]).pack(pady=20)


# Запуск
if __name__ == "__main__":
    app = StanfordBinetTest()
    app.window.mainloop()
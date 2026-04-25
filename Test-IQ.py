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
    """
    ТЕСТ СТЭНФОРД-БИНЕ - Commit 2/10
    Добавлены узоры на фон и кнопка выхода
    """

    # Добавлено в __init__ после self.window.configure:
    self.create_patterns()

    # Добавлены кнопки в show_main_menu:
    btn_exit = tk.Button(main, text="❌ ВЫХОД", font=("Arial", 16, "bold"),
                         bg=self.colors["wrong"], fg=self.colors["text"],
                         command=self.window.quit, cursor="hand2")
    btn_exit.pack(pady=10)


    # Новая функция:
    def create_patterns(self):
        """Создаёт красивые узоры на фоне"""
        self.pattern_canvas = tk.Canvas(
            self.window,
            highlightthickness=0,
            bg=self.colors["bg"]
        )
        self.pattern_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def draw_patterns(event):
            self.pattern_canvas.delete("all")
            width = event.width
            height = event.height

            # Точки
            for x in range(0, width, 50):
                for y in range(0, height, 50):
                    if random.random() > 0.7:
                        self.pattern_canvas.create_oval(
                            x - 2, y - 2, x + 2, y + 2,
                            fill=self.colors["pattern"],
                            outline=""
                        )

            # Волнистые линии
            for y in range(0, height, 100):
                points = []
                for x in range(0, width, 20):
                    points.append(x)
                    points.append(y + 15 * math.sin(x / 50))
                self.pattern_canvas.create_line(
                    points,
                    fill=self.colors["pattern"],
                    width=1,
                    dash=(10, 20)
                )

            # Кружочки по углам
            for x in [20, width - 20]:
                for y in [20, height - 20]:
                    self.pattern_canvas.create_oval(
                        x - 15, y - 15, x + 15, y + 15,
                        outline=self.colors["pattern"],
                        width=1,
                        dash=(5, 5)
                    )

        self.pattern_canvas.bind("<Configure>", draw_patterns)
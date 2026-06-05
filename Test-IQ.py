"""
Добавлена база из 60 уникальных вопросов
"""

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

        # Создаём узоры на фоне
        self.create_patterns()

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

        # Загрузка 60 вопросов
        self.load_60_questions()

        self.show_main_menu()

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

            # Узор 1: Маленькие точки
            for x in range(0, width, 50):
                for y in range(0, height, 50):
                    if random.random() > 0.7:
                        self.pattern_canvas.create_oval(
                            x-2, y-2, x+2, y+2,
                            fill=self.colors["pattern"],
                            outline=""
                        )

            # Узор 2: Волнистые линии
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

            # Узор 3: Маленькие кружочки по углам
            for x in [20, width-20]:
                for y in [20, height-20]:
                    self.pattern_canvas.create_oval(
                        x-15, y-15, x+15, y+15,
                        outline=self.colors["pattern"],
                        width=1,
                        dash=(5, 5)
                    )

        self.pattern_canvas.bind("<Configure>", draw_patterns)

    def create_round_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Создаёт прямоугольник со скруглёнными углами"""
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def create_rounded_button(self, parent, text, command, bg_color=None, width=350, height=50):
        """Создаёт закруглённую кнопку"""
        if bg_color is None:
            bg_color = self.colors["primary"]
        frame = tk.Frame(parent, bg=self.colors["bg"])
        canvas = tk.Canvas(frame, width=width, height=height, bg=self.colors["bg"], highlightthickness=0)
        canvas.pack()
        self.create_round_rect(canvas, 5, 5, width-5, height-5, radius=25, fill=bg_color, outline=bg_color)
        canvas.create_text(width//2, height//2, text=text, font=("Arial", 14, "bold"), fill=self.colors["text"])
        canvas.tag_bind("all", "<Button-1>", lambda e: command())
        canvas.config(cursor="hand2")
        return frame

    def create_rounded_back_button(self, parent, command):
        """Создаёт маленькую закруглённую кнопку назад"""
        frame = tk.Frame(parent, bg=self.colors["bg"])
        canvas = tk.Canvas(frame, width=80, height=35, bg=self.colors["bg"], highlightthickness=0)
        canvas.pack()
        self.create_round_rect(canvas, 5, 5, 75, 30, radius=12, fill=self.colors["secondary"], outline=self.colors["secondary"])
        canvas.create_text(40, 17, text="← Назад", font=("Arial", 10, "bold"), fill=self.colors["text"])
        canvas.tag_bind("all", "<Button-1>", lambda e: command())
        canvas.config(cursor="hand2")
        return frame

    def create_rounded_entry(self, parent, textvariable, width=40):
        """Создаёт поле ввода со скруглёнными углами"""
        frame = tk.Frame(parent, bg=self.colors["bg"])
        frame.pack(fill="x", pady=5)
        canvas = tk.Canvas(frame, height=45, bg=self.colors["bg"], highlightthickness=0)
        canvas.pack(fill="x")
        entry = tk.Entry(canvas, textvariable=textvariable, font=("Arial", 14), bg="white", fg=self.colors["text"], relief="flat", bd=0)
        def redraw(e):
            canvas.delete("rect")
            w = e.width
            self.create_round_rect(canvas, 5, 5, w-5, 40, radius=15, fill="white", outline=self.colors["primary"], width=2, tags="rect")
            canvas.itemconfig(entry, width=w-20)
        canvas.bind("<Configure>", redraw)
        canvas.create_window(10, 22, window=entry, anchor="w", width=canvas.winfo_width()-20)
        return frame

    def add_question(self, level, text, answers, correct, factor):
        """Добавляет вопрос в список"""
        self.all_questions.append({
            'level': level, 'text': text, 'answers': answers,
            'correct': correct, 'factor': factor
        })

    def load_60_questions(self):
        """Загружает 60 уникальных вопросов"""

        questions_raw = [
            # УРОВЕНЬ 2-3 ГОДА (5 вопросов)
            (2, "Что бывает зелёным?", "Трава", ["Трава", "Снег", "Небо", "Солнце"], "Знания"),
            (2, "Какой звук издает корова?", "Му", ["Му", "Гав", "Мяу", "Хрю"], "Знания"),
            (2, "Что мы едим ложкой?", "Суп", ["Суп", "Хлеб", "Конфету", "Мороженое"], "Знания"),
            (2, "Сколько пальцев на одной руке?", "5", ["4", "5", "6", "3"], "Колич. мышление"),
            (2, "Какого цвета молоко?", "Белого", ["Белого", "Красного", "Синего", "Жёлтого"], "Знания"),

            # УРОВЕНЬ 3-4 ГОДА (5 вопросов)
            (3, "Кто дает молоко?", "Корова", ["Корова", "Курица", "Свинья", "Овца"], "Знания"),
            (3, "Сколько будет 1 + 2?", "3", ["3", "4", "5", "6"], "Колич. мышление"),
            (3, "Что бывает красным?", "Помидор", ["Помидор", "Трава", "Небо", "Снег"], "Знания"),
            (3, "Что летает в небе?", "Птица", ["Птица", "Рыба", "Кошка", "Собака"], "Знания"),
            (3, "Что мы пьем из чашки?", "Чай", ["Чай", "Суп", "Кашу", "Хлеб"], "Знания"),

            # УРОВЕНЬ 4-5 ЛЕТ (5 вопросов)
            (4, "Назови фрукт", "Яблоко", ["Яблоко", "Морковь", "Огурец", "Картошка"], "Знания"),
            (4, "Сколько будет 2 + 3?", "5", ["5", "6", "7", "8"], "Колич. мышление"),
            (4, "Что больше: 5 или 3?", "5", ["5", "3", "Одинаковы", "Не знаю"], "Колич. мышление"),
            (4, "Какой предмет нужен, чтобы писать?", "Ручка", ["Ручка", "Тарелка", "Стул", "Кровать"], "Знания"),
            (4, "Что светит на небе днем?", "Солнце", ["Солнце", "Луна", "Звезды", "Облака"], "Знания"),

            # УРОВЕНЬ 5-6 ЛЕТ (5 вопросов)
            (5, "Какое животное живет в воде?", "Рыба", ["Кошка", "Рыба", "Собака", "Птица"], "Знания"),
            (5, "Сколько будет 4 + 3?", "7", ["7", "8", "9", "10"], "Колич. мышление"),
            (5, "Что растет на дереве?", "Яблоко", ["Яблоко", "Морковь", "Картошка", "Огурец"], "Знания"),
            (5, "Сколько углов у треугольника?", "3", ["2", "3", "4", "5"], "Пространств. мышление"),
            (5, "Что мы надеваем зимой?", "Шубу", ["Шубу", "Шорты", "Футболку", "Сандалии"], "Знания"),

            # УРОВЕНЬ 6-7 ЛЕТ (5 вопросов)
            (6, "Столица России?", "Москва", ["Москва", "Санкт-Петербург", "Казань", "Новосибирск"], "Знания"),
            (6, "Сколько будет 5 + 4?", "9", ["9", "10", "11", "12"], "Колич. мышление"),
            (6, "Что лишнее: береза, дуб, роза, сосна?", "Роза", ["Роза", "Береза", "Дуб", "Сосна"], "Текучий интеллект"),
            (6, "Сколько дней в неделе?", "7", ["7", "5", "6", "8"], "Знания"),
            (6, "Как называется наша планета?", "Земля", ["Земля", "Марс", "Венера", "Юпитер"], "Знания"),

            # УРОВЕНЬ 7-8 ЛЕТ (5 вопросов)
            (7, "Сколько месяцев в году?", "12", ["12", "10", "11", "13"], "Знания"),
            (7, "Сколько будет 6 + 7?", "13", ["13", "12", "14", "15"], "Колич. мышление"),
            (7, "Продолжи: 3, 6, 9, 12, ?", "15", ["15", "14", "16", "18"], "Текучий интеллект"),
            (7, "Какая планета самая большая?", "Юпитер", ["Юпитер", "Марс", "Венера", "Земля"], "Знания"),
            (7, "Что такое ветер?", "Движение воздуха", ["Движение воздуха", "Дождь", "Снег", "Туча"], "Знания"),

            # УРОВЕНЬ 8-9 ЛЕТ (5 вопросов)
            (8, "Сколько будет 7 × 6?", "42", ["42", "48", "36", "54"], "Колич. мышление"),
            (8, "Какой газ необходим для дыхания?", "Кислород", ["Кислород", "Азот", "Водород", "Углекислый"], "Знания"),
            (8, "Сколько будет 24 ÷ 3?", "8", ["8", "6", "7", "9"], "Колич. мышление"),
            (8, "Что такое столица?", "Главный город", ["Главный город", "Большой дом", "Деньги", "Памятник"], "Знания"),
            (8, "Кто написал 'Золотой ключик'?", "Толстой", ["Толстой", "Пушкин", "Чуковский", "Маршак"], "Знания"),

            # УРОВЕНЬ 9-10 ЛЕТ (5 вопросов)
            (9, "Кто написал 'Война и мир'?", "Толстой", ["Толстой", "Достоевский", "Пушкин", "Чехов"], "Знания"),
            (9, "Сколько будет 81 ÷ 9?", "9", ["9", "7", "8", "10"], "Колич. мышление"),
            (9, "Продолжи: 1, 4, 9, 16, ?", "25", ["25", "20", "24", "36"], "Текучий интеллект"),
            (9, "Температура кипения воды?", "100°", ["100°", "90°", "110°", "120°"], "Знания"),
            (9, "Что такое атмосфера?", "Воздушная оболочка", ["Воздушная оболочка", "Водная оболочка", "Земная кора", "Магнитное поле"], "Знания"),

            # УРОВЕНЬ 10-11 ЛЕТ (5 вопросов)
            (10, "Самая высокая гора в мире?", "Эверест", ["Эверест", "Эльбрус", "Килиманджаро", "Монблан"], "Знания"),
            (10, "20% от 100 равно?", "20", ["20", "10", "30", "40"], "Колич. мышление"),
            (10, "Сколько осей симметрии у квадрата?", "4", ["4", "2", "6", "8"], "Пространств. мышление"),
            (10, "Какая фигура имеет бесконечно много осей симметрии?", "Круг", ["Круг", "Квадрат", "Треугольник", "Ромб"], "Пространств. мышление"),
            (10, "Что такое фотосинтез?", "Процесс у растений", ["Процесс у растений", "Дыхание", "Питание", "Рост"], "Знания"),

            # УРОВЕНЬ 11-12 ЛЕТ (5 вопросов)
            (11, "Кто изобрёл электрическую лампочку?", "Эдисон", ["Эдисон", "Тесла", "Фарадей", "Лодыгин"], "Знания"),
            (11, "x + 5 = 12. Чему равен x?", "7", ["7", "5", "6", "8"], "Колич. мышление"),
            (11, "Что больше: 1/2 или 2/3?", "2/3", ["2/3", "1/2", "Равны", "Нельзя сравнить"], "Колич. мышление"),
            (11, "Сколько рёбер у куба?", "12", ["12", "8", "16", "24"], "Пространств. мышление"),
            (11, "Что такое инерция?", "Свойство сохранять скорость", ["Свойство сохранять скорость", "Сила тяжести", "Движение", "Падение"], "Знания"),

            # УРОВЕНЬ 12-13 ЛЕТ (5 вопросов)
            (12, "Что такое гравитация?", "Притяжение", ["Притяжение", "Отталкивание", "Движение", "Скорость"], "Знания"),
            (12, "Решите: 15 + (3 × 4) - 7 = ?", "20", ["20", "15", "25", "30"], "Колич. мышление"),
            (12, "Продолжите ряд Фибоначчи: 1, 1, 2, 3, 5, 8, ?", "13", ["13", "11", "12", "14"], "Текучий интеллект"),
            (12, "Сколько диагоналей у пятиугольника?", "5", ["5", "6", "7", "8"], "Пространств. мышление"),
            (12, "Что такое теорема Пифагора?", "a² + b² = c²", ["a² + b² = c²", "a + b = c", "a × b = c", "a - b = c"], "Знания"),

            # УРОВЕНЬ 13-14 ЛЕТ (5 вопросов)
            (13, "Решите: 3² + 4² = ?", "25", ["25", "7", "12", "49"], "Колич. мышление"),
            (13, "Что такое проекция?", "Отображение на плоскость", ["Отображение на плоскость", "Увеличение", "Поворот", "Деление"], "Пространств. мышление"),
            (13, "Какая планета самая близкая к Солнцу?", "Меркурий", ["Меркурий", "Венера", "Земля", "Марс"], "Знания"),
            (13, "Что такое когнитивный диссонанс?", "Конфликт убеждений", ["Конфликт убеждений", "Потеря памяти", "Расстройство речи", "Нарушение сна"], "Знания"),
            (13, "Решите: sin(90°) = ?", "1", ["1", "0", "-1", "∞"], "Колич. мышление"),
        ]

        for level, text, correct_answer, answer_options, factor in questions_raw:
            options = list(enumerate(answer_options, 1))
            random.shuffle(options)
            shuffled_answers = [opt[1] for opt in options]
            new_correct = None
            for i, (original_pos, answer_text) in enumerate(options):
                if answer_text == correct_answer:
                    new_correct = i + 1
                    break
            self.add_question(level, text, shuffled_answers, new_correct, factor)

        print(f"Загружено {len(self.all_questions)} вопросов из 60")

    def show_main_menu(self):
        """Показывает главное меню"""
        for widget in self.window.winfo_children():
            if widget != self.pattern_canvas:
                widget.destroy()

        main = tk.Frame(self.window, bg=self.colors["bg"])
        main.place(relx=0.5, rely=0.5, anchor="center", width=600, height=650)

        tk.Label(main, text="🧠 Тест Стэнфорд-Бине",
                font=("Arial", 32, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=30)
        tk.Label(main, text="Пятая редакция",
                font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["light_text"]).pack(pady=10)
        tk.Label(main, text="", bg=self.colors["bg"]).pack(pady=20)

        btn_start = self.create_rounded_button(main, "🚀 НАЧАТЬ ТЕСТ", self.show_input_screen, self.colors["primary"], 350, 55)
        btn_start.pack(pady=10)

        btn_exit = self.create_rounded_button(main, "❌ ВЫХОД", self.window.quit, self.colors["wrong"], 350, 55)
        btn_exit.pack(pady=10)

    def show_input_screen(self):
        """Экран ввода данных"""
        self.timer_running = False
        for widget in self.window.winfo_children():
            if widget != self.pattern_canvas:
                widget.destroy()

        main = tk.Frame(self.window, bg=self.colors["bg"])
        main.pack(expand=True, fill="both", padx=50, pady=30)

        back_btn = self.create_rounded_back_button(main, self.show_main_menu)
        back_btn.place(x=10, y=10)

        tk.Label(main, text="🧠 Тест Стэнфорд-Бине",
                font=("Arial", 32, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=(20,5))
        tk.Label(main, text="Пятая редакция",
                font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["light_text"]).pack(pady=(0,20))

        info = tk.Frame(main, bg=self.colors["card"], relief="solid", bd=1)
        info.pack(pady=20, fill="x", padx=20)
        info_text = """Тест измеряет пять факторов когнитивных способностей:
        
• Fluid Reasoning (Текучий интеллект)
• Knowledge (Знания)
• Quantitative Reasoning (Количественное мышление)
• Visual-Spatial Processing (Визуально-пространственное мышление)
• Working Memory (Рабочая память)

Всего 60 вопросов для разных возрастных уровней."""
        tk.Label(info, text=info_text, font=("Arial", 11), bg=self.colors["card"],
                fg=self.colors["text"], justify="left", padx=20, pady=15).pack()

        form = tk.Frame(main, bg=self.colors["bg"])
        form.pack(fill="x", pady=20, padx=20)

        tk.Label(form, text="Ваше имя:", font=("Arial", 14, "bold"),
                bg=self.colors["bg"], fg=self.colors["text"], anchor="w").pack(fill="x", pady=(5,5))
        self.create_rounded_entry(form, self.name_var, 40).pack(fill="x", pady=5)

        tk.Label(form, text="Ваш возраст (полных лет):", font=("Arial", 14, "bold"),
                bg=self.colors["bg"], fg=self.colors["text"], anchor="w").pack(fill="x", pady=(15,5))
        self.create_rounded_entry(form, self.age_var, 40).pack(fill="x", pady=5)

        tk.Label(form, text="Например: 25", font=("Arial", 11),
                bg=self.colors["bg"], fg=self.colors["light_text"], anchor="w").pack(fill="x", pady=(5,20))

        start_btn = self.create_rounded_button(form, "🚀 НАЧАТЬ ТЕСТ", self.validate_and_start, self.colors["primary"], 700, 60)
        start_btn.pack(pady=20)

    def validate_and_start(self):
        """Проверка данных и начало теста"""
        name = self.name_var.get().strip()
        age_str = self.age_var.get().strip()

        if not name or not age_str:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            age = int(age_str)
            if age < 2:
                messagebox.showerror("Ошибка", "Возраст должен быть не менее 2 лет")
                return
            self.user_data["name"] = name
            self.user_data["age"] = age
            self.user_data["chronological_age_months"] = age * 12
            self.start_test()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный возраст")

    def start_test(self):
        """Начинает тест (заглушка)"""
        messagebox.showinfo("Информация", f"Тест начнется в следующей версии. Загружено {len(self.all_questions)} вопросов.")
        self.show_main_menu()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = StanfordBinetTest()
    app.run()
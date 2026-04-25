import tkinter as tk
from tkinter import ttk, messagebox
import random


class DifficultyIQTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест IQ - С выбором сложности")
        self.window.geometry("700x600")
        self.window.configure(bg="#1a1a2e")

        # Цветовая схема
        self.colors = {
            "bg": "#1a1a2e",
            "card": "#16213e",
            "primary": "#0f3460",
            "accent": "#e94560",
            "text": "#ffffff",
            "easy": "#2ecc71",
            "medium": "#f39c12",
            "hard": "#e74c3c"
        }

        # Загружаем вопросы по уровням
        self.questions = self.load_all_questions()

        # Показываем меню выбора сложности
        self.show_difficulty_menu()

    def load_all_questions(self):
        """Загружает вопросы по уровням сложности"""
        return {
            "easy": [
                {"category": "Математика", "text": "2 + 3 = ?",
                 "answers": ["4", "5", "6", "7"], "correct": 2, "points": 1},
                {"category": "Математика", "text": "10 ÷ 2 = ?",
                 "answers": ["3", "5", "7", "10"], "correct": 2, "points": 1},
                # ... ещё 8 вопросов для лёгкого уровня
            ],
            "medium": [
                {"category": "Математика", "text": "15 × 3 = ?",
                 "answers": ["30", "35", "40", "45"], "correct": 4, "points": 2},
                {"category": "Логика", "text": "Найдите лишнее:",
                 "answers": ["Собака", "Кошка", "Попугай", "Корова"], "correct": 3, "points": 2},
                # ... ещё 8 вопросов для среднего уровня
            ],
            "hard": [
                {"category": "Математика", "text": "√144 = ?",
                 "answers": ["10", "11", "12", "13"], "correct": 3, "points": 3},
                {"category": "Логика", "text": "Если A > B, B > C, то:",
                 "answers": ["A > C", "A < C", "A = C", "Нельзя определить"], "correct": 1, "points": 3},
                # ... ещё 8 вопросов для сложного уровня
            ]
        }

    def show_difficulty_menu(self):
        """Показывает меню выбора сложности"""
        # Очищаем окно
        for widget in self.window.winfo_children():
            widget.destroy()

        # Фон
        bg_frame = tk.Frame(self.window, bg=self.colors["bg"])
        bg_frame.pack(fill="both", expand=True)

        # Заголовок
        header = tk.Frame(bg_frame, bg=self.colors["primary"], height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🎯 ВЫБЕРИТЕ УРОВЕНЬ СЛОЖНОСТИ",
            font=("Arial", 20, "bold"),
            bg=self.colors["primary"],
            fg="white",
            pady=30
        ).pack()

        # Контент
        content = tk.Frame(bg_frame, bg=self.colors["bg"])
        content.pack(expand=True, fill="both", padx=40, pady=30)

        # Описание
        tk.Label(
            content,
            text="Тест состоит из 10 вопросов выбранного уровня",
            font=("Arial", 14),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            pady=20
        ).pack()

        # Кнопки выбора сложности
        difficulties = [
            ("🎯 ЛЁГКИЙ", "easy", self.colors["easy"],
             "10 простых вопросов\nДля начинающих"),
            ("⚡ СРЕДНИЙ", "medium", self.colors["medium"],
             "10 стандартных вопросов\nДля большинства"),
            ("🔥 СЛОЖНЫЙ", "hard", self.colors["hard"],
             "10 сложных вопросов\nДля экспертов")
        ]

        for text, level, color, description in difficulties:
            frame = tk.Frame(content, bg=self.colors["bg"])
            frame.pack(pady=15)

            # Кнопка выбора
            btn = tk.Button(
                frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg="white",
                width=25,
                height=2,
                command=lambda lvl=level: self.start_test(lvl),
                cursor="hand2"
            )
            btn.pack()

            # Описание
            tk.Label(
                frame,
                text=description,
                font=("Arial", 10),
                bg=self.colors["bg"],
                fg="#aaa"
            ).pack(pady=5)

    def start_test(self, difficulty):
        """Начинает тест выбранной сложности"""
        self.difficulty = difficulty
        self.test_questions = random.sample(self.questions[difficulty], 10)
        self.current_question = 0
        self.score = 0

        self.show_test_interface()
        self.show_question()

    def show_test_interface(self):
        """Показывает интерфейс теста"""
        # Очищаем окно
        for widget in self.window.winfo_children():
            widget.destroy()

        # Верхняя панель
        top_frame = tk.Frame(self.window, bg=self.colors["primary"], height=80)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        # Уровень сложности
        level_colors = {"easy": self.colors["easy"], "medium": self.colors["medium"], "hard": self.colors["hard"]}
        level_names = {"easy": "ЛЁГКИЙ", "medium": "СРЕДНИЙ", "hard": "СЛОЖНЫЙ"}

        tk.Label(
            top_frame,
            text=f"Уровень: {level_names[self.difficulty]}",
            font=("Arial", 14, "bold"),
            bg=level_colors[self.difficulty],
            fg="white",
            padx=20
        ).pack(side="left", padx=30, pady=25)

        # Счётчик вопросов
        self.counter_label = tk.Label(
            top_frame,
            text="Вопрос 1 из 10",
            font=("Arial", 14),
            bg=self.colors["primary"],
            fg="white"
        )
        self.counter_label.pack(side="right", padx=30, pady=25)

        # Прогресс-бар
        self.progress_bar = ttk.Progressbar(
            self.window,
            length=650,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)

        # Основной контент
        main_frame = tk.Frame(self.window, bg=self.colors["bg"])
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        # Категория
        self.category_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 12),
            bg=self.colors["card"],
            fg="#FFD700",
            padx=15,
            pady=5
        )
        self.category_label.pack(anchor="w", pady=(0, 10))

        # Вопрос
        self.question_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            wraplength=600,
            justify="left"
        )
        self.question_label.pack(anchor="w", pady=20)

        # Кнопки ответов
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                main_frame,
                text="",
                font=("Arial", 13),
                bg=self.colors["card"],
                fg=self.colors["text"],
                relief="solid",
                bd=1,
                width=60,
                height=2,
                anchor="w",
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=8, fill="x")
            self.answer_buttons.append(btn)

        # Кнопка "Далее"
        self.next_button = tk.Button(
            main_frame,
            text="Следующий вопрос →",
            font=("Arial", 14, "bold"),
            bg=self.colors["accent"],
            fg="white",
            state=tk.DISABLED,
            command=self.next_question,
            padx=30,
            pady=12
        )
        self.next_button.pack(pady=30)

    def show_question(self):
        """Показывает вопрос"""
        if self.current_question < len(self.test_questions):
            q = self.test_questions[self.current_question]

            # Обновляем счётчик
            self.counter_label.config(
                text=f"Вопрос {self.current_question + 1} из {len(self.test_questions)}"
            )

            # Обновляем прогресс
            progress = ((self.current_question + 1) / len(self.test_questions)) * 100
            self.progress_bar['value'] = progress

            # Показываем категорию
            self.category_label.config(text=f"📂 {q['category']} • ⚡ {q['points']} балла")

            # Показываем вопрос
            self.question_label.config(text=q['text'])

            # Показываем варианты
            for i, btn in enumerate(self.answer_buttons):
                btn.config(
                    text=f"{chr(65 + i)}) {q['answers'][i]}",
                    state=tk.NORMAL,
                    bg=self.colors["card"],
                    fg=self.colors["text"]
                )

            # Скрываем "Далее"
            self.next_button.config(state=tk.DISABLED)
        else:
            self.show_results()

    def check_answer(self, answer_idx):
        """Проверяет ответ"""
        q = self.test_questions[self.current_question]

        # Отключаем кнопки
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)

        # Проверяем
        is_correct = (answer_idx + 1 == q['correct'])

        # Подсвечиваем
        for i, btn in enumerate(self.answer_buttons):
            if i + 1 == q['correct']:
                btn.config(bg="#2ecc71", fg="white")
            elif i == answer_idx and not is_correct:
                btn.config(bg="#e74c3c", fg="white")

        # Начисляем баллы
        if is_correct:
            self.score += q['points']

        # Активируем "Далее"
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        """Следующий вопрос"""
        self.current_question += 1
        self.show_question()

    def show_results(self):
        """Показывает результаты"""
        total_points = sum(q['points'] for q in self.test_questions)
        percentage = (self.score / total_points) * 100

        # Разные формулы для разных уровней
        if self.difficulty == "easy":
            iq_score = 70 + (percentage * 0.6)
        elif self.difficulty == "medium":
            iq_score = 75 + (percentage * 0.5)
        else:  # hard
            iq_score = 80 + (percentage * 0.4)

        # Категория
        if iq_score < 85:
            category = "Ниже среднего"
            emoji = "📚"
        elif iq_score < 100:
            category = "Средний"
            emoji = "👍"
        elif iq_score < 115:
            category = "Выше среднего"
            emoji = "🎯"
        else:
            category = "Высокий"
            emoji = "🌟"

        result_text = f"""
{emoji} РЕЗУЛЬТАТЫ ТЕСТА {emoji}

📊 Уровень: {self.difficulty.upper()}
✅ Баллы: {self.score} из {total_points}
📈 Процент: {percentage:.1f}%

🧮 Ваш IQ: {iq_score:.0f}
🏷️ Категория: {category}

💡 Рекомендации:
Продолжайте тренировать мышление
регулярными упражнениями!
"""

        messagebox.showinfo("Результаты теста", result_text)

        # Спрашиваем, хочет ли пользователь пройти ещё раз
        if messagebox.askyesno("Тест завершён", "Хотите пройти тест ещё раз?"):
            self.show_difficulty_menu()
        else:
            self.window.quit()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()


# Запуск
if __name__ == "__main__":
    app = DifficultyIQTest()
    app.run()
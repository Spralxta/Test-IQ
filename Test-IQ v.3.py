"""
ВЕРСИЯ 3: Улучшенный GUI с категориями вопросов
Добавлены: таймер, больше вопросов, категории
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random


class ImprovedIQTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест IQ - Улучшенная версия")
        self.window.geometry("600x550")
        self.window.configure(bg="#f0f0f0")

        # Загружаем больше вопросов с категориями
        self.questions = self.load_questions()
        random.shuffle(self.questions)
        self.questions = self.questions[:10]  # 10 вопросов

        # Переменные
        self.current_question = 0
        self.score = 0
        self.time_left = 600  # 10 минут на тест

        # Интерфейс
        self.create_interface()
        self.show_question()
        self.update_timer()

    def load_questions(self):
        """Загружает вопросы с категориями"""
        return [
            # Математика
            {"category": "Математика", "text": "15 + 27 = ?",
             "answers": ["40", "42", "44", "45"], "correct": 2},
            {"category": "Математика", "text": "7 × 8 = ?",
             "answers": ["48", "54", "56", "64"], "correct": 3},

            # Логика
            {"category": "Логика", "text": "Стол → Дерево = Стакан → ?",
             "answers": ["Вода", "Стекло", "Кухня", "Прозрачный"], "correct": 2},
            {"category": "Логика", "text": "Найдите лишнее:",
             "answers": ["Яблоко", "Груша", "Морковь", "Апельсин"], "correct": 3},

            # Слова
            {"category": "Слова", "text": "Синоним слова 'БЫСТРЫЙ':",
             "answers": ["Скорый", "Тихий", "Долгий", "Тяжёлый"], "correct": 1},
            {"category": "Слова", "text": "Антоним 'ВЫСОКИЙ':",
             "answers": ["Широкий", "Низкий", "Длинный", "Большой"], "correct": 2},

            # Общие знания
            {"category": "Общие", "text": "Сколько планет в Солнечной системе?",
             "answers": ["7", "8", "9", "10"], "correct": 2},
            {"category": "Общие", "text": "Самый большой океан?",
             "answers": ["Атлантический", "Индийский", "Северный Ледовитый", "Тихий"], "correct": 4},

            # Пространственное мышление
            {"category": "Пространство", "text": "Сколько углов у шестиугольника?",
             "answers": ["5", "6", "7", "8"], "correct": 2},
            {"category": "Пространство", "text": "Какая фигура следующая? ◻ ◼ ◻ ◼ ◻ ?",
             "answers": ["◻", "◼", "●", "▲"], "correct": 2},

            # Ещё вопросы...
            {"category": "Математика", "text": "½ + ¼ = ?",
             "answers": ["¼", "½", "¾", "1"], "correct": 3},
            {"category": "Логика", "text": "Если все кошки - животные, то:",
             "answers": ["Все животные - кошки", "Некоторые животные - кошки",
                         "Кошки не животные", "Нельзя определить"], "correct": 2}
        ]

    def create_interface(self):
        """Создаёт интерфейс"""
        # Заголовок
        header = tk.Frame(self.window, bg="#4CAF50", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧠 ТЕСТ IQ - УЛУЧШЕННАЯ ВЕРСИЯ",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=20
        ).pack()

        # Информационная панель
        info_frame = tk.Frame(self.window, bg="#f0f0f0")
        info_frame.pack(fill="x", padx=20, pady=10)

        # Таймер
        self.timer_label = tk.Label(
            info_frame,
            text="⏱️ Время: 10:00",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333"
        )
        self.timer_label.pack(side="left")

        # Счёт вопросов
        self.counter_label = tk.Label(
            info_frame,
            text="Вопрос 1 из 10",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333"
        )
        self.counter_label.pack(side="right")

        # Прогресс-бар
        self.progress_bar = ttk.Progressbar(
            self.window,
            length=560,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)

        # Основное окно
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Категория вопроса
        self.category_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 11, "bold"),
            bg="#E3F2FD",
            fg="#1565C0",
            padx=10,
            pady=5
        )
        self.category_label.pack(anchor="w", pady=(0, 10))

        # Текст вопроса
        self.question_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#222",
            wraplength=550,
            justify="left"
        )
        self.question_label.pack(anchor="w", pady=10)

        # Кнопки ответов
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                main_frame,
                text="",
                font=("Arial", 12),
                bg="white",
                fg="#333",
                relief="solid",
                bd=1,
                width=50,
                height=2,
                anchor="w",
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=8, fill="x")
            self.answer_buttons.append(btn)

        # Кнопка далее
        self.next_button = tk.Button(
            self.window,
            text="Следующий вопрос →",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            state=tk.DISABLED,
            command=self.next_question,
            padx=20,
            pady=10
        )
        self.next_button.pack(pady=15)

    def show_question(self):
        """Показывает вопрос"""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]

            # Обновляем счётчик
            self.counter_label.config(
                text=f"Вопрос {self.current_question + 1} из {len(self.questions)}"
            )

            # Обновляем прогресс
            progress = ((self.current_question + 1) / len(self.questions)) * 100
            self.progress_bar['value'] = progress

            # Показываем категорию
            self.category_label.config(text=f"📁 Категория: {q['category']}")

            # Показываем вопрос
            self.question_label.config(text=q['text'])

            # Показываем варианты
            for i, btn in enumerate(self.answer_buttons):
                btn.config(
                    text=f"{chr(65 + i)}) {q['answers'][i]}",
                    state=tk.NORMAL,
                    bg="white",
                    fg="#333"
                )

            # Скрываем "Далее"
            self.next_button.config(state=tk.DISABLED)
        else:
            self.show_results()

    def check_answer(self, answer_idx):
        """Проверяет ответ"""
        q = self.questions[self.current_question]

        # Отключаем кнопки
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)

        # Проверяем
        is_correct = (answer_idx + 1 == q['correct'])

        # Подсвечиваем
        for i, btn in enumerate(self.answer_buttons):
            if i + 1 == q['correct']:
                btn.config(bg="#C8E6C9", fg="#1B5E20")  # Зелёный
            elif i == answer_idx and not is_correct:
                btn.config(bg="#FFCDD2", fg="#B71C1C")  # Красный

        # Начисляем баллы
        if is_correct:
            self.score += 1

        # Активируем "Далее"
        self.next_button.config(state=tk.NORMAL)

    def update_timer(self):
        """Обновляет таймер"""
        if self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f"⏱️ Время: {minutes:02d}:{seconds:02d}")

            if hasattr(self, 'window') and self.window.winfo_exists():
                self.time_left -= 1
                self.window.after(1000, self.update_timer)
        else:
            # Время вышло
            messagebox.showwarning("Время вышло!", "Время на прохождение теста истекло!")
            self.show_results()

    def next_question(self):
        """Следующий вопрос"""
        self.current_question += 1
        self.show_question()

    def show_results(self):
        """Показывает результаты"""
        # Останавливаем таймер
        self.time_left = 0

        # Рассчитываем IQ
        percentage = (self.score / len(self.questions)) * 100
        iq_score = 75 + (percentage * 0.45)

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

        # Статистика по категориям
        category_stats = {}
        for i in range(min(self.current_question, len(self.questions))):
            q = self.questions[i]
            cat = q['category']
            if cat not in category_stats:
                category_stats[cat] = {'total': 0, 'correct': 0}
            category_stats[cat]['total'] += 1

        # Формируем текст
        result_text = f"""
{emoji} РЕЗУЛЬТАТЫ ТЕСТА {emoji}

✅ Правильных ответов: {self.score} из {len(self.questions)}
📊 Процент правильных: {percentage:.1f}%

🧮 Ваш IQ: {iq_score:.0f}
🏷️ Категория: {category}

📈 Статистика по категориям:
"""

        for cat, stats in category_stats.items():
            result_text += f"• {cat}: {stats['total']} вопросов\n"

        result_text += "\n🎯 Продолжайте развивать мышление!"

        messagebox.showinfo("Результаты теста", result_text)
        self.window.quit()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()


# Запуск
if __name__ == "__main__":
    app = ImprovedIQTest()
    app.run()
"""
ВЕРСИЯ 2: Базовый GUI с Tkinter
Простой интерфейс с одним вопросом на экране
"""

import tkinter as tk
from tkinter import messagebox


class SimpleIQTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест IQ - Базовая версия")
        self.window.geometry("500x400")

        # Вопросы
        self.questions = [
            ["2 + 2 = ?", "3", "4", "5", "6", 2],
            ["Столица России?", "Москва", "Санкт-Петербург", "Казань", "Новосибирск", 1],
            ["Сколько дней в неделе?", "5", "6", "7", "8", 3],
            ["Яблоко - это...", "Овощ", "Фрукт", "Ягода", "Зерно", 2],
            ["Солнце - это...", "Планета", "Звезда", "Спутник", "Комета", 2]
        ]

        self.current_question = 0
        self.score = 0

        # Создаём интерфейс
        self.create_widgets()
        self.show_question()

    def create_widgets(self):
        """Создаёт виджеты интерфейса"""
        # Заголовок
        self.title_label = tk.Label(
            self.window,
            text="Тест IQ - 5 вопросов",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=10)

        # Прогресс
        self.progress_label = tk.Label(
            self.window,
            text="Вопрос 1 из 5",
            font=("Arial", 10)
        )
        self.progress_label.pack()

        # Вопрос
        self.question_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 14),
            wraplength=450,
            justify="center"
        )
        self.question_label.pack(pady=20)

        # Кнопки ответов
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.window,
                text="",
                font=("Arial", 12),
                width=30,
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        # Кнопка далее
        self.next_button = tk.Button(
            self.window,
            text="Следующий вопрос →",
            font=("Arial", 12),
            state=tk.DISABLED,
            command=self.next_question
        )
        self.next_button.pack(pady=20)

    def show_question(self):
        """Показывает текущий вопрос"""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]

            # Обновляем прогресс
            self.progress_label.config(
                text=f"Вопрос {self.current_question + 1} из {len(self.questions)}"
            )

            # Показываем вопрос
            self.question_label.config(text=q[0])

            # Показываем варианты
            for i, btn in enumerate(self.answer_buttons):
                btn.config(text=f"{i + 1}) {q[i + 1]}", state=tk.NORMAL, bg="SystemButtonFace")

            # Скрываем кнопку "Далее"
            self.next_button.config(state=tk.DISABLED)
        else:
            self.show_results()

    def check_answer(self, answer_idx):
        """Проверяет ответ"""
        q = self.questions[self.current_question]

        # Отключаем кнопки
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)

        # Проверяем ответ
        if answer_idx + 1 == q[5]:
            self.score += 1
            for i, btn in enumerate(self.answer_buttons):
                if i == answer_idx:
                    btn.config(bg="lightgreen")
        else:
            for i, btn in enumerate(self.answer_buttons):
                if i == answer_idx:
                    btn.config(bg="salmon")
                elif i + 1 == q[5]:
                    btn.config(bg="lightgreen")

        # Активируем кнопку "Далее"
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        """Следующий вопрос"""
        self.current_question += 1
        self.show_question()

    def show_results(self):
        """Показывает результаты"""
        iq = 80 + (self.score * 5)

        result_text = f"""
Результаты теста:

✅ Правильных ответов: {self.score} из {len(self.questions)}
🧮 Примерный IQ: {iq}

"""
        if self.score == 5:
            result_text += "🎉 Отличный результат!"
        elif self.score >= 3:
            result_text += "👍 Хороший результат!"
        else:
            result_text += "📚 Есть куда расти!"

        messagebox.showinfo("Результаты теста", result_text)
        self.window.quit()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()


# Запуск
if __name__ == "__main__":
    app = SimpleIQTest()
    app.run()
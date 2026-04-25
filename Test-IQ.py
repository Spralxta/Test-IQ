import tkinter as tk


class StanfordBinetTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест Стэнфорд-Бине")
        self.window.state('zoomed')

        self.colors = {
            "bg": "#faf0e6",
            "primary": "#e6d5c0",
            "secondary": "#d4b8b0",
            "text": "#5d5d5d",
        }

        self.window.configure(bg=self.colors["bg"])
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        main = tk.Frame(self.window, bg=self.colors["bg"])
        main.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        tk.Label(main, text="🧠 Тест Стэнфорд-Бине",
                 font=("Arial", 32, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=30)
        tk.Label(main, text="Пятая редакция",
                 font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=10)


if __name__ == "__main__":
    app = StanfordBinetTest()
    app.window.mainloop()
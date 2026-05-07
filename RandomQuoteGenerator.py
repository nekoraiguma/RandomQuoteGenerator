import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime
import os

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("900x700")

        # Список цитат: [{"text": , "author": , "theme": }]
        self.quotes = self.load_initial_quotes()
        self.history = self.load_history()

        self.create_widgets()
        self.update_history_display()

    def load_initial_quotes(self):
        default_quotes = [
            {"text": "Жизнь — это то, что с тобой происходит, пока ты занят другими планами.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "Мотивация"},
            {"text": "Всё, что мы видим — это лишь сон внутри сна.", "author": "Эдгар Аллан По", "theme": "Философия"},
            {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Мотивация"},
            {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "theme": "Знание"},
            {"text": "Простота — это высшая степень изысканности.", "author": "Леонардо да Винчи", "theme": "Мудрость"},
        ]

        # Загружаем из файла, если существует
        if os.path.exists("quotes.json"):
            try:
                with open("quotes.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return default_quotes

    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # === Верхняя панель ===
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        ttk.Button(top_frame, text="🎲 Сгенерировать цитату", command=self.generate_quote).pack(side="left", padx=5)

        ttk.Button(top_frame, text="➕ Добавить цитату", command=self.add_quote_window).pack(side="left", padx=5)

        ttk.Button(top_frame, text="🗑 Очистить историю", command=self.clear_history).pack(side="right", padx=5)

        # === Фильтры ===
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
        self.author_var = tk.StringVar()
        self.author_combo = ttk.Combobox(filter_frame, textvariable=self.author_var, width=30)
        self.author_combo.grid(row=0, column=1, padx=5)
        self.author_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())

        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self.theme_var = tk.StringVar()
        self.theme_combo = ttk.Combobox(filter_frame, textvariable=self.theme_var, width=30)
        self.theme_combo.grid(row=0, column=3, padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())

        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=0, column=4, padx=10)

        # === Текущая цитата ===
        current_frame = ttk.LabelFrame(self.root, text="Текущая цитата", padding=15)
        current_frame.pack(fill="x", padx=10, pady=5)

        self.current_text = tk.Text(current_frame, wrap="word", height=6, font=("Arial", 11))
        self.current_text.pack(fill="x", padx=5, pady=5)

        self.current_info = ttk.Label(current_frame, text="", font=("Arial", 10, "italic"))
        self.current_info.pack()

        # === История ===
        history_frame = ttk.LabelFrame(self.root, text="История сгенерированных цитат", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview для истории
        columns = ("date", "text", "author", "theme")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=15)

        self.tree.heading("date", text="Дата")
        self.tree.heading("text", text="Цитата")
        self.tree.heading("author", text="Автор")
        self.tree.heading("theme", text="Тема")

        self.tree.column("date", width=120)
        self.tree.column("text", width=400)
        self.tree.column("author", width=150)
        self.tree.column("theme", width=100)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Обновляем комбобоксы с авторами и темами
        self.update_filters()

    def update_filters(self):
        authors = sorted(set(q["author"] for q in self.quotes))
        themes = sorted(set(q["theme"] for q in self.quotes))

        self.author_combo['values'] = [""] + authors
        self.theme_combo['values'] = [""] + themes

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Ошибка", "Список цитат пуст!")
            return

        quote = random.choice(self.quotes)
        
        # Добавляем в историю
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"]
        }
        self.history.insert(0, entry)  # новые сверху
        self.save_history()

        # Отображаем текущую
        self.current_text.delete(1.0, tk.END)
        self.current_text.insert(tk.END, quote["text"])
        
        self.current_info.config(
            text=f"— {quote['author']} | {quote['theme']}"
        )

        self.update_history_display()

    def update_history_display(self, filtered_history=None):
        # Очищаем
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = filtered_history if filtered_history is not None else self.history

        for entry in data:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["text"][:80] + "..." if len(entry["text"]) > 80 else entry["text"],
                entry["author"],
                entry["theme"]
            ))

    def filter_history(self):
        author = self.author_var.get()
        theme = self.theme_var.get()

        filtered = self.history

        if author:
            filtered = [q for q in filtered if q["author"] == author]
        if theme:
            filtered = [q for q in filtered if q["theme"] == theme]

        self.update_history_display(filtered)

    def reset_filters(self):
        self.author_var.set("")
        self.theme_var.set("")
        self.update_history_display()

    def add_quote_window(self):
        win = tk.Toplevel(self.root)
        win.title("Добавить новую цитату")
        win.geometry("500x300")

        ttk.Label(win, text="Текст цитаты:").pack(anchor="w", padx=10, pady=5)
        text_entry = tk.Text(win, height=6, width=60)
        text_entry.pack(padx=10, pady=5)

        ttk.Label(win, text="Автор:").pack(anchor="w", padx=10, pady=5)
        author_entry = ttk.Entry(win, width=50)
        author_entry.pack(padx=10, pady=5)

        ttk.Label(win, text="Тема:").pack(anchor="w", padx=10, pady=5)
        theme_entry = ttk.Entry(win, width=50)
        theme_entry.pack(padx=10, pady=5)

        def save():
            text = text_entry.get("1.0", tk.END).strip()
            author = author_entry.get().strip()
            theme = theme_entry.get().strip()

            if not text or not author or not theme:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            self.quotes.append({"text": text, "author": author, "theme": theme})
            
            # Сохраняем обновлённый список цитат
            with open("quotes.json", "w", encoding="utf-8") as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=2)

            self.update_filters()
            messagebox.showinfo("Успех", "Цитата успешно добавлена!")
            win.destroy()

        ttk.Button(win, text="Сохранить цитату", command=save).pack(pady=10)

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history.clear()
            self.save_history()
            self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGeneratorApp(root)
    root.mainloop()
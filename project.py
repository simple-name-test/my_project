import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")
        
        # Данные
        self.filename = "movies.json"
        self.movies = []
        self.load_movies()
        
        # Создаём интерфейс
        self.create_widgets()
        
        # Показываем фильмы
        self.update_table()
    
    def create_widgets(self):
        # Рамка для ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        # Поля ввода
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5)
        self.title_entry = tk.Entry(input_frame, width=20)
        self.title_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5)
        self.genre_entry = tk.Entry(input_frame, width=15)
        self.genre_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Год:").grid(row=1, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5)
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5)
        
        # Кнопка добавления
        self.add_btn = tk.Button(input_frame, text="Добавить фильм", 
                                  command=self.add_movie, bg="lightgreen")
        self.add_btn.grid(row=1, column=4, padx=10)
        
        # Рамка для фильтров
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side=tk.LEFT, padx=5)
        self.filter_genre = tk.Entry(filter_frame, width=15)
        self.filter_genre.pack(side=tk.LEFT, padx=5)
        self.filter_genre.bind("<KeyRelease>", lambda e: self.update_table())
        
        tk.Label(filter_frame, text="Фильтр по году:").pack(side=tk.LEFT, padx=5)
        self.filter_year = tk.Entry(filter_frame, width=10)
        self.filter_year.pack(side=tk.LEFT, padx=5)
        self.filter_year.bind("<KeyRelease>", lambda e: self.update_table())
        
        tk.Button(filter_frame, text="Сбросить", command=self.clear_filters).pack(side=tk.LEFT, padx=10)
        
        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Название", "Жанр", "Год", "Рейтинг"), 
                                 show="headings", height=15)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Заголовки
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        
        # Ширина колонок
        self.tree.column("Название", width=250)
        self.tree.column("Жанр", width=120)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        
        # Кнопка удаления
        self.del_btn = tk.Button(self.root, text="Удалить выбранный фильм", 
                                  command=self.delete_movie, bg="lightcoral")
        self.del_btn.pack(pady=5)
    
    def add_movie(self):
        # Получаем данные
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        # Проверки
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны!")
            return
        
        # Проверка года
        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        year_num = int(year)
        if year_num < 1888 or year_num > 2026:
            messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026!")
            return
        
        # Проверка рейтинга
        try:
            rating_num = float(rating)
            if rating_num < 0 or rating_num > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return
        except:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return
        
        # Добавляем фильм
        movie = {
            "title": title,
            "genre": genre,
            "year": year_num,
            "rating": rating_num
        }
        
        self.movies.append(movie)
        self.save_movies()
        
        # Очищаем поля
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        
        # Обновляем таблицу
        self.update_table()
        messagebox.showinfo("Успех", "Фильм добавлен!")
    
    def update_table(self):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем фильтры
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()
        
        # Фильтруем фильмы
        filtered = []
        for movie in self.movies:
            # Фильтр по жанру
            if genre_filter and genre_filter not in movie["genre"].lower():
                continue
            
            # Фильтр по году
            if year_filter:
                if year_filter.isdigit():
                    if movie["year"] != int(year_filter):
                        continue
                else:
                    continue
            
            filtered.append(movie)
        
        # Показываем фильмы в таблице
        for movie in filtered:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))
    
    def delete_movie(self):
        # Получаем выбранный фильм
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите фильм для удаления!")
            return
        
        # Получаем название выбранного фильма
        values = self.tree.item(selected[0])["values"]
        title = values[0]
        
        # Подтверждение
        if messagebox.askyesno("Подтверждение", f"Удалить фильм '{title}'?"):
            # Удаляем из списка
            for i, movie in enumerate(self.movies):
                if movie["title"] == title and movie["year"] == values[2]:
                    self.movies.pop(i)
                    break
            
            # Сохраняем и обновляем
            self.save_movies()
            self.update_table()
            messagebox.showinfo("Успех", "Фильм удалён!")
    
    def clear_filters(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table()
    
    def save_movies(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
    
    def load_movies(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        else:
            # Пример начальных данных
            self.movies = [
                {"title": "Побег из Шоушенка", "genre": "Драма", "year": 1994, "rating": 9.3},
                {"title": "Крёстный отец", "genre": "Драма", "year": 1972, "rating": 9.2},
                {"title": "Тёмный рыцарь", "genre": "Боевик", "year": 2008, "rating": 9.0}
            ]
            self.save_movies()

# Запуск программы
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()

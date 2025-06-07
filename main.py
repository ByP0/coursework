import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import requests

class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Музыкальная Фонотека")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f0ff")

        self.bg_color = "#f5f0ff"  
        self.card_color = "#e8e0ff"
        self.primary_color = "#9c89b8"  
        self.secondary_color = "#b8bedd"
        self.accent_color = "#c9b6e4" 
        self.text_color = "#4a4453" 
        self.success_color = "#a8e6cf"
        self.error_color = "#ffaaa5"  

        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.header_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.main_font = tkfont.Font(family="Helvetica", size=12)
        self.small_font = tkfont.Font(family="Helvetica", size=10)

        self.base_url = "http://localhost:8000/api/v1"
        
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        header_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        
        title_label = tk.Label(
            header_frame, 
            text="Музыкальная Фонотека", 
            font=self.title_font,
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_search_tab()
        self.create_add_tab()
        self.create_stats_tab()

        self.status_bar = tk.Label(
            self.main_frame, 
            text="Готово к работе", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=self.small_font,
            fg=self.text_color,
            bg=self.card_color
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

        self.update_stats()
        
    def create_search_tab(self):
        self.search_tab = tk.Frame(self.notebook, bg=self.bg_color) 
        self.notebook.add(self.search_tab, text="Поиск музыки")
 
        search_frame = tk.Frame(
            self.search_tab, 
            bg=self.card_color,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            search_frame, 
            text="Критерии поиска:", 
            font=self.header_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W)

        fields = [
            ("Название трека:", "track_search_entry"),
            ("Исполнитель:", "artist_search_entry"),
            ("Жанр:", "genre_search_entry"),
            ("Год от:", "year_from_entry"),
            ("Год до:", "year_to_entry")
        ]
        
        for i, (label_text, attr_name) in enumerate(fields):
            row_frame = tk.Frame(search_frame, bg=self.card_color)
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row_frame, 
                text=label_text, 
                font=self.main_font,
                fg=self.text_color,
                bg=self.card_color,
                width=15,
                anchor=tk.E
            ).pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(
                row_frame,
                font=self.main_font,
                bg="white",
                fg=self.text_color,
                relief=tk.FLAT
            )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            setattr(self, attr_name, entry)

        button_frame = tk.Frame(search_frame, bg=self.card_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        search_btn = tk.Button(
            button_frame,
            text="Искать",
            font=self.main_font,
            bg=self.primary_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT,
            command=self.search_records
        )
        search_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Сбросить",
            font=self.main_font,
            bg=self.accent_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT,
            command=self.clear_search
        )
        clear_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        results_frame = tk.Frame(self.search_tab, bg=self.bg_color)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.results_tree = ttk.Treeview(
            results_frame,
            columns=("id", "title", "artist", "year", "duration", "genre", "country"),
            show="headings",
            style="Custom.Treeview"
        )

        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background="white",
                       fieldbackground="white",
                       foreground=self.text_color,
                       font=self.main_font)
        style.configure("Custom.Treeview.Heading", 
                        background=self.primary_color,
                        foreground="white",
                        font=self.header_font)

        columns = {
            "id": ("ID", 50),
            "title": ("Название", 200),
            "artist": ("Исполнитель", 150),
            "year": ("Год", 80),
            "duration": ("Длит. (сек)", 80),
            "genre": ("Жанр", 120),
            "country": ("Страна", 100)
        }
        
        for col, (text, width) in columns.items():
            self.results_tree.heading(col, text=text)
            self.results_tree.column(col, width=width, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = tk.Frame(self.search_tab, bg=self.bg_color)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        view_btn = tk.Button(
            action_frame,
            text="Просмотреть детали",
            font=self.main_font,
            bg=self.primary_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT,
            command=self.show_record_details
        )
        view_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="Удалить запись",
            font=self.main_font,
            bg=self.error_color,
            fg="white",
            activebackground="#ff8a80",
            activeforeground="white",
            relief=tk.FLAT,
            command=self.delete_record
        )
        delete_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
    
    def create_add_tab(self):
        self.add_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.add_tab, text="Добавить запись")

        main_frame = tk.Frame(
            self.add_tab, 
            bg=self.card_color,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        main_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            main_frame, 
            text="Основная информация:", 
            font=self.header_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W, pady=(0, 10))

        required_fields = [
            ("Название трека*:", "track_entry"),
            ("Исполнитель*:", "artist_entry"),
            ("Год*:", "year_entry"),
            ("Длительность (сек)*:", "duration_entry"),
            ("Жанр*:", "genre_entry"),
            ("Страна*:", "country_entry")
        ]
        
        for i, (label_text, attr_name) in enumerate(required_fields):
            row_frame = tk.Frame(main_frame, bg=self.card_color)
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row_frame, 
                text=label_text, 
                font=self.main_font,
                fg=self.text_color,
                bg=self.card_color,
                width=20,
                anchor=tk.E
            ).pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(
                row_frame,
                font=self.main_font,
                bg="white",
                fg=self.text_color,
                relief=tk.FLAT
            )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            setattr(self, attr_name, entry)

        group_frame = tk.Frame(
            self.add_tab, 
            bg=self.card_color,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        group_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            group_frame, 
            text="Информация о группе:", 
            font=self.header_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W, pady=(0, 10))
        
        group_fields = [
            ("Год образования:", "formation_year_entry"),
            ("Год распада:", "disband_year_entry"),
            ("Награды:", "awards_entry")
        ]
        
        for i, (label_text, attr_name) in enumerate(group_fields):
            row_frame = tk.Frame(group_frame, bg=self.card_color)
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row_frame, 
                text=label_text, 
                font=self.main_font,
                fg=self.text_color,
                bg=self.card_color,
                width=20,
                anchor=tk.E
            ).pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(
                row_frame,
                font=self.main_font,
                bg="white",
                fg=self.text_color,
                relief=tk.FLAT
            )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            setattr(self, attr_name, entry)

        members_frame = tk.Frame(
            self.add_tab, 
            bg=self.card_color,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        members_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            members_frame, 
            text="Состав группы:", 
            font=self.header_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.members_text = tk.Text(
            members_frame,
            wrap=tk.WORD,
            bg="white",
            fg=self.text_color,
            font=self.main_font,
            padx=5,
            pady=5,
            height=5,
            relief=tk.FLAT
        )
        self.members_text.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            members_frame, 
            text="Формат: Имя, Роль (каждый участник с новой строки)",
            font=self.small_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W, pady=(5, 0))

        button_frame = tk.Frame(self.add_tab, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(
            button_frame,
            text="Добавить запись",
            font=self.main_font,
            bg=self.success_color,
            fg=self.text_color,
            activebackground="#b5ead7",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=self.add_record
        )
        add_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Очистить форму",
            font=self.main_font,
            bg=self.accent_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT,
            command=self.clear_add_form
        )
        clear_btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        tk.Label(
            button_frame, 
            text="* - обязательные поля",
            font=self.small_font,
            fg=self.text_color,
            bg=self.bg_color
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_stats_tab(self):
        self.stats_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.stats_tab, text="Статистика")

        genre_frame = tk.Frame(
            self.stats_tab, 
            bg=self.card_color,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        genre_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            genre_frame, 
            text="Распределение по жанрам:", 
            font=self.header_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.genre_stats_tree = ttk.Treeview(
            genre_frame,
            columns=("genre", "count"),
            show="headings",
            style="Custom.Treeview"
        )
        self.genre_stats_tree.heading("genre", text="Жанр")
        self.genre_stats_tree.heading("count", text="Количество треков")
        self.genre_stats_tree.column("genre", width=200)
        self.genre_stats_tree.column("count", width=150, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(genre_frame, orient="vertical", command=self.genre_stats_tree.yview)
        self.genre_stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.genre_stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        year_frame = tk.Frame(
            self.stats_tab, 
            bg=self.card_color,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        year_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            year_frame, 
            text="Распределение по годам:", 
            font=self.header_font,
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.year_stats_tree = ttk.Treeview(
            year_frame,
            columns=("year", "count"),
            show="headings",
            style="Custom.Treeview"
        )
        self.year_stats_tree.heading("year", text="Год")
        self.year_stats_tree.heading("count", text="Количество треков")
        self.year_stats_tree.column("year", width=200)
        self.year_stats_tree.column("count", width=150, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(year_frame, orient="vertical", command=self.year_stats_tree.yview)
        self.year_stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.year_stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        update_btn = tk.Button(
            self.stats_tab,
            text="Обновить статистику",
            font=self.main_font,
            bg=self.primary_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT,
            command=self.update_stats
        )
        update_btn.pack(pady=10)

    def search_records(self):
        params = {
            "title": self.track_search_entry.get() or None,
            "artist_name": self.artist_search_entry.get() or None,
            "genre": self.genre_search_entry.get() or None,
            "year_after": self.year_from_entry.get() or None,
            "year_before": self.year_to_entry.get() or None
        }
        
        try:
            response = requests.get(f"{self.base_url}/tracks/", params=params)
            response.raise_for_status()
            tracks = response.json()

            for item in self.results_tree.get_children():
                self.results_tree.delete(item)

            for track in tracks:
                self.results_tree.insert("", "end", values=(
                    track["id"],
                    track["title"],
                    track["artist"],
                    track["year"],
                    track["duration"],
                    track["genre"],
                    track["country"]
                ))
            
            self.status_bar.config(text=f"Найдено {len(tracks)} записей")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить поиск: {str(e)}")
            self.status_bar.config(text="Ошибка при поиске")
    
    def show_record_details(self):
        selected_item = self.results_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для просмотра")
            return
        
        track_id = self.results_tree.item(selected_item)["values"][0]
        
        try:
            response = requests.get(f"{self.base_url}/track/{track_id}")
            response.raise_for_status()
            track = response.json()

            details_window = tk.Toplevel(self.root)
            details_window.title(f"Детали записи: {track['title']}")
            details_window.geometry("700x600")
            details_window.configure(bg=self.bg_color)
            
            main_frame = tk.Frame(details_window, bg=self.bg_color)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            info_frame = tk.Frame(
                main_frame, 
                bg=self.card_color,
                bd=2,
                relief=tk.GROOVE,
                padx=10,
                pady=10
            )
            info_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                info_frame, 
                text="Основная информация:", 
                font=self.header_font,
                fg=self.text_color,
                bg=self.card_color
            ).pack(anchor=tk.W, pady=(0, 10))
            
            info_labels = [
                ("Название трека:", track["title"]),
                ("Исполнитель:", track["artist"]),
                ("Год создания:", track["year"]),
                ("Длительность:", f"{track['duration']} сек"),
                ("Жанр:", track["genre"]),
                ("Страна исполнителя:", track["country"])
            ]
            
            for i, (label, value) in enumerate(info_labels):
                row_frame = tk.Frame(info_frame, bg=self.card_color)
                row_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(
                    row_frame, 
                    text=label, 
                    font=self.main_font,
                    fg=self.text_color,
                    bg=self.card_color,
                    width=20,
                    anchor=tk.E
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Label(
                    row_frame, 
                    text=value, 
                    font=self.main_font,
                    fg=self.text_color,
                    bg=self.card_color,
                    anchor=tk.W
                ).pack(side=tk.LEFT)

            if track.get("formation_year"):
                group_frame = tk.Frame(
                    main_frame, 
                    bg=self.card_color,
                    bd=2,
                    relief=tk.GROOVE,
                    padx=10,
                    pady=10
                )
                group_frame.pack(fill=tk.X, pady=10)
                
                tk.Label(
                    group_frame, 
                    text="Информация о группе:", 
                    font=self.header_font,
                    fg=self.text_color,
                    bg=self.card_color
                ).pack(anchor=tk.W, pady=(0, 10))
                
                group_info = [
                    ("Год образования:", track.get("formation_year", "Н/Д")),
                    ("Год распада:", track.get("disband_year", "Н/Д")),
                    ("Награды:", track.get("awards", "Н/Д"))
                ]
                
                for i, (label, value) in enumerate(group_info):
                    row_frame = tk.Frame(group_frame, bg=self.card_color)
                    row_frame.pack(fill=tk.X, pady=5)
                    
                    tk.Label(
                        row_frame, 
                        text=label, 
                        font=self.main_font,
                        fg=self.text_color,
                        bg=self.card_color,
                        width=20,
                        anchor=tk.E
                    ).pack(side=tk.LEFT, padx=5)
                    
                    tk.Label(
                        row_frame, 
                        text=value, 
                        font=self.main_font,
                        fg=self.text_color,
                        bg=self.card_color,
                        anchor=tk.W
                    ).pack(side=tk.LEFT)
                
                if track.get("members"):
                    members_frame = tk.Frame(
                        main_frame, 
                        bg=self.card_color,
                        bd=2,
                        relief=tk.GROOVE,
                        padx=10,
                        pady=10
                    )
                    members_frame.pack(fill=tk.BOTH, expand=True, pady=10)
                    
                    tk.Label(
                        members_frame, 
                        text="Состав группы:", 
                        font=self.header_font,
                        fg=self.text_color,
                        bg=self.card_color
                    ).pack(anchor=tk.W, pady=(0, 10))
                    
                    members_tree = ttk.Treeview(
                        members_frame,
                        columns=("name", "role"),
                        show="headings",
                        style="Custom.Treeview"
                    )
                    members_tree.heading("name", text="Имя")
                    members_tree.heading("role", text="Роль")
                    members_tree.column("name", width=200)
                    members_tree.column("role", width=300)
                    
                    for member in track["members"]:
                        members_tree.insert("", "end", values=(member["name"], member["role"]))
                    
                    scrollbar = ttk.Scrollbar(members_frame, orient="vertical", command=members_tree.yview)
                    members_tree.configure(yscrollcommand=scrollbar.set)
                    
                    members_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось получить детали: {str(e)}")
    
    def delete_record(self):
        selected_item = self.results_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        
        track_id = self.results_tree.item(selected_item)["values"][0]
        track_title = self.results_tree.item(selected_item)["values"][1]
        artist_name = self.results_tree.item(selected_item)["values"][2]
        
        if not messagebox.askyesno(
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить запись:\n{track_title} - {artist_name}?"
        ):
            return
        
        try:
            response = requests.delete(f"{self.base_url}/track/{track_id}")
            response.raise_for_status()
            
            self.search_records()
            self.status_bar.config(text=f"Запись '{track_title}' удалена")
            messagebox.showinfo("Успех", "Запись успешно удалена")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")
            self.status_bar.config(text="Ошибка при удалении")
    
    def add_record(self):
        track_data = {
            "title": self.track_entry.get(),
            "artist": self.artist_entry.get(),
            "year": self.year_entry.get(),
            "duration": self.duration_entry.get(),
            "genre": self.genre_entry.get(),
            "country": self.country_entry.get(),
            "formation_year": self.formation_year_entry.get() or None,
            "disband_year": self.disband_year_entry.get() or None,
            "awards": self.awards_entry.get() or None,
            "members": []
        }

        required_fields = ["title", "artist", "year", "duration", "genre", "country"]
        for field in required_fields:
            if not track_data[field]:
                messagebox.showwarning("Предупреждение", f"Поле '{field}' обязательно для заполнения")
                return

        try:
            track_data["year"] = int(track_data["year"])
            track_data["duration"] = int(track_data["duration"])
            
            if track_data["formation_year"]:
                track_data["formation_year"] = int(track_data["formation_year"])
            if track_data["disband_year"]:
                track_data["disband_year"] = int(track_data["disband_year"])
        except ValueError:
            messagebox.showwarning("Ошибка", "Год и длительность должны быть числами")
            return

        members_text = self.members_text.get("1.0", tk.END).strip()
        if members_text:
            for line in members_text.split('\n'):
                if ',' in line:
                    name, role = line.split(',', 1)
                    track_data["members"].append({
                        "name": name.strip(),
                        "role": role.strip()
                    })

        try:
            response = requests.post(f"{self.base_url}/tracks/", json=track_data)
            response.raise_for_status()
            
            self.clear_add_form()
            messagebox.showinfo("Успех", "Запись успешно добавлена")
            self.status_bar.config(text="Новая запись добавлена")
            self.notebook.select(0)
            self.search_records()  
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись: {str(e)}")
            self.status_bar.config(text="Ошибка при добавлении")
    
    def update_stats(self):
        try:
            response = requests.get(f"{self.base_url}/stats/genres")
            response.raise_for_status()
            genre_stats = response.json()
            
            for item in self.genre_stats_tree.get_children():
                self.genre_stats_tree.delete(item)
            
            for genre, count in genre_stats.items():
                self.genre_stats_tree.insert("", "end", values=(genre, count))

            response = requests.get(f"{self.base_url}/stats/years")
            response.raise_for_status()
            year_stats = response.json()
            
            for item in self.year_stats_tree.get_children():
                self.year_stats_tree.delete(item)
            
            for year, count in year_stats.items():
                self.year_stats_tree.insert("", "end", values=(year, count))
            
            self.status_bar.config(text="Статистика обновлена")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось получить статистику: {str(e)}")
            self.status_bar.config(text="Ошибка при обновлении статистики")
    
    def clear_search(self):
        self.track_search_entry.delete(0, tk.END)
        self.artist_search_entry.delete(0, tk.END)
        self.genre_search_entry.delete(0, tk.END)
        self.year_from_entry.delete(0, tk.END)
        self.year_to_entry.delete(0, tk.END)
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.status_bar.config(text="Поля поиска очищены")
    
    def clear_add_form(self):
        self.track_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.country_entry.delete(0, tk.END)
        self.formation_year_entry.delete(0, tk.END)
        self.disband_year_entry.delete(0, tk.END)
        self.awards_entry.delete(0, tk.END)
        self.members_text.delete("1.0", tk.END)
        
        self.status_bar.config(text="Форма добавления очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
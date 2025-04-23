import tkinter as tk
from tkinter import ttk, messagebox
import asyncio

from databasedb import create_tables
from cruds import *



class PhonoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Фонотека")
        self.root.geometry("900x700")
        self.run_create_tables()

        self.notebook = ttk.Notebook(root)
        self.tab_view = ttk.Frame(self.notebook)
        self.tab_add = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_view, text="Просмотр и поиск")
        self.notebook.add(self.tab_add, text="Добавление")
        self.notebook.pack(fill="both", expand=1)

        frm_search = ttk.Frame(self.tab_view, padding=10)
        frm_search.pack(fill='x')
        self.search_var = tk.StringVar()
        ttk.Label(frm_search, text="Поиск:").pack(side='left')
        ttk.Entry(frm_search, textvariable=self.search_var, width=40).pack(side='left', padx=5)
        ttk.Button(frm_search, text="Поиск", command=self.search).pack(side='left', padx=5)
        ttk.Button(frm_search, text="Показать все", command=self.show_all).pack(side='left', padx=5)

        self.song_list = ttk.Treeview(self.tab_view, columns=('title', 'artist', 'group', 'awards'), show='headings')
        self.song_list.heading('title', text='Песня')
        self.song_list.heading('artist', text='Артист')
        self.song_list.heading('group', text='Группа')
        self.song_list.heading('awards', text='Награды')
        self.song_list.pack(fill='both', expand=1, pady=10, padx=10)

        frm_artist = ttk.LabelFrame(self.tab_add, text="Добавить артиста", padding=10)
        frm_artist.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        self.artist_name = tk.StringVar()
        self.artist_country = tk.StringVar()
        
        ttk.Label(frm_artist, text="Имя:").grid(row=0, column=0)
        ttk.Entry(frm_artist, textvariable=self.artist_name).grid(row=0, column=1)
        ttk.Label(frm_artist, text="Страна:").grid(row=0, column=2)
        ttk.Entry(frm_artist, textvariable=self.artist_country).grid(row=0, column=3)      
        ttk.Button(frm_artist, text="Добавить", command=self.add_artist_btn).grid(row=0, column=4, padx=5)

        frm_genre = ttk.LabelFrame(self.tab_add, text="Добавить жанр", padding=10)
        frm_genre.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        self.genre_name = tk.StringVar()

        ttk.Label(frm_genre, text="Название жанра:").grid(row=0, column=0)
        ttk.Entry(frm_genre, textvariable=self.genre_name).grid(row=0, column=1)

        ttk.Button(frm_genre, text="Добавить", command=self.add_genre).grid(row=0, column=2, padx=5)

        frm_song = ttk.LabelFrame(self.tab_add, text="Добавить песню", padding=10)
        frm_song.grid(row=2, column=0, sticky='ew', padx=10, pady=5)

        self.song_title = tk.StringVar()
        self.artist_name_track = tk.StringVar(value=None)
        self.group_name_track = tk.StringVar(value=None)
        self.release_year = tk.IntVar()
        self.duration = tk.StringVar()
        self.genre_name_track = tk.StringVar()

        ttk.Label(frm_song, text="Название:").grid(row=0, column=0)
        ttk.Entry(frm_song, textvariable=self.song_title).grid(row=0, column=1)
        
        ttk.Label(frm_song, text="Артист:").grid(row=0, column=2)
        ttk.Entry(frm_song, textvariable=self.artist_name_track).grid(row=0, column=3)
        
        ttk.Label(frm_song, text="Группа:").grid(row=0, column=4)
        ttk.Entry(frm_song, textvariable=self.group_name_track).grid(row=0, column=5)

        ttk.Label(frm_song, text="Год выпуска:").grid(row=1, column=0)
        ttk.Entry(frm_song, textvariable=self.release_year).grid(row=1, column=1)
        
        ttk.Label(frm_song, text="Длительность:").grid(row=1, column=2)
        ttk.Entry(frm_song, textvariable=self.duration).grid(row=1, column=3)

        ttk.Label(frm_song, text="Жанр:").grid(row=1, column=4)
        ttk.Entry(frm_song, textvariable=self.genre_name_track).grid(row=1, column=5)

        ttk.Button(frm_song, text="Добавить", command=self.add_song_btn).grid(row=1, column=6)

    def run_create_tables(self):
        asyncio.run(create_tables())

    def add_artist_btn(self):
        name = self.artist_name.get().strip()
        country = self.artist_country.get().strip()      
        if name:
            asyncio.run(add_artist_async(name=name, country=country))
            self.update_artist_group_lists() 
            self.artist_name.set('')
            self.artist_country.set('')
            messagebox.showinfo("Успешно", "Артист добавлен")
        else:
            messagebox.showwarning("Внимание", "Имя артиста не должно быть пустым")
    
    def add_genre(self):
        genre_name = self.genre_name.get().strip()
        if genre_name:
            asyncio.run(add_genre_async(genre_name=genre_name))
            self.genre_name.set('')
            messagebox.showinfo("Успешно", "Жанр добавлен")
        else:
            messagebox.showwarning("Внимание", "Имя жанра не должно быть пустым")
    
    def add_song_btn(self):
        song_title = self.song_title.get().strip() 
        artist_name_track = self.artist_name_track.get().strip() 
        group_name_track = self.group_name_track.get().strip() 
        release_year = self.release_year.get()
        duration = self.duration.get().strip() 
        genre_name_track = self.genre_name_track.get().strip() 
        
        if song_title:
            asyncio.run(add_track_async(song_title=song_title, artist_name=artist_name_track, group_name=group_name_track, release_year=release_year, duration=duration, genre_name=genre_name_track))
            self.song_title.set('')
            self.artist_name_track.set('')
            self.group_name_track.set('')
            self.release_year.set(0)
            self.duration.set('')
            self.genre_name_track.set('')
            self.show_all() 
            messagebox.showinfo("Успешно", "Песня добавлена")
        else:
            messagebox.showwarning("Внимание", "Название песни не должно быть пустым")

    def search(self):
        query = self.search_var.get().strip()


    def show_all(self):
        pass

    def update_artist_group_lists(self):
        pass

    def add_artist(name, awards):
        pass 

    def add_group(name, awards):
        pass

    def add_track(title, artist_id, group_id, awards):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = PhonoApp(root)
    root.mainloop()
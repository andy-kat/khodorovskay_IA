import tkinter as tk
from tkinter import messagebox
import json
import random

def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(task_list):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(task_list, file, ensure_ascii=False, indent=4)

def update_listbox(filtered_tasks=None):
    task_listbox.delete(0, tk.END)
    # Если передан список отфильтрованных задач, используем его, иначе — весь список
    for task in (filtered_tasks if filtered_tasks is not None else tasks):
        task_listbox.insert(tk.END, task)

def add_task():
    sp = [
        ['«Все приходит вовремя для того, кто умеет ждать».', 'Лев Толстой', 'Жизнь'],
        ['«Бог умер: теперь хотим мы, чтобы жил сверхчеловек».', 'Фридрих Ницше', 'Религия'],
        ['«В любви всегда есть немного безумия. Но и в безумии всегда есть немного разума».', 'Фридрих Ницше', 'Любовь'],
        ['«Командовать парадом буду я!».', 'Илья Ильф и Евгений Петров', 'Из фильма'],
        ['«Всё чудесатее и чудесатее!».', 'Льюис Кэрролл', 'Жизнь'],
        ['«Любовь — это когда хочешь переживать с кем-то все четыре времена года».', 'Рэй Брэдбери', 'Любовь']
    ]
    quote, author, topic = random.choice(sp)
    task = f'{quote} — {author} ({topic})'
    tasks.append(task)
    update_listbox()  # Обновляем полный список после добавления
    save_tasks(tasks)

def remove_task():
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks.pop(index)
        update_listbox()
        save_tasks(tasks)
    else:
        messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")

def filter_tasks():
    author_filter = entry_author.get().strip().lower()
    topic_filter = entry_topic.get().strip().lower()

    filtered = []
    for task in tasks:
        parts = task.split(' — ')
        if len(parts) < 2:
            continue
        quote_part = parts[1]
        author_topic = quote_part.split(' (')
        if len(author_topic) < 2:
            continue
        author = author_topic[0].lower()
        topic = author_topic[1].rstrip(')').lower()

        match_author = (author_filter == '' or author_filter in author)
        match_topic = (topic_filter == '' or topic_filter in topic)

        if match_author and match_topic:
            filtered.append(task)

    update_listbox(filtered)

# Загрузка задач
tasks = load_tasks()

# Основное окно
root = tk.Tk()
root.title("Список цитат")
root.geometry("800x700")

# Фильтры
frame_filters = tk.Frame(root)
frame_filters.pack(pady=10)

tk.Label(frame_filters, text="Автор:").pack(side=tk.LEFT, padx=5)
entry_author = tk.Entry(frame_filters, width=25)
entry_author.pack(side=tk.LEFT, padx=5)

tk.Label(frame_filters, text="Тема:").pack(side=tk.LEFT, padx=5)
entry_topic = tk.Entry(frame_filters, width=25)
entry_topic.pack(side=tk.LEFT, padx=5)

btn_filter = tk.Button(frame_filters, text="Фильтровать", command=filter_tasks)
btn_filter.pack(side=tk.LEFT, padx=10)

# Список цитат
task_listbox = tk.Listbox(root, width=100, height=15)
task_listbox.pack(pady=20)

# Кнопки управления
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Сгенерировать цитату", command=add_task)
btn_add.pack(side=tk.LEFT, padx=5)

btn_remove = tk.Button(frame_buttons, text="Удалить выбранную", command=remove_task)
btn_remove.pack(side=tk.LEFT, padx=5)

btn_reset = tk.Button(frame_buttons, text="Показать все", command=lambda: update_listbox())
btn_reset.pack(side=tk.LEFT, padx=5)

# Первоначальное отображение всех задач
update_listbox()

root.mainloop()

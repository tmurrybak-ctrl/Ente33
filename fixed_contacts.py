import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

FILENAME = 'contacts.json'


def load_contacts():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_contacts(contacts):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

contacts_data = load_contacts()
filtered_data = None

root = tk.Tk()
root.title('Телефонная книга')
root.geometry('800x650')
root.resizable(True, True)

input_frame = tk.Frame(root)
input_frame.pack(pady=20)

tk.Label(input_frame, text='Имя:', font=('Arial', 12)).grid(row=0, column=0, sticky='w', padx=5)
name_entry = tk.Entry(input_frame, width=25, font=('Arial', 11))
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text='Номер телефона:', font=('Arial', 12)).grid(row=0, column=2, sticky='w', padx=5)
phone_entry = tk.Entry(input_frame, width=25, font=('Arial', 11))
phone_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text='Поиск по имени:', font=('Arial', 12)).grid(row=1, column=0, sticky='w', padx=5, pady=10)
search_entry = tk.Entry(input_frame, width=25, font=('Arial', 11))
search_entry.grid(row=1, column=1, padx=5, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

list_frame = tk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
listbox = tk.Listbox(list_frame, font=('Arial', 11), selectmode=tk.SINGLE, height=15)
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def current_data():
    return filtered_data if filtered_data is not None else contacts_data


def update_list(data=None):
    if data is None:
        data = current_data()
    listbox.delete(0, tk.END)
    for contact in data:
        listbox.insert(tk.END, f"{contact['name']} | {contact['phone']}")


def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    if name and phone:
        contacts_data.append({'name': name, 'phone': phone})
        save_contacts(contacts_data)
        clear_search()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        update_list()
        messagebox.showinfo('Успех', 'Контакт добавлен!')
    else:
        messagebox.showwarning('Ошибка', 'Заполните имя и номер.')


def delete_contact():
    sel = listbox.curselection()
    if sel:
        idx = sel[0]
        data = current_data()
        if 0 <= idx < len(data):
            contact = data[idx]
            if contact in contacts_data:
                contacts_data.remove(contact)
                save_contacts(contacts_data)
                clear_search()
                update_list()
                name_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
                messagebox.showinfo('Успех', 'Контакт удален!')
    else:
        messagebox.showwarning('Ошибка', 'Выберите контакт из списка.')


def perform_search():
    global filtered_data
    query = search_entry.get().lower().strip()
    if query:
        filtered_data = [c for c in contacts_data if query in c['name'].lower()]
    else:
        filtered_data = None
    update_list()


def clear_search():
    global filtered_data
    filtered_data = None
    search_entry.delete(0, tk.END)
    update_list()


def on_select(event):
    sel = listbox.curselection()
    if sel:
        idx = sel[0]
        data = current_data()
        if 0 <= idx < len(data):
            contact = data[idx]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, contact['name'])
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, contact['phone'])


tk.Button(input_frame, text='🔍 Поиск', command=perform_search, bg='#FF9800', fg='white', font=('Arial', 10)).grid(row=1, column=2, padx=5, pady=10)
tk.Button(input_frame, text='Очистить поиск', command=clear_search, bg='#9E9E9E', fg='white', font=('Arial', 10)).grid(row=1, column=3, padx=5, pady=10)

tk.Button(btn_frame, text='Добавить контакт', command=add_contact, bg='#4CAF50', fg='white', font=('Arial', 11), width=15).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text='Удалить', command=delete_contact, bg='#f44336', fg='white', font=('Arial', 11), width=15).pack(side=tk.LEFT, padx=10)

tk.Label(root, text='Список контактов:', font=('Arial', 13)).pack(pady=(30,10))
listbox.bind('<<ListboxSelect>>', on_select)
update_list()
root.mainloop()

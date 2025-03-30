import tkinter as tk
from tkinter import ttk, messagebox
from models.task import Task
from datetime import datetime
from tkcalendar import Calendar

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do App")
        self.root.geometry("1150x600")
        Task.create_table()
        self.build_ui()
        self.refresh_task_list()

    def build_ui(self):
        # ===== Sección de entrada de datos =====
        entry_frame = tk.LabelFrame(self.root, text="Nueva Tarea", padx=10, pady=10)
        entry_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(entry_frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.entry_name = tk.Entry(entry_frame, width=20)
        self.entry_name.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Descripción:").grid(row=0, column=2, sticky="ne")
        self.entry_desc = tk.Text(entry_frame, width=40, height=4, wrap="word")
        self.entry_desc.grid(row=0, column=3, rowspan=2, padx=5)

        tk.Label(entry_frame, text="Fecha:").grid(row=0, column=4, sticky="e")
        self.entry_due = tk.Entry(entry_frame, width=12, state="readonly")
        self.entry_due.grid(row=0, column=5, padx=2)
        tk.Button(entry_frame, text="📅", command=self.open_calendar).grid(row=0, column=6, padx=2)

        tk.Label(entry_frame, text="Hora (HH:MM):").grid(row=1, column=4, sticky="e")
        self.time_entry = tk.Entry(entry_frame, width=6)
        self.time_entry.grid(row=1, column=5, padx=2)

        tk.Button(entry_frame, text="Agregar tarea", command=self.add_task).grid(row=1, column=6, padx=10)

        # ===== Filtro =====
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        self.filter_var = tk.StringVar(value="Todas")
        tk.Label(filter_frame, text="Filtrar tareas:").pack(side="left")
        self.filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["Todas", "Completadas", "Pendientes"], state="readonly", width=15)
        self.filter_menu.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Aplicar filtro", command=self.refresh_task_list).pack(side="left")

        # ===== Tabla de tareas =====
        self.tree = ttk.Treeview(self.root, columns=("comp", "seq", "nombre", "desc", "due"), show="headings", height=10)
        self.tree.heading("comp", text="Estado")
        self.tree.heading("seq", text="#")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("desc", text="Descripción")
        self.tree.heading("due", text="Fecha Límite")
        self.tree.column("comp", width=60, anchor="center")
        self.tree.column("seq", width=50, anchor="center")
        self.tree.column("nombre", width=150)
        self.tree.column("desc", width=300)
        self.tree.column("due", width=150, anchor="center")
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.show_description)

        # ===== Descripción completa =====
        desc_frame = tk.LabelFrame(self.root, text="Descripción Completa", padx=10, pady=5)
        desc_frame.pack(fill="both", padx=10, pady=5)
        self.full_desc = tk.Text(desc_frame, height=4, wrap="word", state="disabled")
        self.full_desc.pack(fill="both", expand=True)

        # ===== Botones de acción =====
        action_frame = tk.LabelFrame(self.root, text="Acciones", padx=10, pady=5)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Editar tarea", width=20, command=self.edit_task).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Marcar como completada", width=20, command=self.mark_completed).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Marcar como NO completada", width=20, command=self.mark_notcompleted).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Eliminar tarea", width=20, command=self.delete_task).grid(row=0, column=3, padx=5)

    def refresh_task_list(self):
        self.tree.delete(*self.tree.get_children())
        all_tasks = Task.get_all()
        
        filtro = self.filter_var.get()
        if filtro == "Completadas":
            tasks = [t for t in all_tasks if t[5]]
        elif filtro == "Pendientes":
            tasks = [t for t in all_tasks if not t[5]]
        else:
            tasks = all_tasks

        for task in tasks:
            due_str = task[4].strftime("%Y-%m-%d %H:%M") if task[4] else ""
            estado = "✓" if task[5] else "❌"
            resumen = task[3].split('\n')[0][:50] + "..." if len(task[3].split('\n')[0]) > 50 else task[3].split('\n')[0]
            row = (estado, task[1], task[2], resumen, due_str)
            tag = "overdue" if task[4] and datetime.now() > task[4] and not task[5] else ""
            self.tree.insert("", "end", iid=str(task[0]), values=row, tags=(tag,))
        self.tree.tag_configure("overdue", background="lightcoral")

    def add_task(self):
        nombre = self.entry_name.get()
        descripcion = self.entry_desc.get("1.0", tk.END).strip()
        try:
            date = self.entry_due.get()
            time_str = self.time_entry.get()
            due_dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M") if time_str else None
        except ValueError:
            messagebox.showerror("Formato de fecha incorrecto", "Usa el formato YYYY-MM-DD HH:MM")
            return
        if nombre:
            Task.create(nombre, descripcion, due_dt)
            self.clear_inputs()
            self.refresh_task_list()

    def clear_inputs(self):
        self.entry_name.delete(0, tk.END)
        self.entry_desc.delete("1.0", tk.END)
        self.time_entry.delete(0, tk.END)
        self.entry_due.config(state="normal")
        self.entry_due.delete(0, tk.END)
        self.entry_due.config(state="readonly")
        self.full_desc.config(state="normal")
        self.full_desc.delete("1.0", tk.END)
        self.full_desc.config(state="disabled")

    def edit_task(self):
        selected = self.tree.focus()
        if selected:
            task_id = int(selected)
            task = next((t for t in Task.get_all() if t[0] == task_id), None)
            if not task:
                messagebox.showerror("Error", "No se pudo encontrar la tarea seleccionada.")
                return

            old_nombre = task[2]
            old_desc = task[3]
            old_due = task[4]

            nombre = self.entry_name.get().strip() or old_nombre
            descripcion_input = self.entry_desc.get("1.0", tk.END).strip()
            descripcion = descripcion_input if descripcion_input else old_desc

            try:
                date = self.entry_due.get().strip()
                time_str = self.time_entry.get().strip()
                if date and time_str:
                    due_dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
                else:
                    due_dt = old_due
            except ValueError:
                messagebox.showerror("Formato de fecha incorrecto", "Usa el formato YYYY-MM-DD HH:MM")
                return

            Task.update(task_id, nombre, descripcion, due_dt)
            self.clear_inputs()
            self.refresh_task_list()

    def mark_completed(self):
        selected = self.tree.focus()
        if selected:
            Task.mark_completed(int(selected))
            self.refresh_task_list()

    def mark_notcompleted(self):
        selected = self.tree.focus()
        if selected:
            Task.mark_notcompleted(int(selected))
            self.refresh_task_list()

    def delete_task(self):
        selected = self.tree.focus()
        if selected:
            Task.delete(int(selected))
            self.refresh_task_list()

    def open_calendar(self):
        def select_date():
            selected_date = cal.selection_get()
            self.entry_due.config(state="normal")
            self.entry_due.delete(0, tk.END)
            self.entry_due.insert(0, selected_date.strftime("%Y-%m-%d"))
            self.entry_due.config(state="readonly")
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Selecciona la fecha")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=10)

        tk.Button(top, text="Seleccionar", command=select_date).pack(pady=5)

    def show_description(self, event):
        selected = self.tree.focus()
        if selected:
            task_id = int(selected)
            task = next((t for t in Task.get_all() if t[0] == task_id), None)
            if task:
                self.full_desc.config(state="normal")
                self.full_desc.delete("1.0", tk.END)
                self.full_desc.insert(tk.END, task[3])
                self.full_desc.config(state="disabled")

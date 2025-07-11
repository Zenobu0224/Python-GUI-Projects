import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("430x600")
        self.resizable(False, False)
        self.title("To-Do List")
        self.configure(fg_color="#dcd0ff")
        self.iconbitmap('ToDoList/imgs/icon.ico')
        self.task_txt = ctk.StringVar()     # TEMPORARILY STORES THE TEXT_VALUE OF self.task_entry

        logo = tk.PhotoImage(file='ToDoList/imgs/logo.png')         # App LOGO

        # FRAME FOR LOGO & ICON
        top_bar_frame = ctk.CTkFrame(self, fg_color="#c2aaff", corner_radius=4, height=85)
        top_bar_frame.pack(fill="x", pady=(0,40))

        # APP TITLE AND LOGO
        ctk.CTkLabel(top_bar_frame, text="To-Do List", font=("Comic Sans MS", 30), text_color="#000000", image=logo, compound="left").place(x=15, y=18)

        # FRAME FOR ENTRY AND BUTTON(ADD TASK)
        entry_btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        entry_btn_frame.pack()

        self.task_entry = ctk.CTkEntry(entry_btn_frame, textvariable=self.task_txt, placeholder_text="Enter Task", font=("Comic Sans MS", 20), text_color="#000000", fg_color="transparent", width=290)
        self.task_entry.pack(ipadx=8, ipady=5, side="left")

        self.add_btn = ctk.CTkButton(entry_btn_frame, text="➕", width=60, height=42, text_color="black", border_width=1, border_color="black", fg_color="#A3C4BC", hover_color="#7A9F95", command=self.add_task)
        self.add_btn.pack(side="right")

        # ScrollableFrame
        self.task_frame = ScrFrame(self, fg_color="transparent")
        self.task_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.bind("<Return>", self.add_task)    # Event that display's task after pressing RETURN(Enter Button)
        self.load_tasks()                       # Load task to the app

    # DYNAMIC FRAME THAT APPEAR EVERYTIME THE USER ADD TASK
    def create_list_frame(self, task_txt):
        frame = ctk.CTkFrame(self.task_frame, height=50, fg_color="#c2aaff")    #other color: creamy_matcha = A3C4BC, shinobu_purple=c2aaff
        frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkCheckBox(frame, text=task_txt, font=("Comic Sans MS", 16), text_color="#000000", hover_color="#7A9F95", border_color="#1F1F1F").pack(side="left", padx=8, pady=8)

        remove_task_btn = ctk.CTkButton(frame, text="❌", fg_color="red", hover_color="#FF4C4C", width=40, height=35, command=lambda f=frame, t=task_txt: self.destroy_delete_task(f,t))
        remove_task_btn.pack(side="right", padx=8, pady=8)

    def add_task(self, bind_val=None):      # add bind_val argument due to the window binding & setting bind_val to None to use both ADD BUTTON and RETURN(ENTER) at the same time
        yaru_koto = self.task_txt.get().strip()

        if yaru_koto == "":                 # Will not add empty task to the frame
            return
        
        try:
            with open("ToDoList/tasks_db.txt") as file:
                for line in file:
                    existing_task = line.replace("Task: ", "").strip()
                    if existing_task.lower() == yaru_koto.lower():
                        messagebox.showinfo(title="Duplicate task", message="Task already exist")
                        self.task_txt.set("")
                        return
        except FileNotFoundError:
            pass

        self.create_list_frame(yaru_koto)

        self.task_txt.set("")               # After adding task, self.task_entry will be set to ""

        # ADD TASK TO DATABASE( tasks_db.txt -- txt file )
        with open("ToDoList/tasks_db.txt", "a") as task:
            task.write(f"Task: {yaru_koto}\n")

    # LOAD TASK TO THE APP
    def load_tasks(self):

        try:
            with open("ToDoList/tasks_db.txt") as tasks:
                for line in tasks:
                    if line.startswith("Task: "):
                        task = line.replace("Task: ", "").strip()

                        self.create_list_frame(task)

        except FileNotFoundError:
            messagebox.showerror(title="File Not Found", message="404 FileNotFound")
            print("404 FileNotFound")

    # DESTROY FRAME & DELETE TASK FROM DATABASE( tasks_db.txt -- txt file )
    def destroy_delete_task(self, frame, task_txt):
        frame.destroy()

        try:
            with open("ToDoList/tasks_db.txt") as r_task:
                task_lines = r_task.readlines()

        except FileNotFoundError:
            messagebox.showerror(title="File Not Found", message="404 FileNotFound")
            print("404 FileNotFound")

        with open("ToDoList/tasks_db.txt", "w") as tasks:
                for task in task_lines:
                    if task.strip() != f"Task: {task_txt}":
                        tasks.write(task)

# ScrollableFrame for storing task in APP
class ScrFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, scrollbar_button_color="#7A9F95", **kwargs)

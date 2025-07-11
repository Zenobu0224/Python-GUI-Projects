import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("390x570")
        self.title("Calculator")
        self.resizable(False, False)
        self.iconbitmap('CTcalculator/img/dentaku.ico')
        self.configure(fg_color="#C8E6C9")

        #FOR DISPLAY(LABEL WIDGET IN TOP_CONTAINER)
        self.equation_label = ctk.StringVar()
        self.equation_txt = ""

        top_container = ctk.CTkFrame(self, fg_color="transparent")
        top_container.pack(pady=(0,20))

        display = ctk.CTkLabel(top_container, font=("Comic Sans MS", 40), textvariable=self.equation_label, text_color="black", fg_color="#ADCBAE",
                               width=390, height=180, justify="right", anchor="e", padx=20)
        display.pack()

        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack()

        #ROW0-1(BUTTON's)
        ctk.CTkButton(btn_container, text="AC", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.clear_btn()).grid(row=0, column=0, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="÷", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press("÷")).grid(row=0, column=1, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="x", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press("x")).grid(row=0, column=2, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="del", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.delete_btn()).grid(row=0, column=3, padx=2, pady=2)

        #ROW-2 (BUTTON's)
        ctk.CTkButton(btn_container, text="7", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(7)).grid(row=1, column=0, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="8", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(8)).grid(row=1, column=1, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="9", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(9)).grid(row=1, column=2, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="-", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press("-")).grid(row=1, column=3, padx=2, pady=2)

        #ROW-3 (BUTTON's)
        ctk.CTkButton(btn_container, text="4", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(4)).grid(row=2, column=0, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="5", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(5)).grid(row=2, column=1, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="6", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(6)).grid(row=2, column=2, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="+", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press("+")).grid(row=2, column=3, padx=2, pady=2)

        #ROW-4 (BUTTON's)
        ctk.CTkButton(btn_container, text="1", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(1)).grid(row=3, column=0, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="2", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(2)).grid(row=3, column=1, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="3", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(3)).grid(row=3, column=2, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="=", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=135, text_color="black", command=lambda: self.equals()).grid(row=3, column=3, rowspan=2, padx=2, pady=2)
        #ROW-5, (BUTTON's)
        ctk.CTkButton(btn_container, text=".", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(".")).grid(row=4, column=0, padx=2,pady=2)
        ctk.CTkButton(btn_container, text="0", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press(0)).grid(row=4, column=1, padx=2, pady=2)
        ctk.CTkButton(btn_container, text="00", font=("Comic Sans MS", 20, "bold"), fg_color="#A3C4BC", hover_color="#7A9F95", width=85, height=65, text_color="black", command=lambda: self.btn_press("00")).grid(row=4, column=2, padx=2, pady=2)    

    def btn_press(self, num):
        self.equation_txt += str(num)
        self.equation_label.set(self.equation_txt)

    def equals(self):
        total = ""

        try:
            # Replace 'x  with '*  and '÷  wth '/' for evaluation
            self.equation_txt = self.equation_txt.replace("x", "*").replace("÷", "/")
            total = str(eval(self.equation_txt))
        except SyntaxError:
            self.equation_label.set("Syntax Error")
            return
        except ZeroDivisionError:
            self.equation_label.set("Cannot Divide by\n Zero")
            return

        self.equation_label.set(total)
        self.equation_txt = total

    def clear_btn(self):
        self.equation_label.set("")
        self.equation_txt = ""

    def delete_btn(self):
        self.equation_txt = self.equation_txt[:-1]
        self.equation_label.set(self.equation_txt)
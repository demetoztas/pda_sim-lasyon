import tkinter as tk
from tkinter import ttk, messagebox

class ExpressionValidate:
    def __init__(self):
        self.stack = []
        self.state = 'q0'
        self.accepted = False
        self.has_error = False
        self.paren_count = 0
        self.last_char = ''

    def transition(self, char):
        if self.state == 'q0':
            if char.isdigit():
                self.state = 'q1'
            elif char == '(':
                self.stack.append('(')
                self.paren_count += 1
                self.state = 'q0'
            else:
                self.state = 'qe'
        elif self.state == 'q1':
            if char.isdigit():
                self.state = 'q1'
            elif char in '+-*/':
                self.state = 'q2'
            elif char == ')':
                if self.stack and self.stack[-1] == '(':
                    self.stack.pop()
                    self.paren_count -= 1
                    self.state = 'q1'
                else:
                    self.state = 'qe'
            elif char == '(':
                self.stack.append('(')
                self.paren_count += 1
                self.state = 'qe'  # '(' cannot follow a number directly
            else:
                self.state = 'qe'
        elif self.state == 'q2':
            if char.isdigit():
                if char == '0' and self.last_char == '/':
                    self.has_error = True
                self.state = 'q1'
            elif char == '(':
                self.stack.append('(')
                self.paren_count += 1
                self.state = 'q0'
            else:
                self.state = 'qe'
        else:
            self.state = 'qe'

        self.last_char = char

    def process(self, input_string):
        self.last_char = ''
        for char in input_string:
            self.transition(char)
            if self.state == 'qe':
                break

        if self.state == 'q1' and not self.stack and not self.has_error and self.paren_count == 0:
            self.accepted = True
        else:
            self.accepted = False

        return self.accepted

def check_syntax(input_string):
    pda = ExpressionValidate()
    input_without_spaces = input_string.replace(' ', '')
    return pda.process(input_without_spaces)

def check_expression():
    user_input = entry.get()
    result = check_syntax(user_input)
    if result:
        messagebox.showinfo("Sonuç", f"'{user_input}' ifadesi geçerli bir matematiksel ifadedir.")
    else:
        messagebox.showinfo("Sonuç", f"'{user_input}' ifadesi geçersiz bir matematiksel ifadedir.")

def clear_entry():
    entry.delete(0, tk.END)

app = tk.Tk()
app.title("Pushdown Automaton Simülasyonu")
app.geometry("700x600")
app.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')  
style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', font=('Helvetica', 12), padding=10, background="#007acc", foreground="#ffffff")
style.map('TButton', background=[('active', '#005f99')], foreground=[('active', '#ffffff')])
style.configure('TLabel', font=('Helvetica', 14), background='#f0f0f0')
style.configure('TListbox', font=('Helvetica', 12), background='#ffffff', foreground='#000000')

background_frame = ttk.Frame(app, style='TFrame')
background_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(background_frame, width=600, height=500)
canvas.pack(fill=tk.BOTH, expand=True)

gradient = canvas.create_rectangle(0, 0, 600, 500, fill='#ffffff', outline='')
canvas.create_rectangle(0, 0, 600, 500, fill='', outline='')

main_frame = ttk.Frame(canvas, style='TFrame')
canvas.create_window(300, 250, window=main_frame)

label = ttk.Label(main_frame, text="Matematiksel bir ifade girin:", style='TLabel')
label.pack(pady=10)

entry = ttk.Entry(main_frame, width=50, font=("Helvetica", 14), foreground="#333333", background="#e6e6e6")
entry.pack(pady=10)

button_frame = ttk.Frame(main_frame, style='TFrame')
button_frame.pack(pady=10)

check_button = ttk.Button(button_frame, text="Kontrol Et", command=check_expression, style='TButton')
check_button.grid(row=0, column=0, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="Temizle", command=clear_entry, style='TButton')
clear_button.grid(row=0, column=1, padx=5, pady=5)

app.mainloop()
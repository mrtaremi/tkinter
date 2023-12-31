import tkinter as tk
from math import sin, cos, tan, log, pow, radians

class EngineeringCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Engineering Calculator")

        # Entry widget to display the current expression
        self.display_entry = tk.Entry(master, width=30, font=('Arial', 14))
        self.display_entry.grid(row=0, column=0, columnspan=4, pady=10)

        # Define buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('^', 5, 3),
            ('log', 6, 0), ('C', 6, 1), ('(', 6, 2), (')', 6, 3),
        ]

        # Create and place buttons
        for (text, row, col) in buttons:
            button = tk.Button(master, text=text, width=5, height=2, command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5)

    def button_click(self, value):
        current_expression = self.display_entry.get()

        if value == "=":
            try:
                result = eval(current_expression)
                self.display_entry.delete(0, tk.END)
                self.display_entry.insert(tk.END, str(result))
            except Exception as e:
                self.display_entry.delete(0, tk.END)
                self.display_entry.insert(tk.END, "Error")

        elif value == "C":
            self.display_entry.delete(0, tk.END)

        else:
            current_expression += value
            self.display_entry.delete(0, tk.END)
            self.display_entry.insert(tk.END, current_expression)

        if value in ['sin', 'cos', 'tan', 'log', '^']:
            self.perform_math_operation(value)

    def perform_math_operation(self, operation):
        try:
            current_expression = self.display_entry.get()
            if operation == '^':
                operation = '**'
            elif operation == 'log':
                operation = 'log10'

            result = eval(f'{operation}({current_expression})')
            self.display_entry.delete(0, tk.END)
            self.display_entry.insert(tk.END, result)
        except Exception as e:
            self.display_entry.delete(0, tk.END)
            self.display_entry.insert(tk.END, "Error")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = EngineeringCalculator(root)
    root.mainloop()

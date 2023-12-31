import tkinter as tk
from math import sin, cos, tan, log

class Calculator:
    def __init__(self, master):
        # تنظیمات اولیه و ایجاد پنجره
        self.master = master
        master.title("Simple Calculator")

        # ایجاد ویجت ورودی متن
        self.entry = tk.Entry(master, width=20, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # دکمه‌های ماشین حساب
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'sin', 'cos', '+',
            'tan', 'log', '^', '=',
            'C'  # دکمه پاکسازی
        ]

        row_val = 1
        col_val = 0

        # ایجاد دکمه‌ها در شبکه
        for button in buttons:
            tk.Button(master, text=button, width=5, command=lambda b=button: self.handle_button(b)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def handle_button(self, value):
        # دریافت محتوای فعلی ورودی
        current = self.entry.get()

        if value == '=':
            # بستن پرانتزها اگر تعداد بازپرانتزها بیشتر از بسته‌ها باشد
            if '(' in current and current.count('(') > current.count(')'):
                self.entry.insert(tk.END, ')' * (current.count('(') - current.count(')')))
            try:
                # محاسبه نتیجه و نمایش آن
                result = eval(current)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                # نمایش خطا در صورت وجود مشکل
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        elif value in ('sin', 'cos', 'tan', 'log', '^'):
            # جایگزینی محتوای ورودی با نام تابع
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, f"{value}(")
        elif value == 'C':
            # پاکسازی محتوای ورودی
            self.entry.delete(0, tk.END)
        else:
            # اضافه کردن مقدار دکمه به ورودی
            self.entry.insert(tk.END, value)

if __name__ == "__main__":
    # اجرای برنامه
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

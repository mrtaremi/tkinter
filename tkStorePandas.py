import pandas as pd
import tkinter
from datetime import datetime
from tkinter import messagebox

class BookstoreManager:
    def __init__(self, books_file='books.csv', sales_file='sales.csv'):
        self.books_file = books_file
        self.sales_file = sales_file

    def add_book(self, title, author, price, quantity):
    # خواندن دیتافریم کتاب‌ها از فایل
        try:
            df_books = pd.read_csv(self.books_file)
        except FileNotFoundError:
            df_books = pd.DataFrame(columns=['Title', 'Author', 'Price', 'Quantity'])

        # افزودن ردیف جدید
        new_row = {'Title': title, 'Author': author, 'Price': price, 'Quantity': quantity}
        df_books = pd.concat([df_books, pd.DataFrame([new_row])], ignore_index=True)

        # ذخیره کردن دیتافریم در فایل
        df_books.to_csv(self.books_file, index=False)
        print(f"Book '{title}' added successfully.")

    def sell_book(self, title, quantity):
    # خواندن دیتافریم کتاب‌ها از فایل
        try:
            df_books = pd.read_csv(self.books_file)
        except FileNotFoundError:
            print("Error: Books file not found.")
            return

        # جستجو بر اساس نام کتاب
        author_books = df_books[df_books['Title'] == title]

        if not author_books.empty:
            # انتخاب یک کتاب به عنوان نمونه (اگر چند کتاب با همین نویسنده وجود داشته باشد)
            selected_book = author_books.iloc[0]

            # بررسی تعداد موجودی
            if selected_book['Quantity'] >= quantity:
                # کم کردن تعداد موجودی
                df_books.loc[df_books['Title'] == selected_book['Title'], 'Quantity'] -= quantity

                # ذخیره کردن دیتافریم کتاب‌ها
                df_books.to_csv(self.books_file, index=False)

                # ذخیره کردن فروش در دیتافریم فروش
                sale_data = {'Title': selected_book['Title'], 'Quantity': quantity, 'Sale_Date': datetime.now()}
                try:
                    df_sales = pd.read_csv(self.sales_file)
                except FileNotFoundError:
                    df_sales = pd.DataFrame(columns=['Title', 'Quantity', 'Sale_Date'])

                df_sales = pd.concat([df_sales, pd.DataFrame([sale_data])], ignore_index=True)
                df_sales.to_csv(self.sales_file, index=False)

                print(f"Book '{selected_book['Title']}' sold successfully.")
            else:
                print("Error: Not enough inventory.")
        else:
            print(f"Error: No books found for title '{title}'.")

    def search_book(self, keyword):
        # خواندن دیتافریم کتاب‌ها از فایل
        try:
            df_books = pd.read_csv(self.books_file)
        except FileNotFoundError:
            print("Error: Books file not found.")
            return

        # جستجو بر اساس نام نویسنده یا نام کتاب
        result = df_books[df_books.apply(lambda row: keyword.lower() in row['Author'].lower() or keyword.lower() in row['Title'].lower(), axis=1)]

        if not result.empty:
            print("Books found:")
            print(result)
        else:
            print(f"No books found with keyword '{keyword}'.")

    def generate_sales_report(self, start_date, end_date):
        # خواندن دیتافریم فروش از فایل
        try:
            df_sales = pd.read_csv(self.sales_file)
        except FileNotFoundError:
            print("Error: Sales file not found.")
            return

        # جستجو بر اساس بازه زمانی
        result = df_sales[(df_sales['Sale_Date'] >= start_date) & (df_sales['Sale_Date'] <= end_date)]

        if not result.empty:
            print("Sales report:")
            print(result)
        else:
            print("No sales found in this period.")




bookObj = BookstoreManager()




def AddBookFunc():
    BookName = BookNameTbx.get()
    BookWriter = BookWriterTbx.get()
    PriceBook =PriceBookTbx.get()
    CountBook =CountBookTbx.get()
    bookObj.add_book(BookName, BookWriter, PriceBook, CountBook)

def SellBookFunc():
    SBookName =SBookNameTbx.get()
    SCount =int(SCountTbx.get())
    print (SBookName,SCount)
    bookObj.sell_book(SBookName,SCount)

def SearchFunc():
    Search=SearchTbx.get()
    bookObj.search_book(Search)

def ReportFunc():
    From_var =FromTbx.get()
    To_var = ToTbx.get()
    bookObj.generate_sales_report(From_var,To_var)
    # tkinter.messagebox.showwarning(title="Error", message=[From_var,To_var])

mainWindow = tkinter.Tk()
mainWindow.title("Book Store")

MainFrame = tkinter.LabelFrame(mainWindow)


# Add Frame
AddFrame = tkinter.LabelFrame(MainFrame, text="Add Book")

# Add input
AddInputFrame = tkinter.LabelFrame(AddFrame)

BookNameLbl = tkinter.Label(AddInputFrame,text="Name: ",)
BookNameLbl.grid(row=0, column=0)
BookNameTbx = tkinter.Entry(AddInputFrame)
BookNameTbx.grid(row=1, column=0)

BookWriterLbl = tkinter.Label(AddInputFrame,text="Writer: ")
BookWriterLbl.grid(row=0, column=1)
BookWriterTbx = tkinter.Entry(AddInputFrame)
BookWriterTbx.grid(row=1, column=1)

PriceBookLbl= tkinter.Label(AddInputFrame,text="Price: ")
PriceBookLbl.grid(row=2, column=0)
PriceBookTbx = tkinter.Spinbox(AddInputFrame, from_=0 , to_="infinity")
PriceBookTbx.grid(row=3, column=0)

CountBookLbl= tkinter.Label(AddInputFrame,text="Count: ")
CountBookLbl.grid(row=2, column=1)
CountBookTbx = tkinter.Spinbox(AddInputFrame, from_=0 , to_="infinity")
CountBookTbx.grid(row=3, column=1)


for widget in AddInputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


AddInputFrame.grid(row=0, column=0)

AddBtn = tkinter.Button(AddFrame , text="add book", command=AddBookFunc)
AddBtn.grid(row=1, column=0, sticky="news",padx=10, pady=5)

AddFrame.grid(row=0, column=0)



# Sell Frame
SellFrame = tkinter.LabelFrame(MainFrame, text="Sell Book")

SellInputFrame = tkinter.LabelFrame(SellFrame)

SBookNameLbl = tkinter.Label(SellInputFrame,text="Name: ",)
SBookNameLbl.grid(row=0, column=0)
SBookNameTbx = tkinter.Entry(SellInputFrame)
SBookNameTbx.grid(row=0, column=1)


SCountLbl = tkinter.Label(SellInputFrame,text="Count: ",)
SCountLbl.grid(row=1, column=0)
SCountTbx = tkinter.Entry(SellInputFrame)
SCountTbx.grid(row=1, column=1)

for widget in SellInputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

SellInputFrame.grid(row=0,column=0, padx=50, pady=5)

SellBtn = tkinter.Button(SellFrame , text="Sell book" ,command=SellBookFunc)
SellBtn.grid(row=1, column=0, sticky="news",padx=10, pady=5)


SellFrame.grid(row=1, column=0, sticky="news")



# Search Frame
SerachFrame = tkinter.LabelFrame(MainFrame, text="Search Book")

Searchlbl = tkinter.Label(SerachFrame,text="Serach in Book name and writers")
Searchlbl.grid(row=0,column=0)

SearchTbx = tkinter.Entry(SerachFrame)
SearchTbx.grid(row=1, column=0)

for widget in SerachFrame.winfo_children():
    widget.grid_configure(padx=70, pady=5, sticky="news")


SearchBtn = tkinter.Button(SerachFrame , text="Serach", command=SearchFunc)
SearchBtn.grid(row=2, column=0, sticky="news",padx=10, pady=5)


SerachFrame.grid(row=2, column=0, sticky="news")


# Report Frame
ReportFrame = tkinter.LabelFrame(MainFrame, text="Report Sell Book")

ReportInputFrame = tkinter.LabelFrame(ReportFrame)

FromLbl = tkinter.Label(ReportInputFrame,text="From: ",)
FromLbl.grid(row=0, column=0)
FromTbx = tkinter.Entry(ReportInputFrame)
FromTbx.grid(row=0, column=1)


ToLbl = tkinter.Label(ReportInputFrame,text="To: ",)
ToLbl.grid(row=1, column=0)
ToTbx = tkinter.Entry(ReportInputFrame)
ToTbx.grid(row=1, column=1)

for widget in ReportInputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

ReportInputFrame.grid(row=0,column=0, padx=50, pady=5)

Reportbtn = tkinter.Button(ReportFrame , text="Create Report" ,command=ReportFunc)
Reportbtn.grid(row=1, column=0, sticky="news",padx=10, pady=5)

ReportFrame.grid(row=3, column=0)


MainFrame.pack()
mainWindow.mainloop()






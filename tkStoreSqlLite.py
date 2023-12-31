import tkinter
import sqlite3
from tkinter import messagebox
from datetime import datetime

class Bookstore:
    def __init__(self, database):
        try:
            self.db = sqlite3.connect(database)
            self.cursor = self.db.cursor()
        except sqlite3.Error as err:
            messagebox.showerror(title="Error", message=f"Error connecting to the database: {err}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.db.close()
        except sqlite3.Error as err:
            messagebox.showerror(title="Error", message=f"Error closing the database connection: {err}")

    def add_book(self, name, writer, price, count):
        try:
            query = "INSERT INTO books (title, author, price, quantity) VALUES (?, ?, ?, ?)"
            values = (name, writer, price, count)
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo(title="Book added", message="Book added successfully.")
        except sqlite3.Error as err:
            messagebox.showerror(title="Error", message=f"Error adding book: {err}")

    def sell_book(self, name, count):
        try:
            query_select = "SELECT quantity FROM books WHERE title = ?"
            self.cursor.execute(query_select, (name,))
            result = self.cursor.fetchone()

            if result and result[0] >= count:
                query_update = "UPDATE books SET quantity = quantity - ? WHERE title = ?"
                self.cursor.execute(query_update, (count, name))

                query_insert_sale = "INSERT INTO sales (title, quantity, sale_date) VALUES (?, ?, ?)"
                sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute(query_insert_sale, (name, count, sale_date))

                self.db.commit()
                messagebox.showinfo(title="Book sold", message=f"Book sold successfully. Sale date: {sale_date}")
            else:
                messagebox.showwarning(title="Not Enough Inventory", message="Not enough inventory or the book is not available.")
        except sqlite3.Error as err:
            messagebox.showerror(title="Error", message=f"Error selling book: {err}")

    def search_book(self, keyword):
        try:
            query = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?"
            keyword_like = f"%{keyword}%"
            self.cursor.execute(query, (keyword_like, keyword_like))
            result = self.cursor.fetchall()
            if result:
                for book in result:
                    messagebox.showinfo(title="Book found", message=book)
            else:
                messagebox.showwarning(title="Not Found", message="There is no book or writer with " + keyword)
        except sqlite3.Error as err:
            messagebox.showerror(title="Error", message=f"Error searching for book: {err}")

    def generate_sales_report(self, start_date, end_date):
        try:
            query = "SELECT * FROM sales WHERE sale_date BETWEEN ? AND ?"
            self.cursor.execute(query, (start_date, end_date))
            result = self.cursor.fetchall()

            if result:
                for sale in result:
                    messagebox.showinfo(title="Sele found", message=sale)
            else:
                print("No sales found in this period.")
        except sqlite3.Error as err:
            messagebox.showerror(title="Error", message=f"Error generating sales report: {err}")


bookObj = Bookstore("bookstore")




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



import tkinter
import sqlite3
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Bookstore:
    def __init__(self, database):
        try:
            self.db = sqlite3.connect(database)
            self.cursor = self.db.cursor()
        except sqlite3.Error as err:
            messagebox.showerror(
                title="Error", message=f"Error connecting to the database: {err}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.db.close()
        except sqlite3.Error as err:
            messagebox.showerror(
                title="Error", message=f"Error closing the database connection: {err}")

    def add_book(self, name, writer, price, count):
        try:
            query = "INSERT INTO books (title, author, price, quantity) VALUES (?, ?, ?, ?)"
            values = (name, writer, price, count)
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo(title="Book added",
                                message="Book added successfully.")
        except sqlite3.Error as err:
            messagebox.showerror(
                title="Error", message=f"Error adding book: {err}")

    def sell_book(self, name, count):
        try:
            query_select = "SELECT quantity, price FROM books WHERE title = ?"
            self.cursor.execute(query_select, (name,))
            result = self.cursor.fetchone()
            if result and result[0] >= count:
                query_update = "UPDATE books SET quantity = quantity - ? WHERE title = ?"
                self.cursor.execute(query_update, (count, name))

                query_insert_sale = "INSERT INTO sales (title, quantity, price, sale_date) VALUES (?, ?, ?, ?)"
                sale_date = datetime.now().strftime("%Y-%m-%d")
                self.cursor.execute(query_insert_sale,
                                    (name, count, result[1], sale_date))

                self.db.commit()
                messagebox.showinfo(
                    title="Book sold", message=f"Book sold successfully. Sale date: {sale_date}")

            else:
                messagebox.showwarning(
                    title="Not Enough Inventory", message="Not enough inventory or the book is not available.")
        except sqlite3.Error as err:
            messagebox.showerror(
                title="Error", message=f"Error selling book: {err}")

    def generate_sales_report(self, start_date, end_date):
        try:
            query = "SELECT * FROM sales WHERE sale_date BETWEEN ? AND ?"
            self.cursor.execute(query, (start_date, end_date))
            result = self.cursor.fetchall()

            if result:
                for sale in result:
                    # print(sale)
                    return result
            else:
                messagebox.showerror(
                    title="Error", message="No sales found in this period.")
        except sqlite3.Error as err:
            messagebox.showerror(
                title="Error", message=f"Error generating sales report: {err}")

    def Resive_data(self):
        query = "SELECT * FROM books"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def Resive_Sales_data(self):
        query = "SELECT * FROM sales"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def search_book(self, key):
        try:
            query = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?"
            keyword_like = f"%{key}%"
            self.cursor.execute(query, (keyword_like, keyword_like))
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as err:
            messagebox.showerror(
                title="Error", message=f"Error searching for book: {err}")


bookObj = Bookstore("bookstore")
mainWindow = tkinter.Tk()
mainWindow.title("Book Store")
string_varQ = tkinter.StringVar()
string_varSQ = tkinter.StringVar()
string_varSP = tkinter.StringVar()


def AddBookFunc():
    BookName = BookNameTbx.get()
    BookWriter = BookWriterTbx.get()
    PriceBook = PriceBookTbx.get()
    CountBook = CountBookTbx.get()
    if PriceBook.isdigit() and CountBook.isdigit() and not (CountBook.isdigit()):
        bookObj.add_book(BookName, BookWriter, PriceBook, CountBook)
        # clearTable(TableAll)
        All_Data = bookObj.Resive_data()
        ShowData(TableAll, All_Data)
    else:
        messagebox.showerror(
            title="Error", message="The values are not entered correctly")


def SellBookFunc():
    SBookName = SBookNameTbx.get()
    SCount = SCountTbx.get()
    if SCount.isdigit() and int(SCount) > 0:
        # print (SBookName,SCount)
        bookObj.sell_book(SBookName, int(SCount))
        All_Data = bookObj.Resive_data()
        ShowData(TableAll, All_Data)
        All_Seles_Data = bookObj.Resive_Sales_data()
        ShowSalesData(SellTable, All_Seles_Data)
    else:
        messagebox.showerror(
            title="Error", message="The values are not entered correctly")


def SearchFunc():
    key = SearchTbx.get()
    A_Data = bookObj.search_book(key)
    ShowData(TableAll, A_Data)


def ReportFunc():
    From_var = FromTbx.get()
    To_var = ToTbx.get()
    S_Data = bookObj.generate_sales_report(From_var, To_var)
    # S_Data = bookObj.Resive_Sales_data()
    ShowSalesData(SellTable, S_Data)
    return S_Data


def ShowData(widget, Data):
    SumQ = 0
    for i in widget.get_children():
        widget.delete(i)
    for dt in Data:
        if dt[4] != 0:
            widget.insert("", 'end', iid=dt[0], text=dt[0],
                          values=(dt[0], dt[1], dt[2], dt[3], dt[4]))
            SumQ += dt[4]
        else:
            continue

    SumQ = "Total Quantity: " + str(SumQ)
    string_varQ.set(SumQ)


def ShowSalesData(widget, Data):
    try:
        SumSQ = SumSP = 0
        for i in widget.get_children():
            widget.delete(i)
        for dt in Data:
            widget.insert("", 'end', iid=dt[0], text=dt[0],
                          values=(dt[0], dt[1], dt[2], dt[3], dt[4]))
            SumSQ += dt[2]
            SumSP += dt[2]*dt[3]

        SumSP = "Total Sell: " + str(SumSP)
        SumSQ = "Total Quantity: " + str(SumSQ)
        string_varSQ.set(SumSQ)
        string_varSP.set(SumSP)
    except:
        messagebox.showerror(title="Error", message="Error")


def ClearFunc():
    BookNameTbx.delete(0, 'end')
    BookWriterTbx.delete(0, 'end')
    PriceBookTbx.delete(0, 0)
    CountBookTbx.delete(0, 0)
    SBookNameTbx.delete(0, 'end')
    SCountTbx.delete(0, 'end')
    SearchTbx.delete(0, 'end')
    ToTbx.delete(0, 'end')
    FromTbx.delete(0, 'end')
    All_Data = bookObj.Resive_data()
    ShowData(TableAll, All_Data)

    SALE_Date = bookObj.Resive_Sales_data()
    ShowSalesData(SellTable, SALE_Date)


MainFrame = tkinter.LabelFrame(mainWindow)


DataFrame = tkinter.LabelFrame(MainFrame, borderwidth=0)
DataFrame.configure(width=3)
DataFrame.grid(row=0, column=0, sticky="n")

TableAll = ttk.Treeview(DataFrame, selectmode='browse')
TableAll["columns"] = ("1", "2", "3", "4", "5")
# number of columns
TableAll["columns"] = ("1", "2", "3", "4", "5")

# Defining heading
TableAll['show'] = 'headings'

# width of columns and alignment
TableAll.column("1", width=30, anchor='c')
TableAll.column("2", width=80, anchor='c')
TableAll.column("3", width=80, anchor='c')
TableAll.column("4", width=80, anchor='c')
TableAll.column("5", anchor='c')
TableAll  # Headings
# respective columns
TableAll.heading("1", text="ID")
TableAll.heading("2", text="Book Name")
TableAll.heading("3", text="Author")
TableAll.heading("4", text="Price")
TableAll.heading("5", text="Quantity")
TableAll.grid(row=0, column=0, sticky="news", padx=10, pady=5)

All_Data = bookObj.Resive_data()
ShowData(TableAll, All_Data)


TotalQuantity = tkinter.Label(DataFrame, textvariable=string_varQ)
TotalQuantity.grid(row=2, column=0, sticky="w", padx=10, pady=5)


SellTable = ttk.Treeview(DataFrame, selectmode='browse')
SellTable["columns"] = ("1", "2", "3", "4", "5")
# number of columns
SellTable["columns"] = ("1", "2", "3", "4", "5")

# Defining heading
SellTable['show'] = 'headings'

# width of columns and alignment
SellTable.column("1", width=30, anchor='c')
SellTable.column("2", width=80, anchor='c')
SellTable.column("3", width=80, anchor='c')
SellTable.column("4", width=80, anchor='c')
SellTable.column("5", anchor='c')
SellTable  # Headings
# respective columns
SellTable.heading("1", text="ID")
SellTable.heading("2", text="Book Name")
SellTable.heading("3", text="Quantity")
SellTable.heading("4", text="Price")
SellTable.heading("5", text="Sales Date")


SellTable.grid(row=3, column=0, sticky="news", padx=10, pady=5)

Sell_Data = bookObj.Resive_Sales_data()
ShowSalesData(SellTable, Sell_Data)


InfoSell = tkinter.Frame(DataFrame, borderwidth=0)
InfoSell.grid(row=4, column=0, sticky="news", padx=10, pady=(0, 5))

TotalSellQuantity = tkinter.Label(InfoSell, textvariable=string_varSQ)
TotalSellQuantity.grid(row=0, column=0, sticky="w", padx=10, pady=5)

TotalPriceQuantity = tkinter.Label(InfoSell, textvariable=string_varSP)
TotalPriceQuantity.grid(row=0, column=1, sticky="w", padx=10, pady=5)

ClearBtn = tkinter.Button(DataFrame, text="Clear", command=ClearFunc)
ClearBtn.grid(row=5, column=0, sticky="news", padx=10, pady=(0, 5))


ActioFrame = tkinter.LabelFrame(MainFrame, borderwidth=0)
ActioFrame.configure(width=2)
ActioFrame.grid(row=0, column=1, padx=10, pady=5)

# Add Frame
AddFrame = tkinter.LabelFrame(ActioFrame, text="Add Book")

# Add input
AddInputFrame = tkinter.LabelFrame(AddFrame, borderwidth=0)

BookNameLbl = tkinter.Label(AddInputFrame, text="Name")
BookNameLbl.grid(row=0, column=0)
BookNameTbx = tkinter.Entry(AddInputFrame)
BookNameTbx.grid(row=1, column=0)

BookWriterLbl = tkinter.Label(AddInputFrame, text="Writer")
BookWriterLbl.grid(row=0, column=1)
BookWriterTbx = tkinter.Entry(AddInputFrame)
BookWriterTbx.grid(row=1, column=1)

PriceBookLbl = tkinter.Label(AddInputFrame, text="Price")
PriceBookLbl.grid(row=2, column=0)
PriceBookTbx = tkinter.Spinbox(AddInputFrame, from_=0, to_="infinity")
PriceBookTbx.grid(row=3, column=0)

CountBookLbl = tkinter.Label(AddInputFrame, text="Count")
CountBookLbl.grid(row=2, column=1)
CountBookTbx = tkinter.Spinbox(AddInputFrame, from_=0, to_="infinity")
CountBookTbx.grid(row=3, column=1)


for widget in AddInputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


AddInputFrame.grid(row=0, column=0)

AddBtn = tkinter.Button(AddFrame, text="add book", command=AddBookFunc)
AddBtn.grid(row=1, column=0, sticky="news", padx=(10, 0), pady=5)

AddFrame.grid(row=0, column=0, sticky="news")


# Sell Frame
SellFrame = tkinter.LabelFrame(ActioFrame, text="Sell Book")

SellInputFrame = tkinter.LabelFrame(SellFrame, borderwidth=0)

SBookNameLbl = tkinter.Label(SellInputFrame, text="Name: ",)
SBookNameLbl.grid(row=0, column=0)
SBookNameTbx = tkinter.Entry(SellInputFrame)
SBookNameTbx.grid(row=0, column=1)


SCountLbl = tkinter.Label(SellInputFrame, text="Count: ",)
SCountLbl.grid(row=1, column=0)
SCountTbx = tkinter.Spinbox(SellInputFrame, from_=0, to_="infinity")
SCountTbx.grid(row=1, column=1)

for widget in SellInputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

SellInputFrame.grid(row=0, column=0, padx=70, pady=5)

SellBtn = tkinter.Button(SellFrame, text="Sell book", command=SellBookFunc)
SellBtn.grid(row=1, column=0, sticky="news", padx=10, pady=5)


SellFrame.grid(row=1, column=0, sticky="news")


# Search Frame
SerachFrame = tkinter.LabelFrame(ActioFrame, text="Search Book")

Searchlbl = tkinter.Label(SerachFrame, text="Serach in Book name and writers")
Searchlbl.grid(row=0, column=0)

SearchTbx = tkinter.Entry(SerachFrame)
SearchTbx.grid(row=1, column=0)

for widget in SerachFrame.winfo_children():
    widget.grid_configure(padx=90, pady=5, sticky="news")


SearchBtn = tkinter.Button(SerachFrame, text="Serach", command=SearchFunc)
SearchBtn.grid(row=2, column=0, sticky="news", padx=10, pady=5)


SerachFrame.grid(row=2, column=0, sticky="news")


# Report Frame


ReportFrame = tkinter.LabelFrame(ActioFrame, text="Report Sell Book")

ReportInputFrame = tkinter.LabelFrame(ReportFrame, borderwidth=0)

TimePeried = tkinter.Label(ReportInputFrame, text="Time Peried: ")
TimePeried.grid(row=0, column=0)
n = tkinter.StringVar()


def Time_changed(event):
    if TimePeriedCmX.get() == TimePeriedCmX['values'][0]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2023-01-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2023-03-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][1]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2023-04-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2023-06-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][2]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2023-07-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2023-09-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][3]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2023-09-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2023-12-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][4]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2023-01-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2023-06-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][5]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2023-07-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2023-12-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][6]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "2022-01-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, "2022-12-30")
    elif TimePeriedCmX.get() == TimePeriedCmX['values'][7]:
        FromTbx.delete(0, tkinter.END)
        FromTbx.insert(0, "1970-01-01")
        ToTbx.delete(0, tkinter.END)
        ToTbx.insert(0, datetime.now().strftime("%Y-%m-%d"))


TimePeriedCmX = ttk.Combobox(
    ReportInputFrame, textvariable=n, state='readonly')
TimePeriedCmX['values'] = ('The first three months of the year',
                           'The second quarter of the year',
                           'The third quarter of the year',
                           'The fourth quarter of the year',
                           'The first six months of the year',
                           'The second six months of the year',
                           '2022',
                           'from the beginning to the end')
TimePeriedCmX.current(7)

TimePeriedCmX.grid(column=1, row=0, padx=10, pady=5, sticky="w")
TimePeriedCmX.bind('<<ComboboxSelected>>', Time_changed)

FromLbl = tkinter.Label(ReportInputFrame, text="From: ",)
FromLbl.grid(row=1, column=0, sticky="w")
FromTbx = tkinter.Entry(ReportInputFrame)
FromTbx.grid(row=1, column=1, sticky="w")


ToLbl = tkinter.Label(ReportInputFrame, text="To: ",)
ToLbl.grid(row=2, column=0, sticky="w")
ToTbx = tkinter.Entry(ReportInputFrame)
ToTbx.grid(row=2, column=1, sticky="w")

FromTbx.delete(0, tkinter.END)
FromTbx.insert(0, "1970-01-01")
ToTbx.delete(0, tkinter.END)
ToTbx.insert(0, datetime.now().strftime("%Y-%m-%d"))


for widget in ReportInputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

ReportInputFrame.grid(row=0, column=0, padx=50, pady=5)

Reportbtn = tkinter.Button(
    ReportFrame, text="Create Report", command=ReportFunc)
Reportbtn.grid(row=1, column=0, sticky="news", padx=10, pady=5)


def create_plot(data):
    sorted_data = sorted(
        data, key=lambda x: datetime.strptime(x[-1], '%Y-%m-%d'))

    # تبدیل داده‌ها به ساختار مناسب
    dates = [datetime.strptime(entry[-1], '%Y-%m-%d') for entry in sorted_data]
    quantities = [entry[2] for entry in sorted_data]
    total_prices = [entry[3] for entry in sorted_data]

    # رسم نمودار تعداد فروش
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(dates, quantities, marker='o')
    plt.title('Quantity Sold Over Time')
    plt.xlabel('Date')
    plt.ylabel('Quantity Sold')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    # رسم نمودار قیمت کل
    plt.subplot(2, 1, 2)
    plt.plot(dates, total_prices, marker='o', color='orange')
    plt.title('Total Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Price')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.show()


def on_button_click_report():
    create_plot(ReportFunc())


CreatPltbtn = tkinter.Button(
    ReportFrame, text="Draw Charts", command=on_button_click_report)
CreatPltbtn.grid(row=2, column=0, sticky="news", padx=10, pady=5)

ReportFrame.grid(row=3, column=0, sticky="news")


MainFrame.pack()
mainWindow.mainloop()

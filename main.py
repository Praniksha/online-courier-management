from tkcalendar import Calendar
import datetime
import random
from tkinter import *
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect('employee.db')
reg = sqlite3.connect('order.db')
cursor = conn.cursor()
reg_cursor = reg.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee'")
table_exists = cursor.fetchone() is not None

reg_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Orders'")
table_exists2 = reg_cursor.fetchone() is not None

if not table_exists:
    cursor.execute('''CREATE TABLE employee (emp_id INTEGER PRIMARY KEY, emp_name TEXT, emp_contact TEXT, emp_email TEXT)''')

if not table_exists2:
    reg_cursor.execute('''CREATE TABLE Orders(ord_id INTEGER PRIMARY KEY, p_name TEXT, p_price INTEGER, phone INTEGER,address TEXT, name TEXT, tracking_id INTEGER)''')


def order_button():
    global neworder,newproduct,newprice,newphone,newadress,newname
    newWindow = Toplevel(root)
    newWindow.geometry("900x500")
    newWindow.title("New Orders")
    Label(newWindow, text="Add New Orders", font=("Helvetica", 20)).grid(row=0,column=1,padx=10,pady=5)
    Label(newWindow, text="Enter Name:").grid(row=1, column=0,pady=10)
    newname = Entry(newWindow, font=("Helvetica", 10))
    newname.grid(row=1,column=1,pady=5)

    newp = Label(newWindow, text="Enter Product Name:").grid(row=2, column=0, pady=10)
    newproduct = Entry(newWindow, font=("Helvetica", 10))
    newproduct.grid(row=2, column=1, pady=5)

    newpp = Label(newWindow, text="Enter Product Price:").grid(row=3, column=0, pady=10)
    newprice = Entry(newWindow, font=("Helvetica", 10))
    newprice.grid(row=3, column=1, pady=5)\

    newph = Label(newWindow, text="Enter Phone Number:").grid(row=4, column=0, pady=10)
    newphone = Entry(newWindow, font=("Helvetica", 10))
    newphone.grid(row=4, column=1, pady=5)

    newa = Label(newWindow, text="Enter Order Address:").grid(row=5, column=0, pady=10)
    newadress = Entry(newWindow, font=("Helvetica", 10))
    newadress.grid(row=5, column=1, pady=5)

    submit = Button(newWindow, text= "Submit", width=10,command=new_order_submit).grid(row=6,column=1,pady=10,padx=8)

def new_order_submit():
        if newproduct.get() == '' or newprice.get() == '' or newphone.get() == '' or newadress.get() == '':
            messagebox.showerror("Error", "Please fill all the details!")
        else:
            product_name = newproduct.get()
            price = int(newprice.get())
            phone_number = int(newphone.get())
            address = newadress.get()
            name = newname.get()

            while(True):
                # Get the current timestamp as a string
                timestamp_str = str(datetime.datetime.now().timestamp())

                # Remove the decimal point and any non-digit characters
                digits_str = ''.join(filter(str.isdigit, timestamp_str))

                # Pad the string with leading zeros if necessary
                digits_str = digits_str.zfill(9)

                # Convert the string to an integer
                unique_num = int(digits_str)

                # Add a random digit to the end to ensure uniqueness
                Tracking_ID = unique_num * 10 + random.randint(0, 9)

                print(Tracking_ID)

                reg_cursor.execute("SELECT * FROM Orders WHERE tracking_id=?", (Tracking_ID,))
                row = reg_cursor.fetchone()
                if row is not None:
                   continue
                else:
                    reg_cursor.execute("INSERT INTO Orders (p_name,p_price,phone,address,name,tracking_id) VALUES (?, ?, ?, ?, ?, ?)",
                                       (product_name, price, phone_number, address, name, Tracking_ID))
                    reg.commit()
                    messagebox.showinfo("Success", "New order has been added!")
                    break


def track_order_button():
    global c_name,c_phone,tracking_id,view
    view = Toplevel(root)
    view.title("Track Order")
    view.geometry("500x500")

    Label(view,text="Enter Details To Track", font=("Helvetica", 20)).grid(row=0,column=1,pady=5)

    Label(view, text="Enter Name:").grid(row=1, column=0, pady=10)
    c_name = Entry(view, font=("Helvetica", 10))
    c_name.grid(row=1,column=1)

    Label(view, text="Enter Phone Number:").grid(row=2, column=0, pady=10)
    c_phone = Entry(view, font=("Helvetica", 10))
    c_phone.grid(row=2, column=1)

    Label(view, text="Enter Tracking ID:").grid(row=3, column=0, pady=10)
    tracking_id = Entry(view, font=("Helvetica", 10))
    tracking_id.grid(row=3, column=1)

    submit = Button(view, text="Track Order",width=15,command=trackorder)
    submit.grid(row=4,column=1)



def trackorder():
    name = c_name.get()
    phone = c_phone.get()
    track = tracking_id.get()

    reg_cursor.execute("SELECT * FROM Orders WHERE name=? AND phone=? AND tracking_id=?", (name, phone, track))
    order = reg_cursor.fetchone()

    if order:
        Label(view, text=f"Product Name: {order[1]}").grid(row=5, column=1, pady=5)
        Label(view, text=f"Product Price: {order[2]}").grid(row=6, column=1, pady=5)
        Label(view, text=f"Order Address: {order[4]}").grid(row=7, column=1, pady=5)
        Label(view, text=f"Tracking ID: {order[6]}").grid(row=8, column=1, pady=5)
    else:
        messagebox.showerror("Error", "No orders found with the given details!")



root = Tk()
root.title("Online Courier Management")
root.geometry("900x400")

title = Label(root, text="Online Courier Management", font=("Helvetica",40)).grid(row=0,column=1)

new_order = Button(root, text="New Order", width=15, height=6, command=order_button)
new_order .grid(row=1,column=0, padx=4)

track_order = Button(root, text="Track Order", width=15, height=6, command=track_order_button)
track_order.grid(row=1,column=1)

Employee = Button(root, text="Employee", width=15, height=6)
Employee.grid(row=1,column=2)

delivery = Button(root, text="Delivery", width=15, height=6)
delivery.grid(row=2,column=0, pady=10)

Admin = Button(root, text="Admin", width=15, height=6)
Admin.grid(row=2,column=1, pady=10)

Bill = Button(root, text="Bill", width=15, height=6)
Bill.grid(row=2,column=2, pady=10)



root.mainloop()

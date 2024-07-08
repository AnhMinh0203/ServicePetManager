from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime
from tkcalendar import Calendar
def test():
    pass
def refresh_treeview(tree,cursor):
    # Clear the current items in the tree
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM Customers WHERE Status = 1")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
def search_customer(cursor,entr_search,tree):
    text = entr_search.get().strip()
    cursor.execute("SELECT * FROM Customers WHERE Name LIKE %s AND Status = 1", ('%' + text + '%',))
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("","end",values=row)
def add_customer(cursor,customer,tree,window_customer_ad,db):
    cursor.execute("Insert into Customers "
                   "(Name,PhoneNumber, Address,DateOfBirth,Gender,CreateBy,CreateDate,ModifyBy,ModifyDate,Status) "
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (customer.name,customer.phone_number,customer.address,customer.dob,customer.gender,
                    customer.create_by,customer.create_date,customer.modify_by,customer.modify_date, 1))
    db.commit()
    messagebox.showinfo("Success", "Add successfully")
    window_customer_ad.destroy()
    refresh_treeview(tree,cursor)

def update_customer (cursor,customer,tree,window_customer_ad,db,id_emp):
    cursor.execute(
        "Update Customers set Name = %s,PhoneNumber = %s,Address = %s,DateOfBirth = %s, Gender = %s, "
        "ModifyBy = %s, ModifyDate = %s  WHERE Id = %s ",
        (customer.name, customer.phone_number, customer.address, customer.dob, customer.gender, customer.modify_by,
         customer.modify_date, id_emp))
    db.commit()
    messagebox.showinfo("Success", "Update successfully")
    window_customer_ad.destroy()
    refresh_treeview(tree, cursor)

def create_customer_add_form(cursor,tree,db,id_user):
    from ServicePetManager.main import Customer
    def add_customer_action():
        name = entr_customer_name.get().strip()
        phone = entry_customer_phone.get().strip()
        address = entr_customer_address.get().strip()
        dateOfBirth = dob.cget("text")
        gender = gender_var.get()
        create_by = id_user
        modify_by = id_user
        modify_date = datetime.now().strftime('%Y-%m-%d')

        customer = Customer(name, phone,address, dateOfBirth,gender, create_by,modify_by, modify_date)
        add_customer(cursor, customer, tree, window_customer_ad, db)

    window_customer_ad = Tk()
    window_customer_ad.geometry("400x600")
    window_customer_ad.title("Add Product")
    screen_width = window_customer_ad.winfo_screenwidth()
    screen_height = window_customer_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_customer_ad.geometry(f"400x600+{position_x}+{position_y}")

    lable_customer_name = Label(window_customer_ad, text="Name")
    lable_customer_name.place(x=20, y=50, width=50, height=30)

    entr_customer_name = Entry(window_customer_ad)
    entr_customer_name.place(x=20, y=80, width=350, height=30)

    label_customer_phone = Label(window_customer_ad,text="Phone number")
    label_customer_phone.place(x=20, y=110, width=100, height=30)

    entry_customer_phone = Entry(window_customer_ad)
    entry_customer_phone.place(x=20, y=140, width=350, height=30)

    lable_customer_password = Label(window_customer_ad, text="Address")
    lable_customer_password.place(x=20, y=170, width=50, height=30)

    entr_customer_address = Entry(window_customer_ad)
    entr_customer_address.place(x=20, y=200, width=350, height=30)

    gender_var = StringVar(window_customer_ad)
    gender_var.set("Nam")  # set the default value

    gender_menu = OptionMenu(window_customer_ad, gender_var, "Nam", "Nữ")
    gender_menu.place(x=20, y=250, width=80, height=30)
    # Dob
    cal = Calendar(window_customer_ad, selectmode='day', year=2020, month=5, day=22)

    def toggle_calendar():
        if cal.winfo_ismapped():
            cal.place_forget()
        else:
            cal.place(x=140, y=260)
            cal.tkraise()

    dob = Button(window_customer_ad, text="Date of birth", command=toggle_calendar)
    dob.place(x=140, y=250, width=150, height=30)

    cal = Calendar(window_customer_ad, selectmode='day', year=2020, month=5, day=22)

    def on_date_select(event):
        selected_date = cal.get_date()
        dob.config(text=selected_date)
        cal.place_forget()

    # Bind the function to the calendar's date selection event
    cal.bind("<<CalendarSelected>>", on_date_select)

    add_customer_button = Button(window_customer_ad, text="Save", command=add_customer_action)
    add_customer_button.place(x=260, y=350, width=100, height=30)
    window_customer_ad.mainloop()
def detail_customer(cursor,id):
    cursor.execute("Select * from Customers where id = %s",(id,))
    row = cursor.fetchone()
    if row :
        name = row[1]
        phone = row[2]
        address = row[3]
        dateOfBirth = row[4]
        gender = row[5]

        return name, phone, address, dateOfBirth,gender
    else:
        return None
def create_customer_update_form(cursor, tree, id_emp, db,id_user):
    from ServicePetManager.main import Customer
    def update_customer_action():
        name = entr_customer_name.get().strip()
        phone = entry_customer_phone.get().strip()
        address = entr_customer_address.get().strip()
        dateOfBirth = dob.cget("text")
        gender = gender_var.get()
        modify_by = id_user
        modify_date = datetime.now().strftime('%Y-%m-%d')

        customer = Customer(name, phone, address, dateOfBirth, gender,None, modify_by, modify_date)
        update_customer(cursor, customer, tree, window_customer_ad, db,id_emp)

    window_customer_ad = Tk()
    window_customer_ad.geometry("400x600")
    window_customer_ad.title("Add Product")
    screen_width = window_customer_ad.winfo_screenwidth()
    screen_height = window_customer_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_customer_ad.geometry(f"400x600+{position_x}+{position_y}")

    lable_customer_name = Label(window_customer_ad, text="Name")
    lable_customer_name.place(x=20, y=50, width=50, height=30)

    entr_customer_name = Entry(window_customer_ad)
    entr_customer_name.place(x=20, y=80, width=350, height=30)

    label_customer_phone = Label(window_customer_ad, text="Phone number")
    label_customer_phone.place(x=20, y=110, width=100, height=30)

    entry_customer_phone = Entry(window_customer_ad)
    entry_customer_phone.place(x=20, y=140, width=350, height=30)

    lable_customer_password = Label(window_customer_ad, text="Address")
    lable_customer_password.place(x=20, y=170, width=50, height=30)

    entr_customer_address = Entry(window_customer_ad)
    entr_customer_address.place(x=20, y=200, width=350, height=30)

    gender_var = StringVar(window_customer_ad)
    gender_var.set("Nam")  # set the default value

    gender_menu = OptionMenu(window_customer_ad, gender_var, "Nam", "Nữ")
    gender_menu.place(x=20, y=250, width=80, height=30)
    # Dob
    cal = Calendar(window_customer_ad, selectmode='day', year=2020, month=5, day=22)

    def toggle_calendar():
        if cal.winfo_ismapped():
            cal.place_forget()
        else:
            cal.place(x=140, y=260)
            cal.tkraise()

    dob = Button(window_customer_ad, text="Date of birth", command=toggle_calendar)
    dob.place(x=140, y=250, width=150, height=30)

    cal = Calendar(window_customer_ad, selectmode='day', year=2020, month=5, day=22)

    def on_date_select(event):
        selected_date = cal.get_date()
        dob.config(text=selected_date)
        cal.place_forget()

    # Bind the function to the calendar's date selection event
    cal.bind("<<CalendarSelected>>", on_date_select)

    add_customer_button = Button(window_customer_ad, text="Save", command=update_customer_action)
    add_customer_button.place(x=260, y=300, width=100, height=30)


    name, phone, address, dateOfBirth,gender =  detail_customer(cursor,id_emp)
    entr_customer_name.insert(0,name)
    entry_customer_phone.insert(0,phone)
    entr_customer_address.insert(0,address)
    dob.config(text=dateOfBirth)
    gender_var.set(gender)
    window_customer_ad.mainloop()

def delete_customer(cursor,id_product,tree,db):
    ask = messagebox.askyesno("Confirm delete","Do you want to delete this customer ?")
    if ask:
        cursor.execute("Update bill set IdCustomer = NULL where IdCustomer = %s", (id_product,))
        cursor.execute("UPDATE customers SET Status = 0 WHERE id = %s", (id_product,))
        db.commit()
        refresh_treeview(tree,cursor)
        messagebox.showinfo("Delete alert","Delete successfully !")
    else:
        return


def create_customer_manager_form(cursor,db,id_user):
    global selected_id

    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]
        print(selected_id)

    def hide_window():
        window_customer_mg.withdraw()

    window_customer_mg = Tk()
    window_customer_mg.geometry("850x600")
    window_customer_mg.title("Customer Manager")
    # Close the program when clicking the close button
    window_customer_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_customer_mg.winfo_screenwidth()
    screen_height = window_customer_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_customer_mg.geometry(f"850x600+{position_x}+{position_y}")

    # Heading
    heading_customer_mg = Label(window_customer_mg,text="CUSTOMER MANAGEMENT",font=("Helvetica", 20, "bold"), fg="green")
    heading_customer_mg.place(x=200, y=30, width=400, height=30)

    # Search
    entr_search = Entry(window_customer_mg)
    entr_search.place(x=400, y=80, width=300, height=30)

    button_customer_manager = Button(window_customer_mg, text="Search", command=lambda: search_customer(cursor,entr_search,tree))
    button_customer_manager.place(x=720, y=80, width=80, height=30)

    # Add, Update, Delete buttons
    button_customer_manager = Button(window_customer_mg, text="Add", command=lambda: create_customer_add_form(cursor,tree,db,id_user))
    button_customer_manager.place(x=520, y=450, width=80, height=30)

    button_customer_manager = Button(window_customer_mg, text="Update", command=lambda: create_customer_update_form(cursor,tree,selected_id,db,id_user))
    button_customer_manager.place(x=620, y=450, width=80, height=30)

    button_customer_manager = Button(window_customer_mg, text="Delete", command=lambda: delete_customer(cursor,selected_id,tree,db))
    button_customer_manager.place(x=720, y=450, width=80, height=30)
    # Tree view
    columns = ("ID","Name", "PhoneNumber", "Address", "DateOfBirth", "Gender","CreateBy","CreateDate","ModifyBy","ModifyDate")
    tree = ttk.Treeview(window_customer_mg, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("PhoneNumber", text="PhoneNumber")
    tree.heading("Address", text="Address")
    tree.heading("DateOfBirth", text="DateOfBirth")
    tree.heading("Gender", text="Gender")
    tree.heading("CreateBy", text="CreateBy")
    tree.heading("CreateDate", text="CreateDate")
    tree.heading("ModifyBy", text="ModifyBy")
    tree.heading("ModifyDate", text="ModifyDate")

    total_width = 800  # Total width of the Treeview
    column_width = total_width // len(columns)  # Calculate width for each column
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)

    tree.place(x=20, y=130, width=800, height=200)
    cursor.execute("SELECT * FROM Customers WHERE Status = 1")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_customer_mg.mainloop()
from tkcalendar import Calendar
from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime

def test():
    pass
def refresh_treeview(tree,cursor):
    # Clear the current items in the tree
    for item in tree.get_children():
        tree.delete(item)

    # Load new data from the database
    cursor.execute("SELECT * FROM Supplier")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
def search_supplier(cursor,entr_search,tree):
    text = entr_search.get().strip()
    cursor.execute("SELECT * FROM Supplier WHERE Name LIKE %s", ('%' + text + '%',))
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("","end",values=row)
def add_supplier(cursor,supplier,tree,window_supplier_ad,db):
    cursor.execute("Insert into Supplier (Name,PhoneNumber, Address,CreateDate,CreateBy,ModifyDate,ModifiBy) "
                   "values (%s,%s,%s,%s,%s,%s,%s)",
                   (supplier.name,supplier.phone_number,supplier.address,supplier.create_date,supplier.create_by,supplier.modify_date,supplier.modify_by))
    db.commit()
    messagebox.showinfo("Success", "Add successfully")
    window_supplier_ad.destroy()
    refresh_treeview(tree,cursor)

def update_supplier (cursor,supplier,tree,window_supplier_ad,db,id_emp):
    cursor.execute(
        "Update Supplier set Name = %s,PhoneNumber = %s, Address = %s , ModifyDate = %s, ModifiBy = %s WHERE Id = %s ",
        (supplier.name, supplier.phone_number, supplier.address, supplier.modify_date,supplier.modify_by,id_emp))
    db.commit()
    messagebox.showinfo("Success", "Update successfully")
    window_supplier_ad.destroy()
    refresh_treeview(tree, cursor)

def create_supplier_add_form(cursor,tree,db,id_user):
    from ServicePetManager.main import Supplier
    def add_supplier_action():
        name = entr_supplier_name.get().strip()
        phone = entry_supplier_phone.get().strip()
        address =  entr_supplier_address.get().strip()
        create_by = id_user
        modify_by = id_user
        modify_date = datetime.now().strftime('%Y-%m-%d')
        supplier = Supplier(name, phone, address, create_by, modify_by,modify_date)
        add_supplier(cursor, supplier, tree, window_supplier_ad, db)

    window_supplier_ad = Tk()
    window_supplier_ad.geometry("400x600")
    window_supplier_ad.title("Add Supplier")
    screen_width = window_supplier_ad.winfo_screenwidth()
    screen_height = window_supplier_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_supplier_ad.geometry(f"400x600+{position_x}+{position_y}")

    lable_supplier_name = Label(window_supplier_ad, text="Name")
    lable_supplier_name.place(x=20, y=50, width=50, height=30)

    entr_supplier_name = Entry(window_supplier_ad)
    entr_supplier_name.place(x=20, y=80, width=350, height=30)

    label_supplier_phone = Label(window_supplier_ad,text="Phone number")
    label_supplier_phone.place(x=20, y=110, width=100, height=30)

    entry_supplier_phone = Entry(window_supplier_ad)
    entry_supplier_phone.place(x=20, y=140, width=350, height=30)

    lable_supplier_address = Label(window_supplier_ad, text="Address")
    lable_supplier_address.place(x=20, y=170, width=50, height=30)

    entr_supplier_address = Entry(window_supplier_ad)
    entr_supplier_address.place(x=20, y=200, width=350, height=30)


    # cal = Calendar(window_supplier_ad, selectmode='day', year=2020, month=5, day=22)
    #
    # def toggle_calendar():
    #     if cal.winfo_ismapped():
    #         cal.place_forget()
    #     else:
    #         cal.place(x=20, y=370)
    #
    # dob = Button(window_supplier_ad, text="Date of birth", command=toggle_calendar)
    # dob.place(x=120, y=320, width=100, height=30)
    #
    # cal = Calendar(window_supplier_ad, selectmode='day', year=2020, month=5, day=22)
    #
    # def on_date_select(event):
    #     selected_date = cal.get_date()
    #     dob.config(text=selected_date)
    #     cal.place_forget()
    #
    # # Bind the function to the calendar's date selection event
    # cal.bind("<<CalendarSelected>>", on_date_select)

    add_supplier_button = Button(window_supplier_ad, text="Save", command=add_supplier_action)
    add_supplier_button.place(x=140, y=350, width=100, height=30)
    window_supplier_ad.mainloop()
def detail_supplier(cursor,id):
    cursor.execute("Select * from Supplier where id = %s",(id,))
    row = cursor.fetchone()
    if row :
        name = row[1]
        phone = row[2]
        address = row[3]
        return name, phone, address
    else:
        return None
def create_supplier_update_form(cursor, tree, id_emp, db,id_user):
    from ServicePetManager.main import Supplier
    day_update = datetime.now().strftime('%Y-%m-%d')
    def update_supplier_action():
        name = entr_supplier_name.get().strip()
        phone = entry_supplier_phone.get().strip()
        address = entry_supplier_address.get().strip()
        modify_by = id_user

        supplier = Supplier(name, phone, address, None, modify_by, day_update)
        update_supplier(cursor, supplier, tree, window_supplier_ad, db,id_emp)

    window_supplier_ad = Tk()
    window_supplier_ad.geometry("400x600")
    window_supplier_ad.title("Add Supplier")
    screen_width = window_supplier_ad.winfo_screenwidth()
    screen_height = window_supplier_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_supplier_ad.geometry(f"400x600+{position_x}+{position_y}")

    lable_supplier_name = Label(window_supplier_ad, text="Name")
    lable_supplier_name.place(x=20, y=50, width=50, height=30)

    entr_supplier_name = Entry(window_supplier_ad)
    entr_supplier_name.place(x=20, y=80, width=350, height=30)

    label_supplier_phone = Label(window_supplier_ad, text="Phone number")
    label_supplier_phone.place(x=20, y=110, width=100, height=30)

    entry_supplier_phone = Entry(window_supplier_ad)
    entry_supplier_phone.place(x=20, y=140, width=350, height=30)

    lable_supplier_address = Label(window_supplier_ad, text="Address")
    lable_supplier_address.place(x=20, y=170, width=50, height=30)

    entry_supplier_address = Entry(window_supplier_ad)
    entry_supplier_address.place(x=20, y=200, width=350, height=30)

    add_supplier_button = Button(window_supplier_ad, text="Save", command=update_supplier_action)
    add_supplier_button.place(x=140, y=350, width=100, height=30)

    name,phone,address =  detail_supplier(cursor,id_emp)
    entr_supplier_name.insert(0,name)
    entry_supplier_phone.insert(0,phone)
    entry_supplier_address.insert(0, address)

    window_supplier_ad.mainloop()

def delete_supplier(cursor,id_supplier,tree,db):
    ask = messagebox.askyesno("Confirm delete","Do you want to delete this supplier ?")
    if ask:
        cursor.execute("Delete from supplier where id = %s",(id_supplier,))
        db.commit()
        refresh_treeview(tree,cursor)
        messagebox.showinfo("Delete alert","Delete successfully !")
    else:
        return


def create_supplier_manager_form(cursor,db,id_user):
    global selected_id

    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]
        print(selected_id)

    def hide_window():
        window_supplier_mg.withdraw()

    window_supplier_mg = Tk()
    window_supplier_mg.geometry("850x600")
    window_supplier_mg.title("Supplier Manager")
    # Close the program when clicking the close button
    window_supplier_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_supplier_mg.winfo_screenwidth()
    screen_height = window_supplier_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_supplier_mg.geometry(f"850x600+{position_x}+{position_y}")

    # Heading
    heading_supplier_mg = Label(window_supplier_mg,text="SUPPLIER MANAGEMENT",font=("Helvetica", 20, "bold"), fg="green")
    heading_supplier_mg.place(x=200, y=30, width=400, height=30)

    # Search
    entr_search = Entry(window_supplier_mg)
    entr_search.place(x=400, y=80, width=300, height=30)

    button_supplier_manager = Button(window_supplier_mg, text="Search", command=lambda: search_supplier(cursor,entr_search,tree))
    button_supplier_manager.place(x=720, y=80, width=80, height=30)
    # Add, Update, Delete buttons
    button_supplier_manager = Button(window_supplier_mg, text="Add", command=lambda: create_supplier_add_form(cursor,tree,db,id_user))
    button_supplier_manager.place(x=520, y=450, width=80, height=30)

    button_supplier_manager = Button(window_supplier_mg, text="Update", command=lambda: create_supplier_update_form(cursor,tree,selected_id,db,id_user))
    button_supplier_manager.place(x=620, y=450, width=80, height=30)

    button_supplier_manager = Button(window_supplier_mg, text="Delete", command=lambda: delete_supplier(cursor,selected_id,tree,db))
    button_supplier_manager.place(x=720, y=450, width=80, height=30)
    # Tree view
    columns = ("ID","Name", "PhoneNumber", "Address","CreateBy","CreateDate","ModifyBy","ModifyDate")
    tree = ttk.Treeview(window_supplier_mg, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("PhoneNumber", text="Phone number")
    tree.heading("Address", text="Address")
    tree.heading("CreateBy", text="CreateBy")
    tree.heading("CreateDate", text="CreateDate")
    tree.heading("ModifyBy", text="ModifyBy")
    tree.heading("ModifyDate", text="ModifyDate")



    total_width = 800  # Total width of the Treeview
    column_width = total_width // len(columns)  # Calculate width for each column
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)

    tree.place(x=20, y=130, width=800, height=200)
    cursor.execute("SELECT * FROM Supplier")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_supplier_mg.mainloop()
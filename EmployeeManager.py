
from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime

def refresh_treeview(tree,cursor):
    # Clear the current items in the tree
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM Employee")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
def search_employee(cursor,entr_search,tree):
    text = entr_search.get().strip()
    cursor.execute("SELECT * FROM Employee WHERE Name LIKE %s", ('%' + text + '%',))
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("","end",values=row)
def add_employee(cursor,employee,tree,window_employee_ad,db):
    cursor.execute("Insert into Employee (Name,PhoneNumber, Gender,DateOnboard,PasswordHas,Role,CreateDate,CreateBy,ModifyDate,ModifiBy) "
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (employee.name,employee.phone_number,employee.gender,employee.date_onboard,employee.password_hash,employee.role,
                    employee.create_date,employee.create_by,employee.modify_date,employee.modify_by))
    db.commit()
    messagebox.showinfo("Success", "Add successfully")
    window_employee_ad.destroy()
    refresh_treeview(tree,cursor)

def update_employee (cursor,employee,tree,window_employee_ad,db,id_emp):
    cursor.execute(
        "Update Employee set Name = %s,PhoneNumber = %s, Gender = %s,PasswordHas = %s  WHERE Id = %s ",
        (employee.name, employee.phone_number, employee.gender, employee.password_hash,id_emp))
    db.commit()
    messagebox.showinfo("Success", "Update successfully")
    window_employee_ad.destroy()
    refresh_treeview(tree, cursor)

def create_employee_add_form(cursor,tree,db,id_user):
    from ServicePetManager.main import Employee
    def add_employee_action():
        name = entr_employee_name.get().strip()
        phone = entry_employee_phone.get().strip()
        gender = gender_var.get()
        date_onboard = datetime.now().strftime('%Y-%m-%d')
        password = entr_employee_password.get().strip()
        password_repeat = entr_employee_password_repeat.get().strip()
        create_by = id_user
        modify_by = id_user

        if password != password_repeat:
            messagebox.showerror("Warning","Password does not match")
        else:
            employee = Employee(name, phone, gender, date_onboard, password,1,create_by,modify_by)
            add_employee(cursor, employee, tree, window_employee_ad, db)

    window_employee_ad = Tk()
    window_employee_ad.geometry("400x600")
    window_employee_ad.title("Add Product")
    screen_width = window_employee_ad.winfo_screenwidth()
    screen_height = window_employee_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_employee_ad.geometry(f"400x600+{position_x}+{position_y}")

    lable_employee_name = Label(window_employee_ad, text="Name")
    lable_employee_name.place(x=20, y=50, width=50, height=30)

    entr_employee_name = Entry(window_employee_ad)
    entr_employee_name.place(x=20, y=80, width=350, height=30)

    label_employee_phone = Label(window_employee_ad,text="Phone number")
    label_employee_phone.place(x=20, y=110, width=100, height=30)

    entry_employee_phone = Entry(window_employee_ad)
    entry_employee_phone.place(x=20, y=140, width=350, height=30)

    lable_employee_password = Label(window_employee_ad, text="Password")
    lable_employee_password.place(x=20, y=170, width=50, height=30)

    entr_employee_password = Entry(window_employee_ad, show="*")
    entr_employee_password.place(x=20, y=200, width=350, height=30)

    lable_employee_password_repeat = Label(window_employee_ad, text="Repeat password")
    lable_employee_password_repeat.place(x=20, y=240, width=100, height=30)

    entr_employee_password_repeat = Entry(window_employee_ad, show="*")
    entr_employee_password_repeat.place(x=20, y=270, width=350, height=30)

    gender_var = StringVar(window_employee_ad)
    gender_var.set("Nam")  # set the default value

    gender_menu = OptionMenu(window_employee_ad, gender_var, "Nam", "Nữ")
    gender_menu.place(x=20, y=320, width=80, height=30)

    # cal = Calendar(window_employee_ad, selectmode='day', year=2020, month=5, day=22)
    #
    # def toggle_calendar():
    #     if cal.winfo_ismapped():
    #         cal.place_forget()
    #     else:
    #         cal.place(x=20, y=370)
    #
    # dob = Button(window_employee_ad, text="Date of birth", command=toggle_calendar)
    # dob.place(x=120, y=320, width=100, height=30)
    #
    # cal = Calendar(window_employee_ad, selectmode='day', year=2020, month=5, day=22)
    #
    # def on_date_select(event):
    #     selected_date = cal.get_date()
    #     dob.config(text=selected_date)
    #     cal.place_forget()
    #
    # # Bind the function to the calendar's date selection event
    # cal.bind("<<CalendarSelected>>", on_date_select)

    add_employee_button = Button(window_employee_ad, text="Save", command=add_employee_action)
    add_employee_button.place(x=140, y=350, width=100, height=30)
    window_employee_ad.mainloop()
def detail_employee(cursor,id):
    cursor.execute("Select * from Employee where id = %s",(id,))
    row = cursor.fetchone()
    if row :
        name = row[1]
        phone = row[2]
        gender = row[3]
        password = row[5]
        return name, phone, gender, password
    else:
        return None
def create_employee_update_form(cursor, tree, id_emp, db,id_user):
    from ServicePetManager.main import Employee
    def update_employee_action():
        name = entr_employee_name.get().strip()
        phone = entry_employee_phone.get().strip()
        gender = gender_var.get()
        date_onboard = datetime.now().strftime('%Y-%m-%d')
        password = entr_employee_password.get().strip()
        password_repeat = entr_employee_password_repeat.get().strip()
        modify_by = id_user

        if password != password_repeat:
            messagebox.showerror("Warning", "Password does not match")
        else:
            employee = Employee(name, phone, gender, date_onboard, password, 1, None, modify_by)
            update_employee(cursor, employee, tree, window_employee_ad, db,id_emp)

    window_employee_ad = Tk()
    window_employee_ad.geometry("400x600")
    window_employee_ad.title("Add Product")
    screen_width = window_employee_ad.winfo_screenwidth()
    screen_height = window_employee_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_employee_ad.geometry(f"400x600+{position_x}+{position_y}")

    lable_employee_name = Label(window_employee_ad, text="Name")
    lable_employee_name.place(x=20, y=50, width=50, height=30)

    entr_employee_name = Entry(window_employee_ad)
    entr_employee_name.place(x=20, y=80, width=350, height=30)

    label_employee_phone = Label(window_employee_ad, text="Phone number")
    label_employee_phone.place(x=20, y=110, width=100, height=30)

    entry_employee_phone = Entry(window_employee_ad)
    entry_employee_phone.place(x=20, y=140, width=350, height=30)

    lable_employee_password = Label(window_employee_ad, text="Password")
    lable_employee_password.place(x=20, y=170, width=50, height=30)

    entr_employee_password = Entry(window_employee_ad)
    entr_employee_password.place(x=20, y=200, width=350, height=30)

    lable_employee_password_repeat = Label(window_employee_ad, text="Repeat password")
    lable_employee_password_repeat.place(x=20, y=240, width=100, height=30)

    entr_employee_password_repeat = Entry(window_employee_ad)
    entr_employee_password_repeat.place(x=20, y=270, width=350, height=30)

    gender_var = StringVar(window_employee_ad)
    gender_var.set("Nam")  # set the default value

    gender_menu = OptionMenu(window_employee_ad, gender_var, "Nam", "Nữ")
    gender_menu.place(x=20, y=320, width=80, height=30)

    add_employee_button = Button(window_employee_ad, text="Save", command=update_employee_action)
    add_employee_button.place(x=140, y=350, width=100, height=30)

    name,phone,gender,password =  detail_employee(cursor,id_emp)
    entr_employee_name.insert(0,name)
    entry_employee_phone.insert(0,phone)
    gender_var.set(gender)
    entr_employee_password.insert(0, password)
    entr_employee_password_repeat.insert(0,password)
    window_employee_ad.mainloop()

def delete_employee(cursor,id_product,tree,db):
    ask = messagebox.askyesno("Confirm delete","Do you want to delete this employee ?")
    if ask:
        cursor.execute("Delete from employee where id = %s",(id_product,))
        db.commit()
        refresh_treeview(tree,cursor)
        messagebox.showinfo("Delete alert","Delete successfully !")
    else:
        return


def create_employee_manager_form(cursor,db,id_user):
    global selected_id

    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]
        print(selected_id)

    def hide_window():
        window_employee_mg.withdraw()

    window_employee_mg = Tk()
    window_employee_mg.geometry("850x600")
    window_employee_mg.title("Employee Manager")
    # Close the program when clicking the close button
    window_employee_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_employee_mg.winfo_screenwidth()
    screen_height = window_employee_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_employee_mg.geometry(f"850x600+{position_x}+{position_y}")

    # Heading
    heading_employee_mg = Label(window_employee_mg,text="EMPLOYEE MANAGEMENT",font=("Helvetica", 20, "bold"), fg="green")
    heading_employee_mg.place(x=200, y=30, width=400, height=30)

    # Search
    entr_search = Entry(window_employee_mg)
    entr_search.place(x=400, y=80, width=300, height=30)

    button_employee_manager = Button(window_employee_mg, text="Search", command=lambda: search_employee(cursor,entr_search,tree))
    button_employee_manager.place(x=720, y=80, width=80, height=30)

    # Add, Update, Delete buttons
    button_employee_manager = Button(window_employee_mg, text="Add", command=lambda: create_employee_add_form(cursor,tree,db,id_user))
    button_employee_manager.place(x=520, y=450, width=80, height=30)

    button_employee_manager = Button(window_employee_mg, text="Update", command=lambda: create_employee_update_form(cursor,tree,selected_id,db,id_user))
    button_employee_manager.place(x=620, y=450, width=80, height=30)

    button_employee_manager = Button(window_employee_mg, text="Delete", command=lambda: delete_employee(cursor,selected_id,tree,db))
    button_employee_manager.place(x=720, y=450, width=80, height=30)
    # Tree view
    columns = ("ID","Name", "PhoneNumber", "Gender", "DateOnboard", "Password","Role","CreateBy","CreateDate","ModifyBy","ModifyDate")
    tree = ttk.Treeview(window_employee_mg, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("PhoneNumber", text="Phone number")
    tree.heading("Gender", text="Gender")
    tree.heading("DateOnboard", text="Date Onboard")
    tree.heading("Password", text="Password")
    tree.heading("Role", text="Role")
    tree.heading("CreateBy", text="CreateBy")
    tree.heading("CreateDate", text="CreateDate")
    tree.heading("ModifyBy", text="ModifyBy")
    tree.heading("ModifyDate", text="ModifyDate")



    total_width = 800  # Total width of the Treeview
    column_width = total_width // len(columns)  # Calculate width for each column
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)

    tree.place(x=20, y=130, width=800, height=200)
    cursor.execute("SELECT * FROM Employee")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_employee_mg.mainloop()
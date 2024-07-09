import sys
from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime, date

from ServicePetManager.BillManager import create_bill_manager_form
from ServicePetManager.CustomerManager import create_customer_manager_form
from ServicePetManager.EmployeeManager import create_employee_manager_form
from ServicePetManager.ProductManager import add_product, refresh_treeview, create_product_add_form, \
    create_product_update_form, delete_product, search_product, create_product_manager_form
from ServicePetManager.ReportManager import create_report_manager_form
from ServicePetManager.ServiceManager import create_service_manager_form
from ServicePetManager.SupplierManager import create_supplier_manager_form

id_user = None

class Service:
    def __init__(self, name, price,description,create_by,modify_by):
        self.name = name
        self.price = price
        self.description = description
        self.create_date = datetime.now().strftime('%Y-%m-%d')
        self.modify_date = datetime.now().strftime('%Y-%m-%d')
        self.create_by = create_by
        self.modify_by = modify_by
        self.status = 1
class Product:
    def __init__(self, name, type,sold, amount, price,supplier,create_by,modify_by):
        self.name = name
        self.type = type
        self.sold = sold
        self.amount = amount
        self.price = price
        self.supplier = supplier
        self.create_date = datetime.now().strftime('%Y-%m-%d')
        self.modify_date = datetime.now().strftime('%Y-%m-%d')
        self.create_by = create_by
        self.modify_by = modify_by

class Employee:
    def __init__(self, name, phone_number, gender, date_onboard, password_hash, role,create_by,modify_by):
        self.name = name
        self.phone_number = phone_number
        self.gender = gender
        self.date_onboard = date_onboard if date_onboard else date.today()
        self.password_hash = password_hash
        self.role = role
        self.create_date = datetime.now().strftime('%Y-%m-%d')
        self.create_by = create_by
        self.modify_date = datetime.now().strftime('%Y-%m-%d')
        self.modify_by = modify_by
        self.status = 1

class Customer:
    def __init__(self, name, phone_number, address,dob,gender,create_by,modify_by,modify_date):
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.dob = dob
        self.gender = gender
        self.create_by = create_by
        self.create_date = datetime.now().strftime('%Y-%m-%d')
        self.modify_by = modify_by
        self.modify_date = modify_date
        self.status = 1
class Supplier:
    def __init__(self, name, phone_number, address, create_by, modify_by, modify_date):
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.create_by = create_by
        self.modify_by = modify_by
        self.create_date = datetime.now().strftime('%Y-%m-%d')
        self.modify_date = modify_date

class Bill:
    def __init__(self, id_customer, id_employee, create_date, total_price, create_by, modify_by, modify_date):

        self.id_customer = id_customer
        self.id_employee = id_employee
        self.create_date = create_date
        self.total_price = total_price
        self.create_by = create_by
        self.modify_by = modify_by
        self.modify_date = modify_date
        self.status = 1

class BillDetails:
    def __init__(self, bill_id, product_id, quantity, price):
        self.bill_id = bill_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.status = 1

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Abc@123456789",
    database="petmanage"
)
cursor = db.cursor()

def snackManager():
    pass

def log_out(window_main):
    confirm = messagebox.askyesno("Log Out", "Do you want to log out?")
    if confirm:
        messagebox.showinfo("Log Out", "Sign out successfully!")
        window_main.destroy()
        create_login_form(cursor)

def get_username():
    cursor.execute("SELECT Name FROM Employee WHERE ID = %s", (id_user,))
    user_name = cursor.fetchone()[0]  # Lấy tên người dùng từ cơ sở dữ liệu
    return user_name
def show_home_page(window_login,cursor):
    window_login.withdraw()
    window_main = Tk()
    window_main.geometry("1100x600")
    window_main.title("Home")
    window_main.configure(bg='white')
    def on_closing():
        window_main.destroy()
        sys.exit()
    # Set the protocol to call the on_closing function
    window_main.protocol("WM_DELETE_WINDOW", on_closing)
    def update_time():
        current_time = datetime.now().strftime('%H:%M:%S')  # Định dạng thời gian thành HH:MM:SS
        text_time.config(text="Time: " + current_time)
        window_main.after(1000, update_time)  # Cập nhật mỗi giây (1000 mili giây)

    text_time = Label(window_main, text="Time: ")
    text_time.place(x=30, y=10, width=100, height=30)
    text_time.configure(bg='white')
    update_time()

    user_name = get_username()
    text_user = Label(window_main, text="Hello: " + user_name)
    text_user.configure(bg='white')
    text_user.place(x=760, y=10, width=300, height=30)
    # button_service_manager = Button(window_main, text="Quản lý dịch vụ",command=lambda: create_service_manager_form(cursor, db, id_user))
    # button_service_manager.place(x=30, y=50, width=200, height=30)

    button_product_manager = Button(window_main, text="Product Manager", fg='white', command=lambda: create_product_manager_form(cursor,db,id_user))
    button_product_manager.place(x=30, y=50, width=200, height=50)
    button_product_manager.configure(bg='#758694')

    button_employee_manager = Button(window_main, text="Employee Manager", fg='white', command=lambda: create_employee_manager_form(cursor,db,id_user))
    button_employee_manager.place(x=30, y=110, width=200, height=50)
    button_employee_manager.configure(bg='#758694')

    button_supplier_manager = Button(window_main, text="Supplier Management", fg='white',command=lambda: create_supplier_manager_form(cursor, db, id_user))
    button_supplier_manager.place(x=30, y=170, width=200, height=50)
    button_supplier_manager.configure(bg='#758694')

    button_report_manager = Button(window_main, text="Report Management", fg='white', command=lambda:create_report_manager_form(cursor))
    button_report_manager.place(x=30, y=230, width=200, height=50)
    button_report_manager.configure(bg='#758694')

    button_bill_manager = Button(window_main, text="Bill management", fg='white', command=lambda:create_bill_manager_form(cursor,db,id_user))
    button_bill_manager.place(x=30, y=290, width=200, height=50)
    button_bill_manager.configure(bg='#758694')

    button_customer_manager = Button(window_main, text="Customer Manager", fg='white', command=lambda:create_customer_manager_form(cursor,db,id_user))
    button_customer_manager.place(x=30, y=350, width=200, height=50)
    button_customer_manager.configure(bg='#758694')

    button_log_out = Button(window_main, text="Log Out", fg='white', command=lambda: log_out(window_main))
    button_log_out.place(x=30, y=410, width=200, height=50)
    button_log_out.configure(bg='#758694')

    canvas = Canvas(window_main)
    img_home = PhotoImage(master = canvas,file="logo2.png")
    label_img_home = Label(window_main, image=img_home)
    label_img_home.place(x=250, y=50, width=800, height=445)

    window_main.mainloop()
# Login
def login(cursor, window_login, entr_login_name, entr_login_pass):
    global id_user
    phone_number = entr_login_name.get()
    password = entr_login_pass.get()
    # Execute a query to check login credentials
    cursor.execute("SELECT * FROM Employee WHERE PhoneNumber = %s AND PasswordHas = %s AND Status = 1 LIMIT 1", (phone_number, password))
    row = cursor.fetchone()
    if row:
        id_user = row[0]
        show_home_page(window_login,cursor)
    else:
        # If login fails, show an error message
        messagebox.showerror("Login failed", "Incorrect phone number or password")
# Sign In
def sign_up(cursor,entr_sign_up_name, entr_sign_up_phone, gender_var,entr_sign_up_pass,entry_sign_up_pass_repet):
    name = entr_sign_up_name.get()
    phone_number = entr_sign_up_phone.get()
    gender = gender_var.get()

    password = entr_sign_up_pass.get()
    password_repeat = entry_sign_up_pass_repet.get()
    date_onboard = datetime.now().strftime('%Y-%m-%d')
    if password != password_repeat:
        messagebox.showwarning("","Password incorrect")

    cursor.execute("SELECT * FROM Employee WHERE PhoneNumber = %s", (phone_number,))
    existing_employee = cursor.fetchone()

    if existing_employee:
        messagebox.showwarning("", "Phone number already exists")
        return
    else:
        cursor.execute("Insert into Employee (Name,PhoneNumber,Gender,DateOnboard,PasswordHas,Role, Status) values "
                       "(%s,%s,%s,%s,%s,%s, %s)", (name, phone_number, gender, date_onboard, password, 1, 1))
        messagebox.showinfo("","Sign Up successfully !")
    db.commit()
def create_login_form(cursor,current_window=None):
    if current_window:
        current_window.withdraw()
    window_login = Tk()
    window_login.geometry("800x400")
    window_login.title("Login")
    window_login.configure(bg='white')

    canvas = Canvas(window_login)
    img_home = PhotoImage(master=canvas, file="logo-png-01.png")
    label_img_home = Label(window_login, image=img_home)
    label_img_home.place(x=390, y=30, width=224, height=224)
    # Close the program when clicking the close button
    window_login.protocol("WM_DELETE_WINDOW", window_login.quit)
    # Get the screen width and height
    screen_width = window_login.winfo_screenwidth()
    screen_height = window_login.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_login.geometry(f"650x400+{position_x}+{position_y}")

    lable_login = Label(window_login, text="Sign In",font=("Helvetica", 20, "bold"), fg="green")
    lable_login.place(x=100, y=50, width=200, height=30)
    lable_login.configure(bg='white')

    lable_login_name = Label(window_login, text="Phone Number")
    lable_login_name.place(x=50, y=100, width=100, height=30)
    lable_login_name.configure(bg='white')

    entr_login_name = Entry(window_login)
    entr_login_name.place(x=50, y=140, width=300, height=30)
    entr_login_name.configure(bg='#F6F5F5')

    lable_login_pass = Label(window_login, text="PassWord ")
    lable_login_pass.place(x=50, y=180, width=70, height=30)
    lable_login_pass.configure(bg='white')

    entr_login_pass = Entry(window_login, show="*")
    entr_login_pass.place(x=50, y=220, width=300, height=30)
    entr_login_pass.configure(bg='#F6F5F5')

    button_login = Button(window_login, text="Sign In", command=lambda: login(cursor, window_login, entr_login_name, entr_login_pass),
                    bg="green", fg="white")
    button_login.place(x=220, y=280, width=100, height=30)

    button_sign_in = Button(window_login, text="Register", command=lambda: create_sign_up_form(cursor, window_login),
                    bg="green", fg="white")
    button_sign_in.place(x=80, y=280, width=100, height=30)
    window_login.mainloop()

def create_sign_up_form(cursor,current_window=None):
    if current_window:
        current_window.withdraw()
    window_sign_up = Tk()
    window_sign_up.geometry("400x600")
    window_sign_up.title("Sign In")
    window_sign_up.configure(bg='white')

    canvas = Canvas(window_sign_up)
    img_home = PhotoImage(master=canvas, file="logo-png-01.png")
    label_img_home = Label(window_sign_up, image=img_home)
    label_img_home.place(x=390, y=100, width=224, height=224)
    # Close the program when clicking the close button
    window_sign_up.protocol("WM_DELETE_WINDOW", window_sign_up.quit)
    # Get the screen width and height
    screen_width = window_sign_up.winfo_screenwidth()
    screen_height = window_sign_up.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_sign_up.geometry(f"650x600+{position_x}+{position_y}")

    lable_login = Label(window_sign_up, text="REGISTER",font=("Helvetica", 20, "bold"), fg="green")
    lable_login.place(x=100, y=50, width=200, height=30)
    lable_login.configure(bg='white')

    lable_sign_up_name = Label(window_sign_up, text="Full name")
    lable_sign_up_name.place(x=50, y=100, width=80, height=30)
    lable_sign_up_name.configure(bg='white')

    entr_sign_up_name = Entry(window_sign_up)
    entr_sign_up_name.place(x=50, y=140, width=300, height=30)
    entr_sign_up_name.configure(bg='#F6F5F5')

    lable_sign_up_phone = Label(window_sign_up, text="Phone Number")
    lable_sign_up_phone.place(x=50, y=180, width=105, height=30)
    lable_sign_up_phone.configure(bg='white')

    entr_sign_up_phone = Entry(window_sign_up)
    entr_sign_up_phone.place(x=50, y=220, width=200, height=30)
    entr_sign_up_phone.configure(bg='#F6F5F5')

    gender_var = StringVar(window_sign_up)
    gender_var.set("Male")  # set the default value

    gender_menu = OptionMenu(window_sign_up, gender_var, "Male", "FeMale")
    gender_menu.place(x=280, y=220, width=80, height=30)
    gender_menu.configure(bg='#F6F5F5')

    lable_sign_up_pass = Label(window_sign_up, text="Password ")
    lable_sign_up_pass.place(x=50, y=260, width=80, height=30)
    lable_sign_up_pass.configure(bg='white')

    entr_sign_up_pass = Entry(window_sign_up, show="*")
    entr_sign_up_pass.place(x=50, y=300, width=300, height=30)
    entr_sign_up_pass.configure(bg='#F6F5F5')

    lable_sign_up_pass_repet = Label(window_sign_up, text="Confirm Pasword ")
    lable_sign_up_pass_repet.place(x=50, y=340, width=120, height=30)
    lable_sign_up_pass_repet.configure(bg='white')

    entry_sign_up_pass_repet = Entry(window_sign_up, show="*")
    entry_sign_up_pass_repet.place(x=50, y=380, width=300, height=30)
    entry_sign_up_pass_repet.configure(bg='#F6F5F5')

    button_login = Button(window_sign_up, text="Sign In", command=lambda: create_login_form(cursor,window_sign_up),
                    bg="green", fg="white")
    button_login.place(x=220, y=440, width=100, height=30)

    button_sign_un = Button(window_sign_up, text="Register", command=lambda:
    sign_up(cursor,entr_sign_up_name, entr_sign_up_phone, gender_var,entr_sign_up_pass,entry_sign_up_pass_repet),
                    bg="green", fg="white")
    button_sign_un.place(x=80, y=440, width=100, height=30)
    window_sign_up.mainloop()

if __name__ == "__main__":
    try:
        mycursor = db.cursor()
        print(id_user)
        create_login_form(mycursor)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'db' in locals():
            db.close()
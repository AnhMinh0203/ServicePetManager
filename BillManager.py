from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime
from tkcalendar import Calendar
chosing_type = None
def get_name_type(cursor,id):
    cursor.execute("Select name from Type where id = %s",(id,))
    row = cursor.fetchone()
    return row[0]

def get_name_supplier(cursor,id):
    cursor.execute("Select name from Supplier where id = %s",(id,))
    row = cursor.fetchone()
    return row[0]
def detail_bill(cursor,id):
    cursor.execute("Select * from Bill where id = %s",(id,))
    row = cursor.fetchone()
    if row :
        name = row[1]
        type = get_name_type(cursor,row[2])
        supplier = get_name_supplier(cursor,row[3])
        sold = row[4]
        inventory = row[5]
        price = row[6]

        return name, type, supplier,sold,inventory, price
    else:
        return None
def refresh_treeview_type(tree,cursor,status=None):
    for item in tree.get_children():
        tree.delete(item)

    if status == "Manager Type":
        cursor.execute("Select ID, Name from Type")
    else:
        cursor.execute("Select * from Type")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def refresh_treeview_bill(tree,cursor):
    for item in tree.get_children():
        tree.delete(item)
    cursor.callproc("getAllBills")
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
def refresh_treeview(tree,cursor):
    # Clear the current items in the tree
    for item in tree.get_children():
        tree.delete(item)

    # Load new data from the database
    cursor.execute(
        "SELECT p.Id, p.Name, t.Name AS TypeName, s.Name AS SupplierName, p.Sold, p.Inventory, p.Price, "
        "p.CreateBy, p.CreateDate, p.ModifiBy, p.ModifyDate "
        "FROM Bill p "
        "INNER JOIN Type t ON p.IdType = t.Id "
        "INNER JOIN Supplier s ON p.IdSupplier = s.Id"
    )
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def add_bill(cursor, bill, tree, window_bill_ad, db):
    cursor.execute("Insert into Bill (Name,IdType,IdSupplier, Sold,Inventory,Price,CreateBy,CreateDate,ModifiBy,ModifyDate) "
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (bill.name, bill.type,bill.supplier, bill.sold, bill.amount, bill.price, bill.create_by, bill.create_date,bill.modify_by,bill.create_date))
    db.commit()
    messagebox.showinfo("Thành công", "Thêm hóa đơn thành công")
    window_bill_ad.destroy()
    refresh_treeview(tree, cursor)
def update_bill(cursor,bill,tree,window_bill_ad,id,db):
    name = bill.name
    IdType = bill.type
    IdSupplier = bill.supplier
    sold = bill.sold
    amount = bill.amount
    price = bill.price
    modify_by = bill.modify_by
    modify_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
            UPDATE Bill
            SET Name = %s,
                IdType = %s,
                IdSupplier = %s,
                Sold = %s,
                Inventory = %s,
                Price = %s,
                ModifiBy = %s,
                ModifyDate = %s
            WHERE Id = %s
        """, (name, IdType,IdSupplier, sold, amount, price, modify_by, modify_date, id))
    db.commit()
    messagebox.showinfo("Thành công", "Thêm hóa đơn thành công")
    window_bill_ad.destroy()
    refresh_treeview(tree,cursor)

def search_bill(cursor,entr_search,tree):
    text = entr_search.get().strip()
    if not text == "":
        cursor.execute("SELECT * from Bill WHERE ID = %s", (text,))
    else:
        cursor.execute("SELECT * from Bill")
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("","end",values=row)

def Search(cursor, entr_search, tree):
    text = entr_search.get().strip()
    for item in tree.get_children():
        tree.delete(item)

    if not text == "":
        cursor.execute("""SELECT b.Id, c.Name , e.Name , b.TotalPrice, b.CreateDate FROM Bill b
        INNER JOIN Customers c ON b.IdCustomer = c.Id 
        INNER JOIN Employee e ON b.IdEmployee = e.Id WHERE c.name LIKE %s or e.name LIKE %s""",
                       ('%' + text + '%', '%' + text + '%'))
    else:
        cursor.execute("""SELECT b.Id, c.Name , e.Name , b.TotalPrice, b.CreateDate FROM Bill b
        INNER JOIN Customers c ON b.IdCustomer = c.Id 
        INNER JOIN Employee e ON b.IdEmployee = e.Id""")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def create_bill_add_form(cursor,id_user,db,tree_manager):
    global onchange_id_proc, selected_phone_customer, total_price, price_for_each_item, products, onchange_id_servic, price_for_each_service, services
    onchange_id_proc = None
    total_price = 0
    price_for_each_item = 0
    products = []
    services = []
    onchange_id_servic = None
    price_for_each_service = 0

    def get_employee(cursor):
        cursor.execute("SELECT Name FROM employee")
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def get_employee_id(employee_var):
        name = employee_var.get()
        cursor.execute("SELECT id FROM employee where name = %s",(name,))
        row = cursor.fetchone()
        return row[0]

    def update_option_menu(cursor, option_menu, variable):
        values = get_employee(cursor)
        menu = option_menu['menu']
        menu.delete(0, 'end')
        for item in values:
            menu.add_command(label=item, command=lambda value=item: variable.set(value))
        if values:
            variable.set(values[0])

    def add_customer_to_bill():
        name = entry_name_cus.get().strip()
        phone = entry_phone_cus.get().strip()
        address = entry_address_cus.get().strip()
        dateOfBirth = dob.cget("text")
        gender = gender_var.get()
        create_by = id_user
        create_date = datetime.today().strftime('%Y-%m-%d')
        modify_by = id_user
        modify_date = datetime.today().strftime('%Y-%m-%d')

        cursor.execute("SELECT COUNT(*) FROM Customers WHERE PhoneNumber = %s", (phone,))
        phone_count = cursor.fetchone()[0]

        if phone_count > 0:
            messagebox.showerror("Lỗi", f"Số điện thoại đã tồn tại.")
            return

        args = [name,phone,address,dateOfBirth,gender,create_by,create_date,modify_by,modify_date]
        cursor.callproc("addCustomer",args)
        for result in cursor.stored_results():
            result.fetchone()
        db.commit()
        messagebox.showinfo("","Thêm khách hàng thành công!")

    def add_product_to_bill():
        global onchange_id_proc, total_price, price_for_each_item
        quantity_text = entr_quantity.get().strip()
        if not quantity_text:
            messagebox.showwarning("Cảnh báo","Số lượng không được để trống !")
            return
        quantity = int(quantity_text)
        total_price += (float(price_for_each_item) * quantity)
        products.append((onchange_id_proc,quantity,float(price_for_each_item) * quantity))
        messagebox.showinfo("","Thêm sản phẩm thành công")

    def add_service_to_bill():
        global  onchange_id_servic, price_for_each_service, total_price
        service_to_add = (onchange_id_servic, float(price_for_each_service))

        # Check if the service already exists in the list
        if service_to_add not in services:
            services.append(service_to_add)
            total_price += (float(price_for_each_service))
            messagebox.showinfo("", "Thêm dịch vụ thành công")
        else:
            messagebox.showinfo("", "Dịch vụ đã tồn tại")

    def getCustomer ():
        phone_number = entry_search_cus.get().strip()
        cursor.callproc("getCustomerByPhone",[phone_number])

        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                entry_name_cus.delete(0, END)
                entry_name_cus.insert(0, row[1])
                entry_phone_cus.delete(0, END)
                entry_phone_cus.insert(0, row[2])
                entry_address_cus.delete(0, END)
                entry_address_cus.insert(0, row[3])
                dob_str = row[4]
                dob.config(text=dob_str)
                gender_var.set(row[5])
            else:
                messagebox.showwarning("Cảnh báo", "Khách hàng không tồn tại")

    def save_bill():
        global total_price
        create_date = datetime.today().strftime('%Y-%m-%d')
        in_emp = get_employee_id(employee_var)
        phone_cus = entry_phone_cus.get().strip()
        try:
            # Retrieve customer ID
            cursor.execute("SELECT id FROM customers WHERE PhoneNumber = %s LIMIT 1", (phone_cus,))
            id_cus = cursor.fetchone()
            if id_cus:
                id_cus = id_cus[0]
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy khách hàng")
                return

            # Insert into Bill table
            cursor.execute(
                "INSERT INTO Bill(IdCustomer, IdEmployee, CreateDate, TotalPrice, Status) VALUES (%s, %s, %s, %s, 1)",
                (id_cus, in_emp, create_date, total_price))
            id_bill = cursor.lastrowid  # Get the last inserted ID

            # Add products to the bill
            for item in products:
                cursor.callproc("addBillDetail", (id_bill, item[0], item[1], item[2]))

            # Add services to the bill
            for service in services:
                cursor.callproc("addBillService", (id_bill, service[0], service[1]))

            # Commit transaction
            db.commit()

            # Show success message
            messagebox.showinfo("", "Thêm hóa đơn thành công")
            #  sao ko về được bước gọi store
            # Clear products and services lists
            products.clear()
            services.clear()

            # Refresh treeview (assuming tree_manager is your treeview widget)
            refresh_treeview_bill(tree_manager, cursor)

        except Exception as e:
            db.rollback()
            messagebox.showerror("Lỗi", f"Lỗi lưu hóa đơn: {str(e)}")
    #       còn cái này bây giơ


    def hide_window(form):
        form.withdraw()

    def on_tree_product_select(event):
        global onchange_id_proc
        global price_for_each_item
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            product_id = int(item['values'][0])  # Assuming the ID is the first column
            price_for_each_item = item['values'][5]
            onchange_id_proc = product_id
            # print(f"Selected Product ID: {product_id}")
            # print(f"Quantity: {price_for_each_item}")

    def on_treeService_product_select(event):
        global onchange_id_servic
        global price_for_each_service
        selected_item = treeService.selection()
        if selected_item:
            item = treeService.item(selected_item)
            product_id = int(item['values'][0])  # Assuming the ID is the first column
            price_for_each_service = item['values'][2]
            onchange_id_servic = product_id
            # print(f"Selected Product ID: {product_id}")
            # print(f"Quantity: {price_for_each_item}")

    window_bill_add = Tk()
    window_bill_add.geometry("700x600")
    window_bill_add.title("Add bill")
    window_bill_add.protocol("WM_DELETE_WINDOW", lambda: hide_window(window_bill_add))
    screen_width = window_bill_add.winfo_screenwidth()
    screen_height = window_bill_add.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_bill_add.geometry(f"700x600+{position_x}+{position_y}")

    # --- Up ---
    # Search
    entry_search_cus = Entry(window_bill_add)
    entry_search_cus.place(x=20, y=20, width=330, height=30)

    button_search_cus = Button(window_bill_add,text="Tìm kiếm",command=getCustomer)
    button_search_cus.place(x=360, y=20, width=100, height=30)
    # Name
    label_name_cus = Label(window_bill_add,text="Tên khách hàng")
    label_name_cus.place(x=20,y=60,width=100, height=30)
    entry_name_cus = Entry(window_bill_add)
    entry_name_cus.place(x=20,y=100,width=200, height=30)
    # Phone
    label_phone_cus = Label(window_bill_add, text="Số điện thoại")
    label_phone_cus.place(x=270, y=60, width=100, height=30)
    entry_phone_cus = Entry(window_bill_add)
    entry_phone_cus.place(x=270, y=100, width=200, height=30)

    # Address
    label_address_cus = Label(window_bill_add, text="Địa chỉ")
    label_address_cus.place(x=20, y=140, width=100, height=30)
    entry_address_cus = Entry(window_bill_add)
    entry_address_cus.place(x=20, y=180, width=450, height=30)

    # Gender
    gender_var = StringVar(window_bill_add)
    gender_var.set("Nam")  # set the default value

    gender_menu = OptionMenu(window_bill_add, gender_var, "Nam", "Nữ")
    gender_menu.place(x=20, y=220, width=100, height=30)
    # Dob
    cal = Calendar(window_bill_add, selectmode='day', year=2020, month=5, day=22)

    #Employeee
    label_Emplo = Label(window_bill_add,text="Chọn nhân viên: ")
    label_Emplo.place(x=20, y=260, width=100, height=30)

    employee_var = StringVar(window_bill_add)

    employee_menu = OptionMenu(window_bill_add, employee_var, [])
    employee_menu.place(x=130, y=260, width=100, height=30)

    update_option_menu(cursor, employee_menu, employee_var)

    def toggle_calendar():
        if cal.winfo_ismapped():
            cal.place_forget()
        else:
            cal.place(x=270, y=260)
            cal.tkraise()

    dob = Button(window_bill_add, text="Ngày sinh", command=toggle_calendar)
    dob.place(x=270, y=220, width=80, height=30)

    cal = Calendar(window_bill_add, selectmode='day', year=2020, month=5, day=22)

    def on_date_select(event):
        selected_date = cal.get_date()
        date_obj = datetime.strptime(selected_date, '%m/%d/%y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        dob.config(text=formatted_date)
        cal.place_forget()
    cal.bind("<<CalendarSelected>>", on_date_select)

    # Add customer
    button_add_customer = Button(window_bill_add, text="Thêm khách hàng", command=add_customer_to_bill)
    button_add_customer.place(x=530, y=100, width=100, height=30)


    # ---- Down -------
    columns = ("ID", "Name", "Type", "Supplier", "Inventory", "Price")
    tree = ttk.Treeview(window_bill_add,columns = columns, show="headings")
    total_width = 450
    column_width = total_width // len(columns)

    for col in columns:
        tree.heading(col, text=col)
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)
    tree.place(x=20,y=320,width=450,height=200)
    cursor.callproc("getAllProductToAddBill")
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            tree.insert("","end",values=row)
    tree.bind("<<TreeviewSelect>>", on_tree_product_select)

    label_quantity = Label(window_bill_add, text="Số lượng")
    label_quantity.place(x=530, y=300, width=50, height=30)
    entr_quantity = Entry(window_bill_add)
    entr_quantity.place(x=530, y=340, width=100, height=30)

    button_add_product = Button(window_bill_add, text="Thêm sản phẩm",command=add_product_to_bill)
    button_add_product.place(x=530, y=380, width=100, height=30)

    #Service
    columns = ("ID", "Name", "Price", "Description")
    treeService = ttk.Treeview(window_bill_add, columns=columns, show="headings")
    total_width = 450
    column_width = total_width // len(columns)

    for col in columns:
        treeService.heading(col, text=col)
    for col in columns:
        treeService.column(col, anchor=CENTER, width=column_width)
    treeService.place(x=20, y=550, width=450, height=200)
    cursor.callproc("getAllService")
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            treeService.insert("", "end", values=row)
    treeService.bind("<<TreeviewSelect>>", on_treeService_product_select)

    button_add_product = Button(window_bill_add, text="Thêm dịch vụ", command=add_service_to_bill)
    button_add_product.place(x=530, y=640, width=100, height=30)

    # Add bill
    button_save_bill = Button(window_bill_add, text="Lưu hóa đơn",command=save_bill)
    button_save_bill.place(x=530, y=450, width=100, height=30)
    window_bill_add.mainloop()
def create_bill_detail_form(cursor,id_bill):
    def hide_window():
        window_bill_mg.withdraw()

    window_bill_mg = Tk()
    window_bill_mg.geometry("400x400")
    window_bill_mg.title("Bill Manager")
    # Close the program when clicking the close button
    window_bill_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_bill_mg.winfo_screenwidth()
    screen_height = window_bill_mg.winfo_screenheight()


    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_bill_mg.geometry(f"400x400+{position_x}+{position_y}")

    # Heading
    heading_bill_mg = Label(window_bill_mg, text="Chi tiết hóa đơn", font=("Helvetica", 20, "bold"), fg="green")
    heading_bill_mg.place(x=20, y=30, width=400, height=30)

    # Tree view
    columns = ("ID", "Name", "NameService", "Quantity", "TotalPrice")
    tree = ttk.Treeview(window_bill_mg, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name Product")
    tree.heading("NameService", text="Name Service")
    tree.heading("Quantity", text="Quantity")   
    tree.heading("TotalPrice", text="TotalPrice")

    total_width = 360  # Total width of the Treeview
    column_width = total_width // len(columns)  # Calculate width for each column
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)

    tree.place(x=20, y=130, width=360, height=200)
    cursor.callproc("getAllBillDetail",[id_bill])
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            tree.insert("","end",values=row)

    window_bill_mg.mainloop()

def create_manager_type_form(cursor, db):
    global selected_id
    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]

    def create_add_type_form():
        window_bill_type = Tk()
        window_bill_type.geometry("300x300")
        window_bill_type.title("Add Type")

        def hide_window():
            window_bill_type.withdraw()

        def add_type():
            name_type = entry_bill_type.get().strip()
            cursor.execute("SELECT COUNT(*) FROM Type WHERE name = %s", (name_type,))
            result = cursor.fetchone()

            if result[0] > 0:
                messagebox.showwarning("", "Loại sản phẩm đã tồn tại")
            else:
                cursor.execute("Insert into Type (name) values (%s)",(name_type,))
                messagebox.showinfo("","Thêm thành công")
                db.commit()

                window_bill_type.destroy()
                refresh_treeview_type(tree,cursor,"Manager Type")

        window_bill_type.protocol("WM_DELETE_WINDOW", hide_window)
        # Get the screen width and height
        screen_width = window_bill_type.winfo_screenwidth()
        screen_height = window_bill_type.winfo_screenheight()

        # Calculate position x and y coordinates
        position_x = int((screen_width / 2) - (400 / 2))
        position_y = int((screen_height / 3) - (400 / 2))
        window_bill_type.geometry(f"200x200+{position_x}+{position_y}")

        label_bill_type = Label(window_bill_type, text="Tên loại sản phẩm")
        label_bill_type.place(x=20, y=20, width=80, height=30)

        entry_bill_type = Entry(window_bill_type)
        entry_bill_type.place(x=20, y=50, width=160, height=30)

        button_save_type = Button(window_bill_type,text="Lưu",command=add_type)
        button_save_type.place(x=120, y=80, width=60, height=30)
        refresh_treeview_type(tree, cursor)
        window_bill_type.mainloop()

    def delete_type():
        cursor.execute("SELECT COUNT(*) FROM Bill WHERE IdType = %s", (selected_id,))
        result = cursor.fetchone()

        if result[0] > 0:
            messagebox.showwarning("","Cannot delete this type because it is being used in bills. Please delete or change the type in bills first.")
        else:
            cursor.execute("delete from Type where id =(%s)", (selected_id,))
            db.commit()
            refresh_treeview_type(tree, cursor,"Manager Type")
            messagebox.showinfo("Xóa", "Xóa thành cng !")



    window_bill_type = Tk()
    window_bill_type.geometry("400x400")
    window_bill_type.title("Type Manager")

    def hide_window():
        window_bill_type.withdraw()
    window_bill_type.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_bill_type.winfo_screenwidth()
    screen_height = window_bill_type.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_bill_type.geometry(f"400x400+{position_x}+{position_y}")

    columns = ("ID", "Name")
    tree = ttk.Treeview(window_bill_type, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")

    # Heading
    heading_bill_mg = Label(window_bill_type, text="BILL MANAGEMENT", font=("Helvetica", 20, "bold"), fg="green")
    heading_bill_mg.place(x=20, y=30, width=300, height=30)
    total_width = 360
    column_width = total_width // len(columns)
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)
    tree.place(x=20, y=100, width=360, height=200)
    refresh_treeview_type(tree, cursor)

    button_add_type = Button(window_bill_type,text="Thêm",command=create_add_type_form)
    button_add_type.place(x=320, y=320, width=50, height=30)
    button_delete_type = Button(window_bill_type, text="Xóa", command=delete_type)
    button_delete_type.place(x=240,y=320,width=50, height=30)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_bill_type.mainloop()

def delete_bill(cursor,id_bill,tree,db):
    ask = messagebox.askyesno("Xác nhận xóa","Bạn có muốn xóa hóa đơn này không?")
    if ask:
        cursor.callproc("deleteBill",[id_bill])
        for result in cursor.stored_results():
            result.fetchone()
        db.commit()
        refresh_treeview_bill(tree,cursor)
        messagebox.showinfo("Xóa","Xóa thành công !")
    else:
        return
def create_bill_manager_form(cursor,db,id_user):
    global selected_id
    def on_tree_select(event):
        global selected_id
        selected_item = tree_manager.selection()[0]
        selected_id = tree_manager.item(selected_item, "values")[0]
        print(selected_id)
    def hide_window():
        window_bill_mg.withdraw()
    window_bill_mg = Tk()
    window_bill_mg.geometry("850x600")
    window_bill_mg.title("Bill Manager")
    # Close the program when clicking the close button
    window_bill_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_bill_mg.winfo_screenwidth()
    screen_height = window_bill_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_bill_mg.geometry(f"850x600+{position_x}+{position_y}")

    # Heading
    heading_bill_mg = Label(window_bill_mg,text="BILL MANAGEMENT",font=("Helvetica", 20, "bold"), fg="green")
    heading_bill_mg.place(x=200, y=30, width=400, height=30)

    # Tree view
    columns = ("ID","NameCustomer", "NameEmployee", "TotalPrice","CreateDate")
    tree_manager = ttk.Treeview(window_bill_mg, columns=columns, show="headings")
    tree_manager.heading("ID", text="ID")
    tree_manager.heading("NameCustomer", text="NameCustomer")
    tree_manager.heading("NameEmployee", text="NameEmployee")
    tree_manager.heading("TotalPrice", text="TotalPrice")
    tree_manager.heading("CreateDate", text="CreateDate")
    total_width = 800  # Total width of the Treeview
    column_width = total_width // len(columns)  # Calculate width for each column
    for col in columns:
        tree_manager.column(col, anchor=CENTER, width=column_width)

    tree_manager.place(x=20, y=130, width=800, height=200)
    cursor.execute(
        "SELECT b.Id, c.Name , e.Name , b.TotalPrice, b.CreateDate "
        "FROM Bill b "
        "INNER JOIN Customers c ON b.IdCustomer = c.Id "
        "INNER JOIN Employee e ON b.IdEmployee = e.Id"
    )
    # Search
    entr_search = Entry(window_bill_mg)
    entr_search.place(x=400, y=80, width=300, height=30)

    button_bill_manager = Button(window_bill_mg, text="Tìm kiếm", command=lambda: Search(cursor, entr_search, tree_manager))
    button_bill_manager.place(x=720, y=80, width=80, height=30)

    button_bill_manager = Button(window_bill_mg, text="Thêm",
                                 command=lambda: create_bill_add_form(cursor, id_user, db, tree_manager))
    button_bill_manager.place(x=520, y=450, width=80, height=30)

    button_bill_manager = Button(window_bill_mg, text="Chi tiết",
                                 command=lambda: create_bill_detail_form(cursor, selected_id))
    button_bill_manager.place(x=620, y=450, width=80, height=30)

    button_bill_manager = Button(window_bill_mg, text="Xóa",
                                 command=lambda: delete_bill(cursor, selected_id, tree_manager, db))
    button_bill_manager.place(x=720, y=450, width=80, height=30)

    rows = cursor.fetchall()
    for row in rows:
        tree_manager.insert("", "end", values=row)

    tree_manager.bind("<<TreeviewSelect>>", on_tree_select)
    window_bill_mg.mainloop()
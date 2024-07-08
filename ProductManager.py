from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime

chosing_type = None
def get_name_type(cursor,id):
    cursor.execute("Select name from Type where id = %s",(id,))
    row = cursor.fetchone()
    return row[0]

def get_name_supplier(cursor,id):
    cursor.execute("Select name from Supplier where id = %s",(id,))
    row = cursor.fetchone()
    return row[0]
def detail_product(cursor,id):
    cursor.execute("Select * from Product where id = %s",(id,))
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
def refresh_treeview(tree,cursor):
    # Clear the current items in the tree
    for item in tree.get_children():
        tree.delete(item)

    # Load new data from the database
    cursor.callproc('getAllProducts')
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

def add_product(cursor, product, tree, window_product_ad, db):
    cursor.execute("Insert into Product (Name,IdType,IdSupplier, Sold,Inventory,Price,CreateBy,CreateDate,ModifiBy,ModifyDate) "
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (product.name, product.type,product.supplier, product.sold, product.amount, product.price, product.create_by, product.create_date,product.modify_by,product.create_date))
    db.commit()
    messagebox.showinfo("Success", "Product added successfully")
    window_product_ad.destroy()
    refresh_treeview(tree, cursor)
def create_product_add_form(cursor,tree,db,id_user):
    from main import Product

    def get_supplier_id(select_supplier):
        name = select_supplier.get()
        cursor.execute("SELECT id FROM supplier where name = %s",(name,))
        row = cursor.fetchone()
        return row[0]

    def get_type_id(select_type):
        name = select_type.get()
        cursor.execute("SELECT id FROM type where name = %s",(name,))
        row = cursor.fetchone()
        return row[0]

    def add_product_action():
        name = entr_product_name.get().strip()
        type = get_type_id(select_type)
        amount = int(entry_product_amount.get().strip())
        price = float(entry_product_price.get().strip())
        supplier = get_supplier_id(select_supplier)
        create_by = id_user
        modify_by = id_user
        product = Product(name, type, 0,amount, price,supplier,create_by,modify_by)

        add_product(cursor, product, tree, window_product_ad, db)

    def get_types(cursor):
        cursor.execute("SELECT Name FROM Type")
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def get_suppliers(cursor):
        cursor.execute("SELECT * FROM Supplier")
        rows = cursor.fetchall()
        return [row[1] for row in rows]

    def update_option_menu(cursor, option_menu, variable,status):
        if status == "Type":
            values = get_types(cursor)
        else:
            values = get_suppliers(cursor)
        menu = option_menu['menu']
        menu.delete(0, 'end')
        for item in values:
            menu.add_command(label=item, command=lambda value=item: variable.set(value))
        if values:
            variable.set(values[0])

    window_product_ad = Tk()
    window_product_ad.geometry("200x400")
    window_product_ad.title("Add Product")
    screen_width = window_product_ad.winfo_screenwidth()
    screen_height = window_product_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_product_ad.geometry(f"300x400+{position_x}+{position_y}")

    lable_product_name = Label(window_product_ad, text="Name")
    lable_product_name.place(x=20, y=50, width=80, height=30)

    entr_product_name = Entry(window_product_ad)
    entr_product_name.place(x=100, y=50, width=150, height=30)

    label_product_type = Label(window_product_ad,text="Type")
    label_product_type.place(x=20, y =100, width=70,height=30)

    select_type = StringVar(window_product_ad)
    option_menu_type = OptionMenu(window_product_ad, select_type, [])
    option_menu_type.place(x=100, y=100, width=80, height=30)

    update_option_menu(cursor, option_menu_type, select_type,"Type")

    label_product_amount = Label(window_product_ad,text="Amount")
    label_product_amount.place(x=20,y=150,width=50, height=30)

    entry_product_amount = Entry(window_product_ad)
    entry_product_amount.place(x=100, y=150,width=100, height=30)

    label_product_price = Label(window_product_ad,text="Price")
    label_product_price.place(x=20,y=200,width=80,height=30)

    entry_product_price = Entry(window_product_ad)
    entry_product_price.place(x=100, y=200,width=100, height=30)

    label_product_type = Label(window_product_ad, text="Supplier")
    label_product_type.place(x=20, y=250, width=70, height=30)

    select_supplier = StringVar(window_product_ad)
    option_menu_suplier = OptionMenu(window_product_ad, select_supplier, [])
    option_menu_suplier.place(x=100, y=250, width=80, height=30)

    update_option_menu(cursor, option_menu_suplier, select_supplier,"Supplier")

    button_product_add = Button(window_product_ad,text="Add",command=lambda:add_product_action())
    button_product_add.place(x=150, y=300,width=100, height=30)
    window_product_ad.mainloop()

def update_product(cursor,product,tree,window_product_ad,id,db):
    name = product.name
    IdType = product.type
    IdSupplier = product.supplier
    sold = product.sold
    amount = product.amount
    price = product.price
    modify_by = product.modify_by
    modify_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
            UPDATE Product
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
    messagebox.showinfo("Success", "Product added successfully")
    window_product_ad.destroy()
    refresh_treeview(tree,cursor)

def create_product_update_form(cursor,tree,id_product,db,id_user):
    from main import Product


    def get_types(cursor):
        cursor.execute("SELECT Name FROM Type")
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def get_supplier_id(select_supplier):
        name = select_supplier.get()
        cursor.execute("SELECT id FROM supplier where name = %s",(name,))
        row = cursor.fetchone()
        return row[0]

    def get_type_id(select_type):
        name = select_type.get()
        cursor.execute("SELECT id FROM type where name = %s",(name,))
        row = cursor.fetchone()
        return row[0]

    def get_suppliers(cursor):
        cursor.execute("SELECT * FROM Supplier")
        rows = cursor.fetchall()
        return [row[1] for row in rows]

    def update_option_menu(cursor, option_menu, variable,status):
        if status == "Type":
            values = get_types(cursor)
        else:
            values = get_suppliers(cursor)
        menu = option_menu['menu']
        menu.delete(0, 'end')
        for item in values:
            menu.add_command(label=item, command=lambda value=item: variable.set(value))
        if values:
            variable.set(values[0])

    def update_product_action():
        name = entr_product_name.get().strip()
        type = get_type_id(select_type)
        amount = int(entry_product_amount.get().strip())
        price = float(entry_product_price.get().strip())
        supplier = get_supplier_id(select_supplier)

        modify_by = id_user
        product = Product(name, type, 0, amount, price, supplier, None, modify_by)
        update_product(cursor, product, tree, window_product_ad,id_product, db)

    window_product_ad = Tk()
    window_product_ad.geometry("200x400")
    window_product_ad.title("Add Product")
    screen_width = window_product_ad.winfo_screenwidth()
    screen_height = window_product_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_product_ad.geometry(f"300x400+{position_x}+{position_y}")

    lable_product_name = Label(window_product_ad, text="Name")
    lable_product_name.place(x=20, y=50, width=80, height=30)

    entr_product_name = Entry(window_product_ad)
    entr_product_name.place(x=100, y=50, width=150, height=30)

    label_product_type = Label(window_product_ad, text="Type")
    label_product_type.place(x=20, y=100, width=70, height=30)

    select_type = StringVar(window_product_ad)
    option_menu_type = OptionMenu(window_product_ad, select_type, [])
    option_menu_type.place(x=100, y=100, width=80, height=30)

    update_option_menu(cursor, option_menu_type, select_type, "Type")

    label_product_amount = Label(window_product_ad, text="Amount")
    label_product_amount.place(x=20, y=150, width=50, height=30)

    entry_product_amount = Entry(window_product_ad)
    entry_product_amount.place(x=100, y=150, width=100, height=30)

    label_product_price = Label(window_product_ad, text="Price")
    label_product_price.place(x=20, y=200, width=80, height=30)

    entry_product_price = Entry(window_product_ad)
    entry_product_price.place(x=100, y=200, width=100, height=30)

    label_product_type = Label(window_product_ad, text="Supplier")
    label_product_type.place(x=20, y=250, width=70, height=30)

    select_supplier = StringVar(window_product_ad)
    option_menu_suplier = OptionMenu(window_product_ad, select_supplier, [])
    option_menu_suplier.place(x=100, y=250, width=80, height=30)

    update_option_menu(cursor, option_menu_suplier, select_supplier, "Supplier")

    button_product_add = Button(window_product_ad, text="Update", command=lambda: update_product_action())
    button_product_add.place(x=150, y=300, width=100, height=30)

    name,type,supplier,sold,inventory,price = detail_product(cursor,id_product)
    entr_product_name.insert(0,name)
    entry_product_amount.insert(0,inventory)
    select_type.set(type)
    select_supplier.set(supplier)
    entry_product_price.insert(0,price)
    window_product_ad.mainloop()

def delete_product(cursor,id_product,tree,db):
    ask = messagebox.askyesno("Confirm delete","Do you want to delete this product ?")
    if ask:
        cursor.execute("Delete from product where id = %s",(id_product,))
        db.commit()
        refresh_treeview(tree,cursor)
        messagebox.showinfo("Delete alert","Delete successfully !")
    else:
        return

def search_product(cursor,entr_search,tree):
    text = entr_search.get().strip()
    cursor.execute("SELECT * from Product WHERE Name LIKE %s", ('%' + text + '%',))
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("","end",values=row)

def create_manager_type_form(cursor, db):
    global selected_id
    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]

    def create_add_type_form():
        window_product_type = Tk()
        window_product_type.geometry("300x300")
        window_product_type.title("Add Type")

        def hide_window():
            window_product_type.withdraw()

        def add_type():
            name_type = entry_product_type.get().strip()
            cursor.execute("SELECT COUNT(*) FROM Type WHERE name = %s", (name_type,))
            result = cursor.fetchone()

            if result[0] > 0:
                messagebox.showwarning("", "Type already exists")
            else:
                cursor.execute("Insert into Type (name) values (%s)",(name_type,))
                messagebox.showinfo("","Add successfully")
                db.commit()

                window_product_type.destroy()
                refresh_treeview_type(tree,cursor,"Manager Type")

        window_product_type.protocol("WM_DELETE_WINDOW", hide_window)
        # Get the screen width and height
        screen_width = window_product_type.winfo_screenwidth()
        screen_height = window_product_type.winfo_screenheight()

        # Calculate position x and y coordinates
        position_x = int((screen_width / 2) - (400 / 2))
        position_y = int((screen_height / 3) - (400 / 2))
        window_product_type.geometry(f"200x200+{position_x}+{position_y}")

        label_product_type = Label(window_product_type, text="Name type")
        label_product_type.place(x=20, y=20, width=80, height=30)

        entry_product_type = Entry(window_product_type)
        entry_product_type.place(x=20, y=50, width=160, height=30)

        button_save_type = Button(window_product_type,text="Save",command=add_type)
        button_save_type.place(x=120, y=80, width=60, height=30)
        refresh_treeview_type(tree, cursor)
        window_product_type.mainloop()

    def delete_type():
        cursor.execute("SELECT COUNT(*) FROM Product WHERE IdType = %s", (selected_id,))
        result = cursor.fetchone()

        if result[0] > 0:
            messagebox.showwarning("","Cannot delete this type because it is being used in products. Please delete or change the type in products first.")
        else:
            cursor.execute("delete from Type where id =(%s)", (selected_id,))
            db.commit()
            refresh_treeview_type(tree, cursor,"Manager Type")
            messagebox.showinfo("Delete alert", "Delete successfully !")

    window_product_type = Tk()
    window_product_type.geometry("400x400")
    window_product_type.title("Type Manager")

    def hide_window():
        window_product_type.withdraw()
    window_product_type.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_product_type.winfo_screenwidth()
    screen_height = window_product_type.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_product_type.geometry(f"400x400+{position_x}+{position_y}")

    columns = ("ID", "Name")
    tree = ttk.Treeview(window_product_type, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")

    # Heading
    heading_product_mg = Label(window_product_type, text="TYPE MANAGEMENT", font=("Helvetica", 20, "bold"), fg="green")
    heading_product_mg.place(x=20, y=30, width=300, height=30)
    total_width = 360
    column_width = total_width // len(columns)
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)
    tree.place(x=20, y=100, width=360, height=200)
    refresh_treeview_type(tree, cursor)

    button_add_type = Button(window_product_type,text="Add",command=create_add_type_form)
    button_add_type.place(x=320, y=320, width=50, height=30)
    button_delete_type = Button(window_product_type, text="Delete", command=delete_type)
    button_delete_type.place(x=240,y=320,width=50, height=30)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_product_type.mainloop()
def create_product_manager_form(cursor,db,id_user):
    global selected_id
    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]

    def hide_window():
        window_product_mg.withdraw()

    window_product_mg = Tk()
    window_product_mg.geometry("850x600")
    window_product_mg.title("Product Manager")
    # Close the program when clicking the close button
    window_product_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_product_mg.winfo_screenwidth()
    screen_height = window_product_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_product_mg.geometry(f"850x600+{position_x}+{position_y}")

    # Heading
    heading_product_mg = Label(window_product_mg,text="PRODUCT MANAGEMENT",font=("Helvetica", 20, "bold"), fg="green")
    heading_product_mg.place(x=200, y=30, width=400, height=30)

    # Search
    entr_search = Entry(window_product_mg)
    entr_search.place(x=400, y=80, width=300, height=30)

    button_product_manager = Button(window_product_mg, text="Search", command=lambda: search_product(cursor,entr_search,tree))
    button_product_manager.place(x=720, y=80, width=80, height=30)

    # Add, Update, Delete buttons
    button_type_manager = Button(window_product_mg, text="Manage Type", command=lambda: create_manager_type_form(cursor, db))
    button_type_manager.place(x=420, y=450, width=80, height=30)

    button_product_manager = Button(window_product_mg, text="Add", command=lambda: create_product_add_form(cursor,tree,db,id_user))
    button_product_manager.place(x=520, y=450, width=80, height=30)

    button_product_manager = Button(window_product_mg, text="Update", command=lambda: create_product_update_form(cursor,tree,selected_id,db,id_user))
    button_product_manager.place(x=620, y=450, width=80, height=30)

    button_product_manager = Button(window_product_mg, text="Delete", command=lambda: delete_product(cursor,selected_id,tree,db))
    button_product_manager.place(x=720, y=450, width=80, height=30)
    # Tree view
    columns = ("ID","Name", "Type", "Supplier","Sold", "Inventory", "Price","CreateBy","CreateDate","ModifyBy","ModifyDate")
    tree = ttk.Treeview(window_product_mg, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Type", text="Type")
    tree.heading("Supplier", text="Supplier")
    tree.heading("Sold", text="Sold")
    tree.heading("Inventory", text="Inventory")
    tree.heading("Price", text="Price")
    tree.heading("CreateBy", text="CreateBy")
    tree.heading("CreateDate", text="CreateDate")
    tree.heading("ModifyBy", text="ModifyBy")
    tree.heading("ModifyDate", text="ModifyDate")
    total_width = 800  # Total width of the Treeview
    column_width = total_width // len(columns)  # Calculate width for each column
    for col in columns:
        tree.column(col, anchor=CENTER, width=column_width)

    tree.place(x=20, y=130, width=800, height=200)
    cursor.execute(
        "SELECT p.Id, p.Name, t.Name AS TypeName, s.Name AS SupplierName, p.Sold, p.Inventory, p.Price, "
        "p.CreateBy, p.CreateDate, p.ModifiBy, p.ModifyDate "
        "FROM Product p "
        "INNER JOIN Type t ON p.IdType = t.Id "
        "INNER JOIN Supplier s ON p.IdSupplier = s.Id"
    )
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_product_mg.mainloop()
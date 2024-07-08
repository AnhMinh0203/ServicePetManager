from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime

def detail_service(cursor,id):
    cursor.execute("Select * from Service where id = %s",(id,))
    row = cursor.fetchone()
    if row :
        name = row[1]
        price = row[2]
        desc = row[3]

        return name, price, desc
    else:
        return None

def refresh_treeview(tree,cursor):
    # Clear the current items in the tree
    for item in tree.get_children():
        tree.delete(item)

    # Load new data from the database
    cursor.callproc('getAllService')
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

def add_service(cursor, service, tree, window_service_ad, db):
    cursor.execute("Insert into Service (Name,Price,Description,CreateDate,CreateBy,ModifyDate,ModifyBy,Status) "
                   "values (%s,%s,%s,%s,%s,%s,%s,%s)",
                   (service.name,service.price,service.description, service.create_date,service.create_by,service.modify_date,service.modify_by,service.status))
    db.commit()
    messagebox.showinfo("Success", "Service added successfully")
    window_service_ad.destroy()
    refresh_treeview(tree, cursor)
def create_service_add_form(cursor,tree,db,id_user):
    from ServicePetManager.main import Service
    def add_service_action():
        name = entr_service_name.get().strip()
        price_str = entry_service_price.get().strip()
        description = entry_service_desc.get().strip()
        create_by = id_user
        modify_by = id_user

        if not price_str:
            messagebox.showerror("Lỗi", "Giá không thể để trống")
            return

        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Giá phải là một con số hợp lệ")
            return

        service = Service(name, price, description,create_by,modify_by)
        add_service(cursor, service, tree, window_service_ad, db)

    window_service_ad = Tk()
    window_service_ad.geometry("200x400")
    window_service_ad.title("Add Service")
    screen_width = window_service_ad.winfo_screenwidth()
    screen_height = window_service_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_service_ad.geometry(f"300x400+{position_x}+{position_y}")

    lable_service_name = Label(window_service_ad, text="Tên")
    lable_service_name.place(x=20, y=50, width=80, height=30)

    entr_service_name = Entry(window_service_ad)
    entr_service_name.place(x=100, y=50, width=150, height=30)

    label_service_price = Label(window_service_ad, text="Giá")
    label_service_price.place(x=20, y=100, width=80, height=30)

    entry_service_price = Entry(window_service_ad)
    entry_service_price.place(x=100, y=100, width=150, height=30)

    label_service_desc = Label(window_service_ad,text="Mô tả")
    label_service_desc.place(x=20, y=200, width=100,height=30)

    entry_service_desc = Entry(window_service_ad)
    entry_service_desc.place(x=100, y=150,width=150, height=90)

    button_service_add = Button(window_service_ad,text="Thêm",command=lambda:add_service_action())
    button_service_add.place(x=150, y=300,width=100, height=30)
    window_service_ad.mainloop()

def update_service(cursor,service,tree,window_service_ad,id,db):
    name = service.name
    price = service.price
    desc = service.description
    modify_by = service.modify_by
    modify_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
            UPDATE Service
            SET Name = %s,
                Price = %s,
                Description = %s,
                ModifyBy = %s,
                ModifyDate = %s
            WHERE Id = %s
        """, (name,  price, desc,modify_by, modify_date, id))
    db.commit()
    messagebox.showinfo("Thành công", "Thêm dịch vụ thành công")
    window_service_ad.destroy()
    refresh_treeview(tree,cursor)

def create_service_update_form(cursor,tree,id_service,db,id_user):
    from ServicePetManager.main import Service

    def update_service_action():
        name = entr_service_name.get().strip()
        price = float(entry_service_price.get().strip())
        desc = entry_service_desc.get().strip()

        modify_by = id_user
        service = Service(name, price, desc, id_user, id_user)
        update_service(cursor, service, tree, window_service_ad,id_service, db)

    window_service_ad = Tk()
    window_service_ad.geometry("200x400")
    window_service_ad.title("Add Service")
    screen_width = window_service_ad.winfo_screenwidth()
    screen_height = window_service_ad.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_service_ad.geometry(f"300x400+{position_x}+{position_y}")

    lable_service_name = Label(window_service_ad, text="Tên")
    lable_service_name.place(x=20, y=50, width=80, height=30)

    entr_service_name = Entry(window_service_ad)
    entr_service_name.place(x=100, y=50, width=150, height=30)

    label_service_price = Label(window_service_ad, text="Giá")
    label_service_price.place(x=20, y=100, width=80, height=30)

    entry_service_price = Entry(window_service_ad)
    entry_service_price.place(x=100, y=100, width=150, height=30)

    label_service_desc = Label(window_service_ad, text="Mô tả")
    label_service_desc.place(x=20, y=200, width=100, height=30)

    entry_service_desc = Entry(window_service_ad)
    entry_service_desc.place(x=100, y=150, width=150, height=90)


    button_service_add = Button(window_service_ad, text="Sửa", command=lambda: update_service_action())
    button_service_add.place(x=150, y=300, width=100, height=30)

    name,price, desc = detail_service(cursor,id_service)
    entr_service_name.insert(0,name)
    entry_service_price.insert(0,price)
    entry_service_desc.insert(0,desc)
    window_service_ad.mainloop()

def delete_service(cursor,id_service,tree,db):
    ask = messagebox.askyesno("Xác nhận xóa","Bạn có muốn xóa dịch vụ này không ?")
    if ask:
        cursor.execute("UPDATE service SET status = %s WHERE id = %s", (0, id_service))
        db.commit()
        refresh_treeview(tree,cursor)
        messagebox.showinfo("Xóa","Xóa thành công !")
    else:
        return

def search_service(cursor,entr_search,tree):
    text = entr_search.get().strip()
    cursor.execute("SELECT * from Service WHERE Name LIKE %s and Status = 1", ('%' + text + '%',) )
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("","end",values=row)

def create_service_manager_form(cursor,db,id_user):
    global selected_id
    def on_tree_select(event):
        global selected_id
        selected_item = tree.selection()[0]
        selected_id = tree.item(selected_item, "values")[0]

    def hide_window():
        window_service_mg.withdraw()

    window_service_mg = Tk()
    window_service_mg.geometry("850x600")
    window_service_mg.title("Service Manager")
    # Close the program when clicking the close button
    window_service_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_service_mg.winfo_screenwidth()
    screen_height = window_service_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_service_mg.geometry(f"850x600+{position_x}+{position_y}")

    # Heading
    heading_service_mg = Label(window_service_mg,text="SERVICE MANAGEMENT",font=("Helvetica", 20, "bold"), fg="green")
    heading_service_mg.place(x=200, y=30, width=400, height=30)

    # Search
    entr_search = Entry(window_service_mg)
    entr_search.place(x=400, y=80, width=300, height=30)

    button_service_manager = Button(window_service_mg, text="Tìm kiếm", command=lambda: search_service(cursor,entr_search,tree))
    button_service_manager.place(x=720, y=80, width=80, height=30)

    button_service_manager = Button(window_service_mg, text="Thêm", command=lambda: create_service_add_form(cursor,tree,db,id_user))
    button_service_manager.place(x=520, y=450, width=80, height=30)

    button_service_manager = Button(window_service_mg, text="Sửa", command=lambda: create_service_update_form(cursor,tree,selected_id,db,id_user))
    button_service_manager.place(x=620, y=450, width=80, height=30)

    button_service_manager = Button(window_service_mg, text="Xóa", command=lambda: delete_service(cursor,selected_id,tree,db))
    button_service_manager.place(x=720, y=450, width=80, height=30)
    # Tree view
    columns = ("ID","Name", "Price", "Description","CreateDate","CreateBy","ModifyDate","ModifyBy")
    tree = ttk.Treeview(window_service_mg, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Description", text="Description")

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
        "SELECT * from Service where Status = 1"
    )
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    window_service_mg.mainloop()
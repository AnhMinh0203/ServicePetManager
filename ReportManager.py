from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
from tkinter import filedialog
from tkcalendar import Calendar
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import xlsxwriter
def format_currency(value):
    return "{:,.0f} VND".format(value).replace(",", ".")
def create_chart(cursor, window_report_mg, param_date, status, result_total_price_var):
    month_in_year = []
    income = []
    total_income = 0
    title_chart = ''
    dataframe_x = ''
    dataframe_y = 'Income'
    if status == "All months of the year":
        title_chart = 'Income report all months of ' + str(param_date)
        dataframe_x = 'Months'
        cursor.callproc("GetMonthlyIncomeInYear", [param_date])
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                month_in_year.append(int(row[0]))
                income.append(float((row[1])))

    elif status == "Quarter of the year":
        title_chart = 'Income report all quaters of ' + str(param_date)
        dataframe_x = 'Quaters'
        cursor.callproc("GetQuaterlyIncomeInYear", [param_date])
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                month_in_year.append(int(row[0]))
                income.append(float((row[1])))

    elif status == "Day in month":
        title_chart = 'Income report all day in ' + str(param_date[0])
        dataframe_x = 'Day'
        cursor.callproc("GetDayIncomeInMonth", [param_date[0],param_date[1]])
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                month_in_year.append(int(row[0]))
                income.append(float((row[1])))

    data = {dataframe_x: month_in_year,
            dataframe_y: income}
    dataframe = pd.DataFrame(data)
    figure = plt.Figure(figsize=(10, 5), dpi=100)
    figure_plot = figure.add_subplot(1, 1, 1)
    figure_plot.set_ylabel('Income')
    line = FigureCanvasTkAgg(figure, window_report_mg)
    line.get_tk_widget().place(x=20, y=180, width=800, height=450)
    dataframe = dataframe[[dataframe_x, dataframe_y]].groupby(dataframe_x).sum()
    dataframe.plot(kind='line', legend=True, ax=figure_plot, color='r', marker='o', fontsize=10)
    figure_plot.set_title(title_chart)

    total_income = sum(income)
    formatted_total_income = format_currency(total_income)
    result_total_price_var.set(formatted_total_income)


def export_excel(cursor, status, param_date):
    date_input = []
    income = []
    date_obj = datetime.strptime(param_date, '%m/%d/%y')
    year_input = date_obj.year
    df = None

    if status == "All months of the year":
        cursor.callproc("GetMonthlyIncomeInYear", [year_input])
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                date_input.append(int(row[0]))
                income.append(float(row[1]))
        df = pd.DataFrame({
            'Months': date_input,
            'Total Income': income
        })

    elif status == "Quarter of the year":
        cursor.callproc("GetQuaterlyIncomeInYear", [year_input])
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                date_input.append(int(row[0]))
                income.append(float(row[1]))
        df = pd.DataFrame({
            'Quarters': date_input,
            'Total Income': income
        })

    elif status == "Day in month":
        month_input = date_obj.month
        cursor.callproc("GetDayIncomeInMonth", [month_input, year_input])
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                date_input.append(int(row[0]))
                income.append(float(row[1]))
        df = pd.DataFrame({
            'Days': date_input,
            'Total Income': income
        })

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        # Export to Excel with formatting using pandas and xlsxwriter
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            header_format = workbook.add_format({'bg_color': '#66FF00', 'font_color': '#FFFFFF', 'bold': True})
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
def create_report_manager_form(cursor):
    def hide_window():
        window_report_mg.withdraw()

    window_report_mg = Tk()
    window_report_mg.geometry("850x600")
    window_report_mg.title("Report Manager")
    # Close the program when clicking the close button
    window_report_mg.protocol("WM_DELETE_WINDOW", hide_window)
    # Get the screen width and height
    screen_width = window_report_mg.winfo_screenwidth()
    screen_height = window_report_mg.winfo_screenheight()

    # Calculate position x and y coordinates
    position_x = int((screen_width / 2) - (400 / 2))
    position_y = int((screen_height / 3) - (400 / 2))
    window_report_mg.geometry(f"850x700+{position_x}+{position_y}")

    # Heading
    heading_report_mg = Label(window_report_mg, text="REPORT MANAGEMENT", font=("Helvetica", 20, "bold"),
                              fg="green")
    heading_report_mg.place(x=200, y=30, width=400, height=30)
    # Export button
    button_export_excel = Button(window_report_mg,text="Export Excel",command=lambda: export_excel(cursor,select_option.get(),cal.get_date()))
    button_export_excel.place(x=380, y=90, width=150, height=30)
    # Selection
    select_option = StringVar(window_report_mg)
    select_option.set("All months of the year")  # set the default value
    gender_menu = OptionMenu(window_report_mg, select_option,
                             "Day in month", "Quarter of the year", "All months of the year")
    gender_menu.place(x=650, y=90, width=150, height=30)
    # Calendar
    cal = Calendar(window_report_mg, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    def toggle_calendar():
        if cal.winfo_ismapped():
            cal.place_forget()
        else:
            cal.place(x=550, y=130)
            cal.tkraise()

    dob = Button(window_report_mg, text="Date", command=toggle_calendar)
    dob.place(x=550, y=90, width=80, height=30)
    # Total price
    label_total_price_var = Label(window_report_mg, text="Total income", anchor="w", )
    label_total_price_var.place(x=20, y=80, width=150, height=30)
    result_total_price_var = StringVar(window_report_mg, value="")
    result_total_price = Label(window_report_mg, textvariable=result_total_price_var, bg="white", fg="red", anchor="w",font=("Helvetica", 10, "bold"))
    result_total_price.place(x=20, y=120, width=150, height=30)

    def on_date_select(event):
        selected_date = cal.get_date()
        date_obj = datetime.strptime(selected_date, '%m/%d/%y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        dob.config(text=formatted_date)

        if select_option.get() == 'Day in month':
            year = date_obj.year
            month = date_obj.month
            param_date = [month,year]
            create_chart(cursor, window_report_mg, param_date, select_option.get(), result_total_price_var)
        else:
            year = date_obj.year
            create_chart(cursor, window_report_mg, year, select_option.get(), result_total_price_var)
        cal.place_forget()

    current_year = datetime.now().year
    create_chart(cursor, window_report_mg, current_year, select_option.get(), result_total_price_var)
    cal.bind("<<CalendarSelected>>", on_date_select)

    window_report_mg.mainloop()

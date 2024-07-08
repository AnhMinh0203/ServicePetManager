from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector
from datetime import datetime
from tkcalendar import Calendar

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "provipxop",
    database="petmanage"
)
cursor = db.cursor()
result = ''
cursor.callproc('addTest',['aaaa dz',result])
db.commit()

from tkinter import * # modules
import time
import sqlite3
from datetime import date
import xlsxwriter as x
import os

file_name = "log.db" # order number and db name
ord_num = 0

con = sqlite3.connect(file_name) # connection + cursor
cur = con.cursor()

SQL_code = '''CREATE TABLE IF NOT EXISTS c_info (
            c_name VARCHAR(50),
            c_add VARCHAR(50),
            c_id INT,
            c_phone VARCHAR(50) );'''
cur.execute(SQL_code) # customer info

SQL_code = ''' CREATE TABLE IF NOT EXISTS m_info (
            it_name VARCHAR(50),
            it_id INT,
            it_price FLOAT ) '''
cur.execute(SQL_code) # menu info

SQL_code = ''' CREATE TABLE IF NOT EXISTS log (
            it_id INT,
            portions INT,
            date VARCHAR(50),
            total_price FLOAT,
            c_id INT,
            order_pending BOOL,
            order_number INT) '''
cur.execute(SQL_code) # menu info


cur.execute('SELECT * FROM c_info')
if len(cur.fetchall()) == 0:
    cur.execute('INSERT INTO c_info (c_name, c_add, c_id, c_phone) VALUES ("John Doe", "4 Privet Drive", 0, "1234567890")')
    con.commit()

cur.execute('SELECT * FROM m_info')
if len(cur.fetchall()) == 0:
    cur.execute('INSERT INTO m_info (it_name, it_id, it_price) VALUES ("Dish 1", 0, 1.00)')
    con.commit()
    
objects = []
    
def clear():

    global objects
    
    for i in objects:
        i.forget()
    objects = []

def menu():
    
    clear()

    objects.append(filler)

    title.pack()
    objects.append(title)

    filler.pack()



    items.pack()
    objects.append(items)
    people.pack()
    objects.append(people)
    add_orders.pack()
    objects.append(add_orders)
    pending_button.pack()
    objects.append(pending_button)
    export_button.pack()
    objects.append(export_button)


def items_menu():
    clear()
    objects.append(filler)
    filler.pack()
    title.pack()
    objects.append(title)
    item_name.pack()
    item_name.delete(0, END)
    item_name.insert(0,'Enter Item Name')
    objects.append(item_name)
    item_price.pack()
    item_price.delete(0, END)
    item_price.insert(0,'Enter Item Price')
    objects.append(item_price)
    enter_button.pack()
    objects.append(enter_button)
    SQL_code = '''SELECT * FROM m_info'''
    cur.execute(SQL_code)
    menu_list = cur.fetchall()
    for food_tuple in menu_list:
        food = list(food_tuple)
        if len(str(food[2])) != 4:
            for i in range(4-len(str(food[2]))):
                food[2] = str(food[2]) + '0'
        menu_text = str(food[1]) + ', ' + str(food[0]) + ', £' + str(food[2])
        menu_item = Label(root, text=menu_text)
        menu_item.pack()
        objects.append(menu_item)

    item_id.pack()
    item_id.delete(0, END)
    item_id.insert(0, 'ITEM ID TO EDIT')
    objects.append(item_id)

    new_name.pack()
    new_name.delete(0, END)
    new_name.insert(0, 'New Name')
    objects.append(new_name)

    new_price.pack()
    new_price.delete(0, END)
    new_price.insert(0, 'New Price')
    objects.append(new_price)

    edit_enter.pack()
    objects.append(edit_enter)
    
    home.pack()
    objects.append(home)

    
def people_menu():
    
    clear()
    objects.append(filler)
    filler.pack()

    title.pack()
    objects.append(title)

    cust_name.pack()
    cust_name.delete(0, END)
    cust_name.insert(0, 'Customer Name')
    objects.append(cust_name)    
    
    cust_phone.pack()
    cust_phone.delete(0, END)
    cust_phone.insert(0, 'Phone Number')
    objects.append(cust_phone)

    cust_add.pack()
    cust_add.delete(0, END)
    cust_add.insert(0, 'Address')
    objects.append(cust_add)

    c_enter.pack()
    objects.append(c_enter)

    cur.execute('SELECT * FROM c_info')
    customers = cur.fetchall()
    for person in customers:
        customer = list(person)
        
        p_text = str(customer[2]) + ', ' + str(customer[0]) + ', ' + str(customer[3]) + ', ' + str(customer[1])
        p_label = Label(root, text=p_text)
        p_label.pack()
        objects.append(p_label)

    cus_id.pack()
    cus_id.delete(0, END)
    cus_id.insert(0, 'CUSTOMER ID TO EDIT')
    objects.append(cus_id)

    c_new_name.pack()
    c_new_name.delete(0, END)
    c_new_name.insert(0, 'New Name')
    objects.append(c_new_name)

    new_phone.pack()
    new_phone.delete(0, END)
    new_phone.insert(0, 'New Number')
    objects.append(new_phone)

    new_add.pack()
    new_add.delete(0, END)
    new_add.insert(0, 'New Address')
    objects.append(new_add)

    cust_enter.pack()
    objects.append(cust_enter)
    

    home.pack()
    objects.append(home)

def add_item():
    SQL_code = '''SELECT * FROM m_info'''
    cur.execute(SQL_code)
    menu_list = cur.fetchall()

    if len(menu_list) == 0:
        it_num = 0
    elif len(menu_list) > 0:
        it_num = menu_list[-1][1] + 1
    name = item_name.get()
    price = item_price.get()
    it_info = [name, it_num, price]
    SQL_code = 'INSERT INTO m_info (it_name, it_id, it_price) VALUES ("{}", {}, {});'.format(name, it_num, price)
    print(SQL_code)
    cur.execute(SQL_code)
    con.commit()
    items_menu()

def edit_item():
    
    it_num = item_id.get()
    
    if new_name.get() == 'New Name':
        SQL_code = 'SELECT it_name FROM m_info WHERE it_id={}'.format(it_num)
        cur.execute(SQL_code)
        name = cur.fetchall()[0][0]
        print(name)
    else:
        name = new_name.get()
        
    if new_price.get() == 'New Price':
        SQL_code = 'SELECT it_price FROM m_info WHERE it_id={}'.format(it_num)
        cur.execute(SQL_code)
        price = float(cur.fetchall()[0][0])
        print(price)
        
    else:
        price = float(new_price.get())

    SQL_code = 'UPDATE m_info SET it_name="{}", it_price={} WHERE it_id={}'.format(name, price, it_num)
    cur.execute(SQL_code)
    con.commit()

    items_menu()

def add_cust():

    name = cust_name.get()
    phone = str(cust_phone.get())
    address = cust_add.get()

    SQL_code = '''SELECT * FROM c_info'''
    cur.execute(SQL_code)
    cust_list = cur.fetchall()

    if len(cust_list) == 0:
        cust_id = 0
    elif len(cust_list) > 0:
        cust_id = int(cust_list[-1][-2]) +1

    SQL_code = 'INSERT INTO c_info (c_name, c_add, c_id, c_phone) VALUES ( "{}", "{}", {}, "{}");'.format(name, address, cust_id, phone)
    cur.execute(SQL_code)
    con.commit()
    people_menu()


def edit_cust():

    cust_id = cus_id.get()

    if c_new_name.get() == 'New Name':
        cur.execute('SELECT c_name FROM c_info WHERE c_id={}'.format(cust_id))
        name = cur.fetchall()[0][0]
    else:
        name = c_new_name.get()

    if new_phone.get() == 'New Number':
        cur.execute('SELECT c_phone FROM c_info WHERE c_id={}'.format(cust_id))
        phone = cur.fetchall()[0][0]
    else:  
        phone = new_phone.get()

    if new_add.get() == 'New Address':
        cur.execute('SELECT c_add FROM c_info WHERE c_id={}'.format(cust_id))
        address = cur.fetchall()[0][0]
    else:
        address = new_add.get()

    SQL_code = 'UPDATE c_info SET c_name="{}", c_add="{}", c_phone="{}" WHERE c_id={}'.format(name, address, phone, cust_id)
    cur.execute(SQL_code)
    con.commit()

    people_menu()

def add_orders_menu():
    clear()

    global clicked, Clicked, CLICKED

    cur.execute('SELECT * FROM m_info')
    menu_data = cur.fetchall()
    item_options =[]
    for i in menu_data:
        item_options.append(i[0])
    clicked = StringVar()
    clicked.set('CHOOSE ITEM')
    order_drop = OptionMenu(root, clicked, *item_options)
    cur.execute('SELECT * FROM c_info')
    c_data = cur.fetchall()
    person_options = []
    for j in c_data:
        person_options.append(j[0])
    Clicked = StringVar()
    Clicked.set('CHOOSE PERSON')
    person_drop = OptionMenu(root, Clicked, *person_options)
    numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    CLICKED = StringVar()
    CLICKED.set('NUMBER OF PORTIONS')
    portions = OptionMenu(root, CLICKED, *numbers)
    
    objects.append(filler)
    filler.pack()

    title.pack()
    objects.append(title)

    order_drop.pack()
    objects.append(order_drop)

    person_drop.pack()
    objects.append(person_drop)

    portions.pack()
    objects.append(portions)

    make_order.pack()
    objects.append(make_order)

    home.pack()
    objects.append(home)
    
def create_order():
    name = Clicked.get()
    portion = CLICKED.get()
    item = clicked.get()

    cur.execute('SELECT it_id FROM m_info WHERE it_name="{}"'.format(item))
    it_num = int(cur.fetchall()[0][0])

    portion = int(portion)

    today = date.today()
    DATE = today.strftime('%Y-%m-%d')

    cur.execute('SELECT it_price FROM m_info WHERE it_id={}'.format(it_num))
    total_price = portion*cur.fetchall()[0][0]

    cur.execute('SELECT c_id FROM c_info WHERE c_name="{}"'.format(name))
    cust_id = int(cur.fetchall()[0][0])

    pending = 1

    cur.execute('SELECT * FROM log')
    order_list = cur.fetchall()

    if len(order_list) == 0:
        ord_num = 0
    else:
        ord_num = order_list[-1][-1]+1

    cur.execute('INSERT INTO log (it_id, portions, date, total_price, c_id, order_pending, order_number) VALUES ({}, {}, "{}", {}, {}, {}, {});'.format(it_num, portion, DATE, total_price, cust_id, pending, ord_num))
    con.commit()

    add_orders_menu()


def pending_menu():
    
    clear()
    objects.append(filler)
    filler.pack()
    title.pack()
    objects.append(title)

    cur.execute('SELECT * FROM log WHERE order_pending=1')
    log_data = cur.fetchall()
    print(log_data)

    for order in log_data:

        cur.execute('SELECT it_name FROM m_info WHERE it_id={}'.format(order[0]))
        item_name = cur.fetchall()

        cur.execute('SELECT c_name FROM c_info WHERE c_id ={}'.format(order[4]))
        cus_name = cur.fetchall()

        info = [cus_name, item_name, str(order[1])+' portions', '£'+str(order[3]), str(order[2])]
        order_text = str(order[-1]) + '.    ' + cus_name[0][0]+': ' + item_name[0][0] + ', ' +str(order[1])+' portions' + ', '+ '£'+str(order[3])

        order_label = Label(root, text=order_text)
        order_label.pack()
        objects.append(order_label)

    tickoff_entry.pack()
    tickoff_entry.delete(0, END)
    tickoff_entry.insert(0, 'Completed Order ID')
    objects.append(tickoff_entry)

    tickoff_enter.pack()
    objects.append(tickoff_enter)

    

    home.pack()
    objects.append(home)
    
def tick_off():

    ord_num = tickoff_entry.get()
    cur.execute('UPDATE log SET order_pending=0 WHERE order_number={}'.format(ord_num))

    pending_menu()

def export():

    cur.execute('SELECT * FROM m_info')
    menu_info = cur.fetchall()
    menu_info.insert(0, ['it_name', 'it_id', 'it_price'])

    cur.execute('SELECT * FROM c_info')
    customer_info = cur.fetchall()
    customer_info.insert(0, ['c_name', 'c_add', 'c_id', 'c_phone'])

    cur.execute('SELECT * FROM log')
    orders = cur.fetchall()
    orders.insert(0, ['it_id', 'portions', 'date', 'total_price', 'c_id', 'order_pending', 'order_number'])


    for file in os.listdir():
        if file == 'log.xlsx':
            print('file found')
            os.remove('log.xlsx')
    workbook = x.Workbook('log.xlsx')
    worksheet_1 = workbook.add_worksheet('log')
    
    row = 0
    col = 0

    for it_id, portions, date, total_price, c_id, order_pending, order_number in orders:
        worksheet_1.write(row, col, it_id)
        worksheet_1.write(row, col+1, portions)
        worksheet_1.write(row, col+2, date)
        worksheet_1.write(row, col+3, total_price)
        worksheet_1.write(row, col+4, c_id)
        worksheet_1.write(row, col+5, order_pending)
        worksheet_1.write(row, col+6, order_number)
        row +=1


    worksheet_2 = workbook.add_worksheet('m_info')

    row = 0
    col = 0

    for it_name, it_id, it_price in menu_info:
        worksheet_2.write(row, col, it_name)
        worksheet_2.write(row, col+1, it_id)
        worksheet_2.write(row, col+2, it_price)
        row+=1


    worksheet_3 = workbook.add_worksheet('c_info')

    row = 0
    col = 0

    for c_name, c_add, c_id, c_phone in customer_info:
        worksheet_3.write(row, col, c_name)
        worksheet_3.write(row, col+1, c_add)
        worksheet_3.write(row, col+2, c_id)
        worksheet_3.write(row, col+3, c_phone)
        row+=1



    workbook.close()

objects = []
  
root = Tk()
root.geometry('500x600')

filler = Label(root, text='') # Filler

title = Label(root, text='Order log') # Title
title.config(font=('Biome', 44))

items = Button(root, text='Menu', command=items_menu)
people = Button(root, text='People', command=people_menu)
add_orders = Button(root, text='Add Orders', command=add_orders_menu)
home = Button(root, text='Home', command=menu)
item_name = Entry(root)
item_price = Entry(root)
enter_button = Button(root, text='Enter', command=add_item)
cust_name = Entry(root)
cust_phone = Entry(root)
cust_add = Entry(root)
c_enter = Button(root, text='Enter', command=add_cust)
item_id = Entry(root)
new_name = Entry(root)
new_price = Entry(root)
edit_enter = Button(root, text='Enter', command=edit_item)
cus_id = Entry(root)
c_new_name = Entry(root)
new_phone = Entry(root)
new_add = Entry(root)
cust_enter = Button(root, text='Enter', command=edit_cust)




make_order =  Button(root, text='Create Order', command=create_order)
pending_button = Button(root, text='Pending Orders', command=pending_menu)
tickoff_entry = Entry(root)
tickoff_enter = Button(root, text='Mark as Complete', command=tick_off)
export_button = Button(root, text='EXPORT TO EXCEL', command=export)






menu()
root.mainloop()


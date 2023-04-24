"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv


# Создание пустых списков, для их заполнения данными из cvs файлов
data_employees = []
data_customers = []
data_orders = []

# Указание пути до cvs файлов, при необходимости нужно изменить
way_to_employees_data = 'north_data\employees_data.csv'
way_to_customers_data = 'north_data\customers_data.csv'
orders_data = 'north_data\orders_data.csv'

with open(way_to_employees_data, newline='') as File:
    reader = csv.reader(File)
    data_employees.extend(reader)

with open(way_to_customers_data, newline='') as File:
    reader = csv.reader(File)
    data_customers.extend(reader)

with open(orders_data, newline='') as File:
    reader = csv.reader(File)
    data_orders.extend(reader)


# Вместо *** введите свой пароль
conn = psycopg2.connect(host="localhost", database='north', user='postgres', password='***')
try:
    with conn:
        with conn.cursor() as cur:
            numeric_id = 1

            for row in data_employees:
                if row[0] != "first_name" and row[1] != "last_name" and row[2] != "title" and row[3] != 'birth_date':
                    row.insert(0, numeric_id)
                    cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", row)
                    cur.execute("SELECT * FROM employees")
                    numeric_id += 1

            for row in data_customers:
                if row[0] != "customer_id" and row[1] != "company_name" and row[2] != "contact_name":
                    cur.execute("INSERT INTO customers VALUES (%s, %s, %s)", row)
                    cur.execute("SELECT * FROM customers")
            rows = cur.fetchall()
            for row in rows:
                print(row)

            for row in data_orders:
                if row[0] != "order_id" and row[1] != "customer_id" and row[2] != "employee_id":
                    cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", row)
                    cur.execute("SELECT * FROM orders")
finally:
    conn.close()

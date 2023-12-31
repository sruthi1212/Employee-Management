from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(script_dir, 'employees.db')

conn = sqlite3.connect(db_path)
if not os.path.exists(db_path):
    # Creating the database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
if not os.access(db_path, os.W_OK):
    raise Exception(f"The file {db_path} is not writable.")
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, position TEXT NOT NULL, department TEXT NOT NULL)')
    


app = Flask(__name__)

#setting up of SQLite database 

conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS employees')
cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

#Doing CRUDoperations

def get_all_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return employees

def get_employee_by_id(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    return employee

def add_employee(name, position, department):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employees (name, position, department) VALUES (?, ?, ?)', (name, position, department))
    conn.commit()
    conn.close()

def update_employee(employee_id, name, position, department):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE employees
        SET name=?, position=?, department=?
        WHERE id=?
    ''', (name, position, department, employee_id))
    conn.commit()
    conn.close()

def delete_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
    conn.commit()
    conn.close()

#creating Routes

@app.route('/')
def index():
    employees = get_all_employees()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        add_employee(name, position, department)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    employee = get_employee_by_id(employee_id)
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        update_employee(employee_id, name, position, department)
        return redirect(url_for('index'))
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:employee_id>')
def delete(employee_id):
    delete_employee(employee_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

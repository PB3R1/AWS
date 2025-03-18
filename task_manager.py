import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import getpass
import tkinter as tk
from tkinter import messagebox

# Set up the SQLite database
def setup_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            assigned_to TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a task to the database
def add_task(task, assigned_to):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task, assigned_to)
        VALUES (?, ?)
    ''', (task, assigned_to))
    conn.commit()
    conn.close()

# Send an email alert
def send_email(subject, body, to_email):
    from_email = 'your_email@example.com'  # Replace with your email
    password = getpass.getpass('Enter your email password: ')  # Password prompt for security
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f'Email sent to {to_email}')
    except Exception as e:
        print(f'Failed to send email: {e}')

# Function to handle task creation and email sending
def create_task():
    task = task_entry.get()
    assigned_to = email_entry.get()
    
    if not task or not assigned_to:
        messagebox.showerror("Error", "Please fill in both fields.")
        return
    
    add_task(task, assigned_to)
    
    subject = 'New Task Assigned'
    body = f'You have been assigned a new task: {task}'
    
    try:
        send_email(subject, body, assigned_to)
        messagebox.showinfo("Success", "Task created and email sent!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# Set up the Tkinter GUI
def setup_gui():
    root = tk.Tk()
    root.title("Task Manager")

    global task_entry
    global email_entry

    tk.Label(root, text="Task Description:").pack(pady=5)
    task_entry = tk.Entry(root, width=50)
    task_entry.pack(pady=5)

    tk.Label(root, text="Assigned To (Email):").pack(pady=5)
    email_entry = tk.Entry(root, width=50)
    email_entry.pack(pady=5)

    tk.Button(root, text="Create Task", command=create_task).pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    setup_database()
    setup_gui()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

class GroceryManagementStore:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Management Store")
        self.root.geometry("800x600")

        # Database connection
        self.connection = self.create_connection()

        # Load and set background image for all windows
        self.background_image = Image.open("C:\\Users\\Sandra\\Downloads\\grocery.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.set_background(self.root)

        # Initialize login UI
        self.create_login_ui()

    def set_background(self, window):
        background_label = tk.Label(window, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Resize background image according to window size
        def resize_background(event):
            width, height = event.width, event.height
            resized_image = self.background_image.resize((width, height))
            self.background_photo = ImageTk.PhotoImage(resized_image)
            background_label.config(image=self.background_photo)

        window.bind("<Configure>", resize_background)

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='grocery',
                user='root',
                password='admin123'
            )
            if connection.is_connected():
                print("Connected to MySQL database")
            return connection
        except Error as e:
            print(f"Error: '{e}'")
            messagebox.showerror("Database Connection", "Failed to connect to the database")
            return None

    def create_login_ui(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=50)
        self.login_frame.configure(bg='light blue')

        # tk.Label(self.login_frame, text="Welcome to Grocery Management", font=("Times New Roman", 16), bg='light blue').grid(row=0,column=1,padx=10,pady=10)

        tk.Label(self.login_frame, text="Username ",font=("Times New Roman",12)).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_frame, text="Password ",font=("Times New Roman",12)).grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show=".")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.login_frame, text="Login User",font=("Times New Roman",12) ,command=self.login,height=2,width=10).grid(row=2, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login", "Login successful")
            self.login_frame.pack_forget()
            self.create_dashboard()
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def create_dashboard(self):
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(pady=50)
        self.dashboard_frame.configure(bg='light blue')

        tk.Button(self.dashboard_frame,background="white", text="Products",height=5, width=20, command=self.open_products_window).pack(padx=10,pady=10)
        tk.Button(self.dashboard_frame,background="white", text="Employees", height=5,width=20, command=self.open_employees_window).pack(padx=10,pady=10)
        tk.Button(self.dashboard_frame,background="white", text="Bill",height=5, width=20, command=self.open_bill_window).pack(padx=10,pady=10)

    def open_products_window(self):
        self.prdct_window = tk.Toplevel(self.root)
        self.prdct_window.title("Products")
        self.prdct_window.geometry("400x400")
        self.prdct_window.configure(bg="light blue")

        tk.Label(self.prdct_window, text="Product Name  :",font=("Times New Roman",10)).grid(row=0, column=0, padx=10, pady=10)
        self.product_name_entry = tk.Entry(self.prdct_window)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.prdct_window, text="Quantity  :",font=("Times New Roman",10)).grid(row=1, column=0, padx=10, pady=10)
        self.product_qty_entry = tk.Entry(self.prdct_window)
        self.product_qty_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.prdct_window, text="Price  :",font=("Times New Roman",10)).grid(row=2, column=0, padx=10, pady=10)
        self.product_price_entry = tk.Entry(self.prdct_window)
        self.product_price_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.prdct_window,background="white", text=" Add Product ",font=("Times New Roman",14), command=self.add_product).grid(row=4, column=1,padx=20, pady=20)

    def add_product(self):
        product_name = self.product_name_entry.get()
        product_qty = self.product_qty_entry.get()
        product_price = self.product_price_entry.get()

        if product_name and product_qty and product_price:
            try:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO products (product_name, quantity, price) VALUES (%s, %s, %s)",
                               (product_name, product_qty, product_price))
                self.connection.commit()
                messagebox.showinfo("Success", "Product added successfully")
                # self.clear_product_entries()
            except Error as e:
                messagebox.showerror("Error", f"Failed to add product: {e}")
        else:
            messagebox.showerror("Error", "All fields are required")
        pass

    def open_employees_window(self):
        self.emp_window = tk.Toplevel(self.root)
        self.emp_window.title("Employees")
        self.emp_window.geometry("400x400")
        self.emp_window.configure(bg="light blue")

        # employeee name
        tk.Label(self.emp_window,text="Employee Name  :",font=("Times New Roman",10)).grid(row=0, column=0, padx=10, pady=10)
        self.emp_name_entry = tk.Entry(self.emp_window)
        self.emp_name_entry.grid(row=0, column=1, padx=10, pady=10)
        # position
        tk.Label(self.emp_window, text="Position  :",font=("Times New Roman",10)).grid(row=1, column=0, padx=10, pady=10)
        self.emp_position_entry = tk.Entry(self.emp_window)
        self.emp_position_entry.grid(row=1, column=1, padx=10, pady=10)
        # salary
        tk.Label(self.emp_window, text="Salary  :",font=("Times New Roman",10)).grid(row=2, column=0, padx=10, pady=10)
        self.emp_salary_entry = tk.Entry(self.emp_window)
        self.emp_salary_entry.grid(row=2, column=1, padx=10, pady=10)
        # submit
        tk.Button(self.emp_window,font=("Times New Roman",14), text=(" Submit Employee "),command=self.submit_employee).grid(row=3, column=1, pady=10)

    def submit_employee(self):
        emp_name = self.emp_name_entry.get()
        emp_position = self.emp_position_entry.get()
        emp_salary = self.emp_salary_entry.get()

        if emp_name and emp_position and emp_salary:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)",
                           (emp_name, emp_position, emp_salary))
            self.connection.commit()
            messagebox.showinfo("Success", "Employee added successfully")
            self.emp_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required")

    def fetch_items(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM items")
            items = cursor.fetchall()
            return items
        except Error as e:
            messagebox.showerror("Error", f"Failed to fetch items: {e}")
            return []

    def add_item_row(self):
        row = len(self.item_rows) + 1  # Start from row 1 since row 0 is the header
        item_name = ttk.Combobox(self.billing_frame, values=self.item_list, state='readonly', width=20)
        item_name.grid(row=row, column=0, padx=5, pady=5)
        item_name.bind("<<ComboboxSelected>>", lambda event, r=row: self.update_mrp(r))

        quantity = tk.Entry(self.billing_frame, width=10)
        quantity.grid(row=row, column=1, padx=5, pady=5)
        quantity.bind("<KeyRelease>", lambda event, r=row: self.update_total(r))

        mrp = tk.Entry(self.billing_frame, width=10)
        mrp.grid(row=row, column=2, padx=5, pady=5)
        mrp.bind("<KeyRelease>", lambda event, r=row: self.update_total(r))

        total = tk.Label(self.billing_frame, text="0", width=10)
        total.grid(row=row, column=3, padx=5, pady=5)

        self.item_rows.append((item_name, quantity, mrp, total))

    def update_mrp(self, row):
        item_name = self.item_rows[row-1][0].get()
        mrp = next((item[1] for item in self.item_list if item[0] == item_name), 0)
        self.item_rows[row-1][2].delete(0, tk.END)
        self.item_rows[row-1][2].insert(0, str(mrp))
        self.update_total(row)

    def update_total(self, row):
        try:
            quantity = int(self.item_rows[row-1][1].get())
            mrp = float(self.item_rows[row-1][2].get())
            total = quantity * mrp
            self.item_rows[row-1][3].config(text=str(total))
        except ValueError:
            total = 0
            self.item_rows[row-1][3].config(text="0")
        self.calculate_grand_total()

    def calculate_grand_total(self):
        grand_total = sum(float(row[3].cget("text")) for row in self.item_rows)
        self.label_grand_total.config(text=f"Grand Total: {grand_total}")

    def open_bill_window(self):
        self.item_rows = []

        self.bill_window = tk.Toplevel(self.root)
        self.bill_window.title("Billing")
        self.bill_window.geometry("400x400")
        self.bill_window.configure(bg='light blue')

        tk.Label(self.bill_window, text="Welcome to Billing", font=("Times New Roman", 16), bg='light blue').pack(pady=10)

        self.billing_frame = tk.Frame(self.bill_window, bg='light blue')
        self.billing_frame.pack()

        headers = ["Product", "Quantity", "MRP", "Total"]
        for col, header in enumerate(headers):
            tk.Label(self.billing_frame, text=header, bg='light blue').grid(row=0, column=col, padx=5, pady=5)

        self.item_list = self.fetch_items()

        self.add_item_row()

        tk.Button(self.bill_window, text="Add Product ", command=self.add_item_row, width=20, height=2).pack(pady=10)
        tk.Button(self.bill_window, text="Calculate Grand Total", command=self.calculate_grand_total, width=20, height=2).pack(pady=10)

        self.label_grand_total = tk.Label(self.bill_window, text="Grand Total : ", font=("Times New Roman", 14), bg='light blue')
        self.label_grand_total.pack(pady=10)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryManagementStore(root)
    root.mainloop()

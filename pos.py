from tkinter import *
from tkinter import font
from tkinter import ttk
import tkinter.messagebox
import sqlite3
import bcrypt  # Hashing


# https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
def createUser(username: str, password: str, cursor: sqlite3.Cursor):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    cursor.execute("INSERT INTO user (uname, pwd) VALUES(?,?)",
                   (username, hashed))


# https://docs.python.org/3/library/sqlite3.html
# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
# https://stackoverflow.com/questions/26691504/python-sqlite3-data-is-not-saved-permanently

def auth(cur: sqlite3.Cursor, username, password):
    passwordByte = password.encode('utf-8')
    result = cur.execute(
        f"SELECT * FROM user WHERE uname='{username}'").fetchall()
    if result:
        # User exist, check password
        stored_pwd = result[0][1]
        return bcrypt.checkpw(passwordByte, stored_pwd)
    else:
        return False


with sqlite3.connect('POS.db') as conn:
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user(uname TEXT unique, pwd TEXT)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS product(pname TEXT, price INT, stock INT)"
    )

    # Create admin user if there isn't one
    if not cur.execute("SELECT * FROM user WHERE uname='admin'").fetchall():
        createUser('admin', 'admin', cur)
        print("Create admin")
    else:
        print("Admin exists")
        print(cur.execute(
            "SELECT * FROM user WHERE uname='admin'").fetchall())

    # Create dummy product
    if not cur.execute("SELECT * FROM product WHERE pname='DUMMY'").fetchall():
        cur.execute(
            "INSERT INTO product (pname, price, stock) VALUES(?,?,?)", ("DUMMY", 1, 500))
        print("Added dummy product")
    else:
        print("Dummy product exists")
        print(cur.execute("SELECT * FROM product WHERE pname='DUMMY'").fetchall())


class app:
    def __init__(self, master: Tk):
        self.master = master
        self.isLoggedIn = False
        # https://www.geeksforgeeks.org/how-to-change-default-font-in-tkinter/
        self.defaultFont = font.nametofont("TkDefaultFont")
        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family="Helvatica",
                                   size=16)

        self.width = 1200
        self.height = 900
        self.master.title("Point of Sale")
        self.master.geometry(f"{self.width}x{self.height}")
        self.login()

    def login(self):
        # Destroy old frame
        for i in self.master.winfo_children():
            i.destroy()
        # New frame
        self.frame1 = Frame(self.master, width=self.width, height=self.height)
        self.frame1.pack()
        # Text
        self.reg_txt = ttk.Label(self.frame1, text='Please Log In')
        self.reg_txt.pack()

        # Entry for Username/Password
        self.usernameLabel = ttk.Label(self.frame1, text="Username")
        self.usernameLabel.pack(pady=10)
        self.usernameEntry = ttk.Entry(self.frame1, font=16)
        self.usernameEntry.pack(pady=5)

        self.pwdLabel = ttk.Label(self.frame1, text="Password")
        self.pwdLabel.pack(pady=10)
        self.pwdEntry = ttk.Entry(self.frame1, show='*', font=(16))
        self.pwdEntry.pack(pady=5)

        # Back button
        self.register_btn = ttk.Button(
            self.frame1, text="Login", command=self.sale)
        self.register_btn.pack()

    def sale(self):

        if not auth(cur, self.usernameEntry.get(), self.pwdEntry.get()):
            tkinter.messagebox.showerror("Error", "Not Logged In")
            return

        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master, width=self.width, height=self.height)
        self.frame2.pack()
        self.reg_txt2 = ttk.Label(self.frame2, text='register')
        self.reg_txt2.pack()
        self.login_btn = ttk.Button(
            self.frame2, text="Logout", command=self.login)
        self.login_btn.pack()
        # List item
        # Loop through each item in the database list
        
        
    def register(self):
        pass


root = Tk()
app(root)
root.mainloop()

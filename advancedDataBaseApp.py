import tkinter as tk
from tkinter import ttk
import sqlite3


class Employee:
    conn = 0
    c = 0
    currEmployee = 0

    def setUp_db(self):
        self.conn = sqlite3.connect('tutorial.db')
        self.c = self.conn.cursor()
        try:
            self.c.execute("CREATE TABLE IF NOT EXISTS employees(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                           " Fname TEXT NOT NULL, Lname TEXT)")
            self.conn.commit()
        except sqlite3.OperationalError:
            print("UNABLE TO CREATE TABLE-> ERROR IN setup_db")

    def update_listbox(self):
        self.listbox.delete(0, "end")

        try:
            result = self.c.execute("SELECT * FROM employees")

            for row in result:
                listboxId = row[0]
                listboxFname = row[1]
                listboxLname = row[2]

                self.listbox.insert(listboxId,
                                    listboxFname + " " + listboxLname)
        except sqlite3.OperationalError:
            print("1->ERROR IN updat_listbox()->> unable to fetch from table ")

        except:
            print("1->ERROR IN updat_listbox()->> unable to fetch from table ")

    def submit(self):
        try:
            self.c.execute("INSERT INTO employees(Fname, Lname) Values(?,?)",
                           (self.fnEntry.get(), self.lnEntry.get()))
            self.conn.commit()

        except sqlite3.OperationalError:
            print("ERROR IN submit->> unable to insert into table")

        self.fnEntryBox.delete(0, "end")
        self.lnEntryBox.delete(0, "end")
        self.update_listbox()


    def update(self):
        try:
            self.c.execute("UPDATE employees SET Fname = ?, Lname = ? WHERE ID = ?",
                           (self.fnEntry.get(), self.lnEntry.get(), self.currEmployee))
            self.conn.commit()
            self.update_listbox()

        except sqlite3.OperationalError:
            print("ERROR IN update->> unable to update table.")

        self.fnEntryBox.delete(0, "end")
        self.lnEntryBox.delete(0, "end")


    def delete(self):
        try:
            self.c.execute("DELETE FROM employees WHERE ID = ?", self.currEmployee)
            self.conn.commit()
        except sqlite3.OperationalError:
            print("ERROR IN delete->> unable to deleete from the table.")

        self.fnEntryBox.delete(0, "end")
        self.lnEntryBox.delete(0, "end")
        self.update_listbox()



    def load_from_listbox(self, event=None):
        lb_widget = event.widget
        index = str(lb_widget.curselection()[0]+1)

        self.currEmployee = index

        try:
            result = self.c.execute("SELECT Fname ,Lname FROM employees WHERE ID = ?", index)

            for row in result:
                self.fnEntry.set(row[0])
                self.lnEntry.set(row[1])

        except sqlite3.OperationalError:
            print("ERROR IN load_from_listbox->> unable to fetch from the table")



    def __init__(self, root):
        root.title("EMPLOYEE TABLE")
        root.geometry("325x325")

        # ------1st row--------------

        fname_label = tk.Label(root, text = "FIRST NAME", font= 10)
        fname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.fnEntry = tk.StringVar(root, value="")
        self.fnEntryBox = ttk.Entry(root, textvariable=self.fnEntry)
        self.fnEntryBox.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="w"+"e")

        # ------2nd row--------------

        lname_label = tk.Label(root, text="LAST NAME", font=10)
        lname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.lnEntry = tk.StringVar(root, value="")
        self.lnEntryBox = ttk.Entry(root, textvariable=self.lnEntry)
        self.lnEntryBox.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="w"+"e")

        # ------3rd row--------------

        self.submitButton = ttk.Button(root, text="SUBMIT", command=lambda: self.submit())
        self.submitButton.grid(row=2, column=0, padx=4, pady=10)

        self.updateButton = ttk.Button(root, text="UPDATE", command=lambda: self.update())
        self.updateButton.grid(row=2, column=1, padx=4, pady=10)

        self.deleteButton = ttk.Button(root, text="DELETE", command=lambda: self.delete())
        self.deleteButton.grid(row=2, column=2, padx=4, pady=10)

        # -------LIST BOX----------

        self.listbox = tk.Listbox(root)
        self.listbox.bind('<<ListboxSelect>>', self.load_from_listbox)
        self.listbox.insert(0, "                       EMPLOYEE DATA SHOWS HERE")
        self.listbox.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="W"+"E")

        self.setUp_db()
        self.update_listbox()


root = tk.Tk()
app = Employee(root)
root.mainloop()

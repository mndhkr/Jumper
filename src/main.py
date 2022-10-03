
#   IMPORTED LIBRARIES

from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox
import customtkinter
import sqlite3
import rsa
import random
import pyperclip as pc
from PIL import Image, ImageTk
import os
from keys import *
import platform

# MAIN APP

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        #   DATABASE CONNECTION AND CREATION
       
        with sqlite3.connect("./data.db") as self.db:
            self.mycursor = self.db.cursor()
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS logins (username VARCHAR (1000), password VARCHAR (1000));")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS numbers (id INTEGER PRIMARY KEY, owner VARCHAR(1000), number VARCHAR(1000), notes VARCHAR(1000));")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS creditCards (id INTEGER PRIMARY KEY, type VARCHAR (50), number VARCHAR (50), email VARCHAR(50), password VARCHAR(50), notes VARCHAR(1000));")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, websiteOrApp VARCHAR(1000), username VARCHAR(1000), password VARCHAR(1000), notes VARCHAR(1000));")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS theme (theme1 VARCHAR(1000));")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS widgets (widgets1 VARCHAR(1000));")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS code (coding VARCHAR (1000));")
        self.db.commit()

        #   PATH SETUP

        self.PATH = os.path.dirname(os.path.realpath(__file__))

        #   ATTEMPTS FOR LOGIN && RECOVERY CODE

        self.attempts = []
        self.attemptsCode = []

        #   WINDOW SETUP

        if platform.system() == 'Linux':
            self.geometry("1050x500")
        elif platform.system() == 'Windows':
            self.geometry("1000x500")
        self.title("Jumper  v 1.4")
        self.resizable(False, False)
        customtkinter.deactivate_automatic_dpi_awareness()
        customtkinter.set_appearance_mode("dark")

        #   LAUNCH WIDNOW

        self.main()
    
    #   SIGNUP GUI

    def signup(self):
        for i in self.winfo_children():
            i.destroy()
        self.frameSign = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frameSign.pack(padx=20, pady=20, expand=True, fill='both')
        label = customtkinter.CTkLabel(master=self.frameSign, text="Signup", text_font=("Helvetica", 35))
        label.pack(pady= 40, padx=20)
        self.signUse = customtkinter.CTkEntry(master=self.frameSign, placeholder_text="Username (definitive, max. 16)", width=300, height=35, text_font=("Helvetica", 13))
        self.signUse.pack(padx=20, pady=5)
        self.signPas = customtkinter.CTkEntry(show="*", master=self.frameSign, placeholder_text="Password (min. 8, max. 64)", width=300, height=35, text_font=("Helvetica", 13))
        self.signPas.pack(padx=20, pady=5)
        self.signPasr = customtkinter.CTkEntry(show="*",master=self.frameSign, placeholder_text="Repeat password", width=300, height=35, text_font=("Helvetica", 13))
        self.signPasr.pack(padx=20, pady=5)
        space = customtkinter.CTkLabel(master=self.frameSign, text="")
        space.pack(pady= 0, padx=20)
        button = customtkinter.CTkButton(master=self.frameSign, text="Enter", width=160, height=40, text_font=("Helvetica", 14), command=lambda *args, **kwargs: self.saveAccount(self.signUse.get(), self.signPas.get(), self.signPasr.get()))
        button.pack(padx=10, pady=10)
        button2 = customtkinter.CTkButton(master=self.frameSign, text="Back To The Menu", command=self.menu, width=180, height=40, text_font=("Helvetica", 14))
        button2.pack(padx=10, pady=0)

    #   SIGNUP TECHNICAL FUNCTION

    def saveAccount(self, x, y, z):
        if len(y) >= 8 and len(x) >= 1  and len(x) <= 16 and len(y) <= 64:
            if y == z:
                self.mycursor.execute("SELECT COUNT(username) FROM logins;")
                result = self.mycursor.fetchone()[0]
                if result < 1:
                    hashcr = rsa.encrypt(x.encode(), publicKey)
                    hash1 = rsa.encrypt(y.encode(), publicKey)
                    sql = "INSERT INTO logins (username, password) VALUES (?, ?);"
                    self.mycursor.execute(sql, [(hashcr), (hash1)])
                    self.db.commit()
                    return self.recoveryCode()
                else:
                    MessageBox.showerror("Warning!","You already have an account!")
            else:
                MessageBox.showerror("Warning!","Passwords don't match! Please try again.")
        else:
            MessageBox.showerror("Warning!","Invalid credentials! Try again with new credentials.")
        self.signUse.delete(0, END)
        self.signPas.delete(0, END)
        self.signPasr.delete(0, END)

    #   RECOVERY CODE GENERATOR

    def recoveryCode(self):
        for i in self.winfo_children():
            i.destroy()
        self.code =  str(random.randint(111111, 999999))
        self.encryptedCode = rsa.encrypt(self.code.encode(), publicKey)
        sql = "INSERT INTO code (coding) VALUES (?);"
        self.mycursor.execute(sql, [(self.encryptedCode)])
        self.db.commit()
        self.frameCode = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frameCode.pack(padx=20, pady=20, expand=True, fill='both')
        space = customtkinter.CTkLabel(master=self.frameCode, text="")
        space.pack(pady= 5, padx=20)
        label = customtkinter.CTkLabel(master=self.frameCode, text="Recovery Code", text_font=("Helvetica", 35))
        label.pack(pady= 0, padx=20)
        label = customtkinter.CTkLabel(master=self.frameCode, text="This is your new recovery code. You will need it in case of lost password.", text_font=("Helvetica", 15))
        label.pack(pady= 15, padx=20)
        rc = customtkinter.CTkLabel(master=self.frameCode, text=self.code, text_font=("Helvetica", 25), fg_color="#3E3E3E", corner_radius=8)
        rc.pack(pady=42, padx=410, fill='x')
        space = customtkinter.CTkLabel(master=self.frameCode, text="")
        space.pack(pady= 0, padx=20)
        button = customtkinter.CTkButton(master=self.frameCode, text="Copy Code", width=160, height=40, text_font=("Helvetica", 14), command=lambda *args, **kwargs: pc.copy(self.code))
        button.pack(padx=10, pady=10)
        button1 = customtkinter.CTkButton(master=self.frameCode, text="Continue", width=160, height=40, text_font=("Helvetica", 14), command=self.main)
        button1.pack(padx=10, pady=0)

    #   LOGIN GUI

    def login(self):
        for i in self.winfo_children():
            i.destroy()
        self.frameLog = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frameLog.pack(padx=20, pady=20, expand=True, fill='both')
        label = customtkinter.CTkLabel(master=self.frameLog, text="Login", text_font=("Helvetica", 35))
        label.pack(pady= 40, padx=20)
        self.loginUser = customtkinter.CTkEntry(master=self.frameLog, placeholder_text="Username", width=300, height=35, text_font=("Helvetica", 13))
        self.loginUser.pack(padx=20, pady=5)
        self.loginPas = customtkinter.CTkEntry(show="*", master=self.frameLog, placeholder_text="Password", width=300, height=35, text_font=("Helvetica", 13))
        self.loginPas.pack(padx=20, pady=5)
        checkboxLog = customtkinter.CTkCheckBox(master=self.frameLog, text="Show/Hide Password", command=lambda *args, **kwargs: self.HideSee(checkboxLog, self.loginPas), onvalue="on", offvalue="off", width=30, height=30, text_font=("Helvetica", 12))
        checkboxLog.pack(padx=20, pady=10)
        checkboxLog.deselect()
        space = customtkinter.CTkLabel(master=self.frameLog, text="")
        space.pack(pady= 0, padx=20)
        button = customtkinter.CTkButton(master=self.frameLog, text="Enter", width=160, height=40, text_font=("Helvetica", 14), command=lambda *args, **kwargs: self.checkPassword(self.loginUser.get(), self.loginPas.get()))
        button.pack(padx=10, pady=10)
        button2 = customtkinter.CTkButton(master=self.frameLog, text="Back To The Menu", command=self.menu, width=180, height=40, text_font=("Helvetica", 14))
        button2.pack(padx=10, pady=0)

    #   SHOW HIDE PASSWORD

    def HideSee(self, x, y):
        if x.get() == 'on':
            y.configure(show="")
        else:
            y.configure(show="*")

    #   LOGIN TECHNICAL FUNCTION

    def checkPassword(self, x, y):
        self.mycursor.execute("SELECT * FROM logins;")
        cr = self.mycursor.fetchall()
        for hashc, j in cr:
            hashc = rsa.decrypt(hashc, privateKey).decode()
            j = rsa.decrypt(j, privateKey).decode()
            if hashc == x and j == y:
                self.attempts = []
                return self.main()
        self.attempts.append(1)
        if len(self.attempts) < 5:
            MessageBox.showerror("Warning!","Incorrect credentials! Try again.")
            self.loginUser.delete(0, END)
            self.loginPas.delete(0, END)
        else:
            MessageBox.showerror("Warning!","You have failed 5 attempts in a row!")
            self.attempts = []
            return self.recoveryPassword()

    #   RECOVERY PASSWORD PAGE

    def recoveryPassword(self):
        for i in self.winfo_children():
            i.destroy()
        self.frameRecPa = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frameRecPa.pack(padx=20, pady=20, expand=True, fill='both')
        label = customtkinter.CTkLabel(master=self.frameRecPa, text="Password Lost", text_font=("Helvetica", 35))
        label.pack(pady= 40, padx=20)
        self.recCode = customtkinter.CTkEntry(show="*", master=self.frameRecPa, placeholder_text="8 digits recovery code", width=300, height=35, text_font=("Helvetica", 13))
        self.recCode.pack(padx=20, pady=15)
        space = customtkinter.CTkLabel(master=self.frameRecPa, text="")
        space.pack(pady= 10, padx=20)
        button = customtkinter.CTkButton(master=self.frameRecPa, text="Enter", width=160, height=40, text_font=("Helvetica", 14), command=lambda *args, **kwargs: self.checkCode(self.recCode.get()))
        button.pack(padx=10, pady=10)
        button2 = customtkinter.CTkButton(master=self.frameRecPa, text="Exit", command=self.bye1, width=180, height=40, text_font=("Helvetica", 14))
        button2.pack(padx=10, pady=0)

    #    RECOVERY PASSWORD TECHNICAL FUNCTION

    def checkCode(self, x):
        self.mycursor.execute("SELECT * FROM code;")
        getcode = self.mycursor.fetchone()
        if getcode:
            for cod in getcode:
                newcod = rsa.decrypt(cod, privateKey).decode()
            if x == newcod:
                self.mycursor.execute("DELETE FROM code;")
                self.attemptsCode = []
                return self.recoveryCode()
        self.attemptsCode.append(1)
        if len(self.attemptsCode) < 3:
            MessageBox.showerror("Warning!","Incorrect recovery code! Try again.")
            self.recCode.delete(0, END)
        else:
            MessageBox.showerror("Warning!","You have failed 3 recovery password attempts in a row!")
            return self.destroy()

    #   EXIT PROGRAM

    def bye(self):
        if MessageBox.askyesno("Before continuing","Are you sure you want to quit?"):
            self.destroy()
        else:
            return self.menu()
    
    def bye1(self):
        if MessageBox.askyesno("Before continuing","Are you sure you want to quit?"):
            self.destroy()
        else:
            return self.recoveryPassword()

    #   LANDING PAGE

    def menu(self):
        for i in self.winfo_children():
            i.destroy()
        self.frameMenu = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frameMenu.pack(padx=20, pady=20, expand=True, fill='both')
        label = customtkinter.CTkLabel(master=self.frameMenu, text="Welcome to Jumper!", text_font=("Helvetica", 35))
        label.pack(pady= 50, padx=20)
        button = customtkinter.CTkButton(master=self.frameMenu, text="Signup", command=self.signup, width=160, height=40, text_font=("Helvetica", 14))
        button.pack(padx=10, pady=5)
        button1 = customtkinter.CTkButton(master=self.frameMenu, text="Login", command=self.login, width=160, height=40, text_font=("Helvetica", 14))
        button1.pack(padx=10, pady=5)
        button2 = customtkinter.CTkButton(master=self.frameMenu, text="Exit", command=self.bye, width=160, height=40, text_font=("Helvetica", 14))
        button2.pack(padx=10, pady=5)
        label = customtkinter.CTkLabel(master=self.frameMenu, text="Created by Alessandro Bottini", text_font=("Helvetica", 12))
        label.pack(pady=60)

    #   ACCESSIBILITY PAGE

    def accessibility(self):
        for i in self.winfo_children():
            i.destroy()
        self.frameMainUp1 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frameMainUp1.pack(fill='x')
        if platform.system() == 'Linux':
            button = customtkinter.CTkButton(master=self.frameMainUp1, text="Settings", width=326, text_font=("Helvetica", 14), corner_radius=0, height=50)
            button1 = customtkinter.CTkButton(master=self.frameMainUp1, text="Accessibility", width=326, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.accessibility)
            button2 = customtkinter.CTkButton(master=self.frameMainUp1, text="License", width=326, text_font=("Helvetica", 14), corner_radius=0, height=50)
            self.home_image = self.load_image("/img/home.png", 35)
            button3 = customtkinter.CTkButton(master=self.frameMainUp1, text="", image=self.home_image, width=72, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.menu)
        elif platform.system() == 'Windows':
            button = customtkinter.CTkButton(master=self.frameMainUp1, text="Settings", width=310, text_font=("Helvetica", 14), corner_radius=0, height=50)
            button1 = customtkinter.CTkButton(master=self.frameMainUp1, text="Accessibility", width=310, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.accessibility)
            button2 = customtkinter.CTkButton(master=self.frameMainUp1, text="License", width=310, text_font=("Helvetica", 14), corner_radius=0, height=50)
            self.home_image = self.load_image("/img/home.png", 35)
            button3 = customtkinter.CTkButton(master=self.frameMainUp1, text="", image=self.home_image, width=70, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.menu)
        button.grid(row=0, column=0, sticky='nw')
        button1.grid(row=0, column=1, sticky='nw')
        button2.grid(row=0, column=2, sticky='nw')
        button3.grid(row=0, column=3, sticky='nw')
        self.frameAccs = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frameAccs.pack(padx=19, pady=19, expand=True, fill='both')

    #   MAIN PAGE

    def main(self):
        for i in self.winfo_children():
            i.destroy()
        self.frameMainUp = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frameMainUp.pack(fill='x')
        if platform.system() == 'Linux':
            button = customtkinter.CTkButton(master=self.frameMainUp, text="Settings", width=326, text_font=("Helvetica", 14), corner_radius=0, height=50)
            button1 = customtkinter.CTkButton(master=self.frameMainUp, text="Accessibility", width=326, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.accessibility)
            button2 = customtkinter.CTkButton(master=self.frameMainUp, text="License", width=326, text_font=("Helvetica", 14), corner_radius=0, height=50)
            self.home_image = self.load_image("/img/home.png", 35)
            button3 = customtkinter.CTkButton(master=self.frameMainUp, text="", image=self.home_image, width=72, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.menu)
        elif platform.system() == 'Windows':
            button = customtkinter.CTkButton(master=self.frameMainUp, text="Settings", width=310, text_font=("Helvetica", 14), corner_radius=0, height=50)
            button1 = customtkinter.CTkButton(master=self.frameMainUp, text="Accessibility", width=310, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.accessibility)
            button2 = customtkinter.CTkButton(master=self.frameMainUp, text="License", width=310, text_font=("Helvetica", 14), corner_radius=0, height=50)
            self.home_image = self.load_image("/img/home.png", 35)
            button3 = customtkinter.CTkButton(master=self.frameMainUp, text="", image=self.home_image, width=70, text_font=("Helvetica", 14), corner_radius=0, height=50, command=self.menu)
        button.grid(row=0, column=0, sticky='nw')
        button1.grid(row=0, column=1, sticky='nw')
        button2.grid(row=0, column=2, sticky='nw')
        button3.grid(row=0, column=3, sticky='nw')
        self.frameMainCenter = customtkinter.CTkFrame(master=self)
        self.frameMainCenter.pack(fill='both', expand=True)
        self.canvas = Canvas(master=self.frameMainCenter, background='#2a2d2e')
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(self.frameMainCenter, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.secondFrame = customtkinter.CTkFrame(master=self.canvas, width=980)
        self.canvas.create_window((0, 0), window=self.secondFrame, anchor='nw')
        self.thirdFrame = customtkinter.CTkFrame(master=self.secondFrame, width=950, height=440)
        self.thirdFrame.pack(pady=20, padx=10)

        #   PHONE NUMBERS SECTION

        def addNumber(x , y, z):
            if len(x) >= 1 and len(x) <= 20 and len(y) >= 1 and len(y) <= 20 and len(z) >= 1 and len(z) <= 70:
                self.mycursor.execute("SELECT COUNT(id) FROM numbers;")
                result =self. mycursor.fetchone()
                for i in result:
                    pass
                if i <= 20:
                    encryptedNum = rsa.encrypt(x.encode(), publicKeyNumbers)
                    encryptedNum1 = rsa.encrypt(y.encode(), publicKeyNumbers)
                    encryptedNum2 = rsa.encrypt(z.encode(), publicKeyNumbers)
                    sql = "INSERT INTO numbers (owner, number, notes) VALUES (?, ?, ?);"
                    self.mycursor.execute(sql, [(encryptedNum), (encryptedNum1), (encryptedNum2)])
                    self.db.commit()
                    self.main()
                else:
                    MessageBox.showerror("Warning!","You have reached the limit of data that can be added!")
            else:
                MessageBox.showerror("Warning!", "Please insert valide parameters!")
            self.InputNum.delete(0, END)
            self.InputNum1.delete(0, END)
            self.InputNum2.delete(0, END)

        self.framePhone = customtkinter.CTkFrame(master=self.thirdFrame, width=298, height=410)
        self.framePhone.grid(row=0, column=0, pady=13, padx=13, sticky='n')
        label = customtkinter.CTkLabel(master=self.framePhone, text="Phone Numbers", text_font=("Helvetica", 16))
        label.pack(pady= 50, padx=20)
        self.InputNum = customtkinter.CTkEntry(master=self.framePhone, placeholder_text="Owner Name", width=258, height=35, text_font=("Helvetica", 11))
        self.InputNum.pack(padx=20, pady=4)
        self.InputNum1 = customtkinter.CTkEntry(master=self.framePhone, placeholder_text="Number", width=258, height=35, text_font=("Helvetica", 11))
        self.InputNum1.pack(padx=20, pady=4)
        self.InputNum2 = customtkinter.CTkEntry(master=self.framePhone, placeholder_text="Notes (max 70 characters)", width=258, height=35, text_font=("Helvetica", 11))
        self.InputNum2.pack(padx=20, pady=4)
        button = customtkinter.CTkButton(master=self.framePhone, text="Add New", command=lambda *args, **kwargs : addNumber(self.InputNum.get(), self.InputNum1.get(), self.InputNum2.get()), width=140, height=40, text_font=("Helvetica", 12))
        button.pack(padx=10, pady=52)

        #   CREDIT CARDS SECTION

        self.frameCC = customtkinter.CTkFrame(master=self.thirdFrame, width=298, height=410)
        self.frameCC.grid(row=0, column=1, pady=13, sticky='n')
        space = customtkinter.CTkLabel(master=self.frameCC, text="")
        space.grid(pady= 9, padx=20, row=0, column=0)
        label = customtkinter.CTkLabel(master=self.frameCC, text="Credit Cards", text_font=("Helvetica", 16))
        label.grid(pady= 0, padx=20, row=1, column=0)
        space = customtkinter.CTkLabel(master=self.frameCC, text="")
        space.grid(pady= 2, padx=20, row=2, column=0)
        inputCC = customtkinter.CTkEntry(master=self.frameCC, placeholder_text="Card Name", width=258, height=35, text_font=("Helvetica", 11))
        inputCC.grid(padx=20, pady=4, row=3, column=0)
        inputCC1 = customtkinter.CTkEntry(master=self.frameCC, placeholder_text="Owner", width=258, height=35, text_font=("Helvetica", 11))
        inputCC1.grid(padx=20, pady=4, row=5, column=0)
        inputCC2 = customtkinter.CTkEntry(master=self.frameCC, placeholder_text="Card Number", width=258, height=35, text_font=("Helvetica", 11))
        inputCC2.grid(padx=20, pady=4, row=6, column=0)
        self.frameCC1 = customtkinter.CTkFrame(master=self.frameCC, width=287, height=40, fg_color="#2a2d2e")
        self.frameCC1.grid(row=7, column=0, pady=0, sticky='w')
        inputCC3 = customtkinter.CTkEntry(master=self.frameCC1, placeholder_text="Date (MM/YY)", width=118, height=35, text_font=("Helvetica", 11))
        inputCC3.grid(padx=20, pady=4, row=0, column=0, sticky='w')
        inputCC4 = customtkinter.CTkEntry(master=self.frameCC1, placeholder_text="CVV/CVC", width=118, height=35, text_font=("Helvetica", 11))
        inputCC4.grid(padx=0, pady=4, row=0, column=1, sticky='w')
        button = customtkinter.CTkButton(master=self.frameCC, text="Add New", width=140, height=40, text_font=("Helvetica", 12))
        button.grid(row=8, column=0, pady=27)
        space = customtkinter.CTkLabel(master=self.frameCC, text="")
        space.grid(pady= 0, padx=20, row=9, column=0)

        #   PASSWORDS SECTION

        self.framePassw = customtkinter.CTkFrame(master=self.thirdFrame, width=298, height=410)
        self.framePassw.grid(row=0, column=2, pady=13, padx=13, sticky='n')
        space = customtkinter.CTkLabel(master=self.framePassw, text="")
        space.pack(pady= 7, padx=20)
        label = customtkinter.CTkLabel(master=self.framePassw, text="Passwords", text_font=("Helvetica", 16))
        label.pack(pady= 0, padx=20)
        space = customtkinter.CTkLabel(master=self.framePassw, text="")
        space.pack(pady= 2, padx=20)
        inputPass = customtkinter.CTkEntry(master=self.framePassw, placeholder_text="Software/Website", width=258, height=35, text_font=("Helvetica", 11))
        inputPass.pack(padx=20, pady=4)
        inputPass1 = customtkinter.CTkEntry(master=self.framePassw, placeholder_text="Username/Email", width=258, height=35, text_font=("Helvetica", 11))
        inputPass1.pack(padx=20, pady=4)
        inputPass2 = customtkinter.CTkEntry(master=self.framePassw, placeholder_text="Password", width=258, height=35, text_font=("Helvetica", 11))
        inputPass2.pack(padx=20, pady=4)
        inputPass3 = customtkinter.CTkEntry(master=self.framePassw, placeholder_text="Notes (max 70 characters)", width=258, height=35, text_font=("Helvetica", 11))
        inputPass3.pack(padx=20, pady=4)
        button = customtkinter.CTkButton(master=self.framePassw, text="Add New", width=140, height=40, text_font=("Helvetica", 12))
        button.pack(padx=10, pady=29)
        space = customtkinter.CTkLabel(master=self.framePassw, text="")
        space.pack(pady= 0, padx=20)

        #   PHONE NUMBERS LIST

        self.PhoneList = customtkinter.CTkFrame(master=self.secondFrame, width=950, height=440)
        self.PhoneList.pack(pady=40, padx=20) 
        space = customtkinter.CTkLabel(master=self.PhoneList, text="")
        space.pack(pady= 0, padx=20) 
        label = customtkinter.CTkLabel(master=self.PhoneList, text="Phone Numbers", text_font=("Helvetica",20))
        label.pack(pady= 10, padx=20)      
        self.PhoneTreeview = customtkinter.CTkFrame(master=self.PhoneList, width=298, height=410)
        self.PhoneTreeview.pack(pady=20, padx=13)
        self.mycursor.execute("SELECT id, owner, number, notes FROM numbers;")
        rows = self.mycursor.fetchall()
        self.tree = ttk.Treeview(self.PhoneTreeview, selectmode='browse')
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", font=(None, 12))
        self.tree.pack(pady=20, padx=20, expand=True, fill='both')
        self.tree.bind('<Motion>', 'break')
        self.tree["columns"] = ("1", "2", "3", "4")
        self.tree['show'] = 'headings'
        self.tree.column("1", width=70, anchor='c')
        self.tree.column("2", width=230, anchor='c')
        self.tree.column("3", width=230, anchor='c')
        self.tree.column("4", width=400, anchor='c')
        self.tree.heading("1", text="ID")
        self.tree.heading("2", text="Owner")
        self.tree.heading("3", text="Number")
        self.tree.heading("4", text="Notes")
        for id, owner, number, notes in rows:
            decryptNum1 = rsa.decrypt(owner, privateKeyNumbers).decode()
            decryptNum2 = rsa.decrypt(number, privateKeyNumbers).decode()
            decryptNum3 = rsa.decrypt(notes, privateKeyNumbers).decode()
            self.tree.insert('', 'end', values=(id, decryptNum1, decryptNum2, decryptNum3))
        space = customtkinter.CTkLabel(master=self.PhoneTreeview, text="")
        space.pack(pady= 0, padx=20)
        button = customtkinter.CTkButton(master=self.PhoneTreeview, text="Delete", width=140, height=40, text_font=("Helvetica", 12), command=lambda *args, **kwargs : self.remove(self.tree))
        button.pack(padx=10, pady=0)
        space = customtkinter.CTkLabel(master=self.PhoneTreeview, text="")
        space.pack(pady= 0, padx=20)

    #   DELETE A ROW FROM THE LIST

    def remove(self, x):
        y = x.selection()[0]
        x.delete(y)
        #self.mycursor.execute("DELETE FROM numbers WHERE ")

    #   LOAD IMAGES

    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open(self.PATH + path).resize((image_size, image_size)))

if __name__ == "__main__":
    app = App()
    app.mainloop()
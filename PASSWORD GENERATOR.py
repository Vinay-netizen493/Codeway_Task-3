import string
import random
import sqlite3
from tkinter import *
from tkinter import messagebox


class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()
        
        master.title('Password Generator')
        master.config(bg='#FFDAB9')  # Light Peach color
        master.resizable(False, False)

        self.label = Label(text=":PASSWORD GENERATOR:", anchor=N, fg='#800080', bg='#FFDAB9', font='arial 20 bold underline')  # Purple color
        self.label.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky='n')  # Centered across 3 columns

        Label(text="Enter User Name: ", font='times 15 bold', bg='#FFDAB9', fg='#FFA500', pady=5).grid(row=1, column=0, padx=10, sticky='e')  # Light Orange color
        self.textfield = Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.textfield.focus_set()

        Label(text="Enter Password Length: ", font='times 15 bold', bg='#FFDAB9', fg='#FFA500', pady=5).grid(row=2, column=0, padx=10, sticky='e')  # Light Orange color
        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        Label(text="Generated Password: ", font='times 15 bold', bg='#FFDAB9', fg='#FFA500', pady=5).grid(row=3, column=0, padx=10, sticky='e')  # Light Orange color
        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#4682B4')  # Bluish color
        self.generated_password_textfield.grid(row=3, column=1, padx=10, pady=5, sticky='w')
   
        Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#4682B4', bg='#BCEE68', command=self.generate_pass).grid(row=4, column=1, pady=(20, 10))  # Bluish color

        Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#4682B4', bg='#FFFAF0', command=self.accept_fields).grid(row=5, column=1, pady=10)  # Bluish color

        Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#4682B4', bg='#FFFAF0', command=self.reset_fields).grid(row=6, column=1, pady=(10, 20))  # Bluish color

        # Configure column weights
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(2, weight=1)
        
        # Configure row weights
        for i in range(7):
            master.grid_rowconfigure(i, weight=1)


    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"
        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)
        name = self.textfield.get()
        leng = self.length_textfield.get()

        if name == "":
            messagebox.showerror("Error","Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error","Name must be a string")
            self.textfield.delete(0, END)
            return

        length = int(leng) 

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            self.textfield.delete(0, END)
            return

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.generated_password_textfield.delete(0, END)
        self.generated_password_textfield.insert(0, gen_passwd)
        self.generatedpassword.set(gen_passwd)


    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(self.n_username.get())])

            if cursor.fetchall():
                messagebox.showerror("This username already exists!", "Please use another username")
            else:
                insert = "INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)"
                cursor.execute(insert, (self.n_username.get(), self.generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success!", "Password generated successfully")


    def reset_fields(self):
        self.textfield.delete(0, END)
        self.length_textfield.delete(0, END)
        self.generated_password_textfield.delete(0, END)


if __name__=='__main__':
    root = Tk()
    pass_gen = GUI(root)
    
    # Centering the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 450
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    root.mainloop()

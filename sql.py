import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Connect to the MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="user_name",
    password="Your_password", #
    database="database_name" ,
)

cursor = db.cursor()
class LibraryManagementApp:
    def __init__(self, window):  # Renamed root to window
        self.root = window
        self.root.title("Library Management System")
        self.root.geometry("800x500")

        # Title
        title_label = tk.Label(window, text="Library Management System", font=("Arial", 24, "bold"), bg="blue", fg="white")
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Form frame
        form_frame = tk.Frame(window, bd=4, relief=tk.RIDGE, bg="lightgray")
        form_frame.place(x=20, y=60, width=350, height=700)

        tk.Label(form_frame, text="Title", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        tk.Label(form_frame, text="Author", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        tk.Label(form_frame, text="Genre", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        tk.Label(form_frame, text="Year", font=("Arial", 12)).grid(row=3, column=0, pady=10, padx=10, sticky="w")
        tk.Label(form_frame, text="Copies", font=("Arial", 12)).grid(row=4, column=0, pady=10, padx=10, sticky="w")

        # Input fields
        self.title_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.title_entry.grid(row=0, column=1, pady=10, padx=10)

        self.author_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.author_entry.grid(row=1, column=1, pady=10, padx=10)

        self.genre_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.genre_entry.grid(row=2, column=1, pady=10, padx=10)

        self.year_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.year_entry.grid(row=3, column=1, pady=10, padx=10)

        self.copies_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.copies_entry.grid(row=4, column=1, pady=10, padx=10)

        # Buttons
        button_frame = tk.Frame(form_frame, bg="lightgray")
        button_frame.place(x=15, y=300, width=310)

        tk.Button(button_frame, text="Add", command=self.add_book, font=("Arial", 10), width=10, bg="green", fg="white").grid(row=0, column=0, padx=5, pady=10)
        tk.Button(button_frame, text="Update", command=self.update_book, font=("Arial", 10), width=10, bg="orange", fg="white").grid(row=0, column=1, padx=5, pady=10)
        tk.Button(button_frame, text="Delete", command=self.delete_book, font=("Arial", 10), width=10, bg="red", fg="white").grid(row=0, column=2, padx=5, pady=10)

        # Display frame
        display_frame = tk.Frame(window, bd=4, relief=tk.RIDGE, bg="lightgray")
        display_frame.place(x=400, y=60, width=1000, height=700)

        tk.Label(display_frame, text="Books List", font=("Arial", 14, "bold"), bg="lightgray").pack(side=tk.TOP, fill=tk.X)

        # Table
        self.tree = ttk.Treeview(display_frame, columns=("ID", "Title", "Author", "Genre", "Year", "Copies"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Copies", text="Copies")
        self.tree.column("ID", width=10)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select_book)
        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM books")
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.copies_entry.delete(0, tk.END)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        copies = self.copies_entry.get()

        if title and author and genre and year and copies:
            cursor.execute("INSERT INTO books (title, author, genre, year, copies) VALUES (%s, %s, %s, %s, %s)",
                           (title, author, genre, int(year), int(copies)))
            db.commit()
            messagebox.showinfo("Success", "Book added successfully.")
            self.load_data()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def select_book(self, _event):
        selected_row = self.tree.focus()
        values = self.tree.item(selected_row, "values")
        if values:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])

            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, values[2])

            self.genre_entry.delete(0, tk.END)
            self.genre_entry.insert(0, values[3])

            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, values[4])

            self.copies_entry.delete(0, tk.END)
            self.copies_entry.insert(0, values[5])

    def update_book(self):
        selected_row = self.tree.focus()
        values = self.tree.item(selected_row, "values")
        if values:
            book_id = values[0]
            title = self.title_entry.get()
            author = self.author_entry.get()
            genre = self.genre_entry.get()
            year = self.year_entry.get()
            copies = self.copies_entry.get()

            cursor.execute("UPDATE books SET title=%s, author=%s, genre=%s, year=%s, copies=%s WHERE id=%s",
                           (title, author, genre, int(year), int(copies), book_id))
            db.commit()
            messagebox.showinfo("Success", "Book updated successfully.")
            self.load_data()
            self.clear_entries()

    def delete_book(self):
        selected_row = self.tree.focus()
        values = self.tree.item(selected_row, "values")
        if values:
            book_id = values[0]
            cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            db.commit()
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.load_data()
            self.clear_entries()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()

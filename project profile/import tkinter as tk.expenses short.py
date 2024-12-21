import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x1070')  # Adjust window size
        self.root.title("PE'X")

        self.bg_label = None
        self.set_background_image()

        # Set window icon
        self.icon_image = tk.PhotoImage(file=r'C:\Users\diamo\OneDrive\Pictures\10d395485c8e5e5bafb9751bd62534d7.png')
        self.root.iconphoto(True, self.icon_image)

        # Initialize balance and expenses
        self.salary = 0
        self.total_expenses = 0
        self.expenses = []
        self.category_limits = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Other": 0}

        self.create_main_screen()
        self.root.bind("<Configure>", self.on_resize)

    def set_background_image(self):
        # Set the background image to cover window size
        self.bg_image = Image.open(r'C:\Users\diamo\OneDrive\Pictures\finance_money_and_investment.jpg')
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.bg_photo

    def on_resize(self, event):
        # Resize the background image on window resize
        resized_image = self.bg_image.resize((event.width, event.height))
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo

    def create_main_screen(self):
        self.clear_screen()
        self.create_title()  # Add title "PEX TRACK"
        self.create_salary_section()
        self.create_category_limits_section()
        self.create_expense_input_section()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def create_title(self):
        # Create and place title "PEX TRACK" at the top
        title_label = tk.Label(self.root, text="PEX TRACK", font=('Helvetica', 20, 'bold'), fg='black')
        title_label.pack(pady=20)  # Adds padding around the title

    def create_salary_section(self):
        # Salary input section with an option to show/hide
        self.salary_frame = self.create_input_frame("Enter Your Salary:", self.set_salary)
        self.salary_frame.pack(pady=20, fill=tk.X, padx=30)

    def create_input_frame(self, label_text, command):
        # Helper function to create input frames
        frame = tk.Frame(self.root, relief="solid", bd=2, padx=10, pady=10)
        label = tk.Label(frame, text=label_text, font=('Helvetica', 12))
        label.grid(row=0, column=0, padx=5, pady=5)
        entry = tk.Entry(frame, font=('Helvetica', 12))
        entry.grid(row=0, column=1, padx=5, pady=5)
        button = tk.Button(frame, text="Done", command=lambda: command(entry), relief="raised", font=('Helvetica', 10, 'bold'))
        button.grid(row=1, column=0, columnspan=2, pady=10)
        return frame

    def set_salary(self, entry):
        try:
            self.salary = float(entry.get())
            self.update_totals()
        except ValueError:
            messagebox.showerror("Error", "Invalid salary input.")

    def create_category_limits_section(self):
        # Category limit input section
        category_limit_frame = tk.Frame(self.root, relief="solid", bd=2, padx=10, pady=10)
        category_limit_frame.pack(pady=20, fill=tk.X, padx=30)

        tk.Label(category_limit_frame, text="Set Category Limits:", font=('Helvetica', 12)).grid(row=0, column=0, columnspan=2)

        self.entries = self.create_category_input(category_limit_frame)
        tk.Button(category_limit_frame, text="Set Category Limits", command=self.set_category_limits, relief="raised", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, columnspan=2)

    def create_category_input(self, parent_frame):
        # Function to create category limit entries
        entries = {}
        categories = ["Food", "Transportation", "Entertainment", "Other"]
        for i, category in enumerate(categories):
            tk.Label(parent_frame, text=f"{category} Limit:", font=('Helvetica', 12)).grid(row=i+1, column=0, padx=5, pady=5)
            entry = tk.Entry(parent_frame, font=('Helvetica', 12))
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            entries[category] = entry
        return entries

    def set_category_limits(self):
        try:
            # Set the category limits from the input
            for category, entry in self.entries.items():
                self.category_limits[category] = float(entry.get())
            messagebox.showinfo("Category Limits", "Category limits set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid category limit input.")

    def create_expense_input_section(self):
        # Expense input section
        frame = tk.Frame(self.root, relief="solid", bd=2, padx=10, pady=10)
        frame.pack(pady=20, fill=tk.X, padx=30)

        tk.Label(frame, text="Expense Category:", font=('Helvetica', 12)).grid(row=0, column=0, padx=5, pady=5)

        self.category_var = tk.StringVar(value="Food")
        tk.OptionMenu(frame, self.category_var, "Food", "Transportation", "Entertainment", "Other").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Enter Expense Amount:", font=('Helvetica', 12)).grid(row=1, column=0, padx=5, pady=5)
        self.entry_expense = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_expense.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Expense", command=self.add_expense, relief="raised", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, columnspan=2, pady=10)

        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.pack(pady=10, fill=tk.X, padx=30)

        self.listbox = tk.Listbox(self.listbox_frame, width=50, height=10, font=('Helvetica', 10), bd=2)
        self.listbox.pack(side=tk.LEFT, padx=10)

        scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.total_label = tk.Label(self.root, text="Total Expenses: ₱0.00", font=('Helvetica', 12, 'bold'))
        self.remaining_label = tk.Label(self.root, text="Remaining Salary: ₱0.00", font=('Helvetica', 12, 'bold'))
        self.total_label.pack(pady=10)
        self.remaining_label.pack(pady=10)

        tk.Button(self.root, text="Analyze Expenses", command=self.analyze_expenses, relief="raised", font=('Helvetica', 10, 'bold')).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, relief="raised", font=('Helvetica', 10, 'bold')).pack(pady=10)

    def add_expense(self):
        try:
            expense = float(self.entry_expense.get())
            if expense <= 0:
                raise ValueError("Expense must be positive.")
            category = self.category_var.get()

            if expense + self.get_category_total(category) > self.category_limits[category]:
                messagebox.showerror("Error", f"{category} expense exceeds the limit")
                return

            self.expenses.append((category, expense))
            self.listbox.insert(tk.END, f"{category}: ₱{expense:.0f}")
            self.update_totals()
            self.entry_expense.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid expense input.")

    def get_category_total(self, category):
        # Calculate total for a specific category
        return sum(expense for cat, expense in self.expenses if cat == category)

    def update_totals(self):
        # Update total expenses and remaining salary
        self.total_expenses = sum(exp for _, exp in self.expenses)
        remaining = self.salary - self.total_expenses
        if remaining < 0:
         remaining = 0
        self.total_label.config(text=f"Total Expenses: ₱{self.total_expenses:.0f}")
        self.remaining_label.config(text=f"Remaining Salary: ₱{remaining:.0f}")

    def analyze_expenses(self):
        # Show pie chart of expense distribution
        categories = ["Food", "Transportation", "Entertainment", "Other"]
        values = [self.get_category_total(cat) for cat in categories]
        plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title("Expense Distribution")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
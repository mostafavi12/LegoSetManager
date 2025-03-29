import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import sqlite3

import os

def read_sets():
    # Clear the treeview
    tree.delete(*tree.get_children())

    cursor.execute("SELECT * FROM sets")
    sets = cursor.fetchall()

    for set_data in sets:
        tree.insert("", "end", values=(set_data[0], set_data[1], set_data[2], set_data[3]))

    for col in columns_sets:
        tree.column(col, width=100)
        tree.heading(col, text=col, command=lambda col=col: sort_treeview(tree, col))


def on_set_double_click(event):
    selected_item = tree.selection()[0]
    set_number = tree.item(selected_item, "values")[0]

    # Create a new window for displaying Lego parts
    parts_window = tk.Toplevel(root)
    parts_window.title(f"Lego Parts for Set {set_number}")

    # Create a Treeview widget to display parts
    parts_tree = ttk.Treeview(parts_window, columns=("Part Number", "Quantity"))
    parts_tree.heading("#1", text="Part Number")
    parts_tree.heading("#2", text="Quantity")

    # Fetch parts for the selected set
    #cursor.execute("SELECT part_number, quantity FROM parts WHERE set_number = ?", (set_number,))
    cursor.execute(fR"SELECT part_number, quantity FROM parts WHERE set_number = {set_number}")
    parts = cursor.fetchall()

    for part_data in parts:
        parts_tree.insert("", "end", values=(part_data[0], part_data[1]))

    parts_tree.pack(fill="both", expand=True)

    # Button to close the parts window
    close_button = ttk.Button(parts_window, text="Close", command=parts_window.destroy)
    close_button.pack()

    # Button to delete selected part
    delete_button = ttk.Button(parts_window, text="Delete Part", command=lambda: delete_part(set_number, parts_tree))
    delete_button.pack()
def delete_part(set_number, parts_tree):
    selected_item = parts_tree.selection()[0]

    # Ensure that an item is selected
    if not selected_item:
        messagebox.showerror("Error", "Please select a part to delete")
        return

    part_number = parts_tree.item(selected_item, "values")[0]

    if messagebox.askyesno("Confirmation", f"Are you sure you want to delete part {part_number} from this set?"):
        try:
            # Check if the set number and part number combination exists
            cursor.execute("SELECT 1 FROM parts WHERE set_number = ? AND part_number = ?", (set_number, part_number))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "The specified part does not exist in the selected set")
                return

            # Delete the selected part from the parts table
            cursor.execute("DELETE FROM parts WHERE set_number = ? AND part_number = ?", (set_number, part_number))
            conn.commit()
            messagebox.showinfo("Success", "Part deleted successfully")
            # Refresh the parts list
            parts_tree.delete(selected_item)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
def delete_set():
    selected_index = tree.selection()
    if selected_index:
        set_id = tree.item(selected_index[0], "values")[0]

        # Delete the selected set from both sets and parts tables
        cursor.execute("DELETE FROM sets WHERE set_number = ?", (set_id,))
        cursor.execute("DELETE FROM parts WHERE set_number = ?", (set_id,))
        conn.commit()
        read_sets()

def search_part():
    # Clear the search results Treeview
    search_tree.delete(*search_tree.get_children())

    # Get the part number entered by the user
    part_number = entry_search.get().strip()

    if part_number:
        # Execute a SQL query to retrieve sets containing the specified part and its quantity
        cursor.execute("SELECT s.set_number, s.set_name, p.quantity FROM sets AS s "
                       "INNER JOIN parts AS p ON s.set_number = p.set_number "
                       "WHERE p.part_number = ?", (part_number,))
        search_results = cursor.fetchall()

        # Display the search results in the Treeview
        for result in search_results:
            search_tree.insert("", "end", values=(result[0], result[1], result[2]))

def add_lego_part():
    # Get values from the text entry fields
    part_number = entry_part_number.get().strip()
    set_number = entry_set_number.get().strip()
    quantity = entry_quantity.get().strip()

    # Check if any field is empty
    if not part_number or not set_number or not quantity:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        # Check if the Lego set number exists in the database
        cursor.execute("SELECT * FROM sets WHERE set_number = ?", (set_number,))
        set_exists = cursor.fetchone()
        if not set_exists:
            messagebox.showerror("Error", "Lego Set number is invalid")
            return

        # Insert the Lego part into the parts table
        cursor.execute("INSERT INTO parts (set_number, part_number, quantity) VALUES (?, ?, ?)",
                       (set_number, part_number, quantity))
        conn.commit()
        messagebox.showinfo("Success", "Lego part added successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def sort_treeview(tv, col):
    # Get the list of items in the column
    data = [(tv.set(child, col), child) for child in tv.get_children('')]

    # Toggle between ascending and descending order
    if col in sorted_columns:
        if col == "Total Parts":  # Check if it's the "Total Parts" column
            data.sort(key=lambda x: int(x[0]), reverse=not sorted_columns[col])
        else:
            data.sort(key=lambda x: x[0], reverse=not sorted_columns[col])
        sorted_columns[col] = not sorted_columns[col]
    else:
        if col == "#3":  # Check if it's the "Total Parts" column
            data.sort(key=lambda x: int(x[0]))
        else:
            data.sort(key=lambda x: x[0])
        sorted_columns[col] = False

    for index, (val, child) in enumerate(data):
        tv.move(child, '', index)

root = tk.Tk()
root.title("Lego Sets Database")

#conn = sqlite3.connect(R"..\InfoExtractor\db\lego_parts.db")
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "InfoExtractor", "db", "lego_parts.db")
conn = sqlite3.connect(db_path)

#conn = sqlite3.connect(R"/home/ahmad/projects/LegoSetManager/InfoExtractor/db/lego_parts.db")
cursor = conn.cursor()

label_set_number = tk.Label(root, text="Set Number:")
label_part_number = tk.Label(root, text="Part Number")
label_quantity = tk.Label(root, text="Quantity")

entry_set_number = tk.Entry(root)
entry_part_number = tk.Entry(root)
entry_quantity = tk.Entry(root)

button_add_lego_part = tk.Button(root, text="Add Part", command=add_lego_part)
button_read = tk.Button(root, text="Read Sets", command=read_sets)

# Create a Treeview widget to display Lego sets with sorting
# Define columns for sets
columns_sets = ("Set Number", "Set Name", "Total Parts", "Age")

# Create a Treeview widget to display sets with sorting
tree = ttk.Treeview(root, columns=columns_sets)
tree.heading("#1", text="Set Number", command=lambda: sort_treeview(tree, "#1"))
tree.heading("#2", text="Set Name", command=lambda: sort_treeview(tree, "#2"))
tree.heading("#3", text="Total Parts", command=lambda: sort_treeview(tree, "#3"))
tree.heading("#4", text="Age", command=lambda: sort_treeview(tree, "#4"))

tree.grid(row=0, column=2, rowspan=6, columnspan=2)

tree.bind("<Double-1>", on_set_double_click)

button_delete = tk.Button(root, text="Delete Set", command=delete_set)

label_set_number.grid(row=0, column=0)
label_part_number.grid(row=1, column=0)
label_quantity.grid(row=2, column=0)

entry_set_number.grid(row=0, column=1)
entry_part_number.grid(row=1, column=1)
entry_quantity.grid(row=2, column=1)

button_add_lego_part.grid(row=4, column=0, columnspan=2)
button_read.grid(row=5, column=0, columnspan=2)
tree.grid(row=0, column=2, rowspan=6, columnspan=2)
button_delete.grid(row=8, column=0, columnspan=2)

# Add a search input field and button
label_search = tk.Label(root, text="Search Part Number:")
entry_search = tk.Entry(root)
button_search = tk.Button(root, text="Search", command=search_part)

label_search.grid(row=9, column=0)
entry_search.grid(row=9, column=1)
button_search.grid(row=9, column=2)

# Create a Treeview widget to display search results
search_tree = ttk.Treeview(root, columns=("Set Number", "Set Name", "Quantity"))
search_tree.heading("#1", text="Set Number")
search_tree.heading("#2", text="Set Name")
search_tree.heading("#3", text="Quantity")

search_tree.grid(row=10, column=0, columnspan=3)

# Dictionary to keep track of sorted columns and their order
sorted_columns = {col: False for col in columns_sets}

root.mainloop()
conn.close()

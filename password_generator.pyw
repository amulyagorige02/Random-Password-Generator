import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip

# -------------------- Window --------------------
root = tk.Tk()
root.title("Professional Password Generator")
root.geometry("550x700")
root.configure(bg="#1E293B")
root.resizable(False, False)

history = []
AMBIGUOUS = "0O1lI"

# -------------------- Variables --------------------
length_var = tk.IntVar(value=12)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

# -------------------- Title --------------------
title = tk.Label(
    root,
    text="🔐 Random Password Generator",
    bg="#1E293B",
    fg="white",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=15)

# -------------------- Length --------------------
tk.Label(
    root,
    text="Password Length",
    bg="#1E293B",
    fg="white",
    font=("Segoe UI",11)
).pack()

length_spin = tk.Spinbox(
    root,
    from_=8,
    to=64,
    textvariable=length_var,
    font=("Segoe UI",11),
    width=10,
    justify="center"
)
length_spin.pack(pady=10)

# -------------------- Checkboxes --------------------
frame = tk.Frame(root, bg="#1E293B")
frame.pack()

tk.Checkbutton(
    frame,
    text="Uppercase",
    variable=upper_var,
    bg="#1E293B",
    fg="white",
    selectcolor="#334155",
    font=("Segoe UI",10)
).grid(row=0,column=0,padx=15,pady=5,sticky="w")

tk.Checkbutton(
    frame,
    text="Lowercase",
    variable=lower_var,
    bg="#1E293B",
    fg="white",
    selectcolor="#334155",
    font=("Segoe UI",10)
).grid(row=1,column=0,padx=15,pady=5,sticky="w")

tk.Checkbutton(
    frame,
    text="Numbers",
    variable=digit_var,
    bg="#1E293B",
    fg="white",
    selectcolor="#334155",
    font=("Segoe UI",10)
).grid(row=0,column=1,padx=15,pady=5,sticky="w")

tk.Checkbutton(
    frame,
    text="Symbols",
    variable=symbol_var,
    bg="#1E293B",
    fg="white",
    selectcolor="#334155",
    font=("Segoe UI",10)
).grid(row=1,column=1,padx=15,pady=5,sticky="w")

tk.Checkbutton(
    root,
    text="Exclude Ambiguous Characters (0 O 1 l I)",
    variable=exclude_var,
    bg="#1E293B",
    fg="white",
    selectcolor="#334155",
    font=("Segoe UI",10)
).pack(pady=10)
# -------------------- Password Generator --------------------
def update_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 3:
        strength_label.config(text="Strength : Weak", fg="#EF4444")
        progress["value"] = 33
    elif score <= 5:
        strength_label.config(text="Strength : Medium", fg="#F59E0B")
        progress["value"] = 66
    else:
        strength_label.config(text="Strength : Strong", fg="#22C55E")
        progress["value"] = 100


def generate_password():

    length = length_var.get()

    if length < 8:
        messagebox.showerror("Error", "Password length must be at least 8.")
        return

    groups = []

    if upper_var.get():
        groups.append(string.ascii_uppercase)

    if lower_var.get():
        groups.append(string.ascii_lowercase)

    if digit_var.get():
        groups.append(string.digits)

    if symbol_var.get():
        groups.append(string.punctuation)

    if len(groups) < 2:
        messagebox.showerror(
            "Error",
            "Please select at least TWO character types."
        )
        return

    if exclude_var.get():
        temp = []
        for chars in groups:
            temp.append("".join(c for c in chars if c not in AMBIGUOUS))
        groups = temp

    password = []

    for chars in groups:
        password.append(secrets.choice(chars))

    all_chars = "".join(groups)

    while len(password) < length:
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)

    final_password = "".join(password)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, final_password)

    pyperclip.copy(final_password)

    update_strength(final_password)

    history.insert(0, final_password)

    if len(history) > 5:
        history.pop()

    history_box.delete(0, tk.END)

    for item in history:
        history_box.insert(tk.END, item)

    messagebox.showinfo(
        "Success",
        "Password generated successfully!\n\nCopied to Clipboard."
    )
# -------------------- Generate Button --------------------

generate_btn = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    font=("Segoe UI", 12, "bold"),
    width=22,
    relief="flat",
    cursor="hand2"
)
generate_btn.pack(pady=15)

# -------------------- Password Box --------------------

password_entry = tk.Entry(
    root,
    font=("Consolas", 14),
    justify="center",
    width=35,
    bd=2,
    relief="solid",
    bg="#F8FAFC",
    fg="#111827"
)
password_entry.pack(pady=10)

# -------------------- Strength --------------------

strength_label = tk.Label(
    root,
    text="Strength : ",
    bg="#1E293B",
    fg="white",
    font=("Segoe UI", 11, "bold")
)
strength_label.pack(pady=(10, 5))

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "green.Horizontal.TProgressbar",
    thickness=18
)

progress = ttk.Progressbar(
    root,
    style="green.Horizontal.TProgressbar",
    length=320,
    mode="determinate"
)
progress.pack(pady=10)

# -------------------- History --------------------

tk.Label(
    root,
    text="Last 5 Generated Passwords",
    bg="#1E293B",
    fg="white",
    font=("Segoe UI", 11, "bold")
).pack(pady=(15, 5))

history_box = tk.Listbox(
    root,
    width=45,
    height=5,
    font=("Consolas", 10),
    bg="#E2E8F0",
    fg="#111827",
    bd=2
)
history_box.pack()

# -------------------- Footer --------------------

footer = tk.Label(
    root,
    text="✔ Password is automatically copied to Clipboard",
    bg="#1E293B",
    fg="#22C55E",
    font=("Segoe UI", 10, "bold")
)
footer.pack(pady=20)

# -------------------- Run --------------------

root.mainloop()
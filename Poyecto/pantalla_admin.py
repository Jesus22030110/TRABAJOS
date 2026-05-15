import customtkinter as ctk
from tkinter import ttk

# ---------------- CONFIGURACIÓN GENERAL ---------------- #
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Administrador de Inventario")
app.geometry("1050x650")
app.configure(fg_color="#FAF7FF")

# ---------------- COLORES ---------------- #
BG = "#FAF7FF"
SIDEBAR = "#EEE5FF"
CARD = "#FFFFFF"
PRIMARY = "#C9B6FF"
TEXT = "#5D5873"
SOFT = "#A9A3BE"
HOVER = "#DDD0FF"

# ---------------- SIDEBAR ---------------- #
sidebar = ctk.CTkFrame(app, width=210, fg_color=SIDEBAR, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="Cute Scoop",
    font=("Poppins", 24, "bold"),
    text_color=TEXT,
)
logo.pack(pady=(40, 50))

sections = ["Productos", "Pedidos", "Ventas Pasadas"]

for section in sections:
    button = ctk.CTkButton(
        sidebar,
        text=section,
        fg_color="transparent",
        hover_color=HOVER,
        text_color=TEXT,
        anchor="w",
        height=45,
        corner_radius=14,
        font=("Poppins", 14),
    )
    button.pack(fill="x", padx=15, pady=7)

# ---------------- CONTENIDO PRINCIPAL ---------------- #
main = ctk.CTkFrame(app, fg_color=BG)
main.pack(side="right", fill="both", expand=True)

# ---------------- HEADER ---------------- #
header = ctk.CTkFrame(main, fg_color="transparent")
header.pack(fill="x", padx=30, pady=(30, 20))

main_title = ctk.CTkLabel(
    header,
    text="Control de Stock",
    font=("Poppins", 30, "bold"),
    text_color=TEXT,
)
main_title.pack(anchor="w")

subtitle = ctk.CTkLabel(
    header,
    text="Productos disponibles en el inventario",
    font=("Poppins", 13),
    text_color=SOFT,
)
subtitle.pack(anchor="w")

# ---------------- VENTANAS EMERGENTES ---------------- #

def open_add_product():
    popup = ctk.CTkToplevel(app)
    popup.title("Agregar Producto")
    popup.geometry("400x320")
    popup.configure(fg_color=BG)

    popup.grab_set()

    title = ctk.CTkLabel(
        popup,
        text="Nuevo Producto",
        font=("Poppins", 24, "bold"),
        text_color=TEXT,
    )
    title.pack(pady=(25, 20))

    name_entry = ctk.CTkEntry(
        popup,
        placeholder_text="Nombre del producto",
        width=300,
        height=45,
        corner_radius=14,
        fg_color=CARD,
        border_color="#E5DFFF",
    )
    name_entry.pack(pady=10)

    stock_entry = ctk.CTkEntry(
        popup,
        placeholder_text="Cantidad disponible",
        width=300,
        height=45,
        corner_radius=14,
        fg_color=CARD,
        border_color="#E5DFFF",
    )
    stock_entry.pack(pady=10)

    save_button = ctk.CTkButton(
        popup,
        text="Guardar",
        fg_color=PRIMARY,
        hover_color="#B7A0FF",
        text_color="white",
        width=180,
        height=42,
        corner_radius=14,
    )
    save_button.pack(pady=(25, 10))


def open_edit_stock(category, amount):
    popup = ctk.CTkToplevel(app)
    popup.title("Actualizar Stock")
    popup.geometry("400x300")
    popup.configure(fg_color=BG)

    popup.grab_set()

    title = ctk.CTkLabel(
        popup,
        text=category,
        font=("Poppins", 24, "bold"),
        text_color=TEXT,
    )
    title.pack(pady=(30, 10))

    subtitle = ctk.CTkLabel(
        popup,
        text=f"Stock actual: {amount}",
        font=("Poppins", 14),
        text_color=SOFT,
    )
    subtitle.pack(pady=(0, 25))

    stock_entry = ctk.CTkEntry(
        popup,
        placeholder_text="Nueva cantidad",
        width=300,
        height=45,
        corner_radius=14,
        fg_color=CARD,
        border_color="#E5DFFF",
    )
    stock_entry.pack(pady=10)

    update_button = ctk.CTkButton(
        popup,
        text="Actualizar",
        fg_color=PRIMARY,
        hover_color="#B7A0FF",
        text_color="white",
        width=180,
        height=42,
        corner_radius=14,
    )
    update_button.pack(pady=(30, 10))

# ---------------- TARJETAS ---------------- #
cards_frame = ctk.CTkFrame(main, fg_color="transparent")
cards_frame.pack(fill="x", padx=30, pady=(0, 15))

cards = [
    ("Juguetes", "24"),
    ("Cosas de Maquillaje", "17"),
    ("Lego", "12"),
    ("Dibujo", "31"),
    ("Cuidado Personal", "9"),
]

for title, amount in cards:
    card = ctk.CTkFrame(
        cards_frame,
        fg_color=CARD,
        corner_radius=22,
        height=120,
        cursor="hand2"
    )
    card.pack(side="left", expand=True, fill="both", padx=8)

    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=("Poppins", 15),
        text_color=SOFT,
    )
    title_label.pack(anchor="w", padx=20, pady=(25, 5))

    amount_label = ctk.CTkLabel(
        card,
        text=amount,
        font=("Poppins", 34, "bold"),
        text_color=TEXT,
    )
    amount_label.pack(anchor="w", padx=20)

    # Evento click
    card.bind(
        "<Button-1>",
        lambda e, t=title, a=amount: open_edit_stock(t, a)
    )

    title_label.bind(
        "<Button-1>",
        lambda e, t=title, a=amount: open_edit_stock(t, a)
    )

    amount_label.bind(
        "<Button-1>",
        lambda e, t=title, a=amount: open_edit_stock(t, a)
    )

# ---------------- TABLA DE PRODUCTOS ---------------- #
table_frame = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=24,
    height=320
)

table_frame.pack(fill="x", padx=30, pady=15)
table_frame.pack_propagate(False)

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground=TEXT,
    rowheight=44,
    fieldbackground="#FFFFFF",
    borderwidth=0,
    font=("Poppins", 11),
)

style.configure(
    "Treeview.Heading",
    background="#F3EEFF",
    foreground=TEXT,
    borderwidth=0,
    font=("Poppins", 11, "bold"),
)

style.map("Treeview", background=[("selected", "#E2D8FF")])

columns = ( "Productos", "Stock")

product_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
)

for col in columns:
    product_table.heading(col, text=col)
    product_table.column(col, anchor="center")

products = [
    ("Juguetes", "15"),
    ("Sets de lego", "8"),
    ("Cosas de Maquillaje", "20"),
    ("Dibujo", "12"),
    ("Cuidado Personal", "10"),
    
]

for product in products:
    product_table.insert("", "end", values=product)

product_table.pack(fill="both", padx=18, pady=18)

# ---------------- BOTONES ---------------- #
buttons_frame = ctk.CTkFrame(main, fg_color="transparent")
buttons_frame.pack(fill="x", padx=30, pady=(0, 25))

add_button = ctk.CTkButton(
    buttons_frame,
    text="Agregar Producto",
    command=open_add_product,
    fg_color=PRIMARY,
    hover_color="#B7A0FF",
    text_color="white",
    corner_radius=14,
    height=42,
    width=170,
    font=("Poppins", 13, "bold"),
)
add_button.pack(side="left")

edit_button = ctk.CTkButton(
    buttons_frame,
    text="Actualizar Stock",
    fg_color="#EADFFF",
    hover_color="#DDD0FF",
    text_color=TEXT,
    corner_radius=14,
    height=42,
    width=170,
    font=("Poppins", 13),
)
edit_button.pack(side="left", padx=12)

app.mainloop()

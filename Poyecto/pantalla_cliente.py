import customtkinter as ctk

# ---------------- CONFIGURACIÓN ---------------- #
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Compra de Scoops")
app.geometry("900x600")
app.configure(fg_color="#FAF7FF")

# ---------------- COLORES ---------------- #
BG = "#FAF7FF"
CARD = "#FFFFFF"
PRIMARY = "#C9B6FF"
TEXT = "#5D5873"
SOFT = "#A9A3BE"
HOVER = "#B8A0FF"

# ---------------- HEADER ---------------- #
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(fill="x", padx=40, pady=(30, 20))

title = ctk.CTkLabel(
    header,
    text="Compra tus Scoops",
    font=("Poppins", 32, "bold"),
    text_color=TEXT,
)
title.pack(anchor="w")

subtitle = ctk.CTkLabel(
    header,
    text="Selecciona la cantidad de scoops que deseas comprar",
    font=("Poppins", 14),
    text_color=SOFT,
)
subtitle.pack(anchor="w")

# ---------------- CONTENEDOR PRINCIPAL ---------------- #
content = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
content.pack(fill="both", expand=True, padx=40, pady=20)

# ---------------- TARJETAS DE SCOOPS ---------------- #
scoops = [
    ("1 Scoop", "#F9D5E5"),
    ("2 Scoops", "#D5E8F9"),
    ("3 Scoops", "#FCE1C8"),
    ("4 Scoops", "#D8F3DC"),
]

for name, color in scoops:
    card = ctk.CTkFrame(
        content,
        fg_color=CARD,
        corner_radius=24,
        width=180,
        height=230,
    )
    card.pack(side="left", expand=True, padx=12)

    # círculo decorativo
    circle = ctk.CTkFrame(
        card,
        fg_color=color,
        width=90,
        height=90,
        corner_radius=100,
    )
    circle.pack(pady=(30, 20))

    scoop_label = ctk.CTkLabel(
        card,
        text=name,
        font=("Poppins", 22, "bold"),
        text_color=TEXT,
    )
    scoop_label.pack()

    desc = ctk.CTkLabel(
        card,
        text="10 premios/scoop",
        font=("Poppins", 12),
        text_color=SOFT,
    )
    desc.pack(pady=(5, 20))

    buy_button = ctk.CTkButton(
        card,
        text="Seleccionar",
        fg_color=PRIMARY,
        hover_color=HOVER,
        text_color="white",
        corner_radius=14,
        width=130,
        height=40,
        font=("Poppins", 13, "bold"),
    )
    buy_button.pack()

# ---------------- RESUMEN INFERIOR ---------------- #
bottom = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=24,
    height=90
)
bottom.pack(fill="x", padx=40, pady=(0, 30))

bottom.pack_propagate(False)

summary = ctk.CTkLabel(
    bottom,
    text="Selecciona una opción para continuar",
    font=("Poppins", 15),
    text_color=TEXT,
)
summary.pack(side="left", padx=25)

checkout = ctk.CTkButton(
    bottom,
    text="Continuar Compra",
    fg_color=PRIMARY,
    hover_color=HOVER,
    text_color="white",
    width=180,
    height=45,
    corner_radius=14,
    font=("Poppins", 14, "bold"),
)
checkout.pack(side="right", padx=25)

app.mainloop()
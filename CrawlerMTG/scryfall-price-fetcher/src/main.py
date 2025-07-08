import tkinter as tk
root = tk.Tk()

from PIL import Image, ImageTk
import requests
from io import BytesIO
from scryfall_api import search_cards, get_card_price_from_card
import webbrowser
import tkinter.ttk as ttk
from tkinter import filedialog
from collections import Counter
from decklist_view import create_decklist_frame

# --- Theme Colors ---
BG_DARK = "#181818"
BG_PANEL = "#232323"
BG_CARD = "#282828"
FG_LIGHT = "#f8f8f2"
FG_HIGHLIGHT = "#ffb347"
FG_LINK = "#40a2ff"

# --- Decklist and selection tracking ---
decklist = []
selected_card = {"name": "", "price": ""}

# --- Export to Moxfield ---
def export_decklist_to_file(decklist):
    if not decklist:
        print("Decklist is empty.")
        return

    name_counts = Counter(card["name"] for card in decklist)

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Decklist for Moxfield"
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for name, count in name_counts.items():
                f.write(f"{count} {name}\n")
        print(f"Decklist exported to {file_path}")
    except Exception as e:
        print(f"Failed to export: {e}")

# --- Tk Style ---
style = ttk.Style()
style.theme_use('clam')
style.configure(
    "Vertical.TScrollbar",
    gripcount=0,
    background=BG_PANEL,
    darkcolor=BG_PANEL,
    lightcolor=BG_PANEL,
    troughcolor=BG_DARK,
    bordercolor=BG_DARK,
    arrowcolor=BG_PANEL,
    relief="flat"
)
style.map(
    "Vertical.TScrollbar",
    background=[("active", BG_CARD), ("!active", BG_PANEL)],
    arrowcolor=[("active", BG_PANEL), ("!active", BG_PANEL)]
)

# --- App Logic ---
def search():
    price_label.config(text="Searching...", fg=FG_HIGHLIGHT, bg=BG_PANEL)
    link_label.config(text="", cursor="arrow", fg=FG_LINK, bg=BG_PANEL)
    add_button.pack_forget()
    root.update_idletasks()

    query = entry.get()
    for widget in grid_frame.winfo_children():
        widget.destroy()
    global cards, card_images
    cards = search_cards(query)
    card_images.clear()
    columns = 4
    for col in range(columns):
        grid_frame.grid_columnconfigure(col, weight=1)
    for idx, card in enumerate(cards):
        img_url = None
        if "image_uris" in card:
            img_url = card["image_uris"].get("normal")
        elif "card_faces" in card and card["card_faces"]:
            img_url = card["card_faces"][0].get("image_uris", {}).get("normal")
        if img_url:
            try:
                response = requests.get(img_url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((223, 310))
                photo = ImageTk.PhotoImage(img)
                card_images.append(photo)
                btn = tk.Button(
                    grid_frame, image=photo, command=lambda i=idx: show_price(i),
                    bg=BG_CARD, activebackground=BG_PANEL, bd=0, relief="flat", highlightthickness=0
                )
                btn.grid(row=idx // columns, column=idx % columns, padx=20, pady=20, sticky="nsew")
            except Exception as e:
                print(f"Failed to load image for {card.get('name')}: {e}")
                create_text_button(card, idx)
        else:
            create_text_button(card, idx)

    grid_canvas.update_idletasks()
    grid_canvas.config(scrollregion=grid_canvas.bbox("all"))
    price_label.config(text="", fg=FG_HIGHLIGHT, bg=BG_PANEL)

def create_text_button(card, idx):
    btn = tk.Button(
        grid_frame, text=card.get('name'), command=lambda i=idx: show_price(i),
        bg=BG_CARD, fg=FG_LIGHT, activebackground=BG_PANEL, bd=0, relief="flat", highlightthickness=0
    )
    btn.grid(row=idx // 4, column=idx % 4, padx=20, pady=20, sticky="nsew")

def show_price(idx):
    card = cards[idx]
    price_info = get_card_price_from_card(card)
    eur = price_info.get('eur')
    eur_foil = price_info.get('eur_foil')
    cardmarket_url = card.get('purchase_uris', {}).get('cardmarket', '')
    price_text = f"{card.get('name')} ({card.get('set_name')})\n\n"
    price_text += f"EUR (Cardmarket): {eur}\n"
    price_text += f"EUR Foil (Cardmarket): {eur_foil}\n"
    price_label.config(text=price_text, fg=FG_HIGHLIGHT, bg=BG_PANEL)

    if cardmarket_url:
        link_label.config(text="Open in Cardmarket", fg=FG_LINK, cursor="hand2", bg=BG_PANEL)
        link_label.bind("<Button-1>", lambda e: webbrowser.open(cardmarket_url))
    else:
        link_label.config(text="", cursor="arrow", bg=BG_PANEL)
        link_label.unbind("<Button-1>")

    selected_card["name"] = card.get('name')
    selected_card["price"] = eur
    add_button.pack(pady=(0, 20))

def add_to_decklist():
    if selected_card["name"]:
        decklist.append({"name": selected_card["name"], "price": selected_card["price"]})
        print(f"Added to decklist: {selected_card['name']} - EUR {selected_card['price']}")
        add_button.pack_forget()

def show_search():
    decklist_frame.place_forget()
    search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# --- UI Setup ---

root.title("Scryfall Card Search")
root.state('zoomed')
root.configure(bg=BG_DARK)

entry = tk.Entry(root, width=40, bg=BG_PANEL, fg=FG_LIGHT, insertbackground=FG_LIGHT, font=("Arial", 14), relief="flat")
entry.place(relx=0.02, rely=0.01, relwidth=0.5, relheight=0.05)

search_btn = tk.Button(root, text="Search", command=search, bg=FG_HIGHLIGHT, fg=BG_DARK, font=("Arial", 12, "bold"), relief="flat", activebackground=BG_PANEL)
search_btn.place(relx=0.53, rely=0.01, relwidth=0.1, relheight=0.05)

# --- Main Layout ---
main_frame = tk.Frame(root, bg=BG_DARK)
main_frame.place(relx=0, rely=0.07, relwidth=1, relheight=0.93)

search_frame = tk.Frame(main_frame, bg=BG_DARK)
search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

grid_canvas = tk.Canvas(search_frame, bg=BG_DARK, highlightthickness=0)
scrollbar = ttk.Scrollbar(search_frame, orient="vertical", command=grid_canvas.yview, style="Vertical.TScrollbar")
grid_canvas.configure(yscrollcommand=scrollbar.set)

grid_canvas.place(relx=0, rely=0, relwidth=0.7, relheight=1)
scrollbar.place(relx=0.7, rely=0, relwidth=0.02, relheight=1)

grid_frame = tk.Frame(grid_canvas, bg=BG_DARK)
grid_canvas.create_window((0, 0), window=grid_frame, anchor="n")

info_frame = tk.Frame(search_frame, bg=BG_PANEL)
info_frame.place(relx=0.72, rely=0, relwidth=0.28, relheight=1)

price_label = tk.Label(info_frame, text="", justify="left", anchor="nw", font=("Arial", 14), bg=BG_PANEL, fg=FG_HIGHLIGHT, wraplength=350)
price_label.pack(fill="both", expand=True, padx=10, pady=10)

link_label = tk.Label(info_frame, text="", font=("Arial", 12, "underline"), bg=BG_PANEL, fg=FG_LINK, cursor="hand2")
link_label.pack(pady=(0, 10))

add_button = tk.Button(info_frame, text="Add to Decklist", bg=FG_HIGHLIGHT, fg=BG_DARK, font=("Arial", 12, "bold"), relief="flat", activebackground=BG_PANEL, command=add_to_decklist)
add_button.pack(pady=(0, 20))
add_button.pack_forget()

# --- Decklist View ---
decklist_frame, show_decklist = create_decklist_frame(main_frame, show_search, decklist)
# Inject export function
decklist_frame.children["!button2"].configure(command=lambda: export_decklist_to_file(decklist))

# --- Button to Show Decklist ---
show_decklist_btn = tk.Button(root, text="Show Decklist", command=show_decklist, bg=FG_LINK, fg=BG_DARK, font=("Arial", 12, "bold"), relief="flat", activebackground=BG_PANEL)
show_decklist_btn.place(relx=0.64, rely=0.01, relwidth=0.12, relheight=0.05)

# --- State ---
cards = []
card_images = []

def on_configure(event):
    grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))

def _on_mousewheel(event):
    grid_canvas.yview_scroll(int(-1*(event.delta / 120)), "units")

grid_frame.bind("<Configure>", on_configure)
grid_canvas.bind_all("<MouseWheel>", _on_mousewheel)

root.mainloop()

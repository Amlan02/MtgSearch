# search_view.py
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import tkinter.ttk as ttk
from scryfall_api import search_cards, get_card_price_from_card

BG_DARK = "#181818"
BG_CARD = "#282828"
BG_PANEL = "#232323"
FG_LIGHT = "#f8f8f2"
FG_HIGHLIGHT = "#ffb347"
FG_LINK = "#40a2ff"

def create_search_frame(parent, decklist):
    frame = tk.Frame(parent, bg=BG_DARK)

    entry = tk.Entry(
        parent, width=40, bg=BG_PANEL, fg=FG_LIGHT,
        insertbackground=FG_LIGHT, font=("Arial", 14), relief="flat"
    )

    selected_card = {"name": "", "price": ""}
    cards = []
    card_images = []

    canvas = tk.Canvas(frame, bg=BG_DARK, highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(relx=0, rely=0, relwidth=0.7, relheight=1)
    scrollbar.place(relx=0.7, rely=0, relwidth=0.02, relheight=1)

    grid_frame = tk.Frame(canvas, bg=BG_DARK)
    canvas.create_window((0, 0), window=grid_frame, anchor="n")

    info_frame = tk.Frame(frame, bg=BG_PANEL)
    info_frame.place(relx=0.72, rely=0, relwidth=0.28, relheight=1)

    price_label = tk.Label(
        info_frame, text="", justify="left", anchor="nw", font=("Arial", 14),
        bg=BG_PANEL, fg=FG_HIGHLIGHT, wraplength=350
    )
    price_label.pack(fill="both", expand=True, padx=10, pady=10)

    link_label = tk.Label(
        info_frame, text="", font=("Arial", 12, "underline"),
        bg=BG_PANEL, fg=FG_LINK, cursor="hand2"
    )
    link_label.pack(pady=(0, 10))

    add_button = tk.Button(
        info_frame, text="Add to Decklist", bg=FG_HIGHLIGHT, fg=BG_DARK,
        font=("Arial", 12, "bold"), relief="flat", activebackground=BG_PANEL
    )
    add_button.pack(pady=(0, 20))
    add_button.pack_forget()

    def show_price(idx):
        card = cards[idx]
        price_info = get_card_price_from_card(card)
        eur = price_info.get('eur')
        eur_foil = price_info.get('eur_foil')
        cardmarket_url = card.get('purchase_uris', {}).get('cardmarket', '')
        price_text = f"{card.get('name')} ({card.get('set_name')})\n\n"
        price_text += f"EUR (Cardmarket): {eur}\n"
        price_text += f"EUR Foil (Cardmarket): {eur_foil}\n"
        price_label.config(text=price_text)

        if cardmarket_url:
            link_label.config(text="Open in Cardmarket", cursor="hand2")
            link_label.bind("<Button-1>", lambda e: webbrowser.open(cardmarket_url))
        else:
            link_label.config(text="", cursor="arrow")
            link_label.unbind("<Button-1>")

        selected_card["name"] = card.get('name')
        selected_card["price"] = eur
        add_button.pack(pady=(0, 20))

    def add_to_decklist():
        if selected_card["name"]:
            decklist.append({"name": selected_card["name"], "price": selected_card["price"]})
            add_button.pack_forget()

    def create_text_button(card, idx):
        btn = tk.Button(
            grid_frame, text=card.get('name'), command=lambda i=idx: show_price(i),
            bg=BG_CARD, fg=FG_LIGHT, activebackground=BG_PANEL,
            bd=0, relief="flat", highlightthickness=0
        )
        btn.grid(row=idx // 4, column=idx % 4, padx=20, pady=20, sticky="nsew")

    def get_cards():
        price_label.config(text="Searching...")
        link_label.config(text="", cursor="arrow")
        add_button.pack_forget()
        frame.update_idletasks()

        query = entry.get()
        for widget in grid_frame.winfo_children():
            widget.destroy()

        nonlocal cards
        cards = search_cards(query)
        card_images.clear()
        columns = 4
        for col in range(columns):
            grid_frame.grid_columnconfigure(col, weight=1)
        for idx, card in enumerate(cards):
            img_url = card.get("image_uris", {}).get("normal")
            if not img_url and card.get("card_faces"):
                img_url = card["card_faces"][0].get("image_uris", {}).get("normal")
            if img_url:
                try:
                    response = requests.get(img_url)
                    img_data = response.content
                    img = Image.open(BytesIO(img_data)).resize((223, 310))
                    photo = ImageTk.PhotoImage(img)
                    card_images.append(photo)
                    btn = tk.Button(
                        grid_frame, image=photo, command=lambda i=idx: show_price(i),
                        bg=BG_CARD, activebackground=BG_PANEL, bd=0, relief="flat", highlightthickness=0
                    )
                    btn.grid(row=idx // columns, column=idx % columns, padx=20, pady=20, sticky="nsew")
                except:
                    create_text_button(card, idx)
            else:
                create_text_button(card, idx)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        price_label.config(text="")

    def show():
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    grid_frame.bind("<Configure>", on_configure)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    add_button.config(command=add_to_decklist)

    return frame, show, entry, show_price, add_button, get_cards

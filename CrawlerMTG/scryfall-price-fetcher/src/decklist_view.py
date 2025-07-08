import tkinter as tk

BG_DARK = "#181818"
BG_CARD = "#282828"
BG_PANEL = "#232323"
FG_LIGHT = "#f8f8f2"
FG_HIGHLIGHT = "#ffb347"


def create_decklist_frame(parent, show_search_callback, decklist, export_callback):
    frame = tk.Frame(parent, bg=BG_DARK)

    back_button = tk.Button(
        frame,
        text="Back to Search",
        command=show_search_callback,
        bg=FG_HIGHLIGHT,
        fg=BG_DARK,
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground=BG_PANEL
    )
    back_button.pack(pady=10)

    export_button = tk.Button(
        frame,
        text="Export to Moxfield",
        command=export_callback,
        bg=FG_HIGHLIGHT,
        fg=BG_DARK,
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground=BG_PANEL
    )
    export_button.pack(pady=10)

    decklist_text = tk.Text(
        frame,
        bg=BG_CARD,
        fg=FG_LIGHT,
        font=("Arial", 12),
        relief="flat",
        wrap="word"
    )
    decklist_text.pack(fill="both", expand=True, padx=10, pady=10)

    def show():
        decklist_text.delete(1.0, tk.END)
        if not decklist:
            decklist_text.insert(tk.END, "Decklist is empty.")
        else:
            for idx, card in enumerate(decklist, 1):
                decklist_text.insert(tk.END, f"{idx}. {card['name']} - EUR {card['price']}\n")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    return frame, show

import tkinter as tk

BG_DARK = "#181818"
BG_CARD = "#282828"
BG_PANEL = "#232323"
FG_LIGHT = "#f8f8f2"
FG_HIGHLIGHT = "#ffb347"
FG_LINK = "#40a2ff"

def create_decklist_frame(parent, show_search_callback, decklist):
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

    instruction_label = tk.Label(
        frame,
        text="Double-click a card to remove it from the decklist.",
        bg=BG_DARK,
        fg=FG_LIGHT,
        font=("Arial", 10)
    )
    instruction_label.pack(pady=(0, 5))

    listbox = tk.Listbox(
        frame,
        bg=BG_CARD,
        fg=FG_LIGHT,
        font=("Arial", 12),
        selectbackground=FG_HIGHLIGHT,
        selectforeground=BG_DARK,
        activestyle="none",
        relief="flat"
    )
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh():
        listbox.delete(0, tk.END)
        if not decklist:
            listbox.insert(tk.END, "Decklist is empty.")
        else:
            for idx, card in enumerate(decklist, 1):
                listbox.insert(tk.END, f"{idx}. {card['name']} - EUR {card['price']}")

    def show():
        refresh()
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def on_click(event):
        selection = listbox.curselection()
        if not selection or not decklist:
            return
        index = selection[0]
        if index >= len(decklist):
            return
        removed = decklist.pop(index)
        print(f"Removed: {removed['name']} - EUR {removed['price']}")
        refresh()

    listbox.bind("<Double-Button-1>", on_click)

    # Export button with default no-op command,
    # to be overridden by main_app.py
    export_button = tk.Button(
        frame,
        text="Export for Moxfield",
        command=lambda: None,
        bg=FG_LINK,
        fg=BG_DARK,
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground=BG_PANEL
    )
    export_button.pack(pady=10)

    return frame, show

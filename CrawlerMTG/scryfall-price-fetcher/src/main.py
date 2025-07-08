import tkinter as tk
from tkinter import ttk
from decklist_view import create_decklist_frame
from search_view import create_search_frame
from export_utils import export_decklist_to_file

# --- Theme Colors ---
BG_DARK = "#181818"
BG_PANEL = "#232323"
BG_CARD = "#282828"
FG_LIGHT = "#f8f8f2"
FG_HIGHLIGHT = "#ffb347"
FG_LINK = "#40a2ff"

# --- Decklist and selection tracking ---
decklist = []

# --- Tkinter Setup ---
root = tk.Tk()
root.title("Scryfall Card Search")
root.state('zoomed')
root.configure(bg=BG_DARK)

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

# --- Layout ---
main_frame = tk.Frame(root, bg=BG_DARK)
main_frame.place(relx=0, rely=0.07, relwidth=1, relheight=0.93)

# Placeholder for show_search to allow forward reference
def show_search():
    decklist_frame.place_forget()
    search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

search_frame, _, search_entry, show_price, add_button, get_cards = create_search_frame(main_frame, decklist)
decklist_frame, show_decklist = create_decklist_frame(
    main_frame,
    show_search_callback=show_search,
    decklist=decklist,
    export_callback=lambda: export_decklist_to_file(decklist)
)

# Start with the search frame visible
search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# --- Top Bar ---
search_entry.place(relx=0.02, rely=0.01, relwidth=0.5, relheight=0.05)

search_btn = tk.Button(
    root,
    text="Search",
    command=get_cards,
    bg=FG_HIGHLIGHT,
    fg=BG_DARK,
    font=("Arial", 12, "bold"),
    relief="flat",
    activebackground=BG_PANEL
)
search_btn.place(relx=0.53, rely=0.01, relwidth=0.1, relheight=0.05)

show_decklist_btn = tk.Button(
    root,
    text="Show Decklist",
    command=show_decklist,
    bg=FG_LINK,
    fg=BG_DARK,
    font=("Arial", 12, "bold"),
    relief="flat",
    activebackground=BG_PANEL
)
show_decklist_btn.place(relx=0.64, rely=0.01, relwidth=0.12, relheight=0.05)

root.mainloop()

from tkinter import filedialog
from collections import Counter

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

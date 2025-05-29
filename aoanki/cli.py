from pathlib import Path
import sys
import datetime

from aoanki.database import legacy1, get_database
from aoanki.meta.reader import from_apkg_file

# Optional fancy output -------------------------------------------------------
try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

# ─────────────────────────────────────────────────────────────────────────────
# 💡  Stub functions – REPLACE with real Anki logic
#     You promised to implement the actual interaction with Anki.
#     These are just placeholders so that the UI can run right away.
# ─────────────────────────────────────────────────────────────────────────────

def open_deck(deck_path: Path):
    """Open an existing Anki deck and return a deck object.
    Replace this stub with real logic that loads a deck using the Anki APIs.
    """
    # TODO: Implement real loading logic
    # Read deck file, parse it, load version
    meta_version = from_apkg_file(deck_path)
    print("📦  Deck metadata version:", meta_version)
    database = get_database(deck_path)
    cards = database.list_decks()
    print(f"　📚  Found {len(cards)} decks in {deck_path}")
    return {"path": deck_path, "cards": []}


def add_card(deck, front: str, back: str):
    """Add a card (front/back) to the deck.

    Replace this stub with real logic that appends a note/card via Anki APIs.
    """
    # TODO: Implement real add-card logic
    deck["cards"].append({"front": front, "back": back})


def deck_summary(deck):
    """Return a string with a human‑readable summary of the deck."""
    n_cards = len(deck.get("cards", []))
    return f"📚  Path: {deck['path']}  —  Cards: {n_cards}"

# ─────────────────────────────────────────────────────────────────────────────
# 🎨  Helper utilities
# ─────────────────────────────────────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen in a cross‑platform way."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = "🃏  Anki Deck CLI  🃏"
    if RICH_AVAILABLE:
        console.rule(title)
        console.print(f"[grey50]{now}[/grey50]  —  Crafted with ❤️  |  Press Ctrl+C to quit", justify="center")
    else:
        print("=" * len(title))
        print(title)
        print("=" * len(title))
        print(f"{now}  —  Press Ctrl+C to quit\n")


def prompt_path(prompt_text: str) -> Path:
    while True:
        path_str = input(prompt_text).strip().strip("\"")
        if not path_str:
            print("❌  Path cannot be empty. Try again.")
            continue
        path = Path(path_str)
        if path.exists():
            return path
        else:
            print("⚠️  File not found. Please enter a valid path.")


def menu_choice() -> str:
    print("\nSelect an option:")
    print("  1️⃣  Open an existing deck  📂")
    print("  2️⃣  Add a new card       ➕✨")
    print("  3️⃣  Show deck summary    📊")
    print("  4️⃣  Save & Exit          💾🚪")
    choice = input("\nYour choice ⇒ ").strip()
    return choice


def input_card() -> tuple[str, str]:
    print("\n🆕  Adding a new card (leave blank to cancel)")
    front = input("  ➤ Front: ")
    if not front:
        raise KeyboardInterrupt  # Use interrupt to bubble up and cancel
    back = input("  ➤ Back : ")
    if not back:
        raise KeyboardInterrupt
    return front, back

# ─────────────────────────────────────────────────────────────────────────────
# 🚀  Main loop
# ─────────────────────────────────────────────────────────────────────────────

def main():
    current_deck = None

    while True:
        try:
            clear_screen()
            print_header()
            if current_deck is not None:
                # Show quick summary line at top
                if RICH_AVAILABLE:
                    console.print(deck_summary(current_deck), style="bold green")
                else:
                    print(deck_summary(current_deck))
            choice = menu_choice()

            if choice == "1":
                deck_path = prompt_path("Enter deck path ⇒ ")
                current_deck = open_deck(deck_path)
                print("✅  Deck opened successfully!")
                input("\nPress Enter to continue…")

            elif choice == "2":
                if current_deck is None:
                    print("⚠️  No deck is open. Open a deck first!")
                    input("\nPress Enter to continue…")
                    continue
                try:
                    front, back = input_card()
                except KeyboardInterrupt:
                    print("\n❎  Card creation cancelled.")
                    input("\nPress Enter to continue…")
                    continue
                add_card(current_deck, front, back)
                print("🎉  Card added!")
                input("\nPress Enter to continue…")

            elif choice == "3":
                if current_deck is None:
                    print("⚠️  No deck is open.")
                else:
                    if RICH_AVAILABLE:
                        table = Table(title="Deck Summary", box=box.MINIMAL_DOUBLE_HEAD)
                        table.add_column("Field", style="cyan", no_wrap=True)
                        table.add_column("Value", style="magenta")
                        table.add_row("Path", str(current_deck["path"]))
                        table.add_row("Cards", str(len(current_deck.get("cards", []))))
                        console.print(table)
                    else:
                        print(deck_summary(current_deck))
                input("\nPress Enter to continue…")

            elif choice == "4":
                if current_deck is not None:
                    # TODO: Save deck here if necessary
                    print("💾  Deck saved (stub). Bye! 👋")
                else:
                    print("👋  Goodbye!")
                break
            else:
                print("❌  Invalid choice. Try 1‑4.")
                input("\nPress Enter to continue…")

        except KeyboardInterrupt:
            print("\n👋  Interrupted by user. Exiting…")
            break


if __name__ == "__main__":
    main()

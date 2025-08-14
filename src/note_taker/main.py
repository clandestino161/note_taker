import argparse
import os
import subprocess
import sys
from rich.console import Console
from rich.table import Table

# Global paths
NOTES_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "note_taker")
console = Console()


def ensure_notes_dir():
    os.makedirs(NOTES_DIR, exist_ok=True)


def list_notes():
    ensure_notes_dir()
    notes = [f[:-3] for f in os.listdir(NOTES_DIR) if f.endswith(".md")]
    notes.sort()

    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return

    table = Table(title="Your Notes", header_style="bold cyan")
    table.add_column("Title", style="bold green")

    for note in notes:
        table.add_row(note)

    console.print(table)


def add_note(title):
    ensure_notes_dir()
    filepath = os.path.join(NOTES_DIR, f"{title}.md")
    if os.path.exists(filepath):
        console.print(f"[red]Note '{title}' already exists.[/red]")
        return

    # Create empty note
    with open(filepath, "w") as f:
        f.write(f"# {title}\n\n")

    # Open in Neovim
    subprocess.run(["nvim", filepath], check=False)
    console.print(f"[green]Note '{title}' created and saved at {filepath}[/green]")


def edit_note(title):
    ensure_notes_dir()
    filepath = os.path.join(NOTES_DIR, f"{title}.md")

    if not os.path.exists(filepath):
        console.print(f"[red]Note '{title}' not found.[/red]")
        return

    subprocess.run(["nvim", filepath], check=False)
    console.print(f"[cyan]Note '{title}' edited.[/cyan]")


def delete_note(title):
    ensure_notes_dir()
    filepath = os.path.join(NOTES_DIR, f"{title}.md")

    if os.path.exists(filepath):
        os.remove(filepath)
        console.print(f"[green]Note '{title}' deleted.[/green]")
    else:
        console.print(f"[red]Note '{title}' not found.[/red]")


def main():
    parser = argparse.ArgumentParser(description="Simple Neovim-based Note Taking App")
    parser.add_argument("command", choices=["add", "read", "delete", "list"], help="Command to execute")
    parser.add_argument("--title", help="Title of the note")

    args = parser.parse_args()

    if args.command == "list":
        list_notes()
    elif args.command == "add":
        if not args.title:
            console.print("[red]Title is required for adding a note.[/red]")
            sys.exit(1)
        add_note(args.title)
    elif args.command == "read":
        if not args.title:
            console.print("[red]Title is required for reading a note.[/red]")
            sys.exit(1)
        edit_note(args.title)
    elif args.command == "delete":
        if not args.title:
            console.print("[red]Title is required for deleting a note.[/red]")
            sys.exit(1)
        delete_note(args.title)


if __name__ == "__main__":
    main()

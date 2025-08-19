import os
import argparse
import subprocess
from rich.console import Console
from rich.table import Table
import markdown2
from weasyprint import HTML

console = Console()

NOTES_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "note_taker")
os.makedirs(NOTES_DIR, exist_ok=True)


def get_note_path(title: str) -> str:
    safe_title = f"{title}.md".replace(" ", "_")
    return os.path.join(NOTES_DIR, safe_title)


def add_note(title: str):
    note_path = get_note_path(title)
    if os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' already exists.")
        return
    with open(note_path, "w") as f:
        f.write(f"# {title}\n\n")
    subprocess.run(["nvim", note_path])


def edit_note(title: str):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return
    subprocess.run(["nvim", note_path])


def delete_note(title: str):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return
    os.remove(note_path)
    console.print(f"[green]Deleted:[/green] {title}")


def list_notes():
    files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith(".md"))
    if not files:
        console.print("[yellow]No notes found.[/yellow]")
        return

    table = Table(title="Your Notes")
    table.add_column("Title", style="cyan")
    for f in files:
        table.add_row(f.replace("_", " ").removesuffix(".md"))
    console.print(table)


def export_note(title: str, to_pdf: bool, to_html: bool):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return

    with open(note_path, "r") as f:
        content = f.read()

    html_content = markdown2.markdown(content)

    if to_html:
        html_file = note_path.replace(".md", ".html")
        with open(html_file, "w") as f:
            f.write(html_content)
        console.print(f"[green]Exported to HTML:[/green] {html_file}")

    if to_pdf:
        pdf_file = note_path.replace(".md", ".pdf")
        HTML(string=html_content).write_pdf(pdf_file)
        console.print(f"[green]Exported to PDF:[/green] {pdf_file}")


def main():
    parser = argparse.ArgumentParser(prog="note-taker", description="Simple Neovim-based Note Taker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("--title", required=True, help="Title of the note")

    edit_parser = subparsers.add_parser("edit", help="Edit an existing note")
    edit_parser.add_argument("--title", required=True, help="Title of the note")

    delete_parser = subparsers.add_parser("delete", help="Delete an existing note")
    delete_parser.add_argument("--title", required=True, help="Title of the note")

    subparsers.add_parser("list", help="List all notes")

    export_parser = subparsers.add_parser("export", help="Export a note")
    export_parser.add_argument("--title", required=True, help="Title of the note")
    export_parser.add_argument("--pdf", action="store_true", help="Export as PDF")
    export_parser.add_argument("--html", action="store_true", help="Export as HTML")

    args = parser.parse_args()

    if args.command == "add":
        add_note(args.title)
    elif args.command == "edit":
        edit_note(args.title)
    elif args.command == "delete":
        delete_note(args.title)
    elif args.command == "list":
        list_notes()
    elif args.command == "export":
        export_note(args.title, args.pdf, args.html)


if __name__ == "__main__":
    main()

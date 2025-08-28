import os
import argparse
import subprocess
from rich.console import Console
from rich.table import Table
import markdown2
from weasyprint import HTML
import zipfile
import datetime

console = Console()

NOTES_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "notes")
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(NOTES_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def get_note_path(title: str) -> str:
    safe_title = f"{title}.md".replace(" ", "_")
    return os.path.join(NOTES_DIR, safe_title)

def open_in_editor(note_path: str):
    editor = os.environ.get("EDITOR", "nvim")
    try:
        subprocess.run([editor, note_path])
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] Editor '{editor}' not found. Please set $EDITOR.")

def add_note(title: str):
    note_path = get_note_path(title)
    if os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' already exists.")
        return
    with open(note_path, "w") as f:
        f.write("<!-- status: open -->\n")
        f.write(f"# {title}\n\n")
    open_in_editor(note_path)

def edit_note(title: str):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return
    open_in_editor(note_path)

def delete_note(title: str):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return
    os.remove(note_path)
    console.print(f"[green]Deleted:[/green] {title}")

def extract_status(content: str) -> str:
    for line in content.splitlines():
        if line.startswith("<!-- status:"):
            return line.replace("<!-- status:", "").replace("-->", "").strip()
    return "open"

def list_notes():
    files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith(".md"))
    if not files:
        console.print("[yellow]No notes found.[/yellow]")
        return

    table = Table(title="Your Notes")
    table.add_column("Title", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Last Modified", style="green")

    for f in files:
        path = os.path.join(NOTES_DIR, f)
        with open(path, "r") as nf:
            content = nf.read()
        status = extract_status(content)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
        title = f.replace("_", " ").removesuffix(".md")
        table.add_row(title, status, mtime)

    console.print(table)

def set_status(title: str, status: str):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return

    with open(note_path, "r") as f:
        lines = f.readlines()

    if lines and lines[0].startswith("<!-- status:"):
        lines[0] = f"<!-- status: {status} -->\n"
    else:
        lines.insert(0, f"<!-- status: {status} -->\n")

    with open(note_path, "w") as f:
        f.writelines(lines)

    console.print(f"[green]Updated status:[/green] {title} → {status}")

def export_note(title: str, to_pdf: bool, to_html: bool):
    note_path = get_note_path(title)
    if not os.path.exists(note_path):
        console.print(f"[red]Error:[/red] Note '{title}' not found.")
        return

    with open(note_path, "r") as f:
        content = f.read()

    html_content = markdown2.markdown(content)

    if to_html:
        html_file = os.path.join(DOWNLOADS_DIR, f"{title.replace(' ', '_')}.html")
        with open(html_file, "w") as f:
            f.write(html_content)
        console.print(f"[green]Exported to HTML:[/green] {html_file}")

    if to_pdf:
        pdf_file = os.path.join(DOWNLOADS_DIR, f"{title.replace(' ', '_')}.pdf")
        HTML(string=html_content).write_pdf(pdf_file)
        console.print(f"[green]Exported to PDF:[/green] {pdf_file}")

def export_all(to_pdf: bool, to_html: bool):
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")]
    if not files:
        console.print("[yellow]No notes to export.[/yellow]")
        return

    for f in files:
        title = f.replace("_", " ").removesuffix(".md")
        export_note(title, to_pdf, to_html)

def backup_notes():
    backup_file = os.path.join(
        DOWNLOADS_DIR,
        f"notes_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    )

    count = 0
    with zipfile.ZipFile(backup_file, "w") as zipf:
        for f in os.listdir(NOTES_DIR):
            if f.endswith(".md"):
                zipf.write(os.path.join(NOTES_DIR, f), arcname=f)
                count += 1

    console.print(f"[green]Backup created:[/green] {backup_file} ({count} notes)")

def main():
    parser = argparse.ArgumentParser(prog="notes", description="Simple Neovim-based Notes CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("--title", required=True, help="Title of the note")

    edit_parser = subparsers.add_parser("edit", help="Edit an existing note")
    edit_parser.add_argument("--title", required=True, help="Title of the note")

    delete_parser = subparsers.add_parser("delete", help="Delete an existing note")
    delete_parser.add_argument("--title", required=True, help="Title of the note")

    subparsers.add_parser("list", help="List all notes")

    status_parser = subparsers.add_parser("status", help="Change the status of a note")
    status_parser.add_argument("--title", required=True, help="Title of the note")
    status_parser.add_argument("--set", required=True, choices=["open", "in progress", "done"], help="New status")

    export_parser = subparsers.add_parser("export", help="Export notes")
    export_parser.add_argument("--title", help="Title of the note (omit for --all)")
    export_parser.add_argument("--pdf", action="store_true", help="Export as PDF")
    export_parser.add_argument("--html", action="store_true", help="Export as HTML")
    export_parser.add_argument("--all", action="store_true", help="Export all notes")

    subparsers.add_parser("backup", help="Backup all notes as a zip file")

    args = parser.parse_args()

    if args.command == "add":
        add_note(args.title)
    elif args.command == "edit":
        edit_note(args.title)
    elif args.command == "delete":
        delete_note(args.title)
    elif args.command == "list":
        list_notes()
    elif args.command == "status":
        set_status(args.title, args.set)
    elif args.command == "export":
        if args.all:
            export_all(args.pdf, args.html)
        elif args.title:
            export_note(args.title, args.pdf, args.html)
        else:
            console.print("[red]Error:[/red] Please provide --title or --all.")
    elif args.command == "backup":
        backup_notes()

if __name__ == "__main__":
    main()

# CLI Notes

A simple Neovim-based note-taking CLI application written in Python with Markdown support, note management, and export to PDF/HTML.

## Requirements

* Python 3.8+
* Neovim installed
* pipx installed (`python3 -m pip install --user pipx && python3 -m pipx ensurepath`)

## Installation

The recommended way is to use **pipx** so you can run `notes` globally:

```bash
pip install pipx
pipx install git+https://github.com/clandestino161/notes.git
```

To update the app after changes:

```bash
pipx upgrade notes
```

## Features

* create notes in markdown from the cli and open them directly in neovim
* set a status (open, in progress, done) for each note (default is open)
* modify notes directly in neovim
* access all notes from anywhere
* delete notes from anywhere
* display all notes in a list with Title, Status, and Last Modified date
* backup all notes (`.md` files) as a zip archive directly into the downloads directory

## Usage

All commands can be run from anywhere after installation.

### Add a new note

Creates a new note and immediately opens it in Neovim:

```bash
notes add --title "Title of the Note"
```

### Edit a note

Open an existing note in Neovim:

```bash
notes edit --title "Title of the Note"
```

### Delete a note

Delete an existing note:

```bash
notes delete --title "Title of the Note"
```

### List all notes

Shows all saved notes without opening them:

```bash
notes list
```

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Title       ┃ Status       ┃ Last Modified   ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ First Note  │ open         │ 2025-08-24 12:42│
│ Second Note │ in progress  │ 2025-08-24 13:10│
│ Done Note   │ done         │ 2025-08-24 14:05│
└─────────────┴──────────────┴─────────────────┘

### Change status of an existing note

```bash
notes status --title "Title of the Note" --set "in progress"
notes status --title "Title of the Note" --set "done"
```

### Export notes

Export as PDF:

```bash
notes export --title "First Note" --pdf
```

Export as HTML:

```bash
notes export --title "First Note" --html
```

Export as both PDF and HTML:

```bash
notes export --title "First Note" --pdf --html
```

### Backup all notes

Creates a zip archive in the user’s Downloads directory including all `.md` notes:

```bash
notes backup
```

## Notes Directory

All notes are stored in a standard location:

```bash
~/.local/share/notes
```

The directory is created automatically on first run.

## Uninstallation

To completely uninstall note-taker:

```bash
pipx uninstall notes && rm -f /usr/local/bin/notes
```

If you also want to delete all your saved notes (⚠ irreversible):

```bash
rm -rf ~/.local/share/notes
```

## License

MIT

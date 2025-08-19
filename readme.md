# Note Taker CLI

A simple Neovim-based note-taking CLI application written in Python with Markdown support, note management, and export to PDF/HTML.

## Requirements

* Python 3.8+
* Neovim installed
* pipx installed (`python3 -m pip install --user pipx && python3 -m pipx ensurepath`)

## Installation

The recommended way is to use **pipx** so you can run `note-taker` globally:

```bash
pip install pipx
pipx install git+https://github.com/clandestino161/note_taker.git
```

To update the app after changes:

```bash
pipx upgrade note_taker
```

## Usage

All commands can be run from anywhere after installation.

### Add a new note

Creates a new note and immediately opens it in Neovim:

```bash
note-taker add --title "Title of the Note"
```

### Edit a note

Open an existing note in Neovim:

```bash
note-taker edit --title "Title of the Note"
```

### Delete a note

Delete an existing note:

```bash
note-taker delete --title "Title of the Note"
```

### List all notes

Shows all saved notes without opening them:

```bash
note-taker list
```

### Export notes

Export as PDF:

```bash
note-taker export --title "First Note" --pdf
```

Export as HTML:

```bash
note-taker export --title "First Note" --html
```

Export as both PDF and HTML:

```bash
note-taker export --title "First Note" --pdf --html
```

### Backup all notes

Creates a zip archive in the users download directory including all files from note-taker:

```bash
note-taker backup
```

## Notes Directory

All notes are stored in a standard location:

```bash
~/.local/share/note_taker
```

The directory is created automatically on first run.

## License

MIT

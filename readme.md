# Note Taker CLI

A simple Neovim-based note-taking CLI application written in Python.

---

## Installation

It is recommended to install **note-taker** using `pipx` so it can run globally without activating a virtual environment.

### Requirements

- Python 3.8+
- Neovim installed
- pipx installed (`python3 -m pip install --user pipx && python3 -m pipx ensurepath`)

### Install note-taker

1. Clone the repository:
```bash
git clone https://github.com/clandestino161/note_taker.git
cd note_taker
```

2. Install using `pipx`:

```bash
pipx install .
```

Now `note-taker` is available globally:

```bash
note-taker add --title "My Note"
```

## Commands

All commands can be run from anywhere after installation.

### Add a new note

Creates a new note and immediately opens it in Neovim:

```bash
note-taker add --title "Title of the Note"
```

### Read notes

Lists all notes and opens the selected note in Neovim:

```bash
note-taker read
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

## Notes Directory

All notes are stored in a standard location:

```bash
~/.local/share/note_taker
```

The directory is created automatically on first run.

## License

MIT License

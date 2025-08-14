# Note Taker CLI

A simple, fast note-taking command-line app that uses **Neovim** for editing and stores notes locally in `~/.local/share/note_taker`.

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/note_taker.git
cd note_taker
```

### 2. Install Locally

Install using `pip` so the CLI command is available system-wide:

```bash
pip install --user .

```

After installation, you will see:

- A confirmation that the notes directory was created at:
```bash
~/.local/share/note_taker
```

- A check to confirm whether `~/.local/bin` is in your `PATH`.
    - **If missing**, you’ll see instructions like:
    ```bash
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
    ```

⚠️ **Important:** The `--user` flag installs scripts into `~/.local/bin`.
Make sure that folder is in your `PATH` to run `note-taker` from anywhere.

## 📄 Commands

### Create a new note (opens in Neovim immediately)

```bash
note-taker add --title "My New Note"
```

### Open an existing note for editing

```bash
note-taker read --title "My New Note"
```

### Delete a note

```bash
note-taker delete --title "My New Note"
```

### List all notes

```bash
note-taker list
```

## 📂 Storage Location

All notes are stored as Markdown files in:

```bash
~/.local/share/note_taker
```

Example:

```bash
~/.local/share/note_taker/My New Note.md
```

## 🛠 Requirements

- Python 3.8+
- Neovim installed and available as `nvim` in your `PATH`

## 🧹 Uninstall

To uninstall:

```bash
pip uninstall note_taker
```

Your notes in `~/.local/share/note_taker` will remain unless deleted manually.

## 📜 License

MIT License — do whatever you want, but attribution is appreciated.

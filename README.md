# PYDE

A Python-terminal IDE built with Textual. Edit, run, and manage Python (and more) projects directly from your terminal.

---

## Features

- Syntax highlighting for Python, HTML, CSS, JavaScript, JSON, TOML, Markdown
- Auto-closing brackets and quotes
- Smart auto-indentation (detects `if`, `for`, `def`, `class`, etc.)
- Jedi-powered autocompletion
- Per-project virtual environments (`.venv`)
- Install packages directly from the IDE
- Multiple themes (Monokai, Dracula, GitHub Light)
- Project and file management

---

## Installation

### Method 1. - Source code

Requires **Python 3.10+**

```
git clone https://github.com/zedka450/PYDE.git
cd PYDE
pip install textual jedi
python PYDE.py
```

---

### Method 2. - Release (.exe)

Go to [this link](https://github.com/zedka450/PYDE/releases/tag/v1.0) and download the "`PYDE.exe`"

## Usage

```
1. Create project    — creates a folder + venv automatically
2. Add file          — add a file to a project and open it
3. Edit file         — open an existing file
4. Run project       — runs a .py file using the project venv
5. List projects     — shows all projects and their files
6. Settings          — change syntax highlighting theme
7. Add package       — install a pip package into the project venv
8. Exit
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save file |
| `Ctrl+Q` | Quit without saving |

---

## Supported Languages

| Extension | Highlighting |
|-----------|-------------|
| `.py` | Python |
| `.html` | HTML |
| `.css` | CSS |
| `.js` | JavaScript |
| `.json` | JSON |
| `.toml` | TOML |
| `.md` | Markdown |
| `.txt` | None |

---

## Themes

- `monokai` (default)
- `dracula`
- `github_light`
- `css` (no highlighting)

---

## Requirements

- Python 3.10+
- [Textual](https://github.com/Textualize/textual)
- [Jedi](https://github.com/davidhalter/jedi)

---

## License

MIT

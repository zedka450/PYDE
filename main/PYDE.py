import os, sys
import json
import subprocess
from textual.app import App, ComposeResult
from textual.widgets import TextArea, Header, Footer, Label
from textual.binding import Binding
import jedi

PROJECTS_FILE = "projects.json"
SETTINGS_FILE = "settings.json"

LANG_MAP = {
    ".py": "python",
    ".json": "json",
    ".toml": "toml",
    ".md": "markdown",
    ".txt": None,
    ".css": "css",
    ".html": "html",
    ".js": "javascript",
}

# ─── JSON helpers ────────────────────────────────────────────────────────────

def json_read(jsontype):
    file = PROJECTS_FILE if jsontype == "projects" else SETTINGS_FILE
    if not os.path.exists(file):
        return {}
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR: {file} is corrupted!")
        sys.exit(1)

def json_write(data, jsontype):
    file = PROJECTS_FILE if jsontype == "projects" else SETTINGS_FILE
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ─── Textual editor ──────────────────────────────────────────────────────────

class Editor(App):
    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+q", "quit", "Quit without saving"),
    ]

    def __init__(self, filepath: str, content: str, language: str | None, theme: str):
        super().__init__()
        self.filepath = filepath
        self.content = content
        self.language = language
        self.editor_theme = theme
        self.saved = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label(f" {self.filepath}  |  Ctrl+S save  •  Ctrl+Q quit")
        if self.language:
            ta = TextArea.code_editor(self.content, language=self.language, id="editor")
            ta.theme = self.editor_theme
            yield ta
        else:
            yield TextArea(self.content, id="editor")
        yield Footer()

    def action_save(self):
        content = self.query_one("#editor", TextArea).text
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(content)
        self.saved = True
        self.exit()

    def action_quit(self):
        self.exit()

def open_editor(filepath: str):
    ext = os.path.splitext(filepath)[1].lower()
    language = LANG_MAP.get(ext)
    content = ""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    settings = json_read("settings")
    theme = settings.get("coloration", "monokai")
    try:
        app = Editor(filepath, content, language, theme)
        app.run()
    except Exception as e:
        print(f"ERROR: {e}")
        input("Press Enter to continue...")

# ─── Main menu ───────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Press Enter to continue...")

def main():
    clear()
    print(" ////--- PYDE ---\\\\ ")
    print("Hello!")
    print(" 1. Create project")
    print(" 2. Add file to project")
    print(" 3. Edit file")
    print(" 4. Run project")
    print(" 5. List projects")
    print(" 6. Settings")
    print(" 7. Add package")
    print(" 8. Exit")
    ans = input("1-8 ? ")

    if ans == "1":
        create_project()
    elif ans == "2":
        add_file()
    elif ans == "3":
        edit_file()
    elif ans == "4":
        run_project()
    elif ans == "5":
        list_projects()
    elif ans == "6":
        settings()
    elif ans == "7":
        install_package()
    elif ans == "8":
        sys.exit(0)
    else:
        print("Invalid input!")
        pause()
        main()

# ─── Actions ──────────────────────────────────────────────────────────────────

def create_project():
    data = json_read("projects")
    name = input("Project name: ")
    path = input("Folder path: ")

    if not os.path.exists(path):
        print(f"ERROR: '{path}' does not exist.")
        pause(); main()

    if name in data:
        print(f"ERROR: project '{name}' already exists.")
        pause(); main()

    data[name] = {"path": path, "files": []}
    json_write(data, "projects")
    print(f"Project '{name}' created!")

    venv_path = os.path.join(path, ".venv")
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", venv_path])
    print("Virtual environment created!")

    venv_pip = os.path.join(path, ".venv", "Scripts", "pip")
    print("Updating pip...")
    subprocess.run([venv_pip, "install", "--upgrade", "pip"])
    print("pip updated!")

    if input("Add a file now? (y/n) ").lower() == "y":
        _add_file_to(name, data)
    else:
        pause(); main()

def add_file():
    data = json_read("projects")
    name = input("Project name: ")
    if name not in data:
        print(f"ERROR: project '{name}' not found.")
        pause(); main()
    _add_file_to(name, data)

def _add_file_to(name, data):
    filename = input("File name (e.g. main.py, config.json): ")
    filepath = os.path.join(data[name]["path"], filename)

    if filename in data[name]["files"]:
        print("This file already exists in the project.")
        pause(); main()

    if not os.path.exists(filepath):
        open(filepath, "w").close()

    data[name]["files"].append(filename)
    json_write(data, "projects")
    print(f"Opening {filename}...")
    open_editor(filepath)
    main()

def edit_file():
    data = json_read("projects")
    name = input("Project name: ")
    if name not in data:
        print(f"ERROR: project '{name}' not found.")
        pause(); main()

    files = data[name]["files"]
    if not files:
        print("No files in this project.")
        pause(); main()

    print("Available files:")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")

    choice = input("File number: ")
    try:
        filename = files[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        pause(); main()

    filepath = os.path.join(data[name]["path"], filename)
    open_editor(filepath)
    main()

def run_project():
    data = json_read("projects")
    name = input("Project name: ")
    if name not in data:
        print(f"ERROR: project '{name}' not found.")
        pause(); main()

    py_files = [f for f in data[name]["files"] if f.endswith(".py")]
    if not py_files:
        print("No .py file in this project.")
        pause(); main()

    if len(py_files) == 1:
        filename = py_files[0]
    else:
        print("Available .py files:")
        for i, f in enumerate(py_files, 1):
            print(f"  {i}. {f}")
        choice = input("Which one to run? ")
        try:
            filename = py_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            pause(); main()

    filepath = os.path.join(data[name]["path"], filename)
    print(f"\n--- Running {filename} ---\n")
    venv_python = os.path.join(data[name]["path"], ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        python = venv_python
    else:
        python = sys.executable

    result = subprocess.run([python, filepath])
    print(f"--- {'OK' if result.returncode == 0 else f'FAILED (exit {result.returncode})'} ---")
    pause(); main()

def list_projects():
    data = json_read("projects")
    if not data:
        print("No projects found.")
    else:
        print("\n--- Projects ---")
        for name, info in data.items():
            print(f"\n   {name}  →  {info['path']}")
            for f in info["files"]:
                fp = os.path.join(info["path"], f)
                status = "✓" if os.path.exists(fp) else "✗ (missing!)"
                print(f"     {status}  {f}")
    pause(); main()

def settings():
    s = json_read("settings")
    print(f"\n--- Settings ---")
    print(f" Syntax highlighting: {s.get('coloration', 'monokai')}")
    change = input("\nChange? (color/N) ")
    if change.lower() == "color":
        print(" 1. monokai\n 2. dracula\n 3. github_light\n 4. css (no highlighting)")
        choice = input("1-4 ? ")
        themes = {"1": "monokai", "2": "dracula", "3": "github_light", "4": "css"}
        if choice in themes:
            json_write({"coloration": themes[choice]}, "settings")
            print("Saved!")
        else:
            print("Invalid choice.")
    pause(); main()


def install_package():
    data = json_read("projects")
    name = input("Project name: ")
    if name not in data:
        print(f"ERROR: project '{name}' not found.")
        pause();
        main()

    package = input("Package name: ")
    venv_pip = os.path.join(data[name]["path"], ".venv", "Scripts", "pip")

    print(f"Installing {package}...")
    result = subprocess.run([venv_pip, "install", package])

    if result.returncode == 0:
        print(f"'{package}' installed successfully!")
    else:
        print(f"ERROR: failed to install '{package}'.")
    pause();
    main()

if __name__ == "__main__":
    main()

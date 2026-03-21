import os, sys
import json
import subprocess

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(" ////--- PYDE ---\\\\ ")
    print("Hello!")
    print(" 1. create project?")
    print(" 2. edit project?")
    print(" 3. run project?")
    print(" 4. list projects?")
    print(" 5. exit?")
    ans = input("1,2,3,4,5? ")

    if ans == "1":
        try:
            data = json_read()
            name = input("Enter the name of your project: ")
            path = input("Enter the path of your project: ")

            if not os.path.exists(path):
                print(f"ERROR: Path '{path}' does not exist!")
                input("Press Enter to continue...")
                main()

            if name in data:
                print(f"ERROR: Project '{name}' already exists!")
                input("Press Enter to continue...")
                main()

            file = os.path.join(path, f"{name}.py")
            code = write()

            with open(file, "w", encoding="utf-8") as f:
                f.write(code)

            data[name] = path
            with open("projects.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            print(f"Project '{name}' created successfully!")
            input("Press Enter to continue...")
            main()

        except Exception as e:
            print(f"ERROR: {e}")
            input("Press Enter to continue...")
            sys.exit(1)

    elif ans == "2":
        try:
            data = json_read()
            name = input("Enter the name of your project: ")

            if name not in data:
                print(f"ERROR: Project '{name}' not found!")
                input("Press Enter to continue...")
                main()

            file = os.path.join(data[name], f"{name}.py")

            if not os.path.exists(file):
                print(f"ERROR: File '{file}' not found on disk!")
                input("Press Enter to continue...")
                sys.exit(1)

            with open(file, "r", encoding="utf-8") as f:
                code = f.read()

            print(f"Actual code:\n{code}")
            new_code = write()

            with open(file, "w", encoding="utf-8") as f:
                f.write(new_code)

            print("Project saved successfully!")
            input("Press Enter to continue...")
            main()

        except Exception as e:
            print(f"ERROR: {e}")
            input("Press Enter to continue...")
            sys.exit(1)

    elif ans == "3":
        try:
            data = json_read()
            name = input("Enter the name of your project: ")

            if name not in data:
                print(f"ERROR: Project '{name}' not found!")
                input("Press Enter to continue...")
                main()

            file = os.path.join(data[name], f"{name}.py")

            if not os.path.exists(file):
                print(f"ERROR: File '{file}' not found on disk!")
                input("Press Enter to continue...")
                sys.exit(1)

            print(f"\n--- Running {name}.py ---\n")
            result = subprocess.run([sys.executable, file], capture_output=True, text=True)

            print(result.stdout)
            if result.stderr:
                print(f"ERRORS:\n{result.stderr}")

            if result.returncode != 0:
                print(f"--- FAILED (exit code {result.returncode}) ---")
            else:
                print(f"--- Finished successfully ---")

            input("Press Enter to continue...")
            main()

        except Exception as e:
            print(f"ERROR: {e}")
            input("Press Enter to continue...")
            sys.exit(1)

    elif ans == "4":
        try:
            data = json_read()

            if not data:
                print("No projects found!")
            else:
                print("\n--- Projects ---")
                for name, path in data.items():
                    status = "✓" if os.path.exists(os.path.join(path, f"{name}.py")) else "✗ (missing!)"
                    print(f"  {name} → {path} {status}")

            input("\nPress Enter to continue...")
            main()

        except Exception as e:
            print(f"ERROR: {e}")
            input("Press Enter to continue...")
            sys.exit(1)

    elif ans == "5":
        sys.exit(0)

    else:
        print("Invalid input!")
        input("Press Enter to continue...")
        main()


def write():
    lines = []
    print("(blank line to finish)")
    while True:
        line = input("line: ")
        if line == "":
            return "\n".join(lines)
        lines.append(line)


def json_read():
    try:
        if not os.path.exists("projects.json"):
            return {}
        with open("projects.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("ERROR: projects.json is corrupted!")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Obsidian Sanitizer

Obsidian Sanitizer is a command-line utility to purge clutter and normalize folder/file names in your Obsidian vault. It
cleans up stray system files, empty files/folders, renames mis-named Markdown files, and moves non-Markdown assets into
a `resources/sus` folder.

---

## Prerequisites

- **Python** 3.8 or newer installed system-wide
- **uv** CLI (install via `pip install uv`)

---

## Installation

1. **Clone** the repository:
   ```bash
   git clone https://github.com/your-org/obsidian_sanitizer.git
   cd obsidian_sanitizer
   ```

2. **(Optional) Bootstrap a persistent UV project**
   This creates a `.venv` under the project and installs your pinned dependencies there:

   ```bash
   uv init --bare
   uv venv
   uv pip install -r requirements.txt
   ```

---

## Usage

### Recommended: persistent UV venv

From the project root (after running the steps above):

```bash
uv run main.py \
    --source /path/to/your/ObsidianVault \
    --glob "*_YourPattern_*" \
    --log INFO
```

* UV will use the `.venv` you created, with all packages from `requirements.txt` installed.
* Replace `--glob` and `--log` as needed.

### One-off (no-project) invocation

If you just want a throw-away environment and don’t need to keep a `.venv`, you can skip bootstrapping:

```bash
deactivate        # ensure any broken venv is deactivated
uv run --no-project --python 3 main.py \
    --source /path/to/your/ObsidianVault \
    --glob "*_YourPattern_*" \
    --log INFO
```

* `--no-project` tells UV not to build/install the local project.
* `--python 3` forces a clean CPython 3 interpreter.
* UV will still install all dependencies from `requirements.txt` into a temporary env.

---

## File comparison

When two files need merging, Obsidian Sanitizer invokes your system’s `vimdiff`. You should be comfortable with these
shortcuts:

| Shortcut      | Action                                                |
|---------------|-------------------------------------------------------|
| `]c`          | jump to the next change                               |
| `[c`          | jump to the previous change                           |
| `do`          | get changes from other window into the current window |
| `dp`          | put changes from current window into the other window |
| `:xa`         | save all and exit                                     |
| `:diffupdate` | refresh diffs                                         |
| `Ctrl+w w`    | switch between panes                                  |

---

## Sanitizer actions

1. Remove macOS system files (e.g. `.DS_Store`)
2. Delete empty files
3. Remove empty directories
4. Rename folders ending in `.md`
5. Rename folders matching your `--glob` pattern
6. Move non-Markdown assets into `resources/sus`
7. Rename files with no extension → `.md`
8. Rename Markdown files matching your `--glob`
9. Collect all other application files into `resources/`
10. Final pass: remove any newly emptied folders

---

## Finite State Machine

The renaming logic is governed by a `transitions`-based FSM. See the diagram:

![FSM Diagram](utils/fsm_diagram.png)

---

## Help & Contributing

* **Tests** are minimal; improvements welcome
* **Docs** are sparse; pull requests appreciated
* **Feature ideas**:

    * Detect duplicate files across subfolders
    * “Deflate” a folder (flatten + cleanup)
    * Prepend YAML front-matter templates to Markdown

---

## License

This project is licensed under the MIT License.
See [MIT-LICENSE.txt](MIT-LICENSE.txt) for details.

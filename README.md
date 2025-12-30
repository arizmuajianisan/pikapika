# Downloads Folder Cleaner (Python)

A small Python CLI utility to organize your Windows Downloads folder by moving files into category folders based on file extensions, with an optional “junk quarantine” mode for partial downloads and temp files.

## Features

- Organizes files into folders like `Images`, `Documents`, `Archives`, `Installers`, etc., based on file extension rules you can edit.
- Supports a safe preview mode (`--dry-run`) to show what would happen before making changes.
- Avoids overwriting by auto-renaming duplicates (e.g., `file (1).pdf`).
- Optional junk handling for extensions like `.crdownload`/`.part`/`.tmp` (quarantine or send to Recycle Bin/Trash).

- Python 3.9+ recommended.
- Optional (recommended if you want “delete but reversible”):
  - `send2trash` (`pip install send2trash`) to move junk files to Recycle Bin/Trash instead of permanently deleting.

1. Create a folder for scripts (recommended):
   - `C:\Users\<you>\Scripts\`
2. Save the script as:
   - `C:\Users\<you>\Scripts\clean_downloads.py`

## Usage

Open **PowerShell** or **Command Prompt** and run:

### 1 Preview changes (recommended first run)

```bash
python C:\Users\<you>\Scripts\clean_downloads.py --dry-run
```

This prints planned moves without changing anything.

### 2 Run for real

```bash
python C:\Users\<you>\Scripts\clean_downloads.py
```

This creates category folders (if needed) and moves files.

### 3 Use an explicit Downloads path (recommended on Windows)

If your Downloads is the default location:

```bash
python C:\Users\<you>\Scripts\clean_downloads.py --path "%USERPROFILE%\Downloads" --dry-run
```

Using an explicit path helps when a PC has a redirected/moved Downloads folder.

### 4 Quarantine junk files (safe option)

Moves junk files older than N days into `Downloads\_Quarantine`:

```bash
python C:\Users\<you>\Scripts\clean_downloads.py --quarantine-junk --junk-days 7 --dry-run
python C:\Users\<you>\Scripts\clean_downloads.py --quarantine-junk --junk-days 7
```

This helps clean up partial downloads like `.crdownload` and `.part`.

### 5 Send junk to Recycle Bin/Trash (optional)

Requires `send2trash`.

```bash
python C:\Users\<you>\Scripts\clean_downloads.py --quarantine-junk --trash-junk --junk-days 7
```

## Customizing categories

Edit the `CATEGORIES` mapping in `clean_downloads.py` to change where extensions go.

Example:

- Add `.svg` to `Images`
- Add `.md` to `Documents`
- Add `.iso` to `Archives` or a new `DiskImages` category

## Safety notes

- Always run with `--dry-run` after changing rules to verify the moves.
- Keep the script outside Downloads (e.g., in `C:\Users\<you>\Scripts`) to reduce the chance of it being moved during cleanup.
- If you use `--recursive`, be careful when you already have organized folders inside Downloads, since recursive runs can traverse subfolders.

## Troubleshooting

- **Nothing happens**: Try `--dry-run` to confirm the script is seeing files, and confirm the `--path` is correct.
- **Wrong Downloads folder**: On some Windows setups, the real Downloads location can be redirected; pass the correct folder via `--path`.
- **`--trash-junk` does nothing**: Install `send2trash` with `pip install send2trash` and retry.

## License

Use and modify freely for personal productivity (add your preferred license text if you plan to share publicly).
```
# NiceGUI Calculator

A simple calculator built with Python and [NiceGUI](https://nicegui.io/) for the
programming assignment in repository
`Prof-Luis1986/3-A-Programacion`.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install nicegui
python main.py
```

You can also install the pinned project dependency list:

```bash
pip install -r requirements.txt
```

Then open the local URL shown in the terminal. The calculator also accepts
keyboard input:

- `0`–`9` for numbers
- `+`, `-`, `*`, `/` for operations
- `%` for percentage
- `Enter` or `=` to calculate
- `Escape` or `Delete` to clear
- `Backspace` to remove the last digit

## GitHub submission

The intended personal branch is:

```text
3A-pr2-2026
```

From the project folder, create or switch to that branch and push it to the
professor's repository:

```bash
git checkout -b 3A-pr2-2026
git add .
git commit -m "Build NiceGUI calculator"
git push -u origin 3A-pr2-2026
```
# Expense Tracker

A small terminal-first expense tracker built with Python, SQLite, and Rich.

## Features

- fast CLI workflow for daily expense logging
- automatic category suggestions
- recurring expense support
- monthly budget tracking
- text-based reports and charts
- CSV export for external analysis

## Project Layout

```text
expense_tracker/
├── auto_categorizer.py   # keyword-based category matching
├── cli.py                # interactive Rich UI
├── database.py           # SQLite persistence layer
├── models.py             # dataclasses for app entities
├── recurring.py          # recurring expense processing
└── reports.py            # summaries, charts, and export
```

## Run Locally

```bash
python -m pip install -r requirements.txt
python main.py
```

## Validation

```bash
python -m unittest discover -s tests -v
python -m compileall main.py expense_tracker
```

## Notes

- the SQLite database is stored under `~/.expense_tracker/`
- recurring items are processed automatically when the app starts
- CSV exports can be written to nested directories and will create them if needed

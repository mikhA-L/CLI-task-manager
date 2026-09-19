Markdown# CLI Task Manager

A Command-Line Interface (CLI) Task Manager built with Python. Features styled terminal output, persistent JSON storage, CLI flag support, and automated unit testing with GitHub Actions.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![CI](https://github.com/mikhA-L/CLI-task-manager/actions/workflows/tests.yml/badge.svg)

---

## Author

Mi Kha-el (mikhA-L)

---

## Features

- Rich Terminal UI with color-coded priority levels and formatted tables.
- Direct CLI flag execution (`--add`, `--view`, `--mark`, `--dele`).
- Persistent JSON data storage.
- Unit testing with pytest and automated GitHub Actions CI.

---

## Quick Start

1. Clone the repository:
   ```bash
   git clone [https://github.com/mikhA-L/CLI-task-manager.git](https://github.com/mikhA-L/CLI-task-manager.git)
   cd CLI-task-manager
   
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the interactive application:
```bash
python -m tmain.taskmanager
```
| Command | Flag | Description |
|---|---|---|
| View Tasks | `-v`, `--view` | Displays all tasks in a table |
| Add Task | `-a`, `--add` | Adds a new task to your list |
| Mark Complete | `-m`, `--mark` | Marks a task as complete using its ID |
| Delete Task | `-d`, `--dele` | Deletes a task using its ID |

Running Tests
Execute the unit test suite:
```bash
python -m pytest
```
